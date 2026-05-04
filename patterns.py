import re

PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws(.{0,20})?['\"][0-9a-zA-Z/+]{40}['\"]",
    "GitHub Token": r"ghp_[0-9a-zA-Z]{36}",
    "GitHub OAuth": r"gho_[0-9a-zA-Z]{36}",
    "GitHub App Token": r"(ghu|ghs)_[0-9a-zA-Z]{36}",
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "Google OAuth": r"[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com",
    "Stripe Secret Key": r"sk_live_[0-9a-zA-Z]{24}",
    "Stripe Publishable Key": r"pk_live_[0-9a-zA-Z]{24}",
    "Stripe Test Key": r"sk_test_[0-9a-zA-Z]{24}",
    "Slack Token": r"xox[baprs]-([0-9a-zA-Z]{10,48})",
    "Slack Webhook": r"https://hooks\.slack\.com/services/T[a-zA-Z0-9]+/B[a-zA-Z0-9]+/[a-zA-Z0-9]+",
    "Discord Token": r"[MN][a-zA-Z0-9]{23}\.[a-zA-Z0-9-_]{6}\.[a-zA-Z0-9-_]{27}",
    "Discord Webhook": r"https://discord(app)?\.com/api/webhooks/[0-9]+/[a-zA-Z0-9\-_]+",
    "Twitter API Key": r"(?i)twitter(.{0,20})?['\"][0-9a-zA-Z]{35,44}['\"]",
    "Twitter Bearer Token": r"AAAAAAAAAA[a-zA-Z0-9%]{80,}",
    "Azure Storage Key": r"DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[a-zA-Z0-9+/=]{88}",
    "Azure Client Secret": r"(?i)azure(.{0,20})?['\"][0-9a-zA-Z\-_]{34,40}['\"]",
    "Private Key": r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "PGP Private Key": r"-----BEGIN PGP PRIVATE KEY BLOCK-----",
    "Database URL": r"(?i)(mongodb|mysql|postgresql|redis|sqlite):\/\/[^\s]+",
    "Database Password": r"(?i)(db_pass|database_password|db_password)\s*=\s*['\"][^'\"]{6,}['\"]",
    "Generic Password": r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{6,}['\"]",
    "Generic API Key": r"(?i)(api_key|apikey|api-key)\s*=\s*['\"][^'\"]{8,}['\"]",
    "Generic Secret": r"(?i)(secret|token)\s*=\s*['\"][^'\"]{8,}['\"]",
    "Generic Auth": r"(?i)(auth_token|access_token)\s*=\s*['\"][^'\"]{8,}['\"]",
    "Ethereum Private Key": r"(?i)(eth|ethereum)(.{0,20})?['\"][0-9a-fA-F]{64}['\"]",
    "Mailgun API Key": r"key-[0-9a-zA-Z]{32}",
    "Twilio API Key": r"SK[0-9a-fA-F]{32}",
    "SendGrid API Key": r"SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}",
    "NPM Token": r"npm_[a-zA-Z0-9]{36}",
    "PyPI Token": r"pypi-[a-zA-Z0-9_-]{50,}",
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
                    "content": line.strip()[:100]
                })
    return findings
