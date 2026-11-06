"""
Zero-Tolerance Security, PII, Shannon Entropy, and Prompt Injection Gatekeeper.
"""

from collections import Counter
import math
import re
from typing import Any

from metricsthinking.models import SecurityVulnerabilityReport

SECRET_PATTERNS: dict[str, re.Pattern] = {
    "OPENAI_KEY": re.compile(r"\bsk-[a-zA-Z0-9]{20,48}\b"),
    "ANTHROPIC_KEY": re.compile(r"\bsk-ant-[a-zA-Z0-9\-_]{32,96}\b"),
    "AWS_ACCESS_KEY": re.compile(r"\b(AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}\b"),
    "AWS_SECRET_KEY": re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"][A-Za-z0-9/+=]{40}['\"]"),
    "GITHUB_TOKEN": re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,255}\b"),
    "GENERIC_BEARER_TOKEN": re.compile(r"(?i)bearer\s+[a-zA-Z0-9\-_=]{30,}\b"),
    "PRIVATE_KEY_BLOCK": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    "GOOGLE_API_KEY": re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"),
    "SLACK_TOKEN": re.compile(r"\bxox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,32}\b"),
    "HUGGINGFACE_TOKEN": re.compile(r"\bhf_[a-zA-Z0-9]{34}\b"),
}

PII_PATTERNS: dict[str, re.Pattern] = {
    "CREDIT_CARD": re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"),
    "SSN": re.compile(r"\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b"),
    "EMAIL_EXPLICIT": re.compile(r"\b[A-Za-z0-9._%+-]+@(?!example\.com|test\.com)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"),
}

PROMPT_INJECTION_PATTERNS: dict[str, re.Pattern] = {
    "IGNORE_INSTRUCTIONS": re.compile(r"(?i)\b(?:ignore|disregard|forget)\s+(?:all\s+)?(?:previous|prior|above)\s+(?:instructions|prompts|rules)\b"),
    "SYSTEM_OVERRIDE": re.compile(r"(?i)\b(?:system\s+override|admin\s+override|bypass\s+all\s+guardrails)\b"),
    "JAILBREAK_DAN": re.compile(r"(?i)\b(?:you\s+are\s+now\s+DAN|jailbreak\s+mode|unfiltered\s+mode|act\s+as\s+an\s+unfiltered)\b"),
    "EXFILTRATE_ENV": re.compile(r"(?i)\b(?:print|echo|dump|output)\s+(?:all\s+)?(?:env|environment\s+variables|api[-_]keys|passwords)\b"),
}

SAFE_PLACEHOLDERS: list[re.Pattern] = [
    re.compile(r"<REDACTED>", re.IGNORECASE),
    re.compile(r"your[-_]api[-_]key", re.IGNORECASE),
    re.compile(r"placeholder", re.IGNORECASE),
    re.compile(r"dummy[-_]token", re.IGNORECASE),
    re.compile(r"fake[-_]token", re.IGNORECASE),
    re.compile(r"sk-ant-test-dummy", re.IGNORECASE),
    re.compile(r"test[-_]secret", re.IGNORECASE),
    re.compile(r"mock[-_]key", re.IGNORECASE),
    re.compile(r"AKIAIOSFODNN7EXAMPLE", re.IGNORECASE),
]


def calculate_shannon_entropy(data: str) -> float:
    """Computes Shannon entropy in bits per character."""
    if not data:
        return 0.0
    length = len(data)
    counts = Counter(data)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def is_safe_placeholder(text: str) -> bool:
    """Checks if text matches known testing/mock placeholders."""
    return any(p.search(text) for p in SAFE_PLACEHOLDERS)


def scan_file_security(
    file_path: str,
    content: str,
    entropy_threshold: float = 4.5,
) -> dict[str, Any]:
    """
    Scans a single file's content for entropy spikes, exposed secrets, PII, and prompt injections.
    """
    entropy_findings: list[dict[str, Any]] = []
    pii_findings: list[dict[str, Any]] = []
    prompt_findings: list[dict[str, Any]] = []
    max_entropy = 0.0

    lines = content.splitlines()
    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or len(stripped) < 4:
            continue

        if is_safe_placeholder(stripped):
            continue

        # Skip markdown image badges and URLs for entropy checks
        is_url_or_badge = (
            stripped.startswith("![")
            or "https://" in stripped
            or "http://" in stripped
            or "img.shields.io" in stripped
        )

        # 1. Secret patterns
        for name, pattern in SECRET_PATTERNS.items():
            for match in pattern.findall(line):
                matched_str = match if isinstance(match, str) else match[0]
                if is_safe_placeholder(matched_str):
                    continue
                entropy_findings.append({
                    "file_path": file_path,
                    "line": line_idx,
                    "type": "SECRET",
                    "rule": name,
                    "severity": "CRITICAL",
                    "preview": matched_str[:8] + "...",
                })

        # 2. PII patterns
        for name, pattern in PII_PATTERNS.items():
            for match in pattern.findall(line):
                matched_str = match if isinstance(match, str) else match[0]
                if is_safe_placeholder(matched_str):
                    continue
                pii_findings.append({
                    "file_path": file_path,
                    "line": line_idx,
                    "type": "PII",
                    "rule": name,
                    "severity": "HIGH",
                    "preview": matched_str[:4] + "...[REDACTED]",
                })

        # 3. Prompt injection patterns
        for name, pattern in PROMPT_INJECTION_PATTERNS.items():
            if pattern.search(line):
                prompt_findings.append({
                    "file_path": file_path,
                    "line": line_idx,
                    "type": "PROMPT_INJECTION",
                    "rule": name,
                    "severity": "CRITICAL",
                    "preview": stripped[:60],
                })

        # 4. Token-level Shannon entropy check
        if not is_url_or_badge:
            tokens = re.findall(r"[A-Za-z0-9+/=_\-]{16,}", line)
            for token in tokens:
                if is_safe_placeholder(token):
                    continue
                # Skip repository file paths
                if "/" in token and any(seg in token.lower() for seg in ["artifacts", "plans", "metricsthinking", "src", "tests", "crates", "config", "docs", ".context", "schemas", "scripts", "data", "foundation"]):
                    continue
                # Cryptographic secrets have mixed case + digits or long hex sequences
                has_digit = any(c.isdigit() for c in token)
                has_upper = any(c.isupper() for c in token)
                has_lower = any(c.islower() for c in token)
                is_hex = len(token) >= 32 and bool(re.match(r"^[0-9a-fA-F]+$", token))
                if not ((has_digit and has_upper and has_lower) or is_hex):
                    continue

                ent = calculate_shannon_entropy(token)
                if ent > max_entropy:
                    max_entropy = ent
                if ent >= entropy_threshold:
                    entropy_findings.append({
                        "file_path": file_path,
                        "line": line_idx,
                        "type": "HIGH_ENTROPY",
                        "rule": f"H={ent:.2f}>{entropy_threshold}",
                        "severity": "WARNING",
                        "preview": token[:6] + "..." + token[-4:],
                        "entropy": round(ent, 3),
                    })

    has_violations = bool(entropy_findings or pii_findings or prompt_findings)

    return {
        "entropy_findings": entropy_findings,
        "pii_findings": pii_findings,
        "prompt_injection_findings": prompt_findings,
        "max_entropy": round(max_entropy, 3),
        "has_violations": has_violations,
    }


def scan_repository_security(
    file_contents: dict[str, str],
    lockfile_present: bool = True,
    entropy_threshold: float = 4.5,
    ignore_tests: bool = True,
) -> SecurityVulnerabilityReport:
    """
    Performs forensic security and attack surface scan across all collected files.
    """
    all_entropy_findings: list[dict[str, Any]] = []
    all_pii_findings: list[dict[str, Any]] = []
    all_prompt_findings: list[dict[str, Any]] = []
    global_max_entropy = 0.0

    for file_path, content in file_contents.items():
        norm_path = file_path.replace("\\", "/").lower()
        if ignore_tests and (norm_path.startswith("tests/") or "/tests/" in norm_path or "test_" in norm_path):
            continue

        res = scan_file_security(file_path, content, entropy_threshold)
        if res["max_entropy"] > global_max_entropy:
            global_max_entropy = res["max_entropy"]
        all_entropy_findings.extend(res["entropy_findings"])
        all_pii_findings.extend(res["pii_findings"])
        all_prompt_findings.extend(res["prompt_injection_findings"])

    # Calculate Attack Surface Index (0.0 to 100.0, lower is better)
    surface = 0.0
    surface += min(35.0, len(all_entropy_findings) * 5.0)
    surface += min(30.0, len(all_pii_findings) * 10.0)
    surface += min(25.0, len(all_prompt_findings) * 10.0)
    if not lockfile_present:
        surface += 10.0

    attack_surface_index = round(min(100.0, surface), 2)

    return SecurityVulnerabilityReport(
        shannon_entropy_max=round(global_max_entropy, 3),
        entropy_findings=all_entropy_findings,
        pii_matches_count=len(all_pii_findings),
        pii_findings=all_pii_findings,
        prompt_injection_surface_count=len(all_prompt_findings),
        prompt_injection_findings=all_prompt_findings,
        supply_chain_lockfile_pinned=lockfile_present,
        attack_surface_index=attack_surface_index,
    )
