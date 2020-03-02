import pathlib
import wget
import os
import pdfminer
from pdfminer import high_level
import re
from datetime import date
import telegram         #pip install python-telegram-bot


#url = "https://www.poliziadistato.it/statics/09/emilia.pdf"
url = "https://www.poliziadistato.it/statics/21/emilia.pdf"
download_location = str(pathlib.Path().absolute()) + "/"+"emilia.pdf"

# Lista dei dati da inviare per email
data = []
# Indici dell'inizio dei giorni in data
idx_date_data = []
# Istanza di un bot telegram
bot = telegram.Bot(token='1043680925:AAE7Aw-sPROkm1e98eC9uABeTKjpengI_Ks')
#Lista di id chat a cui inviare i messaggi
Lista_chat = [220000708,415720988]

def pdf_fetch():
    """
    Pdf fetch
    :return: none
    """
    print("The download location is " + download_location)
    if os.path.exists(download_location):
        os.remove("emilia.pdf")
        print("removed old file")
    wget.download(url, download_location)
    print("new file downloaded")


def pdf_parser():
    """
    Pdf parser
    :return: none
    """
    i = 0
    skip = 0
    casella = []
    province = ["BO", "FE", "FC", "MO", "PR", "PC", "RA", "RE", "RN"]
    start_of_days = []
    end_of_days = []
    righe_province = []

    print("now parsing pdf file")
    text = pdfminer.high_level.extract_text(download_location)
    print("pdf parsed")
    cells = text.split("\n")
    print("modified text =>")
    for elements in cells:
        if elements == "" or elements == "/" or elements == " " or elements == "Emilia Romagna" \
                or elements == "Fonte: Polizia di Stato – Servizio Polizia Stradale " \
                or elements == "Validità  da" or elements == "a" or elements == "Provincia" or elements == "Giorno" \
                or elements == "Tratto stradale" or elements == "Strada Statale" or elements == "Strada Provinciale" \
                or elements == "Strada Comunale" or elements == "Autostrada":
            skip += 1
        else:
            casella.append(elements)
            i += 1

    i = 0
    for a in casella:
        print(a + "   index: " + str(i))
        x = re.search(r"([0-9]{2}/[0-9]{2}/[0-9]{4})", a)
        if x:
            # lista degli indici di riga delle caselle contenenti il giorno del controllo
            start_of_days.append(i)
            print("^ Its a day")
        for b in province:
            if a == b:
                # lista degli indici di riga delle caselle contenenti le province delle strade dei controlli
                righe_province.append(i)
                print("^ Its a provincia")
        i += 1

    for days in start_of_days:
        print("start_of_days")
        print(days)

    for prov in righe_province:
        print("righe_province")
        print(prov)

    for idx, days in enumerate(start_of_days):
        e = days+1

        while True:
            if casella[e] in province or re.search(r"([0-9]{2}/[0-9]{2}/[0-9]{4})", casella[e]):
                break
            e += 1
        end_of_days.append(e)

    for days in end_of_days:
        print("end of days" + str(days))

    indice_provincia = 0
    for idx, days in enumerate(start_of_days):
        print("Giornata n°" + str(idx+1))
        if idx < 7:
            for idx2 in range(days, end_of_days[idx]):
                if casella[idx2] not in province:
                    if not re.search(r"([0-9]{2}/[0-9]{2}/[0-9]{4})", casella[idx2]):
                        data.append(casella[idx2] + " " + casella[righe_province[indice_provincia]])
                        indice_provincia += 1
                    else:
                        idx_date_data.append(len(data))
                        data.append(casella[idx2])
                    print(casella[idx2])


def send_alert():
    """
        Send an email alert
        :return: none
        """
    print("---IT'S ALERT TIME---")
    for id in Lista_chat:
        bot.send_message(id, "---IT'S ALERT TIME---")
    idx_controllo = -1
    for indice in idx_date_data:
        if data[indice] == date.today().strftime("%d/%m/%Y"):
            idx_controllo = indice

    if idx_controllo == -1: # Non abbiamo dati per la giornata di oggi
        return

    # Stampa i controlli di oggi (da inviare via mail)
    while True:
        print(data[idx_controllo])
        for id in Lista_chat:
            bot.send_message(id, data[idx_controllo])
        idx_controllo += 1
        if idx_controllo == len(data) or re.search(r"([0-9]{2}/[0-9]{2}/[0-9]{4})", data[idx_controllo]):
            break


"""""""""""
MAIN BLOCK
"""""""""""

pdf_fetch()
pdf_parser()
send_alert()
