#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale
import time
import config
# https://pyairtable.readthedocs.io/en/latest/getting-started.html
from pyairtable import Table

debug = False

if not debug:
    from inky import InkyPHAT
    from PIL import Image, ImageDraw, ImageFont
    from font_fredoka_one import FredokaOne
    from font_source_sans_pro import SourceSansProSemibold

# Config
locale.setlocale(locale.LC_ALL, '')

# Fetch records
elizaTable = Table(config.AIRTABLE_API_KEY, config.AIRTABLE_BASE, 'Eliza Transactions')
willTable = Table(config.AIRTABLE_API_KEY, config.AIRTABLE_BASE, 'Will Transactions')

elizaRecords = elizaTable.all()
willRecords = willTable.all()

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
