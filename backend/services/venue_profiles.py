from domain.models import VenueProfile


VENUE_PROFILES = {
    "NeurIPS": VenueProfile(
        venue="NeurIPS", cycle="2026", official_template_url="https://neurips.cc/Conferences/2026/CallForPapers",
        document_class="article", page_limit=9, short_page_limit=9, long_page_limit=14, anonymized_review=True,
        required_sections=["Abstract", "Limitations"], forbidden_tokens=["Penn State", "research@psu.edu"],
    ),
    "ICML": VenueProfile(
        venue="ICML", cycle="2026", official_template_url="https://icml.cc/Conferences/2026/AuthorInstructions",
        document_class="article", page_limit=8, short_page_limit=8, long_page_limit=12, anonymized_review=True,
        required_sections=["Abstract"], forbidden_tokens=["Penn State", "research@psu.edu"],
    ),
    "CVPR": VenueProfile(
        venue="CVPR", cycle="2026", official_template_url="https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines",
        document_class="article", page_limit=8, short_page_limit=8, long_page_limit=12, anonymized_review=True,
        required_sections=["Abstract", "Limitations"], forbidden_tokens=["Penn State", "research@psu.edu"],
    ),
    "ACL": VenueProfile(
        venue="ACL", cycle="ARR", official_template_url="https://aclrollingreview.org/cfp",
        document_class="article", page_limit=8, short_page_limit=4, long_page_limit=8, anonymized_review=True,
        required_sections=["Abstract", "Limitations"], forbidden_tokens=["Penn State", "research@psu.edu"],
    ),
    "IEEEtran": VenueProfile(
        venue="IEEEtran", cycle="journal", document_class="IEEEtran", page_limit=4, short_page_limit=4, long_page_limit=12,
        required_sections=["Abstract"],
    ),
    "ACM": VenueProfile(
        venue="ACM", cycle="journal", document_class="acmart", page_limit=10, short_page_limit=4, long_page_limit=12,
        required_sections=["Abstract"],
    ),
    "IEEE_Access": VenueProfile(
        venue="IEEE_Access", cycle="open_access", document_class="IEEEtran", page_limit=12, short_page_limit=4, long_page_limit=14,
        required_sections=["Abstract"], official_template_url="https://ieeeaccess.ieee.org/submitting-an-article/",
    ),
    "SpringerOpen": VenueProfile(
        venue="SpringerOpen", cycle="open_access", document_class="article", page_limit=14, short_page_limit=6, long_page_limit=16,
        required_sections=["Abstract"], official_template_url="https://www.springeropen.com/getpublished",
    ),
    "Femington": VenueProfile(
        venue="Femington", cycle="open_access", document_class="IEEEtran", page_limit=12, short_page_limit=4, long_page_limit=12,
        required_sections=["Abstract"], official_template_url="https://femington.org/journals",
    ),
    "MDPI": VenueProfile(
        venue="MDPI", cycle="open_access", document_class="article", page_limit=12, short_page_limit=4, long_page_limit=14,
        required_sections=["Abstract"], official_template_url="https://www.mdpi.com/authors/references",
    ),
    "DOAJ": VenueProfile(
        venue="DOAJ", cycle="open_access", document_class="article", page_limit=12, short_page_limit=4, long_page_limit=14,
        required_sections=["Abstract"], official_template_url="https://doaj.org/", is_index_only=True,
    ),
    "arXiv": VenueProfile(
        venue="arXiv", cycle="preprint", document_class="article", page_limit=14, short_page_limit=4, long_page_limit=16,
        required_sections=["Abstract"], official_template_url="https://arxiv.org/help/prep",
    ),
}
