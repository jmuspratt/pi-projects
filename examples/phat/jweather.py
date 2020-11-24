import glob
import time
from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from font_fredoka_one import FredokaOne

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
        weather["summary"] = curr[0].img["alt"].split()[0]
        weather["temperature"] = int(curr[0].find("span", "summary").text.split()[0][:-1])
        press = soup.find_all("div", "pressure")
        weather["pressure"] = int(press[0].find("span", "num").text)
        return weather
    else:
        return weather

weather = get_weather()

# Load the FredokaOne font
font = ImageFont.truetype(FredokaOne, 22)
# intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))
# hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35 * scale_size))
# hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, int(16 * scale_size))

# Draw lines to frame the weather data


# Write text with weather values to the canvas
datetime = time.strftime("%m/%d %H:%M")
draw.text((10, 10), datetime, inky_display.BLACK, font=font)
draw.text((10, 30), weather["summary"], inky_display.BLACK, font=font)
# draw.text((10, 50), "High: " + weather["high"], inky_display.RED, font=font)
draw.text((10, 50), "High temp goes here...", inky_display.RED, font=font)

# Display the text
inky_display.set_image(img)
inky_display.show()

