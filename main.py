import pathlib
import wget
import os
import pdfminer   #ho usato pdfminer.six che è il fork attivo mantenuto dalla comunità
from pdfminer import high_level
import re

i = 0
merda = 0
casella = []
provincie = ["BO","FE","FC","MO","PR","PC","RA","RE","RN"]
start_of_days = []
righe_provincie =[]
url = "https://www.poliziadistato.it/statics/09/emilia.pdf" #piccolo problema sembra che l'url cambi ogni settimana e per adesso lìho lasciato hardcoded
download_location = str(pathlib.Path().absolute()) + "\\"+"emilia.pdf"
print("The download location is " + download_location)
if os.path.exists(download_location):
  os.remove("emilia.pdf")                                   #così magari ci evitiamo qualche file inutile, non lo so magari se poi lo mettiamo alla fine per fare della pulizia ma così se crashiamo a metà siamo tranquilli
  print("removed old file")
wget.download(url,download_location)
print("new file downloaded")
print("now parsing pdf file")
#questo dovrebbe essere il modo più brutale di estrarre il testo dal pdf
text = pdfminer.high_level.extract_text(download_location)
print("pdf parsed")
#print(repr(text))
cells = text.split("\n")
print("modified text =>")
for elements in cells:
  # ok il check a seguire sarebbe da mettere un po' a posto era partito tranquillo ma  degradato velocemente
  if elements == "" or elements == "/" or elements == " " or elements == "Emilia Romagna" or elements=="Emilia Romagna" or elements=="Fonte: Polizia di Stato – Servizio Polizia Stradale " or elements == "Validità  da" or elements == "a" or elements == "Provincia" or elements == "Giorno" or elements == "Tratto stradale" or elements =="Strada Statale" or elements =="Strada Provinciale" or elements=="Strada Comunale" or elements=="Autostrada":
    merda+=1
  else:
    casella.append(elements)                            #un po' di ripulisti generale
    x = re.search("([0-9]{2}\/[0-9]{2}\/[0-9]{4})", elements)
    if (x):
      start_of_days.append(i)                           #lista degli indici di riga delle caselle contenti il giorno del controllo
    for a in provincie:
      if elements == a:
        righe_provincie.append(i)                       #lista degli indici di riga delle caselle conteneti le provincie delle strade dei controlli
    i+=1

for a in casella:
  print(a)

for a in start_of_days:
  print("start_of_days")
  print(a)

for a in righe_provincie:
  print("righe_provincie")
  print(a)