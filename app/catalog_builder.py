import json
from pathlib import Path

from parser import parse_assessment

BASE_DIR = Path(__file__).resolve().parent.parent

URL_FILE = BASE_DIR / "data" / "assessment_urls.json"
OUTPUT_FILE = BASE_DIR / "data" / "catalog.json"


def load_urls():
    with open(URL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_catalog(catalog):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=4)


def build_catalog():

    urls = load_urls()

    catalog = []

    visited = set()

    # Titles that indicate an invalid page
    invalid_titles = {
        "403 ERROR",
        "Down For Maintenance",
        "",
        None,
    }

    print(f"\nFound {len(urls)} URLs\n")

    for index, url in enumerate(urls, start=1):

        if url in visited:
            continue

        visited.add(url)

        print(f"[{index}/{len(urls)}] Parsing")
        print(url)

        try:
            assessment = parse_assessment(url)

            # Skip invalid pages
            if assessment["name"] in invalid_titles:
                print("⚠️ Skipped invalid page\n")
                continue

            catalog.append(assessment)

            save_catalog(catalog)

            print("✓ Saved\n")

        except Exception as e:
            print("❌ Failed")
            print(e)

    print("=" * 50)
    print("Finished!")
    print(f"Assessments Parsed : {len(catalog)}")
    print(f"Saved To : {OUTPUT_FILE}")


if __name__ == "__main__":
    build_catalog()