#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale
import time
import config
debug = False

if not debug:
    from inky import InkyPHAT
    from PIL import Image, ImageDraw, ImageFont
    from font_fredoka_one import FredokaOne
    from font_source_sans_pro import SourceSansProSemibold

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

# Config
locale.setlocale(locale.LC_ALL, '')


elizaEndpoint = 'https://api.airtable.com/v0/appGttbRiDa3ik9mf/Eliza%20Transactions?maxRecords=100&view=Grid%20view'
willEndpoint = 'https://api.airtable.com/v0/appGttbRiDa3ik9mf/Will%20Transactions?maxRecords=100&view=Grid%20view'

elizaResponse = requests.get(elizaEndpoint, headers={
                             'Authorization': 'Bearer ' + config.AIRTABLE_API_KEY})
willResponse = requests.get(willEndpoint, headers={
                            'Authorization': 'Bearer ' + config.AIRTABLE_API_KEY})

elizaRecords = elizaResponse.json()['records']
willRecords = willResponse.json()['records']

elizaSum = 0
for transaction in elizaRecords:
    elizaSum += transaction['fields']['Amount']

willSum = 0
for transaction in willRecords:
    willSum += transaction['fields']['Amount']

elizaColor = "RED" if elizaSum < 0 else "BLACK"
willColor = "RED" if willSum < 0 else "BLACK"

elizaBalance = locale.currency(elizaSum, grouping=True)
willBalance = locale.currency(willSum, grouping=True)

elizaText = "Eliza's balance: " + elizaBalance
willText = "Will's balance: " + willBalance

if debug:
    print(elizaText)
    print(willText)


if not debug:
    # Set up the display
    inky_display = InkyPHAT("black")
    inky_display.set_border(inky_display.BLACK)

    # # Load our backdrop image
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    # # Load the FredokaOne font
    fontTitle = ImageFont.truetype(SourceSansProSemibold, 16)
    fontText = ImageFont.truetype(SourceSansProSemibold, 16)

    # Write text to the canvas
    datetime = time.strftime("%B %d, %I:%M %p")
    draw.text((10, 5), datetime, inky_display.BLACK, font=fontTitle)
    draw.text((10, 40), elizaText,
              getattr(inky_display, elizaColor), font=fontText)
    draw.text((10, 60), willText,
              getattr(inky_display, willColor), font=fontText)

    inky_display.set_image(img)
    inky_display.show()
