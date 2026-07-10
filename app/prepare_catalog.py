import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG_FILE = BASE_DIR / "data" / "catalog.json"


def clean_text(text: str) -> str:
    """Remove extra whitespace."""
    return " ".join(text.split())


def build_embedding_text(item):

    parts = [
        f"Name: {item['name']}",
        f"Category: {item['category']}",
        f"Description: {item['description']}",
    ]

    if item["sections"]:
        parts.append(
            "Sections: " + ", ".join(item["sections"])
        )

    return clean_text(" ".join(parts))


def main():

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    for item in catalog:

        item["id"] = (
            item["name"]
            .lower()
            .replace(" ", "-")
            .replace("(", "")
            .replace(")", "")
        )

        item["embedding_text"] = build_embedding_text(item)

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=4)

    print("✅ Catalog prepared successfully.")


if __name__ == "__main__":
    main()