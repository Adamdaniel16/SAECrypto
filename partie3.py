from scapy.all import *
from scapy.layers.inet import UDP
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def aes_decrypt(key, msg):
    pad = padding.PKCS7(128).padder()
    unpad = padding.PKCS7(128).unpadder()
    msg = pad.update(msg) + pad.finalize()
    iv = msg[:16]
    msg = msg[16:]
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).decryptor()
    decrypted_msg = decryptor.update(msg) + decryptor.finalize()
    return unpad.update(decrypted_msg)

def extract_messages_from_capture(capture_path):
    packets = rdpcap(capture_path)

    messages = []

    for packet in packets:
        # Vérifier si le paquet utilise le port 9999 et en UDP
        if packet.haslayer(UDP):
            # Extraire le le message chiffré et le vecteur d'initialisation (IV)
            data = packet[UDP].payload
            messages.append(data.load)

    return messages

# clé depuis la partie avant
key_from_previous_step = "1110011101101101001100010011111110010010101110011001000001001100"
print(len(key_from_previous_step))
cle_bob_alice = key_from_previous_step + key_from_previous_step + key_from_previous_step + key_from_previous_step
# met cle bob alice en binaire (format OB)
print(len(cle_bob_alice))
cle_bob_alice = int(cle_bob_alice, 2)

# le remet en bytes
print(cle_bob_alice)

cle_bob_alice = cle_bob_alice.to_bytes((cle_bob_alice.bit_length() + 7) // 8,'big')
print(cle_bob_alice)
print(" ")


capture_file_path = "partie 2/trace_sae.cap"

# Afficher les messages déchiffrés
for message in (extract_messages_from_capture(capture_file_path)):
    decrypted_message = aes_decrypt(cle_bob_alice, message)
    utf8_decrypted_message = decrypted_message.decode('utf-8', errors='ignore')
    print("Message déchiffré: " + utf8_decrypted_message)
    print("\n")
