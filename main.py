import pathlib
import wget
import os
import pdfminer   #ho usato pdfminer.six che è il fork attivo mantenuto dalla comunità
from pdfminer import high_level

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
print(repr(text))