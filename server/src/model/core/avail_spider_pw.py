from playwright.sync_api import sync_playwright

from loguru import logger


def _try_click(page, selectors, timeout=1500):
    for selector in selectors:
        try:
            locator = page.locator(selector).first
            if locator.is_visible(timeout=timeout):
                locator.click(timeout=timeout)
                return True
        except Exception:
            continue
    return False


def clear_barriers(page):
    close_selectors = [
        "button[aria-label='Close']",
        "button.close",
        ".btn-close",
        "button:has-text('Close')",
        "button:has-text('Skip')",
        "button:has-text('Not now')",
        "button:has-text('Later')",
        "button:has-text('No thanks')",
    ]
    city_selectors = [
        ".swiper-slide-active button",
        ".swiper-slide button",
        ".swiper-slide a",
        "button:has-text('Select')",
        "button:has-text('Continue')",
        "button:has-text('Apply')",
    ]

    for _ in range(3):
        clicked_close = _try_click(page, close_selectors)
        clicked_city = _try_click(page, city_selectors)
        if not clicked_close and not clicked_city:
            break
        page.wait_for_timeout(500)

def create_browser(playwright):
    try:
        browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )
        return browser

    except Exception as e:
        logger.error(f"Browser launch failed: {e}")
        return None

def avail_movies():
    url = "https://www.inoxmovies.com/"
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

    try:
        with sync_playwright() as playwright:
            browser = create_browser(playwright)
            if browser is None:
                return []

            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=user_agent,
                geolocation={"latitude": 12.9716, "longitude": 77.5946},
                permissions=["geolocation"],
            )
            page = context.new_page()

            page.goto(url, wait_until="domcontentloaded")

            clear_barriers(page)

            page.wait_for_selector("div.now-movies", timeout=15000)

            elements = page.locator(
                "xpath=//div[contains(@class, 'now-movies') and not(ancestor::div[contains(@class, 'hollywood-movie-section')])]//img[contains(@class, 'rounded')]"
            )

            movie_titles = []
            for i in range(elements.count()):
                alt = elements.nth(i).get_attribute("alt")
                if alt:
                    movie_titles.append(alt.strip())

            context.close()
            browser.close()

            return movie_titles[:-9]  # Exclude the last 9 entries which are not movies

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    movies = avail_movies()
    print(movies)

    # driver = create_driver()
    # print(driver)

    # Save the available movie titles to a txt file
    # with open("./output/available_movies.txt", "w") as f:
    #     for title in movies:
    #         f.write(title + "\n")
