from PDFNetPython3 import PDFDoc, Text, Rect, SDFDoc, ColorPt
from docx2pdf import convert
import fitz
import numpy as np
from PIL import Image
import io
import re

class wordObject():
    def __init__(self, text, size, font, bbox):
        self.text = text
        self.size = size 
        self.font = font 
        self.bbox = bbox
        self.struct = None
        self.note = None
        self.unit = None
        self.check_flags()



    def check_flags(self):
        try:
            vals = ["pH", "bar", "Kg", "Kg/NA", "Date", "hrs"]
            expr = r"\b[a-zA-Z]+[]+|[]+[a-zA-Z\s]+\b|[]+[a-zA-Z]+[\][a-zA-Z]+\b|\b[a-zA-Z]+[\][a-zA-Z]+[]|[_]+[a-zA-z]+\b"
            x = re.findall(expr, self.text)
            if x and x[0] in vals: self.unit = x[0]


            expr=r"\bNote[\s][0-9]"
            x = re.findall(expr, self.text)
            if x: self.note = int(x[0].split(" ")[-1])


            expr = r"\A[0-9][0-9][.][0-9][0-9][.][0-9][0-9]|\A[0-9][0-9][.][0-9][0-9][.][0-9]|\A[0-9][0-9][.][0-9][.][0-9][0-9]|\A[0-9][0-9][.][0-9][.][0-9]|\A[0-9][.][0-9][0-9][.][0-9][0-9]|\A[0-9][.][0-9][0-9][.][0-9]|\A[0-9][.][0-9][.][0-9][0-9]|\A[0-9][.][0-9][.][0-9]|\A[0-9][0-9][.][0-9][0-9]|\A[0-9][0-9][.][0-9]|\A[0-9][.][0-9][0-9]|\A[0-9][.][0-9]|\A[0-9]"
            x = re.findall(expr, self.text)
            if x: self.struct =  [int(i) for i in x[0].split('.')]
        
        except:
            pass

    def __repr__(self):
        return self.text

     

class parseDoc():
    def __init__(self, path):
        self.doc =  fitz.open(path)
        self.volume = len(self.doc) 



    def readPage(self, i):
        if i>=self.volume or i<0:
            print ("The Page Doesn't exist")
            return []
        print ("Page No --", i)

        ThisPage = []
        page = self.doc.loadPage(i)
        pix = page.getPixmap()
        data = pix.getImageData("format")
        blocks = page.getText("dict")["blocks"]

        prevLine = None

        lnum = 0
        for b in blocks:
            if b['type'] == 0:
                for line in b["lines"]:
                    Line = []
                    for s in line['spans']:
                        Line.append(wordObject (s['text'], s['size'],s['font'], s['bbox']))
 

                    ThisPage.append(Line)
        return ThisPage


if __name__ == "__main__":    
    obj = parseDoc('data\\HACKATHON_SAMPLE.pdf')
    print (obj.readPage(0))
    # wo = wordObject("2.3.4 hi jadsdsidn _________bar", "12.0", "XYZ",(12,23,56,25))
    # print (wo.note)
    # print (wo.struct)
    # print (wo.unit)
    