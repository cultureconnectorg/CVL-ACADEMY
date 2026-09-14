from __future__ import annotations

from pathlib import Path

from scripts.check_secrets import scan_file


def test_scanner_detects_live_secret_signatures(tmp_path: Path):
    path = tmp_path / "bad.env.txt"
    path.write_text(
        "OPENAI_API_KEY=sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZ123456\n"
        "STRIPE_SECRET_KEY=sk_live_ABCDEFGHIJKLMNOPQRSTUV\n",
        encoding="utf-8",
    )
    hits = scan_file(path)
    kinds = {kind for kind, _line in hits}
    assert "openai" in kinds
    assert "stripe_live" in kinds


def test_scanner_ignores_safe_placeholders(tmp_path: Path):
    path = tmp_path / "example.env.txt"
    path.write_text(
        "OPENAI_API_KEY=your-key-here\n"
        "STRIPE_SECRET_KEY=sk_test_not-a-real-secret\n"
        "JWT_SECRET=replace-me\n",
        encoding="utf-8",
    )
    assert scan_file(path) == []


def test_binary_suffixes_are_skipped(tmp_path: Path):
    path = tmp_path / "archive.zip"
    path.write_bytes(b"sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZ123456")
    assert scan_file(path) == []
