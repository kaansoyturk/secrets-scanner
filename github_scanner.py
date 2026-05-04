import requests
from patterns import scan_content

GITHUB_API = "https://api.github.com"

def get_repo_files(owner, repo, token=None):
    """Repodaki tüm dosyaların listesini al"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    # Repo tree'sini al (recursive)
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print("❌ GitHub token geçersiz!")
        return []
    elif response.status_code == 404:
        print(f"❌ Repo bulunamadı: {owner}/{repo}")
        return []
    elif response.status_code != 200:
        print(f"❌ API hatası: {response.status_code}")
        return []

    data = response.json()
    files = [f for f in data.get("tree", []) if f["type"] == "blob"]
    return files

def get_file_content(owner, repo, file_path, token=None):
    """Dosya içeriğini al"""
    headers = {"Accept": "application/vnd.github.v3.raw"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    return None

def parse_github_url(url):
    """GitHub URL'inden owner ve repo adını çıkar"""
    url = url.rstrip("/")
    url = url.replace("https://github.com/", "")
    url = url.replace("http://github.com/", "")
    url = url.replace(".git", "")
    parts = url.split("/")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None

IGNORED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".pdf",
    ".zip", ".exe", ".bin", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".eot"
}

def scan_github_repo(url, token=None):
    """GitHub reposunu tara"""
    owner, repo = parse_github_url(url)

    if not owner or not repo:
        print("❌ Geçersiz GitHub URL'i!")
        print("   Örnek: https://github.com/kullanici/repo")
        return [], 0

    print(f"\n🐙 GitHub Repo Taranıyor: {owner}/{repo}\n")

    files = get_repo_files(owner, repo, token)
    if not files:
        return [], 0

    print(f"📁 Toplam dosya: {len(files)}")
    print(f"🔍 Taranıyor...\n")

    all_findings = []
    scanned = 0

    for file in files:
        path = file["path"]
        ext = "." + path.split(".")[-1] if "." in path else ""

        if ext.lower() in IGNORED_EXTENSIONS:
            continue

        content = get_file_content(owner, repo, path, token)
        if not content:
            continue

        scanned += 1
        findings = scan_content(content, path)

        if findings:
            for f in findings:
                all_findings.append(f)
                print(f"[!] {f['type']}")
                print(f"    📄 Dosya : {f['file']}")
                print(f"    📍 Satır : {f['line']}")
                print(f"    🔎 İçerik: {f['content']}")
                print()

    print(f"{'='*50}")
    print(f"📊 Taranan dosya : {scanned}")

    if all_findings:
        print(f"🚨 Bulunan secret: {len(all_findings)}")
    else:
        print(f"✅ Hiçbir secret bulunamadı!")

    return all_findings, scanned