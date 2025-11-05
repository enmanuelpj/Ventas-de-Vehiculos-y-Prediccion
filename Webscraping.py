import requests
from bs4 import BeautifulSoup
import pandas as pd

link = "https://www.google.com/finance/quote/USD-DOP"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Edg/111.0.1661.44"
}
response = requests.get(link, headers=headers)
htmlSoup = BeautifulSoup(response.text, "html.parser")
tasa = htmlSoup.find("div", class_="YMlKec fxKbKc").text

dsTasa = pd.DataFrame({"FechaTasa": [pd.Timestamp.now()], "USD_DOP": [tasa]})
