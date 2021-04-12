import glob
import time
from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from font_fredoka_one import FredokaOne
from font_source_sans_pro import SourceSansProSemibold

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    exit("This script requires the bs4 module\nInstall with: sudo pip install beautifulsoup4")


# Set up the display
inky_display = InkyPHAT("black")
inky_display.set_border(inky_display.BLACK)

# Load our backdrop image
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# Query Dark Sky (https://darksky.net/) to scrape current weather data
# Arlington, MA


def get_weather():
    weather = {}
    res = requests.get("https://darksky.net/forecast/42.4119,-71.1473/us12/en")
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "lxml")

        curr = soup.find_all("span", "currently")

        weather["currently"] = curr[0].text.strip()
        weather["temperature"] = int(curr[0].find(
            "span", "summary").text.split()[0][:-1])
        weather["currently_summary"] = soup.find(
            'span', 'currently__summary').text.strip()
        return weather
    else:
        return weather


weather = get_weather()

# Load the FredokaOne font
fontTitle = ImageFont.truetype(SourceSansProSemibold, 16)
fontText = ImageFont.truetype(SourceSansProSemibold, 16)


# Write text with weather values to the canvas
datetime = time.strftime("%B %d, %I:%M %p")
draw.text((10, 5), datetime, inky_display.BLACK, font=fontTitle)
draw.text((10, 25), weather["currently"] + ". " +
          weather["currently_summary"], inky_display.BLACK, font=fontText)

inky_display.set_image(img)
inky_display.show()
