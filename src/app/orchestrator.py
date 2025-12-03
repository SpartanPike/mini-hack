# src/app/orchestrator.py
from src.pii.masker import mask_pii, unmask
from src.rag.retriever import RAGRetriever
from src.rag.prompts import build_context_block, build_user_prompt, RAG_SYSTEM_PROMPT
from src.models.llm import LocalLLM

from src.tools.stores import get_nearby_stores
from src.tools.coupons import get_active_coupons
from src.tools.orders import get_latest_order

retriever = RAGRetriever()
llm = LocalLLM()

def summarize_profile(user_id):
    return f"User {user_id} is a frequent customer who enjoys hot drinks."

def build_tools_context(user_id, lat, lon):
    stores = get_nearby_stores(lat, lon)
    coupons = get_active_coupons(user_id)
    order = get_latest_order(user_id)

    out = "Nearby stores:\n"
    for s in stores:
        out += f"- {s['name']} ({s['id']})\n"

    out += "\nCoupons:\n"
    for c in coupons:
        out += f"- {c['description']} (store {c['store_id']})\n"

    out += "\nLatest order:\n"
    out += f"- {order['order_id']}: {order['status']} (ETA {order['eta']} mins)\n"

    return out

def handle_user_message(user_id, message, lat, lon):
    masked, pii_map = mask_pii(message)
    rag_results = retriever.retrieve(masked)
    profile = summarize_profile(user_id)
    tools_ctx = build_tools_context(user_id, lat, lon)

    context_block = build_context_block(rag_results, tools_ctx, profile)
    user_prompt = build_user_prompt(context_block, masked)

    reply = llm.chat(RAG_SYSTEM_PROMPT, user_prompt)
    reply = unmask(reply, pii_map)

    return {"answer": reply}
