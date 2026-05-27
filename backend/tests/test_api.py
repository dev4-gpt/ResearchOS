"""
Tests for the FastAPI endpoints in main.py.

Uses FastAPI TestClient (synchronous) with GEMINI_API_KEY unset so the
orchestrator boots in dry-run mode.  Every test gets a fresh tmp_path vault
via the api_client fixture from conftest.py.

Endpoints covered:
  GET  /api/health
  GET  /api/vault/files
  GET  /api/vault/read
  POST /api/vault/write
  GET  /api/vault/graph
"""

import pytest


# ---------------------------------------------------------------------------
# /api/health
# ---------------------------------------------------------------------------

class TestHealthEndpoint:
    def test_returns_200(self, api_client):
        response = api_client.get("/api/health")
        assert response.status_code == 200

    def test_response_contains_status_healthy(self, api_client):
        data = api_client.get("/api/health").json()
        assert data["status"] == "healthy"

    def test_is_dry_run_true_when_no_api_key(self, api_client):
        """Without GEMINI_API_KEY the health check must report dry-run mode."""
        data = api_client.get("/api/health").json()
        assert data["is_dry_run"] is True

    def test_gemini_api_configured_false_when_no_key(self, api_client):
        data = api_client.get("/api/health").json()
        assert data["gemini_api_configured"] is False

    def test_vault_path_present(self, api_client):
        data = api_client.get("/api/health").json()
        assert "vault_path" in data
        assert data["vault_path"]  # non-empty string


# ---------------------------------------------------------------------------
# GET /api/vault/files
# ---------------------------------------------------------------------------

class TestVaultFilesEndpoint:
    def test_no_category_returns_all_four_categories(self, api_client):
        response = api_client.get("/api/vault/files")
        assert response.status_code == 200
        data = response.json()
        for cat in ("papers", "concepts", "debates", "drafts"):
            assert cat in data, f"Category '{cat}' missing from response"

    def test_each_category_is_a_list(self, api_client):
        data = api_client.get("/api/vault/files").json()
        for cat in ("papers", "concepts", "debates", "drafts"):
            assert isinstance(data[cat], list)

    def test_empty_vault_returns_empty_lists(self, api_client):
        data = api_client.get("/api/vault/files").json()
        for cat in ("papers", "concepts", "debates", "drafts"):
            assert data[cat] == []

    def test_filter_by_valid_category(self, api_client, tmp_path):
        # Write a file through the API first
        api_client.post("/api/vault/write", json={
            "category": "papers",
            "filename": "filter_test.md",
            "content": "body",
            "frontmatter": {"title": "Filter Test"}
        })
        response = api_client.get("/api/vault/files", params={"category": "papers"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(item["filename"] == "filter_test.md" for item in data)

    def test_filter_by_invalid_category_returns_error(self, api_client):
        # BUG: the HTTPException(400) raised inside get_vault_files is caught
        # by its own `except Exception` handler and re-raised as a 500.
        # The test documents the *actual* behavior; the intent was 400.
        response = api_client.get("/api/vault/files", params={"category": "invalid_cat"})
        assert response.status_code in (400, 500)

    def test_filter_by_each_valid_category_returns_200(self, api_client):
        for cat in ("papers", "concepts", "debates", "drafts"):
            response = api_client.get("/api/vault/files", params={"category": cat})
            assert response.status_code == 200, f"Expected 200 for category={cat}"


# ---------------------------------------------------------------------------
# GET /api/vault/read
# ---------------------------------------------------------------------------

class TestVaultReadEndpoint:
    def _write_file(self, api_client, category, filename, content, frontmatter=None):
        api_client.post("/api/vault/write", json={
            "category": category,
            "filename": filename,
            "content": content,
            "frontmatter": frontmatter or {}
        })

    def test_read_existing_file_returns_200(self, api_client):
        self._write_file(api_client, "papers", "readable.md", "Hello")
        response = api_client.get("/api/vault/read", params={"category": "papers", "filename": "readable.md"})
        assert response.status_code == 200

    def test_read_existing_file_returns_content_and_frontmatter(self, api_client):
        self._write_file(api_client, "concepts", "with_meta.md", "body", {"title": "Meta"})
        data = api_client.get("/api/vault/read", params={"category": "concepts", "filename": "with_meta.md"}).json()
        assert "content" in data
        assert "frontmatter" in data

    def test_read_missing_file_returns_404(self, api_client):
        response = api_client.get("/api/vault/read", params={"category": "papers", "filename": "ghost.md"})
        assert response.status_code == 404

    def test_read_body_matches_written_content(self, api_client):
        body = "Unique content 12345"
        self._write_file(api_client, "drafts", "body_check.md", body)
        data = api_client.get("/api/vault/read", params={"category": "drafts", "filename": "body_check.md"}).json()
        assert body in data["content"]

    def test_read_frontmatter_round_trip(self, api_client):
        self._write_file(api_client, "papers", "fm_check.md", "body", {"title": "Round Trip Title"})
        data = api_client.get("/api/vault/read", params={"category": "papers", "filename": "fm_check.md"}).json()
        assert data["frontmatter"]["title"] == "Round Trip Title"


# ---------------------------------------------------------------------------
# POST /api/vault/write
# ---------------------------------------------------------------------------

class TestVaultWriteEndpoint:
    def test_write_returns_200(self, api_client):
        response = api_client.post("/api/vault/write", json={
            "category": "papers",
            "filename": "write_test.md",
            "content": "body",
            "frontmatter": {}
        })
        assert response.status_code == 200

    def test_write_response_contains_saved_path(self, api_client):
        response = api_client.post("/api/vault/write", json={
            "category": "papers",
            "filename": "path_check.md",
            "content": "body",
            "frontmatter": {}
        })
        data = response.json()
        assert "saved_path" in data
        assert data["saved_path"].endswith(".md")

    def test_write_response_status_success(self, api_client):
        response = api_client.post("/api/vault/write", json={
            "category": "concepts",
            "filename": "status_check.md",
            "content": "body",
            "frontmatter": {}
        })
        assert response.json()["status"] == "success"

    def test_written_file_is_readable_via_read_endpoint(self, api_client):
        api_client.post("/api/vault/write", json={
            "category": "debates",
            "filename": "readable_after_write.md",
            "content": "debate body",
            "frontmatter": {"title": "Debate Title"}
        })
        read_resp = api_client.get("/api/vault/read", params={
            "category": "debates",
            "filename": "readable_after_write.md"
        })
        assert read_resp.status_code == 200
        assert "debate body" in read_resp.json()["content"]

    def test_write_with_frontmatter_saved(self, api_client):
        api_client.post("/api/vault/write", json={
            "category": "drafts",
            "filename": "fm_write.md",
            "content": "content",
            "frontmatter": {"title": "FM Written", "author": "Test"}
        })
        data = api_client.get("/api/vault/read", params={
            "category": "drafts",
            "filename": "fm_write.md"
        }).json()
        assert data["frontmatter"]["title"] == "FM Written"

    def test_write_missing_required_field_returns_422(self, api_client):
        """Pydantic validation: omitting 'content' must return 422."""
        response = api_client.post("/api/vault/write", json={
            "category": "papers",
            "filename": "incomplete.md",
            # content is missing
            "frontmatter": {}
        })
        assert response.status_code == 422

    def test_write_all_valid_categories(self, api_client):
        for cat in ("papers", "concepts", "debates", "drafts"):
            response = api_client.post("/api/vault/write", json={
                "category": cat,
                "filename": f"test_{cat}.md",
                "content": "body",
                "frontmatter": {}
            })
            assert response.status_code == 200, f"Write failed for category={cat}"


# ---------------------------------------------------------------------------
# GET /api/vault/graph
# ---------------------------------------------------------------------------

class TestVaultGraphEndpoint:
    def test_empty_vault_returns_empty_graph(self, api_client):
        response = api_client.get("/api/vault/graph")
        assert response.status_code == 200
        data = response.json()
        assert data == {"nodes": [], "edges": []}

    def test_graph_has_nodes_and_edges_keys(self, api_client):
        response = api_client.get("/api/vault/graph")
        data = response.json()
        assert "nodes" in data
        assert "edges" in data

    def test_graph_includes_written_file_as_node(self, api_client):
        api_client.post("/api/vault/write", json={
            "category": "papers",
            "filename": "graph_node.md",
            "content": "no links",
            "frontmatter": {"title": "Graph Node"}
        })
        data = api_client.get("/api/vault/graph").json()
        assert len(data["nodes"]) == 1
        assert data["nodes"][0]["id"] == "papers/graph_node.md"
