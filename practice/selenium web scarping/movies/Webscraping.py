from bs4 import BeautifulSoup
import os
import pandas as pd

# Add a Rank column
d = {"Rank": [], "Title": [], "Rating": [], "Summary": []}

# Sort files by name so 1–200 go in order
files = sorted(os.listdir("data"))

for i, file in enumerate(files, start=1):  # 🔢 start counting from 1
    with open(f"data/{file}", encoding="utf-8") as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, "html.parser")

    t = soup.find("h3", class_="ipc-title__text")
    title = t.get_text(strip=True) if t else "N/A"

    De = soup.find("div", class_="ipc-html-content-inner-div")
    desc = (
        De.get_text(strip=True) if De else "N/A"
    )  # ✅ fixed small bug: should be De, not d

    r = soup.find("span", class_="ipc-rating-star--rating")
    rating = r.get_text(strip=True) if r else "N/A"

    # Append data
    d["Rank"].append(i)
    d["Title"].append(title)
    d["Rating"].append(rating)
    d["Summary"].append(desc)

# Create DataFrame and save
df = pd.DataFrame(data=d)
df.to_csv("Movies.csv", index=False, encoding="utf-8")

print("✅ Movies.csv saved with rank numbers 1–200!")
