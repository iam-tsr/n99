import asyncio
from playwright.async_api import async_playwright

async def avail_movies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            url = "https://www.inoxmovies.com/"
            await page.goto(url)

            # Wait until the movie title elements are present
            await page.wait_for_selector("div.now-movies", timeout=5000)

            # Fetch all elements with the target class
            xpath = "//div[contains(@class, 'now-movies') and not(ancestor::div[contains(@class, 'hollywood-movie-section')])]//img[contains(@class, 'rounded')]"
            elements = await page.locator(xpath).element_handles()
            
            movie_titles = []
            for el in elements:
                alt = await el.get_attribute("alt")
                if alt and alt.strip():
                    movie_titles.append(alt.strip())

            print(f"Found {len(movie_titles)} movie titles:\n")
            return movie_titles[:-9] if len(movie_titles) >= 9 else movie_titles

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

        finally:
            await browser.close()


if __name__ == "__main__":
    async def main():
        movies = await avail_movies()
        print(movies)

        # Save the available movie titles to a txt file
        # with open("./output/available_movies.txt", "w") as f:
        #     for title in movies:
        #         f.write(title + "\n")

    asyncio.run(main())
