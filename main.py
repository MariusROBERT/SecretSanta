import random
import smtplib
import ssl
import json

configFile = "config.json"

#import config from configPerso.json
with open(configFile) as json_file:
    config = json.load(json_file)

spoil = config["spoiler"]
if not spoil:
    mail = config["mail"]
    password = config["password"]
smtp_adress = config["smtp"]
smtp_port = config["port"]

textMail = config["textMail"]

participants = list(config["participants"].keys())
mails = config["mails"]

try:
    couples = config["couples"]
except KeyError:
    couples = []



def gen(cadeauxL):
    participants2 = [x for x in participants]
    for i in participants:
        p2 = random.choice(participants2)
        cadeauxL[i] = p2
        participants2.remove(p2)
    return cadeauxL


def coupleOk(cadeauxL):
    for i in couples:
        if cadeauxL[i[0]] == i[1] or cadeauxL[i[1]] == i[0]:
            return False

    return True


def soloOk(cadeauxL):
    for key, value in cadeauxL.items():
        #print(i)
        if key == value:
            return False

    return True


def reverseOk(cadeauxL):
    #cadeauxL2 = dict()
    for key, value in cadeauxL.items():
        #cadeauxL2[value] = key
        if cadeauxL[value] == value:
            return False

    return True


def affiche(cadeauxL):
    for key, value in cadeauxL.items():
        print(key + " -> " + value)


def affiche2(cadeauxL):
    first = random.choice(list(cadeauxL.keys()))
    for i in range(len(cadeauxL)):
        print("{:>6} -> {}".format(first, cadeauxL[first]))
        first = cadeauxL[first]


def genF(spoiler):
    cadeauxL = gen(dict())
    while not (coupleOk(cadeauxL) and soloOk(cadeauxL) and reverseOk(cadeauxL)):
        cadeauxL = gen(cadeauxL)
    if spoiler:
        affiche2(cadeauxL)
    else:
        sendMails(cadeauxL)


def getMails(cadeauxL):
    for i in list(cadeauxL.keys()):
        print(i + " " + mails[i])
    print()


context = ssl.create_default_context()


def sendMails(cadeauxL):
    with smtplib.SMTP_SSL(smtp_adress,smtp_port, context=context) as server:
        server.login(mail, password)
        for i in list(cadeauxL.keys()):
            server.sendmail(mail, mails[i], textMail.format(cadeauxL[i], i).encode("utf8"))

genF(spoil)

# for i in range(5):
#     genF()
#     print()
