import random
import smtplib
import ssl
import json
import time
import requests

configFile = "configPerso.json"

with open(configFile) as json_file:
	config = json.load(json_file)

spoil = config["spoiler"]
if not spoil:
	mail = config["mail"]
	password = config["password"]
smtp_adress = config["smtp"]
smtp_port = config["port"]

textMail = config["textMail"]

participants = list(config["mailList"].keys())
mails = config["mailList"]

longer = "\_"

try:
	couples = config["couples"]
except KeyError:
	couples = []

try:
	old = config["old"]
except KeyError:
	old = []

try:
	webhook = config["webhook"]
except KeyError:
	webhook = False


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
		if key == value:
			return False
	return True


def reverseOk(cadeauxL):
	for key, value in cadeauxL.items():
		if cadeauxL[value] == key:
			return False
	return True


def oldOk(cadeauxL):
	for key, value in cadeauxL.items():
		if key in old.keys():
			if cadeauxL[key] == old[key]:
				return False
	return True


def affiche(cadeauxL):
	for key, value in cadeauxL.items():
		print("{:>6} -> {}".format(key, cadeauxL[value]))


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
		affiche(cadeauxL)
		print()
		affiche2(cadeauxL)
	else:
		sendMails(cadeauxL)
	if webhook:
		for gifter, giftee in cadeauxL.items():
			sendWebhook(gifter, giftee)


def getMails(cadeauxL):
	for i in list(cadeauxL.keys()):
		print(i + " " + mails[i])
	print()


context = ssl.create_default_context()


def sendWebhook(gifter, giftee):
	return requests.post(
		webhook,
		json={"content": "",
			  "embeds": [
				  {"title": f"🎁 {gifter} gift 🎁",
				   "description": f"||`{giftee:<20}`||\nClick only if you're {gifter}",
				   "color": 14948291
				   }
			  ]}
	)


def sendMails(cadeauxL):
	with smtplib.SMTP_SSL(smtp_adress, smtp_port, context=context) as server:
		server.login(mail, password)
		for gifter in list(cadeauxL.keys()):
			server.sendmail(mail, mails[gifter], textMail.format(cadeauxL[gifter], gifter).encode("utf8"))

			time.sleep(1)


genF(spoil)
