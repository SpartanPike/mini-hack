# src/rag/prompts.py

RAG_SYSTEM_PROMPT = """
You are a helpful retail customer assistant.
Use ONLY the context given.
If missing info, ask a clarifying question and NEVER hallucinate.
Be concise, friendly, and compliant with store policy.
"""

def build_context_block(rag_chunks, tools, profile):
    ctx = "### User Profile\n" + profile + "\n\n"
    ctx += "### Tools (real-time)\n" + tools + "\n\n"
    ctx += "### RAG Context\n"
    for i, c in enumerate(rag_chunks):
        ctx += f"[{i}] ({c['score']:.4f}) {c['doc_id']}\n{c['text']}\n\n"
    return ctx

def build_user_prompt(context, message):
    return f"""{context}
### User Message:
{message}

### Task:
Use the context above to answer the user:
"""
