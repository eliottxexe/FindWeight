import re
import requests
from bs4 import BeautifulSoup

version = "Beta"

print(f"FindWeight {version}")
print("\n")

def extract_weights_with_context(text):
    # Liste des caractères non acceptés dans l'unité de poids
    invalid_chars = {'G'}  # Ajoutez d'autres caractères non acceptés si nécessaire

    # Utiliser une expression régulière pour trouver tous les poids (nombre suivi d'une seule occurrence de "kg", "lbs" ou "g")
    pattern = re.compile(r"\b(\d+,\d+|\d+(\.\d+)?)(?:\s*(kg|lbs|g))\b", re.IGNORECASE)
    matches = pattern.finditer(text)

    weights_with_context = []
    if matches:
        lines = text.splitlines()  # Séparer le texte en lignes

        for match in matches:
            weight_value = match.group(1)  # Récupérer la valeur du poids
            weight_unit = match.group(3)  # Récupérer l'unité de poids

            # Vérifier si l'unité de poids contient un caractère non accepté
            if any(char in weight_unit for char in invalid_chars):
                continue  # Ignorer ce poids

            # Si l'unité est valide (pas de caractère non accepté), ajouter le poids avec le contexte
            start_pos = match.start()  # Position de début du match
            end_pos = match.end()  # Position de fin du match

            # Trouver la ligne où se trouve le poids
            line_number = sum(
                1 for _ in text[:start_pos].split('\n'))  # Numéro de ligne (basé sur le nombre de '\n' avant le match)
            context_line = lines[line_number - 1].strip() if line_number > 0 else ""  # Ligne de contexte

            # Formater le poids comme une chaîne avec l'unité et la ligne de contexte entre parenthèses
            weight_string = f"{weight_value} {weight_unit} ({context_line})"
            weights_with_context.append(weight_string)

    return weights_with_context if weights_with_context else None


def detect_and_print_weights(url):
    # Faire une requête GET pour obtenir le contenu de la page web
    try:
        with requests.get(url) as response:
            response.raise_for_status()  # Lève une exception en cas d'erreur HTTP

            # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Obtenir le texte de la page
            text = soup.get_text()

            # Extraire tous les poids avec leur contexte
            weights_with_context = extract_weights_with_context(text)

            if weights_with_context:
                print("Les poids trouvés sur la page sont :")
                for weight_info in weights_with_context:
                    print(weight_info)
            else:
                print("Aucun poids ('kg', 'lbs' ou 'g') n'a été trouvé sur la page.")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")

    # Sauter une ligne
    print("\n")

    print(f"Version du programme: {version}")

    # Sauter une ligne
    print("\n")

    # Signature et lien
    signature = "Programme développé par Eliott Exe"
    link = "https://eliottxexe.github.io/Linktree/"
    print(signature)
    print(f"Visitez mon Linktree : {link}")


# URL de la page web à analyser
url = "https://www.videoplusfrance.com/fr/103258-tamron-70-200mm-f-28-sp-di-vc-usd-g2-monture-canon.html"

# Appeler la fonction pour détecter et imprimer les poids avec leur contexte sur la page web
detect_and_print_weights(url)
