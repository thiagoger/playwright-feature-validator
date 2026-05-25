"""Content scanner tests: the demo-safety net that flags bad text before a prospect sees it."""
from feature_checker.core.content_scanner import ContentScanner


def test_clean_business_text_passes():
    scanner = ContentScanner()
    assert scanner.scan_text("Acme Corporation quarterly revenue report", "page") == []


def test_profanity_is_flagged_critical():
    scanner = ContentScanner()
    violations = scanner.scan_text("this damn widget", "Customers")
    assert any(v.category == "profanity" and v.severity == "CRITICAL" for v in violations)


def test_placeholder_caught_at_medium():
    violations = ContentScanner(sensitivity="medium").scan_text("foobar test data here", "page")
    assert any(v.category == "placeholder" for v in violations)


def test_low_sensitivity_ignores_placeholders():
    # No profanity, only placeholders -> low sensitivity should find nothing.
    assert ContentScanner(sensitivity="low").scan_text("foobar lorem ipsum", "page") == []


def test_pii_only_flagged_at_high_sensitivity():
    text = "Customer SSN 123-45-6789 on file"
    assert ContentScanner(sensitivity="medium").scan_text(text, "page") == []
    high = ContentScanner(sensitivity="high").scan_text(text, "page")
    assert any(v.category == "pii" for v in high)


def test_summary_and_report():
    scanner = ContentScanner()
    assert "CLEAN" in scanner.get_report()
    scanner.scan_text("damn", "page")
    assert scanner.get_summary()["CRITICAL"] >= 1
    assert "violation" in scanner.get_report().lower()
