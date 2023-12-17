

def cassage_brutal(message_chiffre, taille_cle1, taille_cle2):
    res = []
    for i in range(2**min(taille_cle1, taille_cle2)):
        res.append(message_chiffre**i)%min(taille_cle1, taille_cle2)
    return res


def cassage_astucieux(message_chiffre): #On peut ajouter des paramètres
    ...