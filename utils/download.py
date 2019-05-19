import requests
from lxml import html

headers = {
	"Referer": "https://www.ric.si/splosna_matura/predmeti/matematika/",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
}

url_base = "https://www.ric.si"
url = url_base + "/splosna_matura/predmeti/matematika/"

r = requests.get(url, headers=headers)

html_content = html.fromstring(r.content)
contentArea = html_content.xpath("//div[@id='contentArea']")

for i in html_content.xpath("//a[@rel='ATTACH']"):
	if "pola 1" in i.text and "italijanska različica" not in i.text and "madžarska različica" not in i.text:
		url = i.get("href")
		print(url_base + url)
		open("../pdfs/matematika/pola 1/" + url.split("/")[2] + ".pdf", "wb").write(requests.get(url_base + url, headers=headers).content)
