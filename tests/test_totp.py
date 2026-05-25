"""TOTP generation tests, anchored to the RFC 6238 reference vector."""
import base64

from feature_checker.auth import totp


def test_matches_rfc6238_reference_vector(monkeypatch):
    # RFC 6238, Appendix B (SHA-1): at T = 59s the secret "12345678901234567890"
    # produces 94287082, i.e. 287082 truncated to six digits.
    monkeypatch.setattr("feature_checker.auth.totp.time.time", lambda: 59)
    secret = base64.b32encode(b"12345678901234567890").decode()
    assert totp.generate_totp(secret) == "287082"


def test_code_is_always_six_digits(monkeypatch):
    monkeypatch.setattr("feature_checker.auth.totp.time.time", lambda: 1_234_567_890)
    code = totp.generate_totp("JBSWY3DPEHPK3PXP")
    assert len(code) == 6 and code.isdigit()


def test_secret_is_case_and_space_insensitive(monkeypatch):
    monkeypatch.setattr("feature_checker.auth.totp.time.time", lambda: 100)
    assert totp.generate_totp("JBSWY3DPEHPK3PXP") == totp.generate_totp("jbsw y3dp ehpk 3pxp")


def test_remaining_seconds(monkeypatch):
    monkeypatch.setattr("feature_checker.auth.totp.time.time", lambda: 1000)  # 1000 % 30 == 10
    assert totp.get_totp_remaining_seconds() == 20
