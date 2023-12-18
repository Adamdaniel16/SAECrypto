import time
from partie1 import chiffrer as chiffrer_sdes
from partie1 import dechiffrer as dechiffrer_sdes
from partie1 import transforme_liste
from partie1 import transforme_msg

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def chiffrer_aes(key, msg_clair):
    msg_clair_bytes = bytes(msg_clair)  # transformer liste d'entiers en objet bytes
    
    # Remplir données si elle n'est pas un multiple de taille
    padding_length = 16-(len(msg_clair_bytes)%16)
    padded_msg_clair = msg_clair_bytes+bytes([padding_length]*padding_length)
    
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_msg_clair)+encryptor.finalize()
    return ciphertext

def dechiffrer_aes(key, msg_chiffre):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_bytes = decryptor.update(msg_chiffre) + decryptor.finalize()

    decrypted_list = [int(byte) for byte in decrypted_bytes]    # transformer liste déchiffrés en une liste d'entiers

    return decrypted_list

if __name__=="__main__":
    with open("textes/arsene_lupin_extrait.txt", "r") as file:
        # msg = file.read()
        msg = "La vie est belle"
        msg_list = transforme_msg(msg)
        k1 = 10
        k2 = 19
        aes_key = b'\x01' * 32
        
        ###########      SDES (partie 1)     ##########
        
        print("\n*** SDES ***")
        start_enc_sdes = time.time()
        cipher = chiffrer_sdes(k1,k2,msg_list)
        duree = time.time() - start_enc_sdes
        # Message crypté
        print(cipher)
        # Durée d'exécution
        print(f"Durée chiffrement SDES: {duree} secondes")
        
        start_dec_sdes = time.time()
        message_trouve = dechiffrer_sdes(k1,k2,cipher)
        duree = time.time() - start_dec_sdes
        # Message décrypté
        print(message_trouve)
        print(message_trouve == msg_list)
        # Durée d'exécution
        print(f"Durée déchiffrement SDES: {duree} secondes")
        
        ##########    AES     ##########
        
        print("\n*** AES ***")
        start_enc_aes = time.time()
        cipher = chiffrer_aes(aes_key,msg_list)
        duree = time.time() - start_enc_aes
        # Message crypté
        print(cipher)
        # Durée d'exécution
        print(f"Durée chiffrement AES: {duree:.5f} secondes")
        
        start_dec_aes = time.time()
        message_trouve = transforme_liste(dechiffrer_aes(aes_key,cipher))
        duree = time.time() - start_dec_aes
        # Message décrypté
        print(message_trouve)
        # Durée d'exécution
        print(f"Durée déchiffrement AES: {duree} secondes")
        