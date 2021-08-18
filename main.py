import os
import re
from io import StringIO

from chinese import ChineseAnalyzer
import pinyin

from pdf2image import convert_from_path

from PIL import Image
from pytesseract import pytesseract
pytesseract.tesseract_cmd = r"C:\Users\Angel\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

from fpdf import FPDF


def chain(mandarin):
    return list(map(lambda word: [word, pinyin.get(word)] if re.match(r"[^\d_\W]+", word) else [word, ""], mandarin))


def convert(string):
    analyzer = ChineseAnalyzer()
    stringList = analyzer.parse(string)
    chineseTokens = stringList.tokens()

    return chain(chineseTokens)

def getInputFiles():
    pdfPath = f"{os.getcwd()}\\assets\\pdf"
    return [f"{pdfPath}\\{pdf}" for pdf in os.listdir(pdfPath)]


def createText():
    files = getInputFiles()
    pages = convert_from_path(files[0], dpi=144)
    completeText = ""
    for page in pages:
        imagePath = "./assets/out/img.jpg"
        page.save(imagePath, "JPEG")
        img = Image.open(imagePath)
        text = pytesseract.image_to_string(img, lang="chi_sim")
        completeText += text
    return chineseCleaner(completeText)

def createText():

    text = ""

    pass


def chineseCleaner(text):
    canSpace = False
    lineList = []
    for line in text.splitlines():
        if line.strip():
            canSpace = True
        elif canSpace:
            canSpace = False
        elif not canSpace:
            continue
        lineList.append(re.sub(r" +", " ", line))
    return "\n".join(lineList)


if __name__ == "__main__":
    # f = open("./assets/out/out.txt", "w")
    # plainText = createText()
    # f.write(plainText)
    # text = convert(plainText)
    # for mandarin, roman in text:
    #     out = f"{mandarin} {roman} "
    #     f.write(out)
    imgPath = f"{os.getcwd()}\\assets\\img"
    imgs = [f"{imgPath}\\{img}" for img in os.listdir(imgPath)]
    text = ""
    for img in imgs:
        img = Image.open(img)
        text += pytesseract.image_to_string(img, lang="chi_sim")
    open("./assets/out/out.txt", "w").write(text)
