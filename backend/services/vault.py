import os
import re
from typing import Dict, List, Any, Optional

class VaultManager:
    def __init__(self, vault_path: str = "../vault"):
        # Resolve path relative to script root if it is default or relative
        if not vault_path or vault_path == "../vault" or vault_path == "vault":
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            self.vault_path = os.path.join(base_dir, "vault")
        elif not os.path.isabs(vault_path):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            self.vault_path = os.path.abspath(os.path.join(base_dir, vault_path))
        else:
            self.vault_path = os.path.abspath(vault_path)

        self.folders = {
            "papers": os.path.join(self.vault_path, "01_Papers"),
            "concepts": os.path.join(self.vault_path, "02_Concepts"),
            "debates": os.path.join(self.vault_path, "03_Debates"),
            "drafts": os.path.join(self.vault_path, "04_Drafts"),
        }
        self._ensure_folders_exist()

    def _ensure_folders_exist(self):
        """Creates the vault directory and subdirectories if they do not exist."""
        os.makedirs(self.vault_path, exist_ok=True)
        for path in self.folders.values():
            os.makedirs(path, exist_ok=True)

    def _clean_filename(self, filename: str) -> str:
        """Strips category/folder prefixes, spaces, and ensures .md extension."""
        if not filename:
            return ""
        cleaned = os.path.basename(filename.strip().replace(" ", ""))
        if not cleaned.endswith(".md"):
            cleaned += ".md"
        return cleaned

    def save_markdown(self, category: str, filename: str, content: str, frontmatter: Dict[str, Any] = None) -> str:
        """Saves a markdown file with optional YAML frontmatter.

        Args:
            category: One of 'papers', 'concepts', 'debates', 'drafts'
            filename: Name of the file (e.g. 'paper_1.md')
            content: Main markdown content
            frontmatter: Dictionary of key-value metadata to write to YAML frontmatter

        Returns:
            The absolute path to the saved file.
        """
        if category not in self.folders:
            raise ValueError(f"Invalid vault category: {category}")

        filename = self._clean_filename(filename)
        file_path = os.path.join(self.folders[category], filename)

        # Build YAML frontmatter string
        file_content = ""
        if frontmatter:
            file_content += "---\n"
            for key, val in frontmatter.items():
                if isinstance(val, list):
                    file_content += f"{key}:\n"
                    for item in val:
                        file_content += f"  - \"{item}\"\n"
                else:
                    file_content += f"{key}: \"{val}\"\n"
            file_content += "---\n"

        file_content += content

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)

        return file_path

    def read_markdown(self, category: str, filename: str) -> Dict[str, Any]:
        """Reads a markdown file and parses YAML frontmatter and body."""
        if category not in self.folders:
            raise ValueError(f"Invalid vault category: {category}")

        filename = self._clean_filename(filename)

        file_path = os.path.join(self.folders[category], filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found in vault: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        return self.parse_markdown_content(text)

    def parse_markdown_content(self, text: str) -> Dict[str, Any]:
        """Helper to parse raw markdown text into frontmatter dict and body content."""
        frontmatter = {}
        content = text

        # Match YAML block at the beginning
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if match:
            fm_text = match.group(1)
            content = text[match.end():]

            # Simple YAML parser
            current_key = None
            for line in fm_text.split("\n"):
                if not line.strip():
                    continue
                # Array item
                if line.startswith("  -") or line.startswith("-"):
                    val = line.split("-", 1)[1].strip().strip('"').strip("'")
                    if current_key and isinstance(frontmatter.get(current_key), list):
                        frontmatter[current_key].append(val)
                elif ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if not val: # Might be start of list
                        frontmatter[key] = []
                        current_key = key
                    else:
                        if val.startswith("{") and val.endswith("}"):
                            import ast
                            try:
                                val = ast.literal_eval(val)
                            except Exception:
                                pass
                        frontmatter[key] = val
                        current_key = None

        return {
            "frontmatter": frontmatter,
            "content": content
        }

    def list_files(self, category: str) -> List[Dict[str, Any]]:
        """Lists files and their parsed metadata in a category."""
        if category not in self.folders:
            raise ValueError(f"Invalid vault category: {category}")

        folder_path = self.folders[category]
        files_data = []

        for file in os.listdir(folder_path):
            if file.endswith(".md"):
                try:
                    data = self.read_markdown(category, file)
                    files_data.append({
                        "filename": file,
                        "title": data["frontmatter"].get("title", file[:-3]),
                        "metadata": data["frontmatter"],
                        "content_preview": data["content"][:200] + "..." if len(data["content"]) > 200 else data["content"]
                    })
                except Exception as e:
                    # Ignore malformed files or log error
                    print(f"Error reading file {file}: {e}")

        return files_data

    def get_knowledge_graph(self) -> Dict[str, List[Dict[str, Any]]]:
        """Scans the entire vault, finds wiki links `[[WikiLink]]`, and builds a node-edge graph."""
        nodes = []
        edges = []

        # Keep track of added node IDs to prevent duplicates
        added_node_ids = set()

        # Map titles/filenames to IDs for link resolution
        title_to_id = {}

        # Temporary storage of parsed files
        all_files = []

        for category, folder_path in self.folders.items():
            for file in os.listdir(folder_path):
                if file.endswith(".md"):
                    try:
                        file_path = os.path.join(folder_path, file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            raw_text = f.read()

                        data = self.parse_markdown_content(raw_text)

                        # Node ID based on category and sanitized filename
                        node_id = f"{category}/{file}"
                        title = data["frontmatter"].get("title", file[:-3])

                        title_to_id[title.lower()] = node_id
                        title_to_id[file.lower()] = node_id
                        title_to_id[file[:-3].lower()] = node_id

                        all_files.append({
                            "id": node_id,
                            "title": title,
                            "category": category,
                            "content": data["content"],
                            "tags": data["frontmatter"].get("tags", []),
                            "metadata": data["frontmatter"]
                        })
                    except Exception as e:
                        print(f"Error processing node {file}: {e}")

        # 1. Add all nodes to graph
        for f in all_files:
            nodes.append({
                "id": f["id"],
                "title": f["title"],
                "category": f["category"],
                "tags": f["tags"],
                "metadata": f["metadata"]
            })
            added_node_ids.add(f["id"])

        # 2. Extract WikiLinks and build edges
        # Regex to find [[WikiLink]] or [[WikiLink|Custom Label]]
        wikilink_re = re.compile(r"\[\[(.*?)\]\]")

        # Set for O(1) edge existence checks
        edge_set = set()

        for f in all_files:
            source_id = f["id"]
            links = wikilink_re.findall(f["content"])

            # Also parse links from YAML frontmatter 'references' or similar if present
            references = f["metadata"].get("references", [])
            if isinstance(references, str):
                references = [references]
            links.extend(references)

            for link in links:
                # Resolve link label (in case of [[Link|Label]])
                target_label = link.split("|")[0].strip()
                target_key = target_label.lower()

                # Check if we can resolve this label to a node ID
                target_id = None
                if target_key in title_to_id:
                    target_id = title_to_id[target_key]
                elif f"{target_key}.md" in title_to_id:
                    target_id = title_to_id[f"{target_key}.md"]
                else:
                    # Let's search inside categories as fallback
                    for cat in self.folders.keys():
                        potential_key = f"{cat}/{target_label}.md".lower()
                        if potential_key in added_node_ids:
                            target_id = potential_key
                            break

                # If target node exists, add a directed edge
                if target_id and target_id != source_id:
                    edge_key = (source_id, target_id)
                    if edge_key not in edge_set:
                        edge_set.add(edge_key)
                        edges.append({
                            "source": source_id,
                            "target": target_id,
                            "type": "links_to"
                        })

        return {
            "nodes": nodes,
            "edges": edges
        }
