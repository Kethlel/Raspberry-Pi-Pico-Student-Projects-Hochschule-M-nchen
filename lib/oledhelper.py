def oledClear(oled):
    oled.fill(0)
    oled.show()

def oledPrint(oled, text, lineNr, show=True, replEcho=True, charHeight=8):
    oled.fill_rect(0, lineNr*charHeight, oled.width, charHeight, 0)
    oled.text(text, 0, lineNr*charHeight)
    if show:
        oled.show()
    if replEcho:
        print(text)

