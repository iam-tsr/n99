import re
import asyncio
from bs4 import BeautifulSoup
from loguru import logger
from playwright.async_api import async_playwright

async def movies_showing(cinema: str, code: str, city: str, target_date: str, movie: str) -> list:
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
            url = f"https://in.bookmyshow.com/cinemas/{city}/{cinema}/buytickets/{code}/{target_date}"
            logger.info(f"Navigating to URL: {url}")
            await page.goto(url)
            
            await page.wait_for_url(url, timeout=5000)
            logger.info("Data is available now. Extracting movie titles...")
            
            await page.wait_for_selector("a.sc-1412vr2-2", timeout=15000)

            html = await page.content()
            soup = BeautifulSoup(html, "lxml")

            movie_titles = soup.find_all("a", class_="sc-1412vr2-2 cPWByY")
            cleaned = clean_titles([tag.text.strip() for tag in movie_titles if tag.text.strip()])
            cleaned = list(set(cleaned))  # Remove duplicates
            
            # logger.info(f"Extracted movie titles: {cleaned}")

            if movie.upper() in cleaned:
                logger.info(f"Movie '{movie}' is showing on {target_date} at {cinema}.")
                return True
            else:
                logger.info(f"Movie '{movie}' is NOT showing on {target_date} at {cinema}.")
                return False
            
        except Exception as e:
            logger.error("Data not available yet.")
            return []
        
        finally:
            await context.close()
            await browser.close()


def clean_titles(titles):
    cleaned_titles = [re.sub(r'\(.*?\)', '', title).strip().upper() for title in titles]
    return cleaned_titles



if __name__ == "__main__":
    async def main():
        movies = await movies_showing(cinema="pvr-vegas-dwarka", code="PVVW", city="national-capital-region-ncr", target_date="20260322")
        print(movies)

    asyncio.run(main())