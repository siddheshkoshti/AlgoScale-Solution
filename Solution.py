from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def findTotalArticlesByLanguages(languages):

    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)


    try:
        driver.get("https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table")
        driver.maximize_window()

        wait = WebDriverWait(driver, 20)
        table = wait.until(EC.presence_of_element_located((By.XPATH, "(//table[@class='sortable jquery-tablesorter'])[1]")))

        rows = table.find_elements(By.XPATH, ".//tbody/tr")

        language_to_articles = {}

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 2:
                language = columns[1].text.strip()
                articles = columns[2].text.strip().replace(',', '')

                if articles.isdigit():
                    language_to_articles[language] = int(articles)

        total_articles = sum(language_to_articles[lang] for lang in languages if lang in language_to_articles)
        return total_articles

    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("error_screenshot.png")
    finally:
        driver.quit()

languages = ["English", "German"]
total = findTotalArticlesByLanguages(languages)
print(f"Total articles for {languages}: {total}")