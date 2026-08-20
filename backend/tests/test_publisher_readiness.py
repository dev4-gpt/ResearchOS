from services.publisher_readiness import PublisherReadinessService
from services.fact_checker import FactCheckerService


def _service():
    return PublisherReadinessService(None)


def _substantive_paper(seed: str = "enterprise systems") -> str:
    domain_detail = (
        "service mesh latency observability queue saturation deployment topology incident response "
        if "enterprise" in seed
        else "stereo correspondence depth estimation camera calibration epipolar geometry pose recovery "
    )
    body = (
        f"# Abstract\nWe propose a novel {seed} method and evaluate it with a benchmark dataset. "
        "Our results report a 12% improvement over the baseline [1].\n\n"
        "## Methodology\nWe describe a reproducible protocol, measurement procedure, and analysis scope.\n\n"
        "## Contributions\nWe present an explicit framework and report findings from the evaluation.\n\n"
        "## Limitations\nThe boundary conditions and threats to validity are discussed.\n\n"
        "## References\n[1] Research Author 2024\n[2] Research Author 2023\n[3] Research Author 2022\n"
    )
    unique_findings = " ".join(f"{domain_detail} {seed} evidence measurement {index}." for index in range(150))
    return unique_findings + body


def test_exact_duplicate_content_is_blocked():
    service = _service()
    report = service.audit_collection_originality({
        "paper_a.md": _substantive_paper(),
        "paper_b.md": _substantive_paper(),
    })

    assert report["passed"] is False
    assert report["per_file"]["paper_a.md"]["status"] == "BLOCKED_DUPLICATE_CONTENT"
    assert any(pair["exact_duplicate"] for pair in report["pairs"])


def test_distinct_substantive_papers_can_pass_originality_and_value():
    service = _service()
    report = service.audit_collection_originality({
        "paper_a.md": _substantive_paper("enterprise orchestration"),
        "paper_b.md": _substantive_paper("robotics planning"),
    })
    value = service.audit_substantive_value(_substantive_paper("enterprise orchestration"))

    assert report["passed"] is True
    assert value["substantive_value_passed"] is True
    assert value["metrics"]["word_count"] >= 450


def test_value_gate_blocks_short_or_unsubstantiated_text():
    service = _service()
    value = service.audit_substantive_value("# Abstract\nA short claim without method or evidence.")

    assert value["substantive_value_passed"] is False
    assert value["checks"]["minimum_substance"]["passed"] is False
    assert value["checks"]["explicit_contribution"]["passed"] is False


def test_fact_checker_blocks_numeric_claim_without_source_support():
    report = FactCheckerService().audit_document(
        "# Abstract\nOur study improves accuracy by 74% (p < 0.001) [[source2024]].",
        source_records={"source2024": "A source that does not report the claimed metric."},
    )

    assert report["status"] == "needs_review"
    assert report["metric_report"]["unverified_count"] >= 1
    assert report["blocking_errors"]


def test_fact_checker_catches_unsupported_scale_claims():
    report = FactCheckerService().audit_document(
        "The benchmark covers 500 enterprise codebases and 18 months of telemetry [[source2024]].",
        source_records={"source2024": "The source describes a conceptual framework only."},
    )

    assert "500 enterprise codebases" in report["metric_report"]["unverified_claims"]
    assert "18 months" in report["metric_report"]["unverified_claims"]
