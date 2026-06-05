## Domain
The SEEK (Search for Education, Elevation, and Knowledge) program at Brooklyn College 
provides financial, academic, and personal support to eligible students. While official 
resources exist, students often struggle to find practical, experience-based guidance 
about navigating the program, things like what advisors are actually helpful, how 
stipends work in practice, and what happens if your GPA slips. This knowledge lives in 
student conversations, not official pages.

## Documents
1. How to Apply to SEEK - https://www.brooklyn.edu/seek/apply-to-seek/
2. SEEK Advisement and Academic Support - https://www.brooklyn.edu/seek/advisement/
3. Student Opportunities with SEEK - https://www.brooklyn.edu/seek/seek-student-opportunities/
4. History of SEEK - https://www.brooklyn.edu/seek/history-of-seek/
5. SEEK Department Services Brochure - https://depthome.brooklyn.cuny.edu/seek/dept_services/admission.html
6. CUNY SEEK Program Overview - https://www.cuny.edu/academics/academic-programs/seek-college-discovery/
7. SEEK FAQ - https://www.brooklyn.cuny.edu/web/1202_SEEK_FAQs.pdf
8. ICORP Research Initiative - https://www.cuny.edu/academics/academic-programs/seek-college-discovery/icorp/
9. Reddit: SEEK Program Experience - https://www.reddit.com/r/CUNY/comments/1qb4cux/seek_program/
10. Reddit: SEEK Summer Session - https://www.reddit.com/r/CUNY/comments/1l1gb7o/seek_program_summer_session/
11. Reddit: SEEK vs ASAP Comparison - https://www.reddit.com/r/CUNY/comments/1c57fjg/seek_vs_asap/

## Chunking Strategy
Two different chunking strategies are used because the documents have fundamentally 
different structures.

Official pages use 500-character chunks with 100-character overlap. These pages contain 
dense, multi-sentence paragraphs where a single idea spans several sentences. Larger 
chunks are needed to capture a complete thought without fragmentation.

Reddit comments use 250-character chunks with 50-character overlap. Reddit comments are 
short, self-contained thoughts. Smaller chunks preserve the natural structure of each 
comment without breaking up meaning.

Overlap ensures that key information falling at a chunk boundary appears in both 
adjacent chunks, so retrieval can still find it.

## Retrieval Approach
Embedding model: all-MiniLM-L6-v2 via sentence-transformers. Runs locally with no API 
key or rate limits.

Top-k: 5 chunks retrieved per query. SEEK questions tend to be specific, so 5 chunks 
provides enough context without diluting the LLM's response with loosely related material.

Production tradeoffs: For a real deployment, I would consider OpenAI's text-embedding-3-small 
for higher accuracy on domain-specific text, but it requires an API key and incurs cost. 
all-MiniLM-L6-v2 is free and local but has a shorter context window (256 tokens) which 
could truncate longer official page chunks. For a multilingual student population, a 
model with multilingual support like paraphrase-multilingual-MiniLM-L12-v2 would be worth 
considering.

## Evaluation Plan
1. What GPA must SEEK students maintain to stay in the program?
   Expected: Students must maintain satisfactory academic progress (specific GPA requirements 
   per SEEK guidelines)

2. What financial support does SEEK provide to students?
   Expected: SEEK provides stipends, the amount varies based on credits taken

3. Is the SEEK summer program mandatory for new students?
   Expected: Answer drawn from official pages describing summer program requirements

4. How do you transfer into SEEK from another CUNY college?
   Expected: Submit CUNY Transfer Application and Special Programs Transfer Request Form, 
   deadlines are January 15 (spring) and July 30 (fall)

5. What do students say about the SEEK advising experience compared to general BC advising?
   Expected: Student perspective from Reddit threads describing advisor quality and 
   accessibility

## Anticipated Challenges
1. Chunk boundary splits: Key eligibility information on official pages spans multiple 
sentences. If a chunk boundary falls mid-sentence, neither chunk will contain the complete 
requirement, causing retrieval to return incomplete context.

2. Thin Reddit threads: The three Reddit threads may contain only a handful of substantive 
comments. If the student voice documents are too sparse, queries about student experience 
will return weak matches with high distance scores.

## AI Tool Plan
1. Ingestion and chunking (ingest.py): I will provide Claude with my Documents section 
and Chunking Strategy section and ask it to implement a script that loads URLs and PDFs, 
cleans them, and chunks them using the two strategies described above.

2. Embedding and retrieval (embed.py, retrieve.py): I will provide Claude with my 
Retrieval Approach section and ask it to implement ChromaDB storage with source metadata 
and a retrieval function returning top-k chunks with distance scores.

## Architecture
Document Ingestion (requests, BeautifulSoup, pdfplumber)
        ↓
Chunking (langchain-text-splitters, two strategies)
        ↓
Embedding (sentence-transformers: all-MiniLM-L6-v2)
        ↓
Vector Store (ChromaDB)
        ↓
Retrieval (semantic similarity search, top-k=5)
        ↓
Generation (Groq: llama-3.3-70b-versatile)
        ↓
Interface (Gradio)