"""
User Profile Service — stores publication history, O-1A criteria coverage,
and expertise areas to drive intelligent venue recommendations.
"""
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime


DEFAULT_PROFILE = {
    "name": "",
    "field": "Computer Science / Artificial Intelligence",
    "institution": "",
    "expertise_areas": ["Machine Learning", "Computer Vision", "Natural Language Processing"],
    "publication_history": [],
    "citation_count": 0,
    "h_index": 0,
    "o1a_criteria_met": [],
    "target_timeline": "normal",  # "urgent" | "normal" | "journal"
    "submission_goals": "balanced",  # "top_conference" | "balanced" | "safe_accept" | "journal_impact"
    "created_at": datetime.utcnow().isoformat(),
    "updated_at": datetime.utcnow().isoformat()
}


class UserProfileService:
    """JSON-backed user profile store for publication history and venue strategy."""

    PROFILE_FILENAME = "user_profile.json"

    def __init__(self, vault_path: str):
        self.profile_path = os.path.join(vault_path, self.PROFILE_FILENAME)

    def load(self) -> Dict[str, Any]:
        """Load user profile from disk. Returns default if not found."""
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, "r") as f:
                    data = json.load(f)
                # Merge with defaults for any missing keys
                merged = {**DEFAULT_PROFILE, **data}
                return merged
            except Exception:
                pass
        return dict(DEFAULT_PROFILE)

    def save(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Save user profile to disk."""
        profile["updated_at"] = datetime.utcnow().isoformat()
        os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
        with open(self.profile_path, "w") as f:
            json.dump(profile, f, indent=2)
        return profile

    def add_publication(self, pub: Dict[str, Any]) -> Dict[str, Any]:
        """Add a published paper entry to the portfolio history."""
        profile = self.load()
        if "publication_history" not in profile:
            profile["publication_history"] = []
        pub["added_at"] = datetime.utcnow().isoformat()
        profile["publication_history"].append(pub)
        return self.save(profile)

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Returns a summary of the user's academic portfolio for venue scoring."""
        profile = self.load()
        pubs = profile.get("publication_history", [])
        venue_history = [p.get("venue", "") for p in pubs if p.get("venue")]
        accepted_top_venues = [v for v in venue_history if v in ("NeurIPS", "ICML", "CVPR", "ACL")]
        return {
            "total_publications": len(pubs),
            "citation_count": profile.get("citation_count", 0),
            "h_index": profile.get("h_index", 0),
            "accepted_top_venues": accepted_top_venues,
            "expertise_areas": profile.get("expertise_areas", []),
            "o1a_criteria_met": profile.get("o1a_criteria_met", []),
            "submission_goals": profile.get("submission_goals", "balanced"),
            "target_timeline": profile.get("target_timeline", "normal"),
        }
