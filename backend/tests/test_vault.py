"""
Tests for services/vault.py — VaultManager.

Coverage targets:
  - _ensure_folders_exist      : folders created on init
  - save_markdown              : happy path, frontmatter, no-.md extension, slash
                                 sanitization, invalid category
  - read_markdown              : round-trip, no-.md extension, missing file,
                                 invalid category
  - list_files                 : populated category, empty category, invalid category
  - parse_markdown_content     : plain body, YAML scalar, YAML list, no frontmatter
  - get_knowledge_graph        : shape, nodes, edges via wikilinks
"""

import os
import pytest

from services.vault import VaultManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_CATEGORIES = ["papers", "concepts", "debates", "drafts"]
FOLDER_NAMES = ["01_Papers", "02_Concepts", "03_Debates", "04_Drafts"]


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

class TestInit:
    def test_vault_root_created(self, tmp_path):
        """VaultManager must create the vault root when it does not exist."""
        vault_root = tmp_path / "new_vault"
        VaultManager(str(vault_root))
        assert vault_root.is_dir()

    def test_all_subdirectories_created(self, tmp_path):
        """All four category folders must exist after construction."""
        vm = VaultManager(str(tmp_path))
        for folder in FOLDER_NAMES:
            assert (tmp_path / folder).is_dir(), f"{folder} was not created"

    def test_vault_path_attribute_is_absolute(self, tmp_path):
        vm = VaultManager(str(tmp_path))
        assert os.path.isabs(vm.vault_path)

    def test_folders_dict_contains_all_categories(self, tmp_path):
        vm = VaultManager(str(tmp_path))
        assert set(vm.folders.keys()) == set(VALID_CATEGORIES)


# ---------------------------------------------------------------------------
# save_markdown
# ---------------------------------------------------------------------------

class TestSaveMarkdown:
    def test_writes_file_to_correct_folder(self, vault, tmp_path):
        """A saved paper lands in 01_Papers/."""
        path = vault.save_markdown("papers", "test_paper.md", "# Hello")
        assert os.path.isfile(path)
        assert "01_Papers" in path

    def test_adds_md_extension_when_missing(self, vault, tmp_path):
        """Filenames without .md must get the extension appended."""
        path = vault.save_markdown("concepts", "my_concept", "body")
        assert path.endswith(".md")
        assert os.path.isfile(path)

    def test_slug_already_has_md_no_double_extension(self, vault):
        """Passing a filename that already ends in .md must not produce .md.md."""
        path = vault.save_markdown("drafts", "draft.md", "body")
        assert not path.endswith(".md.md")

    def test_slash_in_filename_sanitized(self, vault):
        """Forward-slash in the filename must be replaced with underscore."""
        path = vault.save_markdown("papers", "group/paper.md", "body")
        basename = os.path.basename(path)
        assert "/" not in basename
        assert "_" in basename

    def test_backslash_in_filename_sanitized(self, vault):
        path = vault.save_markdown("papers", "foo\\bar.md", "body")
        basename = os.path.basename(path)
        assert "\\" not in basename

    def test_other_illegal_chars_sanitized(self, vault):
        """Characters * ? : < > | must be replaced."""
        path = vault.save_markdown("papers", 'bad*:?"<>|name.md', "body")
        basename = os.path.basename(path)
        for ch in '*?:"<>|':
            assert ch not in basename

    def test_invalid_category_raises_value_error(self, vault):
        with pytest.raises(ValueError, match="Invalid vault category"):
            vault.save_markdown("nonexistent", "file.md", "body")

    def test_body_content_written_to_disk(self, vault):
        body = "This is my paper body."
        path = vault.save_markdown("papers", "body_test.md", body)
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        assert body in raw

    def test_frontmatter_scalar_written(self, vault):
        fm = {"title": "My Paper", "author": "Alice"}
        path = vault.save_markdown("papers", "fm_scalar.md", "body", frontmatter=fm)
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        assert raw.startswith("---\n")
        assert 'title: "My Paper"' in raw
        assert 'author: "Alice"' in raw

    def test_frontmatter_list_written(self, vault):
        fm = {"tags": ["ai", "nlp", "llm"]}
        path = vault.save_markdown("papers", "fm_list.md", "body", frontmatter=fm)
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        assert "tags:" in raw
        assert '- "ai"' in raw
        assert '- "nlp"' in raw
        assert '- "llm"' in raw

    def test_no_frontmatter_writes_body_only(self, vault):
        body = "Plain body, no metadata."
        path = vault.save_markdown("concepts", "plain.md", body)
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        assert not raw.startswith("---")
        assert raw == body

    def test_returns_absolute_path(self, vault):
        path = vault.save_markdown("debates", "debate.md", "body")
        assert os.path.isabs(path)

    def test_overwrites_existing_file(self, vault):
        vault.save_markdown("drafts", "overwrite.md", "old content")
        vault.save_markdown("drafts", "overwrite.md", "new content")
        with open(os.path.join(vault.folders["drafts"], "overwrite.md"), encoding="utf-8") as f:
            raw = f.read()
        assert "new content" in raw
        assert "old content" not in raw


# ---------------------------------------------------------------------------
# read_markdown
# ---------------------------------------------------------------------------

class TestReadMarkdown:
    def test_round_trip_body_only(self, vault):
        """Content written without frontmatter must come back intact."""
        vault.save_markdown("concepts", "rt_body.md", "Hello world")
        result = vault.read_markdown("concepts", "rt_body.md")
        assert result["content"] == "Hello world"
        assert result["frontmatter"] == {}

    def test_round_trip_with_frontmatter_scalars(self, vault):
        fm = {"title": "Round Trip", "author": "Bob"}
        vault.save_markdown("papers", "rt_fm.md", "body text", frontmatter=fm)
        result = vault.read_markdown("papers", "rt_fm.md")
        assert result["frontmatter"]["title"] == "Round Trip"
        assert result["frontmatter"]["author"] == "Bob"
        assert "body text" in result["content"]

    def test_round_trip_with_frontmatter_lists(self, vault):
        fm = {"tags": ["a", "b", "c"]}
        vault.save_markdown("papers", "rt_list.md", "body", frontmatter=fm)
        result = vault.read_markdown("papers", "rt_list.md")
        assert isinstance(result["frontmatter"]["tags"], list)
        assert set(result["frontmatter"]["tags"]) == {"a", "b", "c"}

    def test_auto_appends_md_extension(self, vault):
        vault.save_markdown("concepts", "auto_ext.md", "content")
        # Read without the extension
        result = vault.read_markdown("concepts", "auto_ext")
        assert result["content"] == "content"

    def test_missing_file_raises_file_not_found(self, vault):
        with pytest.raises(FileNotFoundError):
            vault.read_markdown("papers", "does_not_exist.md")

    def test_invalid_category_raises_value_error(self, vault):
        with pytest.raises(ValueError, match="Invalid vault category"):
            vault.read_markdown("badcat", "file.md")

    def test_returns_dict_with_required_keys(self, vault):
        vault.save_markdown("drafts", "keys_test.md", "content")
        result = vault.read_markdown("drafts", "keys_test.md")
        assert "frontmatter" in result
        assert "content" in result


# ---------------------------------------------------------------------------
# list_files
# ---------------------------------------------------------------------------

class TestListFiles:
    def test_empty_category_returns_empty_list(self, vault):
        result = vault.list_files("papers")
        assert result == []

    def test_saved_file_appears_in_listing(self, vault):
        vault.save_markdown("papers", "listed.md", "body", frontmatter={"title": "Listed"})
        result = vault.list_files("papers")
        filenames = [item["filename"] for item in result]
        assert "listed.md" in filenames

    def test_multiple_files_all_listed(self, vault):
        vault.save_markdown("papers", "p1.md", "body")
        vault.save_markdown("papers", "p2.md", "body")
        vault.save_markdown("papers", "p3.md", "body")
        result = vault.list_files("papers")
        assert len(result) == 3

    def test_list_items_contain_required_keys(self, vault):
        vault.save_markdown("concepts", "struct.md", "body", frontmatter={"title": "T"})
        result = vault.list_files("concepts")
        item = result[0]
        for key in ("filename", "title", "metadata", "content_preview"):
            assert key in item, f"Key '{key}' missing from list_files item"

    def test_title_from_frontmatter(self, vault):
        vault.save_markdown("papers", "titled.md", "body", frontmatter={"title": "Great Paper"})
        result = vault.list_files("papers")
        assert result[0]["title"] == "Great Paper"

    def test_title_falls_back_to_stem_when_no_frontmatter(self, vault):
        vault.save_markdown("papers", "my_stem.md", "body")
        result = vault.list_files("papers")
        assert result[0]["title"] == "my_stem"

    def test_content_preview_truncated_at_200_chars(self, vault):
        long_body = "x" * 500
        vault.save_markdown("papers", "long.md", long_body)
        result = vault.list_files("papers")
        assert len(result[0]["content_preview"]) <= 203  # 200 + "..."

    def test_invalid_category_raises_value_error(self, vault):
        with pytest.raises(ValueError, match="Invalid vault category"):
            vault.list_files("nonexistent")

    def test_non_md_files_not_included(self, vault):
        """A .txt file placed in the folder must not appear in the listing."""
        txt_path = os.path.join(vault.folders["papers"], "note.txt")
        with open(txt_path, "w") as f:
            f.write("not markdown")
        result = vault.list_files("papers")
        filenames = [item["filename"] for item in result]
        assert "note.txt" not in filenames


# ---------------------------------------------------------------------------
# parse_markdown_content
# ---------------------------------------------------------------------------

class TestParseMarkdownContent:
    def setup_method(self):
        # parse_markdown_content is a pure function; instantiate minimally.
        # We need a VaultManager but we don't care about the path for this test.
        import tempfile
        self._tmp = tempfile.mkdtemp()
        self.vm = VaultManager(self._tmp)

    def test_no_frontmatter_returns_full_text_as_content(self):
        text = "Just body text\nNo frontmatter here."
        result = self.vm.parse_markdown_content(text)
        assert result["content"] == text
        assert result["frontmatter"] == {}

    def test_frontmatter_scalar_parsed(self):
        text = '---\ntitle: "My Title"\nauthor: "Alice"\n---\nbody'
        result = self.vm.parse_markdown_content(text)
        assert result["frontmatter"]["title"] == "My Title"
        assert result["frontmatter"]["author"] == "Alice"
        assert result["content"] == "body"

    def test_frontmatter_list_parsed(self):
        text = '---\ntags:\n  - "ai"\n  - "ml"\n---\nbody'
        result = self.vm.parse_markdown_content(text)
        assert isinstance(result["frontmatter"]["tags"], list)
        assert "ai" in result["frontmatter"]["tags"]
        assert "ml" in result["frontmatter"]["tags"]

    def test_empty_frontmatter_block(self):
        text = "---\n\n---\nbody after empty frontmatter"
        result = self.vm.parse_markdown_content(text)
        # Frontmatter block is empty; content must still be extracted correctly.
        assert "body after empty frontmatter" in result["content"]

    def test_body_preserved_after_frontmatter(self):
        text = '---\ntitle: "T"\n---\nLine 1\nLine 2'
        result = self.vm.parse_markdown_content(text)
        assert "Line 1" in result["content"]
        assert "Line 2" in result["content"]


# ---------------------------------------------------------------------------
# get_knowledge_graph
# ---------------------------------------------------------------------------

class TestGetKnowledgeGraph:
    def test_empty_vault_returns_empty_nodes_and_edges(self, vault):
        graph = vault.get_knowledge_graph()
        assert graph == {"nodes": [], "edges": []}

    def test_returns_dict_with_nodes_and_edges_keys(self, vault):
        graph = vault.get_knowledge_graph()
        assert "nodes" in graph
        assert "edges" in graph
        assert isinstance(graph["nodes"], list)
        assert isinstance(graph["edges"], list)

    def test_single_file_becomes_one_node(self, vault):
        vault.save_markdown("papers", "solo.md", "no links here", frontmatter={"title": "Solo"})
        graph = vault.get_knowledge_graph()
        assert len(graph["nodes"]) == 1
        assert graph["edges"] == []

    def test_node_has_required_fields(self, vault):
        vault.save_markdown("concepts", "concept.md", "body", frontmatter={"title": "Concept A"})
        graph = vault.get_knowledge_graph()
        node = graph["nodes"][0]
        for field in ("id", "title", "category", "tags", "metadata"):
            assert field in node, f"Node missing field '{field}'"

    def test_node_id_format(self, vault):
        vault.save_markdown("papers", "my_paper.md", "body")
        graph = vault.get_knowledge_graph()
        node = graph["nodes"][0]
        assert node["id"] == "papers/my_paper.md"

    def test_node_category_matches_folder(self, vault):
        vault.save_markdown("debates", "d.md", "body")
        graph = vault.get_knowledge_graph()
        assert graph["nodes"][0]["category"] == "debates"

    def test_wikilink_creates_edge(self, vault):
        """A [[target]] link in a source file must produce a directed edge."""
        vault.save_markdown("papers", "source.md", "See [[target]]")
        vault.save_markdown("papers", "target.md", "Target body")
        graph = vault.get_knowledge_graph()
        edges = graph["edges"]
        assert len(edges) == 1
        edge = edges[0]
        assert edge["source"] == "papers/source.md"
        assert edge["target"] == "papers/target.md"
        assert edge["type"] == "links_to"

    def test_wikilink_with_label_creates_edge(self, vault):
        """[[Target|Custom Label]] must resolve correctly."""
        vault.save_markdown("papers", "src.md", "See [[tgt|My Label]]")
        vault.save_markdown("papers", "tgt.md", "Target")
        graph = vault.get_knowledge_graph()
        edges = graph["edges"]
        assert len(edges) == 1

    def test_unresolvable_wikilink_produces_no_edge(self, vault):
        """A link to a file that does not exist must not generate an edge."""
        vault.save_markdown("papers", "lonely.md", "See [[ghost]]")
        graph = vault.get_knowledge_graph()
        assert graph["edges"] == []

    def test_no_duplicate_edges(self, vault):
        """Two identical [[link]] occurrences must yield only one edge."""
        vault.save_markdown("papers", "dup_src.md", "See [[dup_tgt]] and [[dup_tgt]]")
        vault.save_markdown("papers", "dup_tgt.md", "Target")
        graph = vault.get_knowledge_graph()
        assert len(graph["edges"]) == 1

    def test_multiple_files_across_categories(self, vault):
        vault.save_markdown("papers", "p.md", "body", frontmatter={"title": "P"})
        vault.save_markdown("concepts", "c.md", "body", frontmatter={"title": "C"})
        vault.save_markdown("debates", "d.md", "body", frontmatter={"title": "D"})
        graph = vault.get_knowledge_graph()
        assert len(graph["nodes"]) == 3

    def test_no_self_edges(self, vault):
        """A file linking to itself by name must not produce an edge."""
        vault.save_markdown("papers", "self_ref.md", "See [[self_ref]]")
        graph = vault.get_knowledge_graph()
        assert graph["edges"] == []
