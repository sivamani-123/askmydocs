from app.services.rag import chunk_text


def test_chunking_overlaps():
    text = " ".join(f"w{i}" for i in range(400))
    chunks = chunk_text(text, size=100, overlap=20)
    assert len(chunks) >= 4
    assert chunks[0].split()[-20:] == chunks[1].split()[:20]
