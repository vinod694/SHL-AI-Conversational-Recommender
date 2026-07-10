import json
import time
from playwright.sync_api import sync_playwright


def get_category(url: str):
    """Extract category from the URL."""

    parts = url.strip("/").split("/")

    if "personality-assessment" in parts:
        return "Personality Assessment"

    elif "behavioral-assessments" in parts:
        return "Behavioral Assessment"

    elif "cognitive-assessments" in parts:
        return "Cognitive Assessment"

    elif "skills-and-simulations" in parts:
        return "Skills & Simulations"

    elif "job-focused-assessments" in parts:
        return "Job Focused Assessment"

    elif "assessment-and-development-centers" in parts:
        return "Assessment & Development Center"

    return "Unknown"


def parse_assessment(url: str):
    """Parse a single SHL assessment page."""

    MAX_RETRIES = 3

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            ),
        )

        page = context.new_page()

        # ----------------------------
        # Retry loading page
        # ----------------------------
        success = False

        for attempt in range(MAX_RETRIES):

            try:
                print(f"Attempt {attempt + 1}...")

                page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=60000
                )

                success = True
                break

            except Exception as e:

                print("Retrying...", e)

                time.sleep(5)

        if not success:

            browser.close()

            return None

        # ----------------------------
        # Accept Cookies
        # ----------------------------
        try:
            page.get_by_role("button", name="Allow all").click(timeout=3000)
            page.wait_for_timeout(1000)
        except:
            pass

        assessment = {
            "name": "",
            "description": "",
            "category": get_category(url),
            "sections": [],
            "url": url
        }

        # ----------------------------
        # H1
        # ----------------------------
        try:
            assessment["name"] = page.locator("h1").first.inner_text().strip()
        except:
            assessment["name"] = ""

        # ----------------------------
        # Detect invalid pages
        # ----------------------------
        invalid_titles = {
            "403 ERROR",
            "Down For Maintenance",
            "",
        }

        if assessment["name"] in invalid_titles:

            print(f"Skipping invalid page: {assessment['name']}")

            browser.close()

            return None

        # ----------------------------
        # JSON-LD Description
        # ----------------------------
        scripts = page.locator("script[type='application/ld+json']")

        for i in range(scripts.count()):

            try:

                data = json.loads(scripts.nth(i).inner_text())

                if (
                    isinstance(data, dict)
                    and data.get("@type") == "WebPage"
                ):

                    assessment["description"] = data.get(
                        "description",
                        ""
                    )

                    break

            except:
                continue

        # ----------------------------
        # Sections
        # ----------------------------
        headings = page.locator("h2,h3")

        for i in range(headings.count()):

            try:

                text = headings.nth(i).inner_text().strip()

                if (
                    text
                    and text != "Outdated browser detected"
                    and text not in assessment["sections"]
                ):
                    assessment["sections"].append(text)

            except:
                pass

        browser.close()

        return assessment


if __name__ == "__main__":

    url = (
        "https://www.shl.com/products/assessments/"
        "personality-assessment/"
        "shl-occupational-personality-questionnaire-opq/"
    )

    result = parse_assessment(url)

    if result:
        print(json.dumps(result, indent=4))
    else:
        print("Assessment could not be parsed.")