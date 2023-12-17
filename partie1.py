from SDES import *

# double chiffrement d'une message clair avec 2 clés k1 et k2
def chiffrer(k1, k2, message_clair):
    res = []
    for b in message_clair:
        res.append(encrypt(k1,encrypt(k2,b)))
    return res

# double déchiffrement avec 2 clés k1 et k2
def dechiffrer(k1,k2,cipher):
    msg = []
    for b in cipher:
        msg.append(decrypt(k2,decrypt(k1,b)))
    return msg

# découpe un message clair en une liste de 8 bits (pour le chiffrement)
def transforme_msg(message_clair):
    res = []
    for c in message_clair:
        res.append(ord(c))
    return res

# transformer une liste de 8 bits en un message clair
def transforme_liste(message_chiffre):
    res = []
    for c in message_chiffre:
        res.append(chr(c))
    return "".join(res)

with open("textes/arsene_lupin_extrait.txt", "r") as f:
    cle1 = 0b110100001
    cle2 = 0b011011010
    msg = f.read()
    cipher = chiffrer(cle1, cle2, transforme_msg(msg))
    print(cipher)
    msg_clair = transforme_liste(dechiffrer(cle1, cle2, cipher))
    print(msg_clair)
    print(msg_clair == msg)

def cassage_brutal(message_clair, message_chiffre):
    pass

def cassage_astucieux(message_chiffre): #On peut ajouter des paramètres
    pass