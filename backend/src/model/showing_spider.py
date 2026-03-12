from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

def movies_showing(name: str, code: str, city: str, date: str) -> list:
    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://in.bookmyshow.com/cinemas/{city}/{name}/buytickets/{code}/{date}"
        driver.get(url)

        WebDriverWait(driver, 5).until(EC.url_to_be(url))
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.sc-1412vr2-2"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        # Extract movie names from the cinema session listing
        movie_titles = soup.find_all("a", class_="sc-1412vr2-2 cPWByY")
        return [tag.text.strip() for tag in movie_titles if tag.text.strip()]
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    finally:
        driver.quit()



if __name__ == "__main__":
    movies = movies_showing(name="inox-janak-place", code="SCJN", city="national-capital-region-ncr", date="20260312")
    # print(movies)

    # Save the showing movie titles to a txt file
    with open("./output/showing_movies.txt", "w") as f:
        for title in movies:
            f.write(title + "\n")