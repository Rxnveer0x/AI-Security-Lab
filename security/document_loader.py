from pathlib import Path


DOCUMENT_DIR = Path("data/documents")


def load_documents():
    """
    Load text documents from the document directory.
    """

    documents = []

    if not DOCUMENT_DIR.exists():
        return documents

    for file_path in DOCUMENT_DIR.glob("*.txt"):

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

            documents.append({
                "name": file_path.name,
                "content": content
            })

        except OSError:
            continue

    return documents