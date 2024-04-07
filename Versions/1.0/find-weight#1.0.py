import re
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import webbrowser

version = "1.0"
url_entry = None

def validate_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def extract_weights_with_context(text, target_units):
    pattern = re.compile(r"\b(\d+,\d+|\d+(\.\d+)?)(?:\s*(kg|lbs|g))\b", re.IGNORECASE)
    matches = pattern.finditer(text)

    weights_with_context = []
    if matches:
        lines = text.splitlines()

        for match in matches:
            weight_value = match.group(1)
            weight_unit = match.group(3)

            if weight_unit.lower() not in target_units:
                continue

            start_pos = match.start()
            line_number = sum(1 for _ in text[:start_pos].split('\n'))
            context_line = lines[line_number - 1].strip() if line_number > 0 else ""

            weight_string = f"{weight_value} {weight_unit} ({context_line})"
            weights_with_context.append(weight_string)

    return weights_with_context if weights_with_context else None

def detect_and_print_weights():
    global url_entry
    url = url_entry.get().strip()

    if not validate_url(url):
        messagebox.showerror("URL invalide", "Veuillez saisir une URL valide.")
        return

    target_units = ["kg", "lbs", "g"]  # Unités de poids à rechercher
    try:
        with requests.get(url) as response:
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()

            weights_with_context = extract_weights_with_context(text, target_units)

            if weights_with_context:
                result_message = "\n".join(weights_with_context)
                messagebox.showinfo("Poids trouvés sur la page", result_message)
                show_signature_and_version()
            else:
                messagebox.showinfo("Aucun poids trouvé", "Aucun poids ('kg', 'lbs' ou 'g') n'a été trouvé sur la page.")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erreur de requête", f"Erreur lors de la requête HTTP : {e}")

def show_signature_and_version():
    signature = "Programme développé par Eliott Exe"
    link = "https://eliottxexe.github.io/Linktree/"

    popup = tk.Toplevel()
    popup.title("Informations")

    info_label = tk.Label(popup, text=f"{signature}\nVersion du programme : {version}", padx=20, pady=20)
    info_label.pack()

    def open_link():
        webbrowser.open(link)

    link_label = tk.Label(popup, text="Visitez mon lien", fg="blue", cursor="hand2")
    link_label.pack(pady=10)
    link_label.bind("<Button-1>", lambda event: open_link())

def main():
    global url_entry
    root = tk.Tk()
    root.title("Détection de poids sur les pages web")

    url_label = tk.Label(root, text="URL de la page web :")
    url_label.pack(pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    detect_button = tk.Button(root, text="Détecter les poids", command=detect_and_print_weights)
    detect_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
