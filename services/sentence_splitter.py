import re

def clean_text(text: str) -> str:
    """
    Normalize text by fixing line breaks and spacing
    """
    # Replace multiple newlines with space
    text = re.sub(r"\n+", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_into_sentences(text: str) -> list:
    """
    Split text into sentences while handling technical documents
    """
    # Basic sentence split using punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Clean and filter short garbage sentences
    sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 10
    ]

    return sentences
