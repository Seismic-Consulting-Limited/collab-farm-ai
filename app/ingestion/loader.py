from pathlib import Path


def load_markdown_documents(folder):

    documents = []

    path = Path(folder)

    for file in path.glob("*.md"):

        content = file.read_text(
            encoding="utf-8"
        )

        documents.append(
            {
                "content": content,
                "source": file.name
            }
        )

    return documents