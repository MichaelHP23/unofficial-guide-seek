# The Unofficial Guide: SEEK at Brooklyn College

## Domain
This system helps students navigate the SEEK (Search for Education, Elevation, 
and Knowledge) program at Brooklyn College. While official resources exist, 
students often struggle to find practical guidance about eligibility, financial 
support, advisement, and program requirements. This knowledge lives in student 
conversations and scattered official pages rather than one accessible place.

## Documents
1. How to Apply to SEEK - https://www.brooklyn.edu/seek/apply-to-seek/
2. SEEK Advisement - https://www.brooklyn.edu/seek/advisement/
3. Student Opportunities - https://www.brooklyn.edu/seek/seek-student-opportunities/
4. History of SEEK - https://www.brooklyn.edu/seek/history-of-seek/
5. SEEK Brochure - https://depthome.brooklyn.cuny.edu/seek/dept_services/admission.html
6. CUNY SEEK Overview - https://www.cuny.edu/academics/academic-programs/seek-college-discovery/
7. SEEK FAQ (PDF) - https://www.brooklyn.cuny.edu/web/1202_SEEK_FAQs.pdf
8. ICORP Initiative - https://www.cuny.edu/academics/academic-programs/seek-college-discovery/icorp/
9. Reddit: SEEK Program - r/CUNY (manual export)
10. Reddit: SEEK Summer Session - r/CUNY (manual export)
11. Reddit: SEEK vs ASAP - r/CUNY (manual export)

## Chunking Strategy
Two strategies were used based on document structure.

Official pages use 500-character chunks with 100-character overlap. These pages 
contain dense multi-sentence paragraphs where one idea spans several sentences. 
Larger chunks capture complete thoughts without fragmentation.

Reddit comments use 250-character chunks with 50-character overlap. Reddit 
comments are short self-contained thoughts. Smaller chunks preserve their 
natural structure without breaking meaning.

Overlap ensures that key information falling at a chunk boundary appears in 
both adjacent chunks so retrieval can still find it.

## Sample Chunks

**Chunk 1** (Source: seek_brochure)
"SEEK (Search for Education, Elevation and Knowledge) is a higher education 
opportunity program found at each of the senior colleges of CUNY. The SEEK 
Program provides special academic, financial and counseling assistance to 
students entering college for the first time."

**Chunk 2** (Source: cuny_seek_overview)
"Be a resident of New York State for at least one year prior to entering 
college. Be a high school graduate or recipient of a state-approved equivalency 
diploma. Be inadmissible according to the admissions criteria established for 
the CUNY four-year college you want to attend."

**Chunk 3** (Source: reddit_seek_program)
"SEEK is a great program as it offers various benefits such as priority 
registration, extra stipends, and other benefits."

**Chunk 4** (Source: seek_advisement)
"As a SEEK student, you are assigned an academic student support specialist 
(SEEK counselor) who will help you navigate your academic journey at Brooklyn 
College."

**Chunk 5** (Source: seek_faq)
"I did not receive my stipend. Registration for Summer 2020 began mid March. 
Please make an appointment with your counselor/advisor via SAAT appointment 
system in CUNYFirst for registration assistance."

Note: Chunk 5 references 2020 dates. This is an outdated source and represents 
a known limitation of the system.

## Embedding Model
Model: all-MiniLM-L6-v2 via sentence-transformers. Runs locally with no API 
key or rate limits.

Production tradeoffs: For a real deployment I would consider OpenAI's 
text-embedding-3-small for higher accuracy on domain-specific text, but it 
requires an API key and has per-token cost. all-MiniLM-L6-v2 has a 256-token 
context window which can truncate longer official page chunks. For a 
multilingual student population, paraphrase-multilingual-MiniLM-L12-v2 would 
be worth considering despite its higher latency.

## Retrieval Test Results

**Query 1:** "How do I apply to SEEK?"
Top chunks returned:
- apply_to_seek (distance: 0.737) - eligibility criteria for first-time students
- seek_brochure (distance: 0.810) - SEEK creation and purpose
- reddit_seek_program (distance: 0.849) - student describing SEEK benefits

The apply_to_seek chunk is relevant because it directly addresses eligibility 
for joining SEEK. Distance of 0.737 indicates a reasonable semantic match.

**Query 2:** "What financial support does SEEK provide?"
Top chunks returned:
- reddit_seek_program (distance: 0.916) - mentions stipends and benefits
- cuny_seek_overview (distance: 1.014) - eligibility criteria
- reddit_seek_vs_asap (distance: 1.020) - compares SEEK and ASAP stipends

Distances above 0.9 indicate weak matches. The word "financial" does not 
appear frequently in the documents even though SEEK provides financial support. 
This is a vocabulary mismatch between the query and the corpus.

**Query 3:** "What do students say about SEEK advisors?"
Top chunks returned:
- seek_advisement (distance: 0.899) - official advisement page
- cuny_seek_overview (distance: 0.949) - mentions academic advising
- history_of_seek (distance: 0.998) - program history

This query should return Reddit chunks since it asks for student opinions, but 
official pages dominate. The Reddit content about advisors is sparse, so the 
embedding model matched official advisement content instead.

## Grounded Generation
Grounding is enforced through the system prompt passed to llama-3.3-70b-versatile 
via the Groq API. The prompt explicitly instructs the model to answer using only 
the retrieved context and to respond with "I don't have enough information about 
that in my sources." when the context is insufficient. Temperature is set to 0.1 
to reduce creative generation. Sources are programmatically extracted from 
retrieved chunk metadata and appended to every response.

## Example Responses

**Response 1:** "How do I apply to SEEK?"
Answer: "The context does not provide a step-by-step guide on how to apply to 
SEEK, but it mentions that to be considered for the SEEK program, the student 
applicant must meet certain eligibility criteria, such as being a first-time 
college student or transferring from a college where they were part of an 
Opportunity Program. (Source: apply_to_seek)"
Sources: seek_brochure, seek_faq, history_of_seek, apply_to_seek

**Response 2:** "What financial support does SEEK provide?"
Answer: "The context mentions that the SEEK program provides financial 
assistance, but it does not specify the details of the financial support. 
(Source: history_of_seek)"
Sources: seek_brochure, seek_faq, history_of_seek, apply_to_seek

**Out-of-scope query:** "Can I get a SEEK scholarship for grad school?"
Answer: "I don't have enough information about that in my sources."
Sources: history_of_seek, seek_faq, seek_brochure, icorp, apply_to_seek

## Query Interface
The interface is built with Gradio and runs at http://localhost:7860.

Input: A text box labeled "Your question" with placeholder text.
Output: Two text boxes — "Answer" showing the LLM response with inline source 
citations, and "Sources" listing the document names the answer was drawn from.

Sample interaction:
User: "What financial support does SEEK provide?"
Answer: "The context mentions that the SEEK program provides financial 
assistance, but it does not specify the details. (Source: history_of_seek)"
Sources: seek_brochure, seek_faq, history_of_seek, apply_to_seek

## Evaluation Report

| Question | Expected Answer | System Response | Accuracy |
|---|---|---|---|
| How do I apply to SEEK? | Eligibility criteria and application steps | Found eligibility but missed steps | Partially Accurate |
| What financial support does SEEK provide? | Stipends, tuition, book allowances | Vague answer, missing specifics | Partially Accurate |
| Can I get a SEEK scholarship for grad school? | System should refuse — SEEK is undergrad only | Correctly refused | Accurate |
| Can seniors join SEEK? | No — SEEK is for first-time freshmen and transfers | Correctly identified eligibility constraint | Partially Accurate |
| Are there any mandatory events from SEEK? | Yes — orientation workshops for transfers | Could not find answer | Inaccurate |

## Failure Case
When asked "Can I get a SEEK scholarship for grad school?", the system 
initially retrieved ICORP research program chunks due to vocabulary overlap 
with terms like "SEEK", "credits", and "GPA". The LLM misinterpreted this 
adjacent content as answering the question about grad school funding, producing 
a confidently wrong answer instead of refusing. After reviewing the system 
prompt, the refusal instruction was strengthened and the system now correctly 
refuses this question. This is a retrieval failure causing a generation failure: 
the embedding model cannot distinguish between "SEEK scholarship for grad 
school" and "ICORP research eligibility" because they share vocabulary in the 
same domain.

A second failure: Question 5 about mandatory events returned no answer despite 
the transfer orientation section of the official pages mentioning mandatory 
workshops. The relevant sentence was split across a chunk boundary during 
ingestion, so neither chunk contained the complete information needed to answer.

## Spec Reflection
The spec helped by forcing chunking decisions before writing any code. Deciding 
on 500 vs 250 character chunks for different document types before implementation 
meant the ingestion pipeline was built correctly the first time rather than 
having to refactor later.

One divergence: the spec assumed Reddit could be scraped automatically. In 
practice Reddit returned 403 errors for all three threads. The workaround was 
manually copying comment text into .txt files. This is documented as a 
limitation — the Reddit content is a snapshot and will not update automatically.

## AI Usage
1. Claude generated the full ingest.py based on my planning.md chunking 
strategy and document list. I reviewed the Reddit loader and identified that 
it would fail with a 403 error, which led to the manual .txt workaround. I 
also identified that the len(chunk) > 50 filter was needed to remove empty 
chunks that the splitter was producing.

2. Claude generated generate.py including the system prompt. I identified that 
the grounding prompt was failing on the grad school question because retrieved 
chunks were topically adjacent but factually wrong. I documented this as a 
failure case rather than hiding it.