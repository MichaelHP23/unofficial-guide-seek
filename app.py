import gradio as gr
from generate import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="SEEK Unofficial Guide") as demo:
    gr.Markdown("# SEEK Unofficial Guide\nAsk anything about navigating the SEEK program at Brooklyn College.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. How do I apply to SEEK?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()