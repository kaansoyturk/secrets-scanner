import re

PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws(.{0,20})?['\"][0-9a-zA-Z/+]{40}['\"]",
    "GitHub Token": r"ghp_[0-9a-zA-Z]{36}",
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "Stripe Secret Key": r"sk_live_[0-9a-zA-Z]{24}",
    "Private Key": r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
    "Generic Password": r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{6,}['\"]",
    "Generic API Key": r"(?i)(api_key|apikey|api-key)\s*=\s*['\"][^'\"]{8,}['\"]",
    "Generic Secret": r"(?i)(secret|token)\s*=\s*['\"][^'\"]{8,}['\"]",
    "Database URL": r"(?i)(mongodb|mysql|postgresql|redis):\/\/[^\s]+",
}

def scan_content(content, filename=""):
    findings = []
    lines = content.split("\n")

    for line_num, line in enumerate(lines, 1):
        for secret_type, pattern in PATTERNS.items():
            if re.search(pattern, line):
                findings.append({
                    "type": secret_type,
                    "file": filename,
                    "line": line_num,
                    "content": line.strip()[:100]  # İlk 100 karakter
                })

    return findings