import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from bs4 import BeautifulSoup
import requests
import json


app33 = FastAPI()


@app33.get("/download")
async def download_website_data():
    url = "https://www.pewpewtactical.com/best-remington-700-upgrades/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        data_to_return = []

        for item in soup.find_all("div"):
            text = item.get_text(strip=True)
            a_element = item.find("a")
            link = a_element["href"] if a_element and "href" in a_element.attrs else None

            extracted_data = {"text": text, "link": link}
            data_to_return.append(extracted_data)

        # Create a JSON file with the extracted data
        json_data = json.dumps(data_to_return, indent=2, ensure_ascii=False)
        filename = "scraped_data.json"

        # Return the JSON file as a downloadable file
        return StreamingResponse(content=json_data, media_type="application/json",
                                 headers={"Content-Disposition": f'attachment; filename="{filename}"'})
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error: {response.status_code}")


if __name__ == '__main__':
    uvicorn.run(app='testfetchanddownload:app33', host="127.0.0.1", port=8371, reload=True, debug=True)
