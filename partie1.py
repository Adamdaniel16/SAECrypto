from SDES import *
import time

# double chiffrement d'une message clair avec 2 clés k1 et k2
def chiffrer(k1, k2, message_clair):
    res = []
    for b in message_clair:
        res.append(encrypt(k1,encrypt(k2,b)))
    return res

# double déchiffrement avec 2 clés k1 et k2
def dechiffrer(k1,k2,message_chiffre):
    msg = []
    for b in message_chiffre:
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

# les tests pour double chiffrement et déchiffrement
with open("textes/arsene_lupin_extrait.txt", "r") as f:
    cle1 = 0b110100001
    cle2 = 0b011011010
    msg = f.read()
    cipher = chiffrer(cle1, cle2, transforme_msg(msg))
    # print(cipher)
    msg_clair = transforme_liste(dechiffrer(cle1, cle2, cipher))
    # print(msg_clair)
    print(msg_clair == msg)

# retrouver les clés de chiffrement (toutes les possibilités)
def cassage_brutal(message_clair, message_chiffre):
    nb_tentatives = 0
    for c1 in range(2**10):
        for c2 in range(2**10):
            nb_tentatives += 1
            if chiffrer(c1, c2, message_clair) == message_chiffre:
                return (c1,c2,nb_tentatives)
    return None

# chiffrement simple d'une message clair avec une clé k1
def chiffrer_simple(k1, message_clair):
    res = []
    for b in message_clair:
        res.append(encrypt(k1,b))
    return res

# déchiffrement simple d'une message chiffré avec une clé k1
def dechiffrer_simple(k1, message_chiffre):
    res = []
    for b in message_chiffre:
        res.append(decrypt(k1,b))
    return res

# retrouver les clés de chiffrement (moins de possibilité de clés)
def cassage_astucieux(message_clair, message_chiffre):
    nb_tentatives = 0
    dec = []
    enc = []
    for cle in range(2**10):
        nb_tentatives += 1
        chi = chiffrer_simple(cle, message_clair)
        dechi = dechiffrer_simple(cle, message_chiffre)
        dec.append(dechi)
        enc.append(chi)
        if chi in dec:
            return (dec.index(chi), enc.index(chi), nb_tentatives)
        elif dechi in enc:
            return (dec.index(dechi), enc.index(dechi), nb_tentatives)
    return None

# les tests pour les fonctions pour retrouver les clés (cassage)
with open("textes/arsene_lupin_extrait.txt", "r") as f:
    # msg = f.read()
    msg = "La vie est belle"
    msg_list = transforme_msg(msg)
    k1 = 10
    k2 = 19
    cipher = chiffrer(k1, k2, msg_list)
    
    # cassage brutal (Brute-Force Attack)
    print("\nCassage Brutal:")
    start = time.time()
    brute_force = cassage_brutal(msg_list, cipher)
    duree = time.time()-start
    nbt = brute_force[2]
    print((brute_force[0], brute_force[1]) == (k1,k2))
    print(brute_force)
    print(f"Durée: {duree:.5f} secondes")
    print(f"Nombre de tentatives: {nbt} fois\n")
    
    # cassage astucieux
    print("Cassage Astucieux:")
    start = time.time()
    astucieux = cassage_astucieux(msg_list, cipher)
    duree = time.time()-start
    nbt = astucieux[2]
    print((astucieux[0], astucieux[1]) == (k1,k2))
    print(astucieux)
    print(f"Durée: {duree:.5f} secondes")
    print(f"Nombre de tentatives: {nbt} fois\n")