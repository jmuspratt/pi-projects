
try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    exit("This script requires the bs4 module\nInstall with: sudo pip install beautifulsoup4")


def get_weather():
    weather = {}
    res = requests.get("https://darksky.net/forecast/42.4119,-71.1473/us12/en")
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "lxml")
        curr = soup.find_all("span", "currently")
        weather["summary"] = curr[0].img["alt"].split()[0]
        weather["temperature"] = int(curr[0].find("span", "summary").text.split()[0][:-1])
        press = soup.find_all("div", "pressure")
        weather["pressure"] = int(press[0].find("span", "num").text)
        return weather
    else:
        return weather

weather = get_weather()



print(weather["summary"])