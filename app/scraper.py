from playwright.sync_api import sync_playwright

URL = "https://www.shl.com/solutions/products/product-catalog/"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        print("Opening SHL Product Catalog...")

        page.goto(URL)

        page.wait_for_timeout(5000)

        print("Page Title:")
        print(page.title())

        input("Press Enter to close browser...")

        browser.close()


if __name__ == "__main__":
    main()