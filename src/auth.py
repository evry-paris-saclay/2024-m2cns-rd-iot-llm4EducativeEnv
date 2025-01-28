import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk


def open_etudiant_interface():
    """Ouvrir l'interface Étudiant."""
    try:
        subprocess.run(["python", "etudiant.py"], check=True)
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec lors de l'ouverture de l'interface Étudiant : {e}")


def open_prof_interface():
    """Ouvrir la fenêtre d'authentification pour le professeur."""
    auth_window = tk.Toplevel(root)
    auth_window.title("Authentification Professeur")
    center_window(auth_window, 400, 200)

    tk.Label(auth_window, text="Nom :", font=("Arial", 12)).pack(pady=5)
    name_entry = tk.Entry(auth_window, font=("Arial", 12))
    name_entry.pack(pady=5)

    tk.Label(auth_window, text="Code secret :", font=("Arial", 12)).pack(pady=5)
    code_entry = tk.Entry(auth_window, show="*", font=("Arial", 12))
    code_entry.pack(pady=5)

    def authenticate():
        """Vérifier les informations et ouvrir l'interface professeur si correct."""
        name = name_entry.get()
        code = code_entry.get()

        if code == "prof1234":
            auth_window.destroy()
            try:
                subprocess.run(["python", "prof.py"], check=True)
            except Exception as e:
                messagebox.showerror("Erreur", f"Échec lors de l'ouverture de l'interface Professeur : {e}")
        else:
            messagebox.showerror("Erreur", "Code secret incorrect. Veuillez réessayer.")

    tk.Button(auth_window, text="Valider", command=authenticate, font=("Arial", 12)).pack(pady=10)


def center_window(window, width, height):
    """Centrer la fenêtre sur l'écran."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# Fenêtre principale
root = tk.Tk()
root.title("Authentification")
center_window(root, 500, 300)

# Chargement des icônes
try:
    etudiant_icon = ImageTk.PhotoImage(Image.open("eleve.png").resize((80, 80)))
    prof_icon = ImageTk.PhotoImage(Image.open("prof.png").resize((80, 80)))
except Exception as e:
    etudiant_icon = prof_icon = None

# Titre principal
title_label = tk.Label(root, text="Bienvenue !", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# Boutons Étudiant et Professeur
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

button_etudiant = tk.Button(
    button_frame, text="Étudiant", image=etudiant_icon, compound=tk.TOP,
    command=open_etudiant_interface, width=120, height=120, bd=0, font=("Arial", 12)
)
button_etudiant.grid(row=0, column=0, padx=40)

button_prof = tk.Button(
    button_frame, text="Professeur", image=prof_icon, compound=tk.TOP,
    command=open_prof_interface, width=120, height=120, bd=0, font=("Arial", 12)
)
button_prof.grid(row=0, column=1, padx=40)

root.mainloop()