from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure headless Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disk-cache-size=0")
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

def avail_movies():
    driver = webdriver.Chrome(options=options)

    try:
        url = "https://www.inoxmovies.com/"
        driver.get(url)

        # Wait until the movie title elements are present
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.now-movies"))
        )

        # Fetch all elements with the target class
        elements = driver.find_elements(By.XPATH,
            "//div[contains(@class, 'now-movies') and not(ancestor::div[contains(@class, 'hollywood-movie-section')])]//img[contains(@class, 'rounded')]"
        )

        movie_titles = [el.get_attribute("alt").strip() for el in elements if el.get_attribute("alt")]

        print("Available movies fetched successfully.")
        return movie_titles[:-9]  # Exclude the last 9 entries which are not movies

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    finally:
        driver.quit()

if __name__ == "__main__":
    movies = avail_movies()
    print(movies)

    # Save the available movie titles to a txt file
    # with open("./output/available_movies.txt", "w") as f:
    #     for title in movies:
    #         f.write(title + "\n")
