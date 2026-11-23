"""Research ranking adapter for the actual pinned Harness² recursion/library engine.

A restricted text-only proposer replaces its CLI executor. No generated scripts,
plugins, shell commands, permissions or judge data are exposed to the model.
"""
import json
from pathlib import Path

from services import research_ranking as ranking
from services.research_engines import load_upstream, parse_json, write_json

BASE_PROMPT = 'Rank the supplied papers by reciprocal rank fusion of the source rankings.'
REFINED_PROMPT = 'Rank papers by query word overlap with their titles, highest first; break ties by document ID.'
EDITABLE = frozenset({'systemprompt.md', 'tool_descriptions/tool_guidance.md'})
PROPOSAL_SCHEMA = {'type': 'object', 'required': ['text', 'edits'], 'properties': {
    'text': {'type': 'string'}, 'edits': {'type': 'object', 'properties': {
        path: {'type': 'string'} for path in sorted(EDITABLE)}, 'additionalProperties': False}},
    'additionalProperties': False}


def apply_edits(workspace, edits):
    if not isinstance(edits, dict) or not set(edits) <= EDITABLE:
        raise ValueError('Only system prompt and tool guidance may be edited')
    for key, value in edits.items():
        if not isinstance(value, str) or len(value) > 12000:
            raise ValueError('Harness edit must be bounded text')
        target = workspace / key
        if target.is_symlink() or not target.resolve().is_relative_to(workspace.resolve()):
            raise ValueError('Unsafe harness path')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value)


def refine(spec, path, tasks, model, meter):
    load_upstream('harness2')
    from harness2.core import tree
    from harness2.core.proposer import Proposer, Reply, ProposerError
    from harness2.core.spec import BenchPrompts, BenchSpec, ChannelSpec
    from harness2.core.schedule import run_domain, Namespace
    from harness2.substrate.opencode import OpencodeSubstrate
    work = path / 'harness2'
    work.mkdir()

    def solve(task, prompt):
        meter.check()
        if model is None:
            return ranking.lexical(task) if 'word overlap' in prompt else ranking.rrf(task)
        answer = parse_json(model.generate(
            prompt + '\nReturn a JSON array of every document ID, ordered by relevance.\n' + json.dumps(task),
            schema={'type': 'array', 'items': {'type': 'string', 'enum': [d['id'] for d in task['documents']]},
                    'minItems': len(task['documents']), 'maxItems': len(task['documents'])},
        ))
        return ranking.validate_ranking(answer, task)

    class Adapter:
        def __init__(self):
            self.substrate = OpencodeSubstrate()  # surface/schema only; never launch this executor
            channel = ChannelSpec('opencode', 'local/research-text')
            self.spec = BenchSpec(name='research-ranking', runs_root=work / 'runs', install_mode='workspace_config',
                prompts=BenchPrompts(work='rank every supplied paper by relevance to a research query; return each paper ID exactly once',
                    inv_levers='Edit only systemprompt.md and tool_descriptions/tool_guidance.md. Keep other files unchanged.',
                    dom_levers='Use query and paper text to order every document identifier; never omit IDs.'),
                channels={'proposer': channel, 'selector': channel}, leak_globs=('labels.json',))
            self.base = {name: '' for name in self.substrate.surface().always_on}
            self.base['systemprompt.md'] = BASE_PROMPT
            self.base['guardrails.md'] = 'Return supplied IDs only. Do not execute code or access the network.'
            tree.write_tree(self.substrate.surface(), self.base, self.base_harness(), stubs=False)
            for task in tasks:
                write_json(self.task_files(task['id']) / 'task.json', task)

        def tasks(self, split='all'): return [t['id'] for t in tasks]
        def domain_of(self, task_id): return 'research'
        def task_prompt(self, task_id): return 'Return every supplied paper ID exactly once, ordered by relevance to the query.'
        def task_files(self, task_id): return work / 'sources' / task_id
        def base_harness(self): return work / 'base'
        def validate_tree(self, proposed):
            for key in set(proposed) | set(self.base):
                if key not in EDITABLE and proposed.get(key, '') != self.base.get(key, ''):
                    raise ValueError('Non-editable harness component changed: ' + key)
            if set(proposed) - set(self.base):
                raise ValueError('Additional harness files are not permitted')
        def execute(self, task_id, harness_dir, run_id, *, timeout=None):
            task = next(t for t in tasks if t['id'] == task_id)
            harness_dir = harness_dir or self.base_harness()
            prompt = '\n'.join((harness_dir / k).read_text() for k in sorted(EDITABLE))
            ids = solve(task, prompt)
            output = work / 'executions' / run_id
            write_json(output / 'answer.json', ids)
            (output / 'trajectory.md').write_text('[ACTION] Order supplied paper IDs\n[OBSERVATION]\n' + json.dumps(ids))
            return output
        def delivered(self, run_dir): return (run_dir / 'answer.json').is_file()
        def trajectory(self, run_dir, *, obs_trunc):
            target = run_dir / 'trajectory.md'
            return target.read_text()[:obs_trunc] if target.is_file() else ''
        def deliverable_text(self, run_dir):
            target = run_dir / 'answer.json'
            return target.read_text() if target.is_file() else ''
        def deliverable_files(self, run_dir):
            # Upstream asks for artifacts even when a trial failed before delivery.
            # Preserve delivered=False rather than masking its failure with FileNotFoundError.
            return {'answer.json': self.deliverable_text(run_dir)} if self.delivered(run_dir) else {}

    class TextProposer(Proposer):
        def call(self, mission, context_dir, label, **kwargs):
            meter.check()
            context = Path(context_dir)
            workspace = None
            if model is None:
                if label.startswith('experience.'):
                    text = '<experience>\ncue: Query terms occur in paper titles\nlesson: Compare query words with titles.\nevidence: The ordering changed after the prompt edit.\nconfidence: limited to this synthetic fixture\n</experience>'
                elif label.startswith('select.'):
                    raise ProposerError('Demo supports k=1 final composition only')
                else:
                    workspace = context / 'harness'
                    apply_edits(workspace, {'systemprompt.md': REFINED_PROMPT})
                    text = '<notes>Order papers using their query/title overlap.</notes>'
            else:
                files = {}
                total = 0
                for f in sorted(context.rglob('*')):
                    if f.is_file() and not f.is_symlink() and f.suffix in ('.md', '.json', '.txt'):
                        body = f.read_text()[:1800]
                        total += len(body)
                        if total > 6000:
                            break
                        files[str(f.relative_to(context))] = body
                instruction = '\nReturn JSON {"text": "your response with the requested XML tags", "edits": {"systemprompt.md": "..."}}. Edits may only change systemprompt.md or tool_descriptions/tool_guidance.md. No tools or code execution.'
                try:
                    reply = parse_json(model.generate(mission + instruction + '\n' + json.dumps(files),
                                                      schema=PROPOSAL_SCHEMA))
                    text = reply['text']
                    if not isinstance(text, str): raise ValueError('text must be a string')
                    if not label.startswith(('select.', 'experience.')):
                        workspace = context / 'harness'
                        apply_edits(workspace, reply.get('edits', {}))
                    elif reply.get('edits'):
                        raise ValueError('Selection/reflection must not edit harness files')
                except (ValueError, KeyError) as exc:
                    raise ProposerError(str(exc)) from exc
            reply = Reply(label=label, text=text, ok=True, attempts=1, workspace=workspace)
            self._calls.append(reply)
            return reply

    adapter = Adapter()
    proposer = TextProposer(adapter.spec.channels['proposer'])
    report = run_domain('research', adapter.tasks(), 1, adapter=adapter, prop=proposer,
                        runs_root=adapter.spec.runs_root, library_root=work / 'library', modes=('seq',), seed=spec.seed)
    write_json(path / 'harness2_report.json', report)
    if model is not None:
        meter.execution.remaining()
    if report['failed']:
        raise ValueError('Harness² refinement incomplete; see harness2_report.json')
    # Adopt only the final DEVELOPMENT task's committed selection; no held-out feedback.
    last = tasks[-1]['id']
    summaries = list((work / 'runs').glob(f'*/{last}/summary.json'))
    if len(summaries) != 1:
        raise ValueError('Missing/ambiguous Harness² task summary')
    summary = json.loads(summaries[0].read_text())
    choice = summary['selections']['seq']['chosen_label']
    selected = Namespace(adapter.spec.name, adapter.substrate.name, 'seq', 1, spec.seed).task_dir(adapter.spec.runs_root, last) / 'harnesses' / choice
    proposed = tree.read_tree(adapter.substrate.surface(), selected)
    adapter.validate_tree(proposed)
    prompt = '\n'.join(proposed[k] for k in sorted(EDITABLE))
    write_json(path / 'adopted_harness.json', proposed)
    return lambda task: solve(task, prompt), prompt
