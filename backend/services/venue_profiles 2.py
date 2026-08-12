from domain.models import VenueProfile


VENUE_PROFILES = {
    "NeurIPS": VenueProfile(
        venue="NeurIPS", cycle="2026", official_template_url="https://neurips.cc/Conferences/2026/CallForPapers",
        document_class="article", page_limit=9, anonymized_review=True,
        required_sections=["Abstract", "Limitations"], forbidden_tokens=["Penn State", "research@psu.edu"],
    ),
    "ICML": VenueProfile(
        venue="ICML", cycle="2026", official_template_url="https://icml.cc/Conferences/2026/AuthorInstructions",
        document_class="article", page_limit=8, anonymized_review=True,
        required_sections=["Abstract"], forbidden_tokens=["Penn State", "research@psu.edu"],
    ),
    "CVPR": VenueProfile(
        venue="CVPR", cycle="2026", official_template_url="https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines",
        document_class="article", page_limit=8, anonymized_review=True,
        required_sections=["Abstract", "Limitations"], forbidden_tokens=["Penn State", "research@psu.edu"],
    ),
    "ACL": VenueProfile(
        venue="ACL", cycle="ARR", official_template_url="https://aclrollingreview.org/cfp",
        document_class="article", page_limit=8, anonymized_review=True,
        required_sections=["Abstract", "Limitations"], forbidden_tokens=["Penn State", "research@psu.edu"],
    ),
    "IEEEtran": VenueProfile(
        venue="IEEEtran", cycle="journal", document_class="IEEEtran", page_limit=None,
        required_sections=["Abstract"],
    ),
    "ACM": VenueProfile(
        venue="ACM", cycle="journal", document_class="acmart", page_limit=None,
        required_sections=["Abstract"],
    ),
}

