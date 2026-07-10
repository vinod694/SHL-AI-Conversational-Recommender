from playwright.sync_api import sync_playwright

URL = "https://www.shl.com/products/assessments/"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(URL, wait_until="domcontentloaded")

    page.wait_for_timeout(3000)

    # Try to accept cookies
    try:
        page.get_by_role("button", name="Allow all").click(timeout=3000)
        print("✅ Cookie popup accepted.")
    except:
        try:
            page.get_by_role("button", name="Accept").click(timeout=3000)
            print("✅ Cookie popup accepted.")
        except:
            print("⚠️ No cookie popup found.")

    page.wait_for_timeout(2000)

    print("\nPage Title:", page.title())

    links = page.locator("a")

    print(f"\nTotal Links: {links.count()}")

    print("\nSearching for SHL assessment links...\n")

    for i in range(links.count()):
        try:
            text = links.nth(i).inner_text().strip()
            href = links.nth(i).get_attribute("href")

            if href and "/products/assessments/" in href:
                print(text)
                print(href)
                print("-" * 40)

        except:
            pass

    input("Press Enter to close...")

    browser.close()