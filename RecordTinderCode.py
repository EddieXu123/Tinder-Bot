import pytesseract
from PIL import Image
import pyscreenshot as ImageGrab


def screen_shot():
    # coordinate of message notification gotten by sending dozens of messages to phone
    # and then using a notepad to mark where the key is on my screen. Then, trial and error to
    # pinpoint where the code is on my screen to extract to text using OCR
    image = ImageGrab.grab(bbox=(1123, 70, 1280, 90))
    image.save('code5.png')

    # Using our OCR
    im = Image.open('code5.png')
    text = pytesseract.image_to_string(im, lang="eng")
    print(text)

    write_file = open("output1.txt", "w")
    write_file.write(text)
    write_file.close()

    # Extracting the code from the screen shot
    screen = open("output1.txt", "r")
    output = screen.readline()
    output2 = output.split()
    code = output2[4]
    print(code)


screen_shot()
