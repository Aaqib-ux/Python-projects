from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Chrome()
file = 0

driver.get(
    "https://www.imdb.com/search/title/?title_type=feature&genres=thriller&sort=num_votes,desc"
)

time.sleep()

last_height = driver.execute_script("return document.body.scrollHeight")

while True:

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height


elems = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")
print(f"Total movie found: {len(elems)}")

for elem in elems:
    Html = elem.get_attribute("outerHTML")
    with open(f"data/movies_{file}.html", "w", encoding="utf-8") as f:
        f.write(Html)
        file += 1


driver.close()
