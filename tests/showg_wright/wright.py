import re
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def movies_showing(name: str, code: str, city: str, date: str) -> list:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            url = f"https://in.bookmyshow.com/cinemas/{city}/{name}/buytickets/{code}/{date}"
            await page.goto(url)
            
            # Wait for URL to load
            await page.wait_for_url(url, timeout=5000)
            print("Data is available now.\n\nExtracting movie titles...")
            
            # Wait for specific elements to appear
            await page.wait_for_selector("a.sc-1412vr2-2", timeout=15000)

            # Get the page source and parse with BeautifulSoup as before
            html = await page.content()
            soup = BeautifulSoup(html, "lxml")

            # Extract movie names from the cinema session listing
            movie_titles = soup.find_all("a", class_="sc-1412vr2-2 cPWByY")
            print(clean_titles([tag.text.strip() for tag in movie_titles if tag.text.strip()]))
            
        except Exception as e:
            print("Data not available yet.")
            return []
        
        finally:
            await browser.close()


def clean_titles(titles):
    cleaned_titles = [re.sub(r'\(.*?\)', '', title).strip().upper() for title in titles]
    return cleaned_titles


if __name__ == "__main__":
    import time
    start_time = time.time()
    async def main():
        movies = await movies_showing(name="inox-janak-place", code="SCJN", city="national-capital-region-ncr", date="20260314")
        # print(movies)

    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")