import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Response

import uvicorn

app = FastAPI()

# URL of the website
url = "https://www.data.jma.go.jp/gmd/risk/obsdl/index.php"

# Perform an initial request to get cookies
initial_response = requests.get(url)

# Extract cookies from the response
cookies = initial_response.cookies.get_dict()
print(cookies)


# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(initial_response.content, 'html.parser')

# Find the input element with id 'sid' to get the sid value
sid_element = soup.find('input', {'id': 'sid'})
sid = sid_element['value']
print(sid)


payload = f'stationNumList=%5B%22s47662%22%5D&aggrgPeriod=9&elementNumList=%5B%5B%22201%22%2C%22%22%5D%5D&interAnnualFlag=1&ymdList=%5B%222024%22%2C%222024%22%2C%221%22%2C%222%22%2C%226%22%2C%226%22%5D&optionNumList=%5B%5D&downloadFlag=true&rmkFlag=1&disconnectFlag=1&youbiFlag=0&fukenFlag=0&kijiFlag=0&huukouFlag=0&csvFlag=1&jikantaiFlag=0&jikantaiList=%5B1%2C24%5D&ymdLiteral=1&PHPSESSID={sid}'

# Set User-Agent in headers
headers = {
        'Content-Type': 'application/x-www-form-urlencoded','Content-Transfer-Encoding':'binary',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
    }


# Define a path operation to get CSV data
@app.get("/csv-data")
async def get_csv_data():
    url = "https://www.data.jma.go.jp/gmd/risk/obsdl/show/table"
    response = requests.post(url=url, headers=headers,data=payload)
    if response.status_code == 200:
        return response.content.decode('shift-jis')
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


# Define a path operation to download CSV data
@app.get("/download-csv")
async def download_csv_data():
    url = "https://www.data.jma.go.jp/gmd/risk/obsdl/show/table"
    response = requests.post(url=url,headers=headers, data=payload)
    if response.status_code == 200:
        content = response.content
        # Set response headers for CSV download
        csv_response = Response(content=content, media_type="text/x-comma-separated-values")
        csv_response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        return csv_response
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


if __name__ == '__main__':
    uvicorn.run(app='TestCSVAPI7:app', host="127.0.0.1", port=8411, reload=True)
