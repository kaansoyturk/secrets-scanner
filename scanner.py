import os
import sys
from colorama import init, Fore, Style
from patterns import scan_content
from reporter import generate_report
from github_scanner import scan_github_repo

init(autoreset=True)

IGNORED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".exe", ".bin"}
IGNORED_DIRS = {"venv", ".git", "node_modules", "__pycache__"}

def scan_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return scan_content(content, filepath)
    except Exception:
        return []

def scan_directory(path):
    all_findings = []
    scanned_files = 0

    print(f"\n{Fore.CYAN}🔍 Taranıyor: {path}{Style.RESET_ALL}\n")

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORED_EXTENSIONS:
                continue

            filepath = os.path.join(root, file)
            findings = scan_file(filepath)
            scanned_files += 1

            if findings:
                for f in findings:
                    all_findings.append(f)
                    print(f"{Fore.RED}[!] {f['type']}{Style.RESET_ALL}")
                    print(f"    📄 Dosya : {f['file']}")
                    print(f"    📍 Satır : {f['line']}")
                    print(f"    🔎 İçerik: {f['content']}")
                    print()

    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"📊 Taranan dosya : {scanned_files}")

    if all_findings:
        print(f"{Fore.RED}🚨 Bulunan secret: {len(all_findings)}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}✅ Hiçbir secret bulunamadı!{Style.RESET_ALL}")

    report_path = "scan_report.pdf"
    generate_report(all_findings, scanned_files, report_path)

    return all_findings

def print_help():
    print(f"""
{Fore.CYAN}🔑 Secrets Scanner{Style.RESET_ALL}

Kullanim:
  {Fore.GREEN}Klasor tarama:{Style.RESET_ALL}
    python3 scanner.py /taranacak/klasor

  {Fore.GREEN}GitHub repo tarama:{Style.RESET_ALL}
    python3 scanner.py --github https://github.com/kullanici/repo

  {Fore.GREEN}GitHub repo (token ile):{Style.RESET_ALL}
    python3 scanner.py --github https://github.com/kullanici/repo --token TOKEN
    """)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    # GitHub tarama
    if "--github" in sys.argv:
        idx = sys.argv.index("--github")
        if idx + 1 >= len(sys.argv):
            print(f"{Fore.RED}❌ GitHub URL eksik!{Style.RESET_ALL}")
            sys.exit(1)

        github_url = sys.argv[idx + 1]
        token = None

        if "--token" in sys.argv:
            token_idx = sys.argv.index("--token")
            if token_idx + 1 < len(sys.argv):
                token = sys.argv[token_idx + 1]

        findings, scanned = scan_github_repo(github_url, token)
        generate_report(findings, scanned, "scan_report.pdf")

    # Klasör tarama
    else:
        path = sys.argv[1]
        if not os.path.exists(path):
            print(f"{Fore.RED}❌ Hata: '{path}' bulunamadı!{Style.RESET_ALL}")
            sys.exit(1)
        scan_directory(path)