import os
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')
import glob
import shutil
import json
from PIL import Image
import pyocr
import requests
import random
import re

#OCRの環境設定
#pyocr.tesseract.TESSERACT_CMD = r'OCR-PATH'
tools = pyocr.get_available_tools()
tool = tools[0]
screenshot_path = os.environ["SCREENSHOT_PATH"] or ""

#OCR対象の決定
#:TODO スクショしたファイルを指定できるようする
list_of_files = glob.glob(screenshot_path)  # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
#print(latest_file)
img = Image.open(latest_file)

#画像から文字を抽出する
builder = pyocr.builders.TextBuilder(tesseract_layout=6)
text = tool.image_to_string(img, lang="jpn", builder=builder)
# text = text.replace('\"','\\\"')
# text = text.replace('\'',"\\'")
# text = text.replace('&','%26')
# text = text.replace('\\"','\"')
# text = text.replace(" ","")
text = text.replace('\n',' ')
text = text.replace('．','。').replace('，','、')
resultText = text

cnt = len(resultText)
start=0
tao=[]
subtex=text
resultText=resultText.replace("\\'","\'")
resultText=re.sub('([あ-んア-ン一-龥ー])\s+((?=[あ-んア-ン一-龥ー]))',r'\1\2', resultText)#全角に囲まれた半角スペース削除（日本語間の空白の削除）
#print(resultText)
numForTitle=50
startForTitle=0
endend=0
while True:
    cnt-=numForTitle
    if cnt>0:
        endend=numForTitle
        for i in range(numForTitle):
            if i==0:
                endbreak=resultText[startForTitle+endend-1:startForTitle+endend]
                if endbreak == " ":
                    break
            else:
                endbreak=resultText[startForTitle+endend-1:startForTitle+endend]
                if endbreak == " ":
                    break
                endend-=1
        nowForTitle=resultText[startForTitle:startForTitle+endend]
    if start == 0:
        if cnt>0:
            a={"title":nowForTitle,"arg":nowForTitle}
        else:
            a={"title":resultText[startForTitle:],"arg":resultText[startForTitle:]}
    else:
        if cnt>0:
            a={"title":nowForTitle,"arg":nowForTitle}
        else:
            a={"title":resultText[startForTitle:],"arg":resultText[startForTitle:]}
    startForTitle+=endend
    tmpStart=start
    if tmpStart+numForTitle<cnt:
        start=tmpStart+numForTitle
    else:
        start=tmpStart
    tao.append(a)
    if cnt < 0:
        break
sys.stdout.write(json.dumps({'items': tao}, ensure_ascii=False))

#os.remove(latest_file) #完全削除
#shutil.move(latest_file,'/Users/kt/.Trash/') #ごみ箱へ移動する場合