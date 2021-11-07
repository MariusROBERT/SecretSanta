#Secret Santa

---
###What is Secret Santa?

Secret santa is a fun and easy way to get together with your friends and/or family with a gift for them.

The idea is to have a list of friends and/or family members and then randomly select a person to get a gift for.

---

###How to use this Secret Santa?

- Copy the `configExample.json` file and rename it `config.json` then add the partipant's names : you have to add the name of the person and his email address like in the example.
- You can edit the `textMail` value in the `config.json` file to change the text of the email sent to the person (`{0}` represent the person to whom you will gift and `{1}` represent your name).
- You can add couples if you want to avoid couples gifting their partner (leave it empty if you don't have couples or don't care if they can gift each other), the names in the couple must be exactly the same as the name of the persons.
- If you want to see the draw, set spoiler to `true` in the `config.json` file (not recommanded if you participate), else it will be sent by email.
- If `spoiler` is set to false, the draw will be sent by email, so you have to add your email address (and password) in the `config.json` file, the example is made for gmail addresses, but you can configure if for another service. If you use a gmail adresse, you will have to go on https://myaccount.google.com/lesssecureapps and enable the use of less secure apps.

---

###Rules
There are 3 rules defined in this code:
- You can't gift yourself (or this will be a sad Christmas)
- You can't gift your partner if you are in a registred couple in config.json
- You can't gift back the person who gifted you

