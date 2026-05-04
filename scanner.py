import os
import sys
from colorama import init, Fore, Style
from patterns import scan_content

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
        # Görmezden gelinecek klasörler
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

    return all_findings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Fore.YELLOW}Kullanım: python3 scanner.py <klasör_yolu>{Style.RESET_ALL}")
        print(f"Örnek   : python3 scanner.py /Users/kaansoyturk/projelerim")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"{Fore.RED}❌ Hata: '{path}' bulunamadı!{Style.RESET_ALL}")
        sys.exit(1)

    scan_directory(path)