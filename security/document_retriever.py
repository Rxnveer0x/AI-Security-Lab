import re

from security.rag_processor import get_safe_documents
from security.security_logger import log_security_event


def normalize_words(text):
    """
    Convert text into clean lowercase words.
    """

    if not isinstance(text, str):
        return set()

    words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

    return {
        word
        for word in words
        if len(word) > 2
    }


def retrieve_documents(query, top_k=3):
    """
    Retrieve safe documents related to the user's query.
    """

    if not isinstance(query, str):
        return []

    query_words = normalize_words(query)

    safe_documents, _ = get_safe_documents()

    scored_documents = []

    for document in safe_documents:

        content_words = normalize_words(
            document["content"]
        )

        score = len(
            query_words.intersection(content_words)
        )

        if score > 0:
            scored_documents.append(
                (score, document)
            )

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    selected_documents = [
        document
        for score, document in scored_documents[:top_k]
    ]

    for document in selected_documents:
        log_security_event(
            f"Retrieved document: {document['name']} "
            f"| Query: {query[:200]}",
            "RAG_DOCUMENT_RETRIEVED"
        )

    return selected_documents