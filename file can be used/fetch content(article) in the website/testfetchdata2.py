import mysql.connector
import uvicorn
from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()
conn = mysql.connector.connect()


@app.get("/scrape")
async def scrape_website():
    url = "https://www.pewpewtactical.com/best-remington-700-upgrades/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        data_to_return = []

        for item in soup.find_all("div"):
            a_element = item.find("a")
            link = a_element["href"] if a_element and "href" in a_element.attrs else None

            # Extracted data
            extracted_data = {"text": item.get_text(strip=True), "link": link}
            data_to_return.append(extracted_data)

        return {"data": data_to_return}
    else:
        return {"error": f"Error: {response.status_code}"}


if __name__ == '__main__':
    uvicorn.run(app='testfetchdata2:app', host="127.0.0.1", port=8971, reload=True, debug=True)