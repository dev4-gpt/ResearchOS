import os
import json
import time
from typing import Dict, Any, Callable, Optional
import google.generativeai as genai
from services.search import AcademicSearchService
from services.vault import VaultManager

# System personas and configurations
AGENT_PERSONAS = {
    "Scout": {
        "name": "Senior Scout Researcher",
        "role": "Literature Discovery & Bibliography Mapping",
        "model": "gemini-3.5-flash",
        "instruction": (
            "You are a Senior Scout Researcher at a top-tier academic institute. "
            "Your task is to search literature databases and map bibliography networks. "
            "You select high-impact, high-citation papers, parse their relevance to the research topic, "
            "and lay the groundwork for a systematic literature review. You focus on citations, "
            "recency, publication venues, and mapping references."
        )
    },
    "Analyst": {
        "name": "Lead Analyst",
        "role": "Methodology Extraction & Literature Ingestion",
        "model": "gemini-3.5-flash",
        "instruction": (
            "You are a Lead Analyst specialized in scientific literature analysis. "
            "Your task is to read research metadata and abstracts, extract precise information "
            "(exact hypotheses, methodology, datasets used, quantitative results, limitations), "
            "and structure this knowledge as clean, searchable Obsidian Markdown notes with YAML metadata."
        )
    },
    "Engineer": {
        "name": "Senior Systems Engineer",
        "role": "Algorithmic & Technical Implementation Audit",
        "model": "gemini-3.5-flash",
        "instruction": (
            "You are a Senior Systems Engineer. You scrutinize the technical claims of research papers. "
            "You look at algorithmic complexity, neural network architecture, data scaling parameters, "
            "computational requirements (FLOPs, memory footprint), code viability, and practical deployment bottlenecks."
        )
    },
    "Statistician": {
        "name": "Senior Statistician & Methods Critic",
        "role": "Quantitative Methods & Validation Rigor Audit",
        "model": "gemini-3.5-flash",
        "instruction": (
            "You are a Senior Statistician and Quantitative Methods Critic. You audit the scientific rigor "
            "of experimental designs. You check sample sizes, statistical significance, p-values, baseline comparisons, "
            "control groups, validation benchmarks, and potential sources of selection or survival bias."
        )
    },
    "Reviewer2": {
        "name": "Reviewer #2 / Academic Editor",
        "role": "Hostile Peer Review & Rejection Risk Assessor",
        "model": "gemini-3.5-flash",
        "instruction": (
            "You are the infamous, highly critical 'Reviewer #2' at a prestigious journal. "
            "Your job is to look for any logic gap, overhyped claim, formatting error, or lack of novelty. "
            "You raise hard objections and list key rejection risks. You focus on citations, "
            "recency, publication venues, and mapping references."
        )
    },
    "Chairman": {
        "name": "CEO / Institute Chairman",
        "role": "Debate Moderator & Consensus Synthesizer",
        "model": "gemini-3.5-flash",
        "instruction": (
            "You are the CEO and Chairman of the Research Institute. You moderate the council debates. "
            "You read individual critiques from the Scout, Analyst, Engineer, Statistician, and Reviewer #2. "
            "You identify areas of consensus, highlight key points of tension or debate, synthesize "
            "conflicting claims, and draft a high-level conceptual outline for the final paper."
        )
    },
    "Writer": {
        "name": "Senior Research Writer & Publisher",
        "role": "Journal-Ready Manuscript Drafting & Publishing Prep",
        "model": "gemini-3.5-flash",
        "instruction": (
            "You are a world-class Senior Research Writer and Publisher who regularly publishes in Nature, Science, "
            "IEEE, and ACM journals. Your task is to take the Chairman's outline, paper summaries, and the council "
            "debate, and draft a formal, high-impact literature review. You write using rigorous academic tone, "
            "ensure structured journal sections (Abstract, Introduction, Related Work, Methodological Audit, Discussion, "
            "Conclusion), and use proper inline Obsidian links/citations (e.g. `[[arxiv:XXXX]]` or `[[openalex:YYYY]]`)."
        )
    }
}

class CouncilOrchestrator:
    def __init__(self, vault_path: str = "../vault"):
        self.vault = VaultManager(vault_path)
        self.search_service = AcademicSearchService()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.is_dry_run = not bool(self.api_key)
        
        if not self.is_dry_run:
            genai.configure(api_key=self.api_key)  # type: ignore[attr-defined]
            
        print(f"CouncilOrchestrator initialized. Dry Run Mode: {self.is_dry_run}")

    def _call_gemini(self, agent_key: str, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Helper to invoke Gemini API with appropriate model and instructions."""
        if self.is_dry_run:
            # Simulate slight lag
            time.sleep(0.5)
            return f"[MOCK RESPONSE from {agent_key}] Based on the research, this is a simulated analysis of your query."

        agent_cfg = AGENT_PERSONAS[agent_key]
        model_name = agent_cfg["model"]
        # Standardize model names for SDK (if they are 2.5, the SDK uses gemini-2.5-pro / gemini-2.5-flash)
        # Note: If the environment has specific overriding model names, we can check for them.
        # Allow override from env
        env_model_pro = os.getenv("GEMINI_PRO_MODEL")
        env_model_flash = os.getenv("GEMINI_FLASH_MODEL")
        
        if "pro" in model_name and env_model_pro:
            model_name = env_model_pro
        elif "flash" in model_name and env_model_flash:
            model_name = env_model_flash

        instruction = system_instruction or agent_cfg["instruction"]
        
        import random
        max_retries = 6
        retry_delay = 5.0
        
        for attempt in range(max_retries):
            try:
                model = genai.GenerativeModel(  # type: ignore[attr-defined]
                    model_name=model_name,
                    system_instruction=instruction
                )
                response = model.generate_content(prompt)
                return str(response.text)
            except Exception as e:
                error_msg = str(e)
                is_rate_limit = "429" in error_msg or "ResourceExhausted" in error_msg or "quota" in error_msg.lower()
                
                if is_rate_limit and attempt < max_retries - 1:
                    sleep_time = (2.0 ** attempt) * retry_delay + random.uniform(0.1, 1.0)
                    print(f"Gemini API rate limited (429) for {agent_key}. Retrying in {sleep_time:.2f}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(sleep_time)
                    continue
                
                print(f"Error calling Gemini for {agent_key} ({model_name}): {e}")
                raise RuntimeError(f"Agent {agent_cfg['name']} encountered a fatal exception: {str(e)}")

        raise RuntimeError(f"Agent {agent_key} exhausted all {max_retries} retries without returning.")

    def run_research(self, topic: str, log_callback: Callable[[Dict[str, Any]], None]) -> Dict[str, Any]:
        """Runs the full multi-agent research and LLM council debate pipeline.
        
        Stages:
        1. Ingestion: Scout searches databases and Analyst creates markdown papers.
        2. Technical Critique: Engineer, Statistician, and Reviewer #2 write parallel notes.
        3. Boardroom Debate: Multi-turn debate between agents.
        4. Synthesis: Chairman reviews critiques & debate, writes review outline.
        5. Drafting: Writer creates the final paper in LaTeX/Markdown style.
        """
        project_id = f"project_{int(time.time())}"
        
        def send_log(stage: str, agent: str, message: str, data: Any = None):
            log_callback({
                "projectId": project_id,
                "timestamp": time.time(),
                "stage": stage,
                "agent": agent,
                "message": message,
                "data": data
            })

        send_log("Initialization", "System", f"Starting research pipeline for topic: '{topic}'", {"dryRun": self.is_dry_run})
        
        # --- STAGE 1: INGESTION (Scout & Analyst) ---
        send_log("Ingestion", "Senior Scout Researcher", "Searching arXiv and OpenAlex for relevant literature...")
        
        papers = []
        if self.is_dry_run:
            time.sleep(2)
            # Mock paper metadata
            papers = [
                {
                    "id": "arxiv:2305.18290",
                    "title": "Direct Preference Optimization: Your Language Model is Secretly a Reward Model",
                    "authors": ["Rafael Rafailov", "Archit Sharma", "Eric Mitchell", "Stefano Ermon", "Christopher D. Manning", "Chelsea Finn"],
                    "abstract": "We present Direct Preference Optimization (DPO), a stable, performant, and computationally lightweight algorithm for aligning LLMs to human preferences without training a reward model or using reinforcement learning.",
                    "url": "https://arxiv.org/abs/2305.18290",
                    "published": "2023-05-29",
                    "citations": 1240,
                    "source": "arXiv & OpenAlex"
                },
                {
                    "id": "arxiv:2005.14165",
                    "title": "Language Models are Few-Shot Learners",
                    "authors": ["Tom B. Brown", "Benjamin Mann", "Nick Ryder", "Melanie Subbiah", "Jared Kaplan", "Prafulla Dhariwal", "Arvind Neelakantan", "Pranav Shyam", "Girish Sastry", "Amanda Askell", "Sandhini Agarwal", "Ariel Herbert-Voss", "Gretchen Krueger", "Tom Henighan", "Rewon Child", "Aditya Ramesh", "Daniel M. Ziegler", "Jeffrey Wu", "Clemens Winter", "Christopher Hesse", "Mark Chen", "Eric Sigler", "Mateusz Litwin", "Scott Gray", "Benjamin Chess", "Jack Clark", "Christopher Berner", "Sam McCandlish", "Alec Radford", "Ilya Sutskever", "Dario Amodei"],
                    "abstract": "We demonstrate that scaling up language models greatly improves few-shot performance, sometimes even matching or exceeding prior state-of-the-art fine-tuning approaches. We train GPT-3, a 175-billion parameter autoregressive language model, and evaluate its performance on a wide variety of NLP tasks.",
                    "url": "https://arxiv.org/abs/2005.14165",
                    "published": "2020-05-28",
                    "citations": 25400,
                    "source": "arXiv & OpenAlex"
                },
                {
                    "id": "arxiv:2203.02155",
                    "title": "Training language models to follow instructions with human feedback",
                    "authors": ["Long Ouyang", "Jeff Wu", "Xu Jiang", "Diogo Almeida", "Carroll L. Wainwright", "Pamela Mishkin", "Chong Zhang", "Sandhini Agarwal", "Katarina Slama", "Alex Ray", "John Schulman", "Jacob Hilton", "Fraser Kelton", "Luke Miller", "Maddie Simens", "Amanda Askell", "Peter Welinder", "Paul Christiano", "Jan Leike", "Ryan Lowe"],
                    "abstract": "We show how to fine-tune language models on a wide range of tasks to align them with user intent. By using reinforcement learning from human feedback (RLHF), we fine-tune GPT-3 to follow instructions. We call the resulting models InstructGPT.",
                    "url": "https://arxiv.org/abs/2203.02155",
                    "published": "2022-03-04",
                    "citations": 4350,
                    "source": "arXiv & OpenAlex"
                }
            ]
        else:
            import re
            # 1. Extract potential arXiv IDs from the topic using regex
            arxiv_ids = re.findall(r'\b\d{4}\.\d{4,5}\b', topic)
            
            # Fetch papers by exact IDs first
            papers_by_id = []
            if arxiv_ids:
                send_log("Ingestion", "Senior Scout Researcher", f"Detected specific arXiv IDs in topic: {arxiv_ids}. Fetching directly...")
                papers_by_id = self.search_service.fetch_arxiv_by_ids(arxiv_ids)
                send_log("Ingestion", "Senior Scout Researcher", f"Successfully retrieved {len(papers_by_id)} paper(s) by ID.")
            
            # 2. Extract search terms/keywords using Gemini if the topic is a long prompt
            search_queries = [topic]
            if len(topic.split()) > 6 and not self.is_dry_run:
                try:
                    send_log("Ingestion", "Senior Scout Researcher", "Analyzing topic to extract academic search queries...")
                    extraction_prompt = (
                        f"Extract 1 to 3 clean academic search queries (paper titles or key keywords) "
                        f"from the following user request, to find the papers in academic databases:\n\n"
                        f"'{topic}'\n\n"
                        f"Do not include instructions, URLs, or formatting. "
                        f"Return ONLY a JSON list of strings, e.g. [\"Self-Consistency chain of thought\", \"LLM-as-a-Judge\"]."
                    )
                    response_text = self._call_gemini(
                        "Scout", 
                        extraction_prompt, 
                        system_instruction="You are an academic query extractor. Return only a JSON list of query strings."
                    )
                    # Clean up response text
                    clean_text = response_text.replace("```json", "").replace("```", "").strip()
                    extracted = json.loads(clean_text)
                    if isinstance(extracted, list) and len(extracted) > 0:
                        search_queries = extracted
                        send_log("Ingestion", "Senior Scout Researcher", f"Extracted academic search queries: {search_queries}")
                except Exception as e:
                    print(f"Error extracting search queries: {e}")
            
            # If we still need more papers, perform searches
            papers_by_search = []
            for query in search_queries:
                if len(papers_by_id) + len(papers_by_search) < 4:
                    results = self.search_service.run_combined_search(query, limit=3)
                    papers_by_search.extend(results)
            
            # Merge and de-duplicate papers
            all_papers = []
            seen_titles = set()
            
            for p in papers_by_id + papers_by_search:
                title_key = p["title"].lower().strip()
                if title_key not in seen_titles:
                    seen_titles.add(title_key)
                    all_papers.append(p)
                    
            papers = all_papers[:4]
            
        if not papers:
            send_log("Ingestion", "System", "No papers discovered. Aborting pipeline.", {"success": False})
            return {"success": False, "error": "No papers found"}
            
        send_log("Ingestion", "Senior Scout Researcher", f"Discovered {len(papers)} key papers. Commencing bibliographic extraction...", {"papers": [p["title"] for p in papers]})
        
        # Lead Analyst writes paper notes into Vault
        extracted_papers_info = []
        for i, paper in enumerate(papers):
            send_log("Ingestion", "Lead Analyst", f"Ingesting paper {i+1}/{len(papers)}: '{paper['title']}'...")
            
            prompt = (
                f"Analyze this scientific paper metadata and abstract, and create a highly structured Obsidian vault summary.\n\n"
                f"Paper Title: {paper['title']}\n"
                f"Authors: {', '.join(paper['authors'])}\n"
                f"Source/URL: {paper['url']}\n"
                f"Publication Date: {paper['published']}\n"
                f"Citations: {paper['citations']}\n"
                f"Abstract: {paper['abstract']}\n\n"
                f"Your output must be structured as an Obsidian note, starting with YAML frontmatter. Provide:\n"
                f"- exact claims and hypotheses\n"
                f"- methodologies and algorithms used\n"
                f"- experimental results and datasets\n"
                f"- limitations acknowledged by the authors\n"
                f"Ensure you format references and concepts with Obsidian links [[ConceptName]] or [[PaperId]]."
            )
            
            # Call Gemini Analyst
            note_content = self._call_gemini("Analyst", prompt)
            
            # Format frontmatter for the vault file
            frontmatter = {
                "title": paper["title"],
                "authors": paper["authors"],
                "url": paper["url"],
                "published": paper["published"],
                "citations": paper["citations"],
                "source": paper["source"],
                "id": paper["id"],
                "tags": ["research-paper", topic.replace(" ", "-").lower()]
            }
            
            # Save to Obsidian Vault 01_Papers
            filename = f"{paper['id'].replace(':', '_')}.md"
            self.vault.save_markdown("papers", filename, note_content, frontmatter)
            extracted_papers_info.append({
                "id": paper["id"],
                "title": paper["title"],
                "filename": filename,
                "content": note_content
            })
            
        send_log("Ingestion", "Lead Analyst", "All research papers successfully ingested and saved into the Obsidian Vault under '01_Papers/'.")
        
        # --- STAGE 2: CRITIQUE (Engineer, Statistician, Reviewer #2) ---
        send_log("Critique", "System", "Spawning parallel auditing council (Systems Engineer, Statistician, Reviewer #2)...")
        
        # Gather summaries for critique prompt
        summaries_text = "\n\n---\n\n".join([
            f"Paper ID: {p['id']}\nTitle: {p['title']}\nSummary:\n{p['content']}" 
            for p in extracted_papers_info
        ])
        
        critiques = {}
        
        # 1. Senior Systems Engineer Audit
        send_log("Critique", "Senior Systems Engineer", "Auditing papers for algorithmic feasibility, parameter efficiency, and hardware viability...")
        eng_prompt = (
            f"Review the following research summaries compiled for the topic '{topic}':\n\n{summaries_text}\n\n"
            f"Provide a rigorous technical evaluation. Identify deployment bottlenecks, FLOPs limitations, memory scalability, "
            f"and algorithmic constraints. Save your critique structured with headings for each paper."
        )
        critiques["Engineer"] = self._call_gemini("Engineer", eng_prompt)
        
        # 2. Statistician Methods Audit
        send_log("Critique", "Senior Statistician & Methods Critic", "Auditing experimental designs, statistical tests, and baseline selections...")
        stat_prompt = (
            f"Review the following research summaries compiled for the topic '{topic}':\n\n{summaries_text}\n\n"
            f"Provide a strict quantitative methods critique. Examine sample sizes, metric selection, statistical tests, baseline comparisons, "
            f"and validation validity. Highlight any potential validation leaks or weaknesses."
        )
        critiques["Statistician"] = self._call_gemini("Statistician", stat_prompt)
        
        # 3. Reviewer #2 Critique
        send_log("Critique", "Reviewer #2 / Academic Editor", "Assessing absolute novelty, structural deficiencies, and rejection risks...")
        rev_prompt = (
            f"Review the following research summaries compiled for the topic '{topic}':\n\n{summaries_text}\n\n"
            f"As Reviewer #2, challenge the claims. Identify overhype, logical gaps, structural omissions, and state-of-the-art novelty conflicts. "
            f"Write a list of critical rejection objections that must be addressed."
        )
        critiques["Reviewer2"] = self._call_gemini("Reviewer2", rev_prompt)
        
        # --- STAGE 3: THE BOARDROOM DEBATE ---
        send_log("Debate", "System", "Convening the LLM Council Boardroom Debate...")
        
        # Simulate a threaded debate where agents review each other's opinions
        debate_log = []
        
        # Turn 1: Systems Engineer presents major technical flags
        debate_log.append({
            "agent": "Senior Systems Engineer",
            "message": f"From a systems perspective, here is my core audit regarding '{topic}':\n\n" + critiques["Engineer"][:400] + "..."
        })
        send_log("Debate", "Senior Systems Engineer", debate_log[-1]["message"])
        
        # Turn 2: Statistician highlights methodological flaws
        stat_response_prompt = (
            f"You are in a boardroom debate about '{topic}'. The Systems Engineer has just shared their initial thoughts:\n"
            f"'{debate_log[-1]['message']}'\n\n"
            f"Here is your own quantitative analysis:\n{critiques['Statistician']}\n\n"
            f"Combine your analysis and respond directly to the Systems Engineer's claims. Agree, extend, or debate their points."
        )
        stat_reply = self._call_gemini("Statistician", stat_response_prompt)
        debate_log.append({
            "agent": "Senior Statistician & Methods Critic",
            "message": stat_reply
        })
        send_log("Debate", "Senior Statistician & Methods Critic", stat_reply[:400] + "...")
        
        # Turn 3: Reviewer #2 interjects with rejection risks
        rev2_response_prompt = (
            f"You are in a boardroom debate about '{topic}'. The Systems Engineer and Statistician have discussed the technicalities:\n"
            f"Engineer: '{debate_log[0]['message'][:300]}...'\n"
            f"Statistician: '{debate_log[1]['message'][:300]}...'\n\n"
            f"Here is your Reviewer #2 list of objections:\n{critiques['Reviewer2']}\n\n"
            f"Interject in the debate. Challenge both of their assumptions and point out why these papers collectively might still fail "
            f"the novelty bar for important journals."
        )
        rev2_reply = self._call_gemini("Reviewer2", rev2_response_prompt)
        debate_log.append({
            "agent": "Reviewer #2 / Academic Editor",
            "message": rev2_reply
        })
        send_log("Debate", "Reviewer #2 / Academic Editor", rev2_reply[:400] + "...")
        
        # --- STAGE 4: CHAIRMAN SYNTHESIS ---
        send_log("Synthesis", "CEO / Institute Chairman", "Consolidating council opinions and structuring synthesis outline...")
        
        debate_transcript = "\n\n".join([f"[{d['agent']}]: {d['message']}" for d in debate_log])
        
        chairman_prompt = (
            f"You are moderating the research council debate on the topic '{topic}'.\n\n"
            f"Here is the debate transcript between the Systems Engineer, Statistician, and Reviewer #2:\n\n{debate_transcript}\n\n"
            f"Review the original paper summaries:\n\n{summaries_text}\n\n"
            f"Write a comprehensive moderator's synthesis. You must:\n"
            f"1. Summarize the major agreements (consensus) reached by the council.\n"
            f"2. Detail the critical points of disagreement or skepticism.\n"
            f"3. Create a detailed structural outline for our final published literature review, outlining key concepts to be researched further."
        )
        
        synthesis_content = self._call_gemini("Chairman", chairman_prompt)
        
        # Save debate transcript and synthesis to Vault
        import re
        safe_topic_slug = re.sub(r'[^a-zA-Z0-9\s_-]', '', topic)
        safe_topic_slug = re.sub(r'[\s_-]+', '_', safe_topic_slug).strip('_').lower()
        if len(safe_topic_slug) > 50:
            safe_topic_slug = safe_topic_slug[:50].rstrip('_')

        debate_filename = f"debate_{safe_topic_slug}.md"
        self.vault.save_markdown(
            "debates", 
            debate_filename, 
            synthesis_content + "\n\n## Transcript\n\n" + debate_transcript,
            {"title": f"Council Debate on {topic}", "topic": topic, "type": "debate_summary", "tags": [topic.replace(" ", "-").lower(), "debate"]}
        )
        
        send_log("Synthesis", "CEO / Institute Chairman", "Debate synthesized and outlines written to '03_Debates/'. Spawning Research Writer...")
        
        # --- STAGE 5: ACADEMIC DRAFTING (Writer) ---
        send_log("Drafting", "Senior Research Writer & Publisher", f"Drafting formal journal-ready literature review for '{topic}'...")
        
        writer_prompt = (
            f"You are drafting a peer-review grade literature review paper on the topic: '{topic}'.\n\n"
            f"Here is the Chairman's debate synthesis, consensus, and structural outline:\n\n{synthesis_content}\n\n"
            f"Here are the summaries of the source papers we are citing:\n\n{summaries_text}\n\n"
            f"Write a formal academic literature review paper. The language must be extremely academic, formal, and authoritative. "
            f"Include the following sections:\n"
            f"- Title\n"
            f"- Abstract (summarize findings, significance, and peer consensus)\n"
            f"- Introduction (introduce topic and highlight the research gaps identified by the council)\n"
            f"- Literature Review & Taxonomy (synthesize findings from the source papers, using inline backlinks like [[arxiv_XXXX]] or [[openalex_YYYY]] as citations)\n"
            f"- Methodological & Technical Critique (incorporate the critiques of the Systems Engineer and Statistician)\n"
            f"- Open Challenges & Rejection Objections (incorporate Reviewer #2's insights on what the field is missing)\n"
            f"- Conclusion (final thoughts on future directions)\n\n"
            f"Make sure every paper in our corpus is cited using its exact note link (e.g. [[arxiv_2305_18290]] or [[openalex_W438290]]). "
            f"Do not write placeholders. Draft the paper in full."
        )
        
        final_paper_content = self._call_gemini("Writer", writer_prompt)
        
        # Save final paper draft to 04_Drafts in Vault
        draft_filename = f"review_{safe_topic_slug}.md"
        self.vault.save_markdown(
            "drafts",
            draft_filename,
            final_paper_content,
            {"title": f"Literature Review: {topic}", "topic": topic, "status": "draft", "format": "IEEE/ACM markdown", "tags": [topic.replace(" ", "-").lower(), "literature-review", "draft"]}
        )
        
        send_log("Drafting", "Senior Research Writer & Publisher", f"Final academic draft completed and written to '04_Drafts/{draft_filename}'!")
        
        send_log("Completion", "System", "Research pipeline completed successfully!", {
            "success": True,
            "vaultFiles": {
                "papersCount": len(papers),
                "debateFile": debate_filename,
                "draftFile": draft_filename
            }
        })
        
        return {
            "success": True,
            "project_id": project_id,
            "papers_count": len(papers),
            "debate_file": debate_filename,
            "draft_file": draft_filename
        }
