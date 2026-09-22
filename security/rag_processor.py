from security.document_loader import load_documents
from security.rag_security import validate_rag_context
from security.security_logger import log_security_event


def get_safe_documents():
    """
    Load documents and remove documents containing
    suspicious RAG instructions.
    """

    documents = load_documents()

    safe_documents = []
    blocked_documents = []

    for document in documents:

        is_safe, message = validate_rag_context(
            document["content"]
        )

        if is_safe:

            safe_documents.append(document)

        else:

            blocked_documents.append({
                "name": document["name"],
                "reason": message
            })

            log_security_event(
                f"Document: {document['name']} | "
                f"Reason: {message}",
                "RAG_INJECTION_BLOCKED"
            )

    return safe_documents, blocked_documents