import re


def chunk_text_by_characters(text_content, chunk_size=150, offset=50):
    chunks = []
    start_idx = 0

    while start_idx < len(text_content):
        end_idx = min(start_idx + chunk_size, len(text_content))
        chunks.append(text_content[start_idx:end_idx])

        if end_idx < len(text_content):
            start_idx = end_idx - offset
        else:
            start_idx = len(text_content)

        return chunks


def chunk_text_by_sentence(text_content, max_sentences_per_chunk=3, offset=1):
    sentences = re.split(r"(?<=[.!?])\s+", text_content.strip())
    chunks = []
    start_idx = 0

    while start_idx < len(sentences):
        end_idx = min(start_idx + max_sentences_per_chunk, len(sentences))
        chunks.append(" ".join(sentences[start_idx:end_idx]))

        if end_idx < len(sentences):
            start_idx = end_idx - offset
        else:
            start_idx = len(sentences)

    return chunks


def chunk_by_section(markdown_text):
    sections = re.split(r"\n?## ", markdown_text)
    return [section.strip() for section in sections if section.strip()]
