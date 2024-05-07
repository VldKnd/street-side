import requests

url = "https://www.cmegroup.com/clearing/cpmi-iosco-reporting.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
}
response = requests.get(
    url=url,
)
content = response.content
print(content)