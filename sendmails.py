#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gmailAPI as gmail

#Le fichier .csv où se trouvent les numéros (no) des étudiants et leurs mails (email)
#Il doit y figurer une colonne "no" et une "email"
codes = "/path/to/the/file/codes.csv"

#Le dossier dans lequel se trouvent les corrections
#Attention, les pdf doivent commencer par le numéro des étudiants suivi d'un point
scans_directory = "/path/to/the/project/cr/corrections/pdf"

#Le séparateur utilisé dans le fichier .csv
sep = ":"

#Le nom de l'expéditeur du mail et son adresse (ça passe par gmail mais vous pouvez mettre autre chose)
sender = "Your mail <your@mail>"

#Le corps du message
message_text = 'Bonjour,\n\n'
message_text += 'En pièce jointe de ce message se trouve la correction '
message_text += 'de votre QCM. Quelques indications pour la lire :\n'
message_text += '- la note est indiquée (sur 10) en haut à gauche\n'
message_text += '- les réponses entourées en rouge sont des réponses qui ont été cochées et qui sont fausses\n'
message_text += '- les réponses entourées en bleu sont des réponses qui ont été cochées et qui sont justes\n'
message_text += "- les réponses cochées en rouge sont des bonnes réponses qui n'ont pas été cochées\n\n"
message_text += "En cas de doute, où si vous pensez que votre copie a mal été scannée, n'hésitez pas à me contacter.\n\n"
message_text += "Cordialement,\n\n"


#En dessous de cette ligne, rien à modifier.
def readCodes(codes,sep):
    """Va chercher le fichier csv et créé une liste de dictionnaires.
       Chaque dictionnaire correspond à un étudiant avec toutes les
       informations données sur la première ligne du csv
    """
    f = open(codes,"r")
    plop = []
    k = 0
    for etudiant in f.readlines():
        etudiant = etudiant[:-1].split(sep) #on découpe la ligne du fichier csv
        if k==0:
            indices = etudiant  #on repère les noms des colonnes
            k = 1
        else:
            plop.append({}) #on créé un dictionnaire par étudiant
            for j in range(len(etudiant)):
                plop[-1][indices[j]] = etudiant[j]
    return plop

def sendMails(sender, scans_directory, codes, message_text):
    """Envoie les corrections des QCM aux étudiants"""
    liste_codes = readCodes(codes, sep)
    for f in os.listdir(scans_directory):
        code_corr = f.split('.')[0]
        for etudiant in liste_codes:
            if etudiant['no'] == code_corr:
                sendCorrection(sender, scans_directory, f, etudiant['email'], message_text)
                break
    
def sendCorrection(sender, file_dir, filename, email, message_text):
    """Envoie la correction à un étudiant en particulier"""
    to = email
    subject = "Correction QCM"
    message = gmail.CreateMessageWithAttachment(sender, to, subject, message_text, file_dir, filename)
    gmail.AuthenticateAndSendMessage(message)



if __name__ == '__main__':
    print("Attention, vous êtes sur le point d'envoyer les corrections des QCM. Pour info:")
    print("Répertoire : " + scans_directory)
    print("Lise des étudiants : " + codes)
    a = raw_input("Souhaitez-vous continuer ? (o/n) ")
    if a=='o':
        print("Envoie en cours...")
        sendMails(sender, scans_directory, codes, message_text)
    else:
        print("Envoie annulé")
