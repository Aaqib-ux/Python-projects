from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import random
import time
import pandas as pd
import os
from datetime import datetime
import pytz


class PriceTracker:
    def __init__(self, query):
        self.query = query
        self.flipkart_data = {"Title": [], "Price": []}
        self.amazon_data = {"Title": [], "Price": [], "Link": []}
        self.timezone = pytz.timezone("Asia/Kolkata")

    def driver_Setup(self):

        # setup chorme browser and agent for non blockage

        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/121.0",
        ]

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)

    def scrape_flipkart(self, limit=5):
        """Scrape Flipkart product titles and prices for the given query."""
        print("-" * 50)
        print(f"Scraping Flipkart Data for: {self.query}...")
        print("-" * 50)

        driver = self.driver_Setup()

        try:
            # Construct search URL
            url = (
                f"https://www.flipkart.com/search?q={self.query}"
                "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"
            )
            driver.get(url)
            time.sleep(3)

            product_card = driver.find_elements(By.CLASS_NAME, "CGtC98")
            count = 0

            for product in product_card[:limit]:
                try:
                    titles = product.find_element(By.CLASS_NAME, "KzDlHZ")
                    prices = product.find_element(By.CLASS_NAME, "Nx9bqj")

                    title_text = titles.text.strip()
                    price_text = prices.text.strip()

                    if title_text and price_text:
                        self.flipkart_data["Title"].append(title_text)
                        self.flipkart_data["Price"].append(price_text)
                        count += 1

                except NoSuchElementException:
                    continue

                if count >= limit:
                    break

            print(f"✅ Found {count} products on Flipkart")

            # Save results
            if count > 0:
                df = pd.DataFrame(self.flipkart_data)
                os.makedirs("data", exist_ok=True)
                df.to_csv("data/flipkart_data.csv", index=False, encoding="utf-8-sig")

                print("💾 Flipkart data saved to data/flipkart_data.csv")

            return count

        finally:
            driver.quit()
            print("🧹 Browser closed.")

    def scarpe_amazon(self):
        # scarping amazon data
        print("-" * 50)
        print(f"Scarping amazon data for flipkart product")
        print("-" * 50)

        driver = self.driver_Setup()
        titles = self.flipkart_data["Title"]

        try:
            for index, title in enumerate(titles):
                print(f"{index+1}/{len(titles)} searching Amazon for : {title[:50]}")

                encoded_query = quote_plus(title)
                driver.get(f"https://www.amazon.in/s?k={encoded_query}")
                time.sleep(random.uniform(10, 15))

                product_cards = driver.find_elements(
                    By.CSS_SELECTOR, "[data-component-type='s-search-result']"
                )

                saved = False
                for card in product_cards:
                    # Skip sponsored products
                    if card.find_elements(By.CLASS_NAME, "puis-label-popover-default"):
                        continue

                    # Get the HTML of this card
                    card_html = card.get_attribute("outerHTML")

                    # Save each card with unique filename
                    filename = f"compare/amazon_{index}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(card_html)

                    saved = True
                    break

                if not saved:
                    with open(
                        f"compare/amazon_{index}.html", "w", encoding="utf-8"
                    ) as f:
                        f.write("")
        finally:
            driver.quit()

        return len(self.flipkart_data["Title"])  # FIX: Return count

    def parsing_amazon_html(self):

        print(f"{'-'*60}")
        print(f"STEP 3: Parsing Amazon HTML files")
        print(f"{'-'*60}")

        flipkart_titles = self.flipkart_data["Title"]

        for index in range(len(flipkart_titles)):
            print(f"Processing flipkart product {index+1}/{len(flipkart_titles)}")
            files = f"compare/amazon_{index}.html"

            if not files:
                print(f"Missing file for index {index}")
                self.amazon_data["Title"].append("N/A")
                self.amazon_data["Price"].append("N/A")
                self.amazon_data["Link"].append("N/A")
                continue

            with open(files, encoding="utf-8") as f:
                html_docs = f.read()

            soup = BeautifulSoup(html_docs, "html.parser")

            t = soup.find(
                "h2",
                class_="a-size-medium a-spacing-none a-color-base a-text-normal",
            )
            if t:
                title = t.get_text(strip=True)
            else:
                title = "N/A"

            p = soup.find("span", class_="a-offscreen")
            if not p:
                p = soup.find("span", class_="a-price-whole")
            if not p:
                p = soup.find("span", {"data-a-color": "price"})
            price = p.get_text(strip=True) if p else "N/A"

            l = soup.find(
                "a",
                class_="a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal",
            )

            if l and l.get("href"):
                link = "https://www.amazon.in" + l["href"]
            else:
                "N/A"

            self.amazon_data["Title"].append(title)
            self.amazon_data["Price"].append(price)
            self.amazon_data["Link"].append(link)

        print(f"parsed {len(self.amazon_data['Title'])} Amazon product")

    def comparison_both(self):
        """Compare both files using pandas"""
        print(f"{'-'*60}")
        print(f"STEP 4: Creating comparison report")
        print(f"{'-'*60}")

        flipkart_df = pd.read_csv("data/flipkart_data.csv")

        # create comparison with pandas

        comparison_df = pd.DataFrame(
            {
                "Flipkart_Title": flipkart_df["Title"],
                "Flipkart_Price": flipkart_df["Price"],
                "Amazon_Title": self.amazon_data["Title"],
                "Amazon_price": self.amazon_data["Price"],
                "Amazon_link": self.amazon_data["Link"],
            }
        )

        def price_comparison(row):

            try:
                flipkart_price = float(
                    row["Flipkart_Price"].replace("₹", "").replace(",", "")
                )
                amazon_price = float(
                    row["Amazon_price"].replace("₹", "").replace(",", "")
                )

                if flipkart_price < amazon_price:
                    return f"Flipkart cheaper by ₹{amazon_price-flipkart_price:.2f}"
                elif flipkart_price > amazon_price:
                    return f"Amazon Cheaper by ₹{flipkart_price-amazon_price:.2f}"
                else:
                    return "Same"

            except:
                return "Compare price"

        comparison_df["Price_Comparison"] = comparison_df.apply(
            price_comparison, axis=1
        )

        # Save with time stamp:
        now = datetime.now(self.timezone)
        timestamp = now.strftime("%d%m%Y_%H%M")
        file_name = f"report/price_comparison_{timestamp}.csv"
        comparison_df.to_csv(file_name, index=False, encoding="UTF-8-sig")

        print(f"Comparison report saved to {file_name}")
        print(f"✓ Report generated at: {now.strftime('%d-%m-%Y %I:%M:%S %p IST')}")
        print(f"\n{'-'*60}")
        print(f"Summary")
        print(f"\n{'-'*60}")
        print(f"Total product compared {len(comparison_df)}")
        print(f"Query: {self.query}")
        print(f"\nFirst 5 result")
        print(
            print(
                comparison_df[
                    [
                        "Flipkart_Title",
                        "Flipkart_Price",
                        "Amazon_price",
                        "Price_Comparison",
                    ]
                ].head()
            )
        )

        return file_name

    def run(self):

        start_time = time.time()

        print(f"\n{'-'*60}")
        print(f" # Price Tracker - starting query: {self.query}")
        print(f"\n{'-'*60}")

        os.makedirs("data", exist_ok=True)
        os.makedirs("compare", exist_ok=True)
        os.makedirs("report", exist_ok=True)

        try:
            num_product = self.scrape_flipkart(limit=5)

            if num_product == 0:
                print(f"No product found for {self.query}. Exiting...")
                return

            self.scarpe_amazon()

            self.parsing_amazon_html()

            report_file = self.comparison_both()

            elapsed_time = time.time() - start_time

            print(f"\n{'='*60}")
            print(f"✓ COMPLETED in {elapsed_time:.2f} seconds")
            print(f"{'='*60}\n")

            return report_file

        except Exception as e:
            print(f"\n Error {str(e)}")


if __name__ == "__main__":

    query = input("Enter the product you wanna compare: ")
    tracker = PriceTracker(query)
    tracker.run()

    print("\n✓ Done! Check the 'reports' folder for your comparison.")
