import requests
import pandas as pd
import time
import sqlite3
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15'
}

all_books = []

conn = sqlite3.connect("books_store.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS books")

def parsing_book_information():
    for page in range(1, 51):
        page_url = f"{BASE_URL}/catalogue/page-{page}.html"
        response = requests.get(page_url, headers=headers)
        if response.status_code == 200:
            page_soup = BeautifulSoup(response.text, "html.parser")
            books = page_soup.find_all("article", class_="product_pod")
            for book in books:
                values = []

                price_str = book.find("p", class_="price_color").text.replace("Â","").replace("£","")
                price = float(price_str)
                name = book.find("h3").find("a")["title"]
                rate = book.find("p", class_="star-rating")["class"][1]
                
                raw_link = book.find("h3").find("a")["href"].replace("catalogue/", "")
                link = f"{BASE_URL}/catalogue/{raw_link}"

                values.append(price)
                values.append(name)
                if rate == "One":
                    values.append(1)
                elif rate == "Two":
                    values.append(2)
                elif rate == "Three":
                    values.append(3)
                elif rate == "Four":
                    values.append(4)
                elif rate == "Five":
                    values.append(5)

                book_response = requests.get(link, headers=headers)
                time.sleep(0.2)
                if book_response.status_code == 200:
                    book_soup = BeautifulSoup(book_response.text, "html.parser")

                    category = book_soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
                    stock_txt = book_soup.find("p",class_="instock availability").text.strip().split()[2]
                    stock = int(stock_txt.replace("(",""))

                    values.append(category)
                    values.append(stock)
                    
                book_dict = {
                    "Name":values[1],
                    "Category":values[3],
                    "Price":values[0],
                    "Rate":values[2],
                    "Stock":values[4]
                }
                all_books.append(book_dict)
        print(f"Page {page} done")

def export_data():
    df = pd.DataFrame(all_books)
    df = df.drop_duplicates()
    df = df.sort_values(by=["Rate","Price"],ascending=[False,True])

    df.to_sql("books", conn, if_exists="replace", index=False)
    df.to_csv('clean_books.csv',index=False)

    df2 = pd.DataFrame()

    df2["Stock_of_all"] = df.groupby('Category')['Name'].count()
    df2["Price_of_all"] = df.groupby('Category')['Price'].mean().round(2)
    df2["Max_price"] = df.groupby('Category')['Price'].max()
    df2["Stock1"] = df.groupby('Category')['Stock'].sum()
    df2 = df2.reset_index()

    with pd.ExcelWriter("report.xlsx") as writer:
        df.to_excel(writer, sheet_name="All_Books", index=False)
        df2.to_excel(writer, sheet_name="Category_Stats", index=False)

    conn.close()

def main():
    parsing_book_information()
    export_data()

if __name__ == "__main__":
    main()