"""LLM answer generation grounded on retrieved context. Falls back to extractive mode without an API key."""
from typing import List
from .. import config

SYSTEM = (
    "You are AskMyDocs, an assistant that answers strictly from the provided context. "
    "Cite sources as [1], [2]. If the context does not contain the answer, say so."
)


def generate(question: str, contexts: List[str]):
    if not contexts:
        return "No documents found. Upload a document first.", "extractive"
    if not config.ANTHROPIC_API_KEY:
        return "LLM key not configured. Most relevant passage:\n\n" + contexts[0], "extractive"
    import anthropic
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    context_block = "\n\n".join(f"[{i + 1}] {c}" for i, c in enumerate(contexts))
    msg = client.messages.create(
        model=config.LLM_MODEL,
        max_tokens=700,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Context:\n{context_block}\n\nQuestion: {question}"}],
    )
    return msg.content[0].text, "llm"
