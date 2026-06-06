from groq import Groq
from retrieve import retrieve
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant for students navigating the SEEK program at Brooklyn College.
Answer questions using ONLY the information provided in the context below.
If the context does not contain enough information to answer the question, say exactly:
"I don't have enough information about that in my sources."
Do not use any outside knowledge. Do not guess. Cite which source your answer comes from."""

def ask(question):
    chunks = retrieve(question, k=5)
    
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Source: {chunk['source']}]\n{chunk['text']}\n\n"
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000,
        temperature=0.1
    )
    
    answer = response.choices[0].message.content
    sources = list(set(c["source"] for c in chunks))
    
    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }

if __name__ == "__main__":
    test_questions = [
        "How do I apply to SEEK?",
        "What financial support does SEEK provide?",
        "Can I get a SEEK scholarship for grad school?"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("─" * 50)
        result = ask(question)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {', '.join(result['sources'])}")
        print()