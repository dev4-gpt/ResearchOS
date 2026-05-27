import os
import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import urllib.parse

_CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "aryamandev777@gmail.com")
_POLITE_UA = f"ResearchingOS/0.1 (mailto:{_CONTACT_EMAIL})"

class AcademicSearchService:
    def __init__(self):
        self.client = httpx.Client(timeout=20.0, follow_redirects=True)

    def search_arxiv(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the arXiv API for papers related to the query."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results={limit}&sortBy=relevance"

        try:
            response = self.client.get(url, timeout=10.0)
            if response.status_code != 200:
                print(f"arXiv API returned status {response.status_code}")
                return []
                
            # Parse XML response
            root = ET.fromstring(response.content)
            
            # XML namespaces
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            papers = []
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                id_elem = entry.find('atom:id', ns)
                published_elem = entry.find('atom:published', ns)

                title = (title_elem.text or "").strip().replace("\n", " ") if title_elem is not None else "Untitled"
                summary = (summary_elem.text or "").strip().replace("\n", " ") if summary_elem is not None else ""
                url_link = (id_elem.text or "").strip() if id_elem is not None else ""
                published_raw = (published_elem.text or "").strip() if published_elem is not None else ""
                published = published_raw[:10]

                arxiv_id = url_link.split("/abs/")[-1].split("v")[0] if url_link else ""

                authors = []
                for author in entry.findall('atom:author', ns):
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text.strip())

                papers.append({
                    "id": f"arxiv:{arxiv_id}" if arxiv_id else url_link,
                    "title": title or "Untitled",
                    "authors": authors,
                    "abstract": summary,
                    "url": url_link,
                    "published": published,
                    "citations": 0,
                    "source": "arXiv"
                })
            return papers
        except Exception as e:
            print(f"Error querying arXiv: {e}")
            return []

    def fetch_arxiv_by_ids(self, ids: List[str]) -> List[Dict[str, Any]]:
        """Fetches specific papers from the arXiv API by their IDs."""
        if not ids:
            return []
        import re
        sanitized_ids = [re.sub(r'[^0-9.]', '', idx) for idx in ids]
        sanitized_ids = [idx for idx in sanitized_ids if idx]
        if not sanitized_ids:
            return []
        
        ids_str = ",".join(sanitized_ids)
        url = f"https://export.arxiv.org/api/query?id_list={ids_str}"

        try:
            response = self.client.get(url, timeout=10.0)
            if response.status_code != 200:
                print(f"arXiv API returned status {response.status_code}")
                return []
                
            # Parse XML response
            root = ET.fromstring(response.content)
            
            # XML namespaces
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            papers = []
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                id_elem = entry.find('atom:id', ns)
                published_elem = entry.find('atom:published', ns)

                title = (title_elem.text or "").strip().replace("\n", " ") if title_elem is not None else "Untitled"
                summary = (summary_elem.text or "").strip().replace("\n", " ") if summary_elem is not None else ""
                url_link = (id_elem.text or "").strip() if id_elem is not None else ""
                published_raw = (published_elem.text or "").strip() if published_elem is not None else ""
                published = published_raw[:10]

                arxiv_id = url_link.split("/abs/")[-1].split("v")[0] if url_link else ""

                authors = []
                for author in entry.findall('atom:author', ns):
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text.strip())

                if title or summary:
                    papers.append({
                        "id": f"arxiv:{arxiv_id}" if arxiv_id else url_link,
                        "title": title or "Untitled",
                        "authors": authors,
                        "abstract": summary,
                        "url": url_link,
                        "published": published,
                        "citations": 0,
                        "source": "arXiv"
                    })
            return papers
        except Exception as e:
            print(f"Error fetching specific papers from arXiv: {e}")
            return []

    def search_openalex(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the OpenAlex API for research works, including citation metadata."""
        encoded_query = urllib.parse.quote(query)
        # OpenAlex requires a user-agent/email for the polite pool, let's add a custom header
        headers = {
            "User-Agent": _POLITE_UA
        }
        url = f"https://api.openalex.org/works?search={encoded_query}&per-page={limit}"
        
        try:
            response = self.client.get(url, headers=headers)
            if response.status_code != 200:
                print(f"OpenAlex API returned status {response.status_code}")
                return []
                
            data = response.json()
            papers = []
            
            for work in data.get("results", []):
                title = work.get("title", "Untitled")
                doi = work.get("doi", "")
                url_link = work.get("id", doi or "")
                
                # Retrieve citations count
                citations = work.get("cited_by_count", 0)
                published = work.get("publication_date", "")
                
                # Extract abstract (OpenAlex uses inverted index for abstracts to comply with copyright)
                abstract_inverted = work.get("abstract_inverted_index", {})
                abstract = ""
                if abstract_inverted:
                    # Reconstruct abstract from inverted index
                    words_pos = []
                    for word, positions in abstract_inverted.items():
                        for pos in positions:
                            words_pos.append((pos, word))
                    words_pos.sort()
                    abstract = " ".join([word for _, word in words_pos])
                
                authors = []
                for authorship in work.get("authorships", []):
                    author = authorship.get("author", {})
                    if author.get("display_name"):
                        authors.append(author.get("display_name"))
                
                # Standardize paper representation
                papers.append({
                    "id": f"openalex:{work.get('id').split('/')[-1]}" if work.get('id') else url_link,
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "url": url_link,
                    "published": published,
                    "citations": citations,
                    "source": "OpenAlex"
                })
            return papers
        except Exception as e:
            print(f"Error querying OpenAlex: {e}")
            return []

    def search_semanticscholar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the Semantic Scholar API for research works, including citation metadata."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded_query}&limit={limit}&fields=title,authors,abstract,url,citationCount,publicationDate"
        
        try:
            response = self.client.get(url, timeout=5.0)
            if response.status_code != 200:
                print(f"Semantic Scholar API returned status {response.status_code}")
                return []
                
            data = response.json()
            papers = []
            
            for work in data.get("data", []):
                title = work.get("title", "Untitled")
                paper_id = work.get("paperId", "")
                url_link = work.get("url") or f"https://www.semanticscholar.org/paper/{paper_id}" if paper_id else ""
                
                # Retrieve citations count
                citations = work.get("citationCount", 0) or 0
                published = work.get("publicationDate", "") or ""
                abstract = work.get("abstract", "") or ""
                
                authors = []
                for author in work.get("authors", []):
                    if author.get("name"):
                        authors.append(author["name"])
                
                # Standardize paper representation
                papers.append({
                    "id": f"semanticscholar:{paper_id}" if paper_id else url_link,
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "url": url_link,
                    "published": published,
                    "citations": citations,
                    "source": "Semantic Scholar"
                })
            return papers
        except Exception as e:
            print(f"Error querying Semantic Scholar: {e}")
            return []

    def search_europepmc(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the EuropePMC API for research works, including citation metadata."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={encoded_query}&format=json&pageSize={limit}"
        
        try:
            response = self.client.get(url, timeout=5.0)
            if response.status_code != 200:
                print(f"EuropePMC API returned status {response.status_code}")
                return []
                
            data = response.json()
            papers = []
            
            results = data.get("resultList", {}).get("result", [])
            for work in results:
                title = work.get("title", "Untitled")
                pmcid = work.get("pmcid", "")
                pmid = work.get("id", "")
                doi = work.get("doi", "")
                
                url_link = ""
                if pmcid:
                    url_link = f"https://europepmc.org/article/PMC/{pmcid}"
                elif doi:
                    url_link = f"https://doi.org/{doi}"
                elif pmid:
                    url_link = f"https://europepmc.org/article/MED/{pmid}"
                
                citations = work.get("citedByCount", 0) or 0
                published = work.get("pubYear", "") or ""
                abstract = work.get("abstractText", "") or ""
                
                # Parse author string if list isn't provided
                authors = []
                author_string = work.get("authorString", "")
                if author_string:
                    authors = [a.strip() for a in author_string.split(",") if a.strip()]
                
                paper_id = pmcid or pmid or doi or title.replace(" ", "_")
                
                # Standardize paper representation
                papers.append({
                    "id": f"europepmc:{paper_id}",
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "url": url_link,
                    "published": published,
                    "citations": citations,
                    "source": "EuropePMC"
                })
            return papers
        except Exception as e:
            print(f"Error querying EuropePMC: {e}")
            return []

    def search_crossref(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the Crossref REST API for research works."""
        encoded_query = urllib.parse.quote(query)
        headers = {
            "User-Agent": _POLITE_UA
        }
        url = f"https://api.crossref.org/works?query={encoded_query}&rows={limit}"
        
        try:
            response = self.client.get(url, headers=headers, timeout=5.0)
            if response.status_code != 200:
                print(f"Crossref API returned status {response.status_code}")
                return []
                
            data = response.json()
            papers = []
            
            for item in data.get("message", {}).get("items", []):
                title = item.get("title", ["Untitled"])[0] if item.get("title") else "Untitled"
                doi = item.get("DOI", "")
                url_link = item.get("URL", f"https://doi.org/{doi}" if doi else "")
                
                citations = item.get("is-referenced-by-count", 0) or 0
                
                published = ""
                created = item.get("created", {})
                if created.get("date-parts"):
                    published = "-".join(map(str, created["date-parts"][0]))
                
                abstract = item.get("abstract", "") or ""
                import re
                abstract = re.sub(r'<[^>]+>', '', abstract).strip()
                
                authors = []
                for author in item.get("author", []):
                    name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                    if name:
                        authors.append(name)
                
                papers.append({
                    "id": f"crossref:{doi}" if doi else url_link,
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "url": url_link,
                    "published": published,
                    "citations": citations,
                    "source": "Crossref"
                })
            return papers
        except Exception as e:
            print(f"Error querying Crossref: {e}")
            return []

    def search_doaj(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the DOAJ REST API for open access articles."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://doaj.org/api/v2/search/articles/{encoded_query}?pageSize={limit}"
        
        try:
            response = self.client.get(url, timeout=5.0)
            if response.status_code != 200:
                print(f"DOAJ API returned status {response.status_code}")
                return []
                
            data = response.json()
            papers = []
            
            for result in data.get("results", []):
                bib = result.get("bibjson", {})
                title = bib.get("title", "Untitled")
                
                url_link = ""
                for link in bib.get("link", []):
                    if link.get("url"):
                        url_link = link["url"]
                        break
                        
                published = bib.get("year", "")
                abstract = bib.get("abstract", "") or ""
                
                authors = []
                for author in bib.get("author", []):
                    if author.get("name"):
                        authors.append(author["name"])
                        
                citations = 0
                paper_id = result.get("id", title.replace(" ", "_"))
                
                papers.append({
                    "id": f"doaj:{paper_id}",
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "url": url_link,
                    "published": published,
                    "citations": citations,
                    "source": "DOAJ"
                })
            return papers
        except Exception as e:
            print(f"Error querying DOAJ: {e}")
            return []

    def search_plos(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the PLOS Solr API for research articles."""
        encoded_query = urllib.parse.quote(query)
        url = f"http://api.plos.org/search?q={encoded_query}&wt=json&fl=id,title,author,abstract,publication_date&rows={limit}"
        
        try:
            response = self.client.get(url, timeout=5.0)
            if response.status_code != 200:
                print(f"PLOS API returned status {response.status_code}")
                return []
                
            data = response.json()
            papers = []
            
            for doc in data.get("response", {}).get("docs", []):
                title = doc.get("title", "Untitled")
                doi = doc.get("id", "")
                url_link = f"https://doi.org/{doi}" if doi else ""
                
                abstract_list = doc.get("abstract", [])
                abstract = abstract_list[0] if abstract_list else ""
                
                published = doc.get("publication_date", "")[:10]
                authors = doc.get("author", [])
                
                papers.append({
                    "id": f"plos:{doi}" if doi else url_link,
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "url": url_link,
                    "published": published,
                    "citations": 0,
                    "source": "PLOS"
                })
            return papers
        except Exception as e:
            print(f"Error querying PLOS: {e}")
            return []

    def search_hal(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the HAL French Open Science Archive search API."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.hal.science/search/?q={encoded_query}&fl=docid,title_s,abstract_s,authFullName_s,uri_s,producedDateY_i&wt=json&rows={limit}"
        
        try:
            response = self.client.get(url, timeout=5.0)
            if response.status_code != 200:
                print(f"HAL API returned status {response.status_code}")
                return []
                
            data = response.json()
            papers = []
            
            for doc in data.get("response", {}).get("docs", []):
                title_list = doc.get("title_s", [])
                title = title_list[0] if title_list else "Untitled"
                
                abstract_list = doc.get("abstract_s", [])
                abstract = abstract_list[0] if abstract_list else ""
                
                url_link = doc.get("uri_s", "")
                published = str(doc.get("producedDateY_i", ""))
                authors = doc.get("authFullName_s", [])
                
                papers.append({
                    "id": f"hal:{doc.get('docid')}",
                    "title": title,
                    "authors": authors,
                    "abstract": abstract,
                    "url": url_link,
                    "published": published,
                    "citations": 0,
                    "source": "HAL"
                })
            return papers
        except Exception as e:
            print(f"Error querying HAL: {e}")
            return []

    def search_pubmed(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the NCBI Entrez ESearch & ESummary APIs."""
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={encoded_query}&retmode=json&retmax={limit}"
        
        try:
            response = self.client.get(search_url, timeout=5.0)
            if response.status_code != 200:
                print(f"PubMed ESearch returned status {response.status_code}")
                return []
                
            data = response.json()
            uids = data.get("esearchresult", {}).get("idlist", [])
            
            if not uids:
                return []
                
            uids_str = ",".join(uids)
            summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={uids_str}&retmode=json"
            
            response2 = self.client.get(summary_url, timeout=5.0)
            if response2.status_code != 200:
                print(f"PubMed ESummary returned status {response2.status_code}")
                return []
                
            summary_data = response2.json()
            results = summary_data.get("result", {})
            
            papers = []
            for uid in uids:
                item = results.get(uid, {})
                title = item.get("title", "Untitled")
                published = item.get("pubdate", "")[:10]
                
                authors = []
                for author in item.get("authors", []):
                    if author.get("name"):
                        authors.append(author["name"])
                        
                url_link = f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
                
                papers.append({
                    "id": f"pubmed:{uid}",
                    "title": title,
                    "authors": authors,
                    "abstract": "",
                    "url": url_link,
                    "published": published,
                    "citations": 0,
                    "source": "PubMed"
                })
            return papers
        except Exception as e:
            print(f"Error querying PubMed: {e}")
            return []

    def search_dblp(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the DBLP Computer Science bibliography REST API."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://dblp.org/search/publ/api?q={encoded_query}&format=json&h={limit}"
        
        try:
            response = self.client.get(url, timeout=5.0)
            if response.status_code != 200:
                print(f"DBLP API returned status {response.status_code}")
                return []
                
            data = response.json()
            papers = []
            
            hits = data.get("result", {}).get("hits", {}).get("hit", [])
            if isinstance(hits, dict):
                hits = [hits]
                
            for hit in hits:
                info = hit.get("info", {})
                title = info.get("title", "Untitled")
                
                authors = []
                author_data = info.get("authors", {}).get("author", [])
                if isinstance(author_data, dict):
                    author_data = [author_data]
                for author in author_data:
                    if author.get("$"):
                        authors.append(author["$"])
                        
                url_link = info.get("ee", "")
                published = info.get("year", "")
                doi = info.get("doi", "")
                
                paper_id = hit.get("@id", doi or title.replace(" ", "_"))
                
                papers.append({
                    "id": f"dblp:{paper_id}",
                    "title": title,
                    "authors": authors,
                    "abstract": "",
                    "url": url_link,
                    "published": published,
                    "citations": 0,
                    "source": "DBLP"
                })
            return papers
        except Exception as e:
            print(f"Error querying DBLP: {e}")
            return []

    def search_github(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the GitHub Repository Search API."""
        encoded_query = urllib.parse.quote(query)
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ResearchingOS/0.1"
        }
        url = f"https://api.github.com/search/repositories?q={encoded_query}&per-page={limit}"
        
        try:
            response = self.client.get(url, headers=headers, timeout=5.0)
            if response.status_code != 200:
                print(f"GitHub API returned status {response.status_code}")
                return []
                
            data = response.json()
            repos = []
            
            for item in data.get("items", []):
                full_name = item.get("full_name", "")
                description = item.get("description", "") or ""
                url_link = item.get("html_url", "")
                stars = item.get("stargazers_count", 0)
                language = item.get("language") or ""
                owner = item.get("owner", {}).get("login", "")
                published = item.get("created_at", "")[:10]
                
                repos.append({
                    "id": f"github:{full_name}",
                    "title": f"Repository: {full_name} ({language})" if language else f"Repository: {full_name}",
                    "authors": [owner] if owner else [],
                    "abstract": f"GitHub Repository: {description} (Stars: {stars}, Language: {language})",
                    "url": url_link,
                    "published": published,
                    "citations": stars,
                    "source": "GitHub"
                })
            return repos
        except Exception as e:
            print(f"Error querying GitHub: {e}")
            return []

    def search_huggingface(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the Hugging Face Hub Models API."""
        encoded_query = urllib.parse.quote(query)
        url = f"https://huggingface.co/api/models?search={encoded_query}&limit={limit}"
        
        try:
            response = self.client.get(url, timeout=5.0)
            if response.status_code != 200:
                print(f"Hugging Face API returned status {response.status_code}")
                return []
                
            data = response.json()
            models = []
            
            for item in data:
                model_id = item.get("modelId") or item.get("id") or ""
                if not model_id:
                    continue
                    
                author = item.get("author", model_id.split("/")[0] if "/" in model_id else "unknown")
                downloads = item.get("downloads", 0) or 0
                likes = item.get("likes", 0) or 0
                
                url_link = f"https://huggingface.co/{model_id}"
                
                models.append({
                    "id": f"huggingface:{model_id}",
                    "title": f"HuggingFace Model: {model_id}",
                    "authors": [author],
                    "abstract": f"HuggingFace Model Hub ID: {model_id} (Downloads: {downloads}, Likes: {likes})",
                    "url": url_link,
                    "published": "",
                    "citations": likes,
                    "source": "Hugging Face"
                })
            return models
        except Exception as e:
            print(f"Error querying Hugging Face: {e}")
            return []

    def run_combined_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries all 12 academic sources in parallel, de-duplicates, and ranks via RRF + citations."""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        batch = limit * 2
        search_fns = [
            ("openalex",       lambda: self.search_openalex(query, limit=batch)),
            ("arxiv",          lambda: self.search_arxiv(query, limit=batch)),
            ("semanticscholar",lambda: self.search_semanticscholar(query, limit=batch)),
            ("europepmc",      lambda: self.search_europepmc(query, limit=batch)),
            ("crossref",       lambda: self.search_crossref(query, limit=batch)),
            ("doaj",           lambda: self.search_doaj(query, limit=batch)),
            ("plos",           lambda: self.search_plos(query, limit=batch)),
            ("hal",            lambda: self.search_hal(query, limit=batch)),
            ("pubmed",         lambda: self.search_pubmed(query, limit=batch)),
            ("dblp",           lambda: self.search_dblp(query, limit=batch)),
            ("github",         lambda: self.search_github(query, limit=batch)),
            ("huggingface",    lambda: self.search_huggingface(query, limit=batch)),
        ]

        source_results: dict[str, List[Dict[str, Any]]] = {}
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = {executor.submit(fn): name for name, fn in search_fns}
            for future in as_completed(futures):
                name = futures[future]
                try:
                    source_results[name] = future.result()
                except Exception as e:
                    print(f"Search source '{name}' failed: {e}")
                    source_results[name] = []

        combined: dict[str, Dict[str, Any]] = {}
        rrf_scores: dict[str, float] = {}

        def merge_paper(p: Dict[str, Any], rank: int) -> None:
            key = p["title"].lower().strip()
            score = 1.0 / (rank + 1)
            if key in combined:
                existing = combined[key]
                if not existing["abstract"] and p["abstract"]:
                    existing["abstract"] = p["abstract"]
                if not existing["url"] and p["url"]:
                    existing["url"] = p["url"]
                if p["citations"] > existing["citations"]:
                    existing["citations"] = p["citations"]
                if not existing["published"] and p["published"]:
                    existing["published"] = p["published"]
                if p["source"] not in existing["source"]:
                    existing["source"] += " & " + p["source"]
            else:
                combined[key] = p
            rrf_scores[key] = rrf_scores.get(key, 0.0) + score

        ordered_sources = [
            "openalex", "arxiv", "semanticscholar", "europepmc",
            "crossref", "doaj", "plos", "hal", "pubmed", "dblp",
            "github", "huggingface",
        ]
        for src in ordered_sources:
            for rank, p in enumerate(source_results.get(src, [])):
                merge_paper(p, rank)

        sorted_papers = sorted(
            combined.values(),
            key=lambda x: (
                rrf_scores[x["title"].lower().strip()],
                x.get("citations", 0),
                x.get("published", ""),
            ),
            reverse=True,
        )
        return sorted_papers[:limit]
