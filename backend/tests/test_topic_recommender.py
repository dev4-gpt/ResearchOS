import pytest
from services.topic_recommender import TopicRecommenderService

def test_topic_recommender_list():
    service = TopicRecommenderService()
    topics = service.list_curated_topics()
    assert len(topics) >= 5
    assert topics[0]["id"] == "enterprise-genai-roi"
    assert "Systematic Review" in topics[0]["title"]
    assert "98/100" in topics[0]["impact_score"]

def test_topic_recommender_get_by_id():
    service = TopicRecommenderService()
    topic = service.get_topic_by_id("test-time-compute-reasoning")
    assert topic["id"] == "test-time-compute-reasoning"
    assert "Test-Time Compute" in topic["title"]
