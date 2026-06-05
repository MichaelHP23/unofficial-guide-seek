import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pdfplumber
import os

# ── Sources ──────────────────────────────────────────────────────────────────

OFFICIAL_URLS = [
    {"url": "https://www.brooklyn.edu/seek/apply-to-seek/",          "source": "apply_to_seek"},
    {"url": "https://www.brooklyn.edu/seek/advisement/",             "source": "seek_advisement"},
    {"url": "https://www.brooklyn.edu/seek/seek-student-opportunities/", "source": "student_opportunities"},
    {"url": "https://www.brooklyn.edu/seek/history-of-seek/",        "source": "history_of_seek"},
    {"url": "https://depthome.brooklyn.cuny.edu/seek/dept_services/admission.html", "source": "seek_brochure"},
    {"url": "https://www.cuny.edu/academics/academic-programs/seek-college-discovery/", "source": "cuny_seek_overview"},
    {"url": "https://www.cuny.edu/academics/academic-programs/seek-college-discovery/icorp/", "source": "icorp"},
]

REDDIT_FILES = [
    {"path": "documents/reddit_seek_program.txt.txt",  "source": "reddit_seek_program"},
    {"path": "documents/reddit_seek_summer.txt.txt",   "source": "reddit_seek_summer"},
    {"path": "documents/reddit_seek_vs_asap.txt.txt",  "source": "reddit_seek_vs_asap"},
]

PDF_SOURCES = [
    {"path": "documents/seek_faq.pdf", "source": "seek_faq"},
]

# ── Loaders ───────────────────────────────────────────────────────────────────

def load_webpage(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["nav", "footer", "script", "style", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def load_reddit_file(path):
    if not os.path.exists(path):
        print(f"  File not found: {path}")
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(path):
    if not os.path.exists(path):
        print(f"  PDF not found: {path}")
        return ""
    with pdfplumber.open(path) as pdf:
        pages = [p.extract_text() for p in pdf.pages if p.extract_text()]
    return "\n\n".join(pages)

# ── Chunkers ──────────────────────────────────────────────────────────────────

official_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " "],
)

reddit_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "],
)

# ── Pipeline ──────────────────────────────────────────────────────────────────

def run_ingestion():
    all_chunks = []

    print("Loading official pages...")
    for item in OFFICIAL_URLS:
        print(f"  {item['source']}")
        text = load_webpage(item["url"])
        chunks = official_splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) > 50:
                all_chunks.append({
                    "text": chunk.strip(),
                    "source": item["source"],
                    "chunk_index": i,
                    "type": "official"
                })

    print("Loading Reddit threads...")
    for item in REDDIT_FILES:
        print(f"  {item['source']}")
        text = load_reddit_file(item["path"])
        if not text:
            continue
        chunks = reddit_splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) > 30:
                all_chunks.append({
                    "text": chunk.strip(),
                    "source": item["source"],
                    "chunk_index": i,
                    "type": "reddit"
                })

    print("Loading PDFs...")
    for item in PDF_SOURCES:
        print(f"  {item['source']}")
        text = load_pdf(item["path"])
        if text:
            chunks = official_splitter.split_text(text)
            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) > 50:
                    all_chunks.append({
                        "text": chunk.strip(),
                        "source": item["source"],
                        "chunk_index": i,
                        "type": "pdf"
                    })

    print(f"\nTotal chunks: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = run_ingestion()
    # Print 5 sample chunks so you can inspect quality
    print("\n── Sample Chunks ──")
    import random
    for chunk in random.sample(chunks, min(5, len(chunks))):
        print(f"\nSource: {chunk['source']} | Type: {chunk['type']}")
        print(chunk['text'])
        print("─" * 40)