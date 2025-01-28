import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime
from tkinter import simpledialog


def run_script(script_name):
    """Lancer un script Python."""
    try:
        subprocess.run(["python", script_name], check=True)
        messagebox.showinfo("Succès", f"Le script {script_name} a été exécuté avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec lors de l'exécution de {script_name} : {e}")


def open_verif_interface():
    """Ouvrir l'interface de verif.py."""
    verif_root = tk.Toplevel(root)
    verif_root.title("Interface pour Verif.py")
    center_window(verif_root, 700, 400)

    def get_files():
        """Lister les fichiers Excel disponibles dans le répertoire."""
        files = [file for file in os.listdir(".") if file.endswith(".xlsx")]
        if not files:
            messagebox.showerror("Erreur", "Aucun fichier Excel trouvé dans le répertoire.")
        return files

    def select_file():
        """Afficher la liste des fichiers disponibles."""
        files = get_files()
        if not files:
            return

        file_window = tk.Toplevel(verif_root)
        file_window.title("Sélectionnez un fichier Excel")

        label = tk.Label(file_window, text="Fichiers disponibles :", font=("Arial", 12))
        label.pack(pady=10)

        file_list = tk.Listbox(file_window, width=50)
        file_list.pack(padx=10, pady=10)

        for f in files:
            file_list.insert(tk.END, f)

        def confirm_file():
            selected_file = file_list.get(tk.ACTIVE)
            if not selected_file:
                messagebox.showerror("Erreur", "Veuillez sélectionner un fichier.")
                return
            selected_file_label.config(text=f"Fichier sélectionné : {selected_file}")
            file_window.destroy()
            load_sheets(selected_file)

        confirm_button = tk.Button(file_window, text="Confirmer", command=confirm_file, font=("Arial", 12), bd=0)
        confirm_button.pack(pady=10)

    def load_sheets(filename):
        """Afficher la liste des feuilles disponibles dans le fichier Excel sélectionné."""
        try:
            sheet_names = pd.ExcelFile(filename).sheet_names
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")
            return

        sheet_window = tk.Toplevel(verif_root)
        sheet_window.title("Sélectionnez une feuille")

        label = tk.Label(sheet_window, text="Feuilles disponibles :", font=("Arial", 12))
        label.pack(pady=10)

        sheet_list = tk.Listbox(sheet_window, width=50)
        sheet_list.pack(padx=10, pady=10)

        for sheet in sheet_names:
            sheet_list.insert(tk.END, sheet)

        def confirm_sheet():
            selected_sheet = sheet_list.get(tk.ACTIVE)
            if not selected_sheet:
                messagebox.showerror("Erreur", "Veuillez sélectionner une feuille.")
                return
            selected_sheet_label.config(text=f"Feuille sélectionnée : {selected_sheet}")
            sheet_window.destroy()
            run_verif_script(filename, selected_sheet)

        confirm_button = tk.Button(sheet_window, text="Confirmer", command=confirm_sheet, font=("Arial", 12), bd=0)
        confirm_button.pack(pady=10)

    def run_verif_script(filename, sheet_name):
        """Exécuter verif.py avec le fichier et la feuille sélectionnés."""
        try:
            subprocess.run(
                ["python", "verif.py"],
                input=f"{filename}\n{sheet_name}\n",
                text=True,
                check=True,
            )
            messagebox.showinfo(
                "Succès",
                f"Le script verif.py a été exécuté avec succès pour le fichier {filename} et la feuille {sheet_name}.",
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec lors de l'exécution de verif.py : {e}")

    selected_file_label = tk.Label(verif_root, text="Aucun fichier sélectionné.", font=("Arial", 12))
    selected_file_label.pack(pady=10)

    selected_sheet_label = tk.Label(verif_root, text="Aucune feuille sélectionnée.", font=("Arial", 12))
    selected_sheet_label.pack(pady=10)

    select_file_button = tk.Button(
        verif_root,
        text="Sélectionner un fichier",
        command=select_file,
        font=("Arial", 12),
        bd=0,
    )
    select_file_button.pack(pady=10)


def transform_excel_to_csv():
    """Transformer un fichier Excel en CSV et gérer les conflits de noms."""
    # Fenêtre pour choisir un fichier Excel
    file_path = filedialog.askopenfilename(
        title="Sélectionnez un fichier Excel",
        filetypes=[("Fichiers Excel", "*.xlsx")]
    )
    if not file_path:
        messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
        return

    try:
        # Lire le fichier Excel
        quiz_data_excel = pd.read_excel(file_path)

        # Renommer les colonnes pour correspondre au format attendu
        quiz_data_excel.rename(columns={
            "Option A": "Choice 1",
            "Option B": "Choice 2",
            "Option C": "Choice 3",
            "Option D": "Choice 4",
            "Réponse correcte": "Correct Answer"
        }, inplace=True)

        # Définir le chemin de sortie par défaut
        output_csv_path = "quiz_questions.csv"

        # Vérifier si le fichier quiz_questions.csv existe déjà
        if os.path.exists(output_csv_path):
            # Demander un nom personnalisé à l'utilisateur
            new_name = simpledialog.askstring(
                "Nom personnalisé",
                "Entrez un nom pour sauvegarder l'ancien fichier (sans extension) :"
            )
            if not new_name:
                messagebox.showerror("Erreur", "Nom invalide. Opération annulée.")
                return

            # Ajouter un timestamp pour différencier les fichiers
            date_suffix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_file_name = f"quiz_questions_{new_name}_{date_suffix}.csv"

            # Renommer le fichier existant
            os.rename(output_csv_path, new_file_name)
            messagebox.showinfo("Info", f"Le fichier existant a été renommé : {new_file_name}")

        # Sauvegarder le nouveau fichier CSV
        quiz_data_excel.to_csv(output_csv_path, index=False, encoding="utf-8")
        messagebox.showinfo("Succès", f"Le fichier CSV a été généré avec succès : {output_csv_path}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue lors de la transformation : {e}")


def open_file_explorer_graphs():
    """Explorer les graphes (fichiers PNG)."""
    explorer_root = tk.Toplevel(root)
    explorer_root.title("Explorer les graphes")
    center_window(explorer_root, 600, 400)

    def list_png_files():
        """Lister les fichiers PNG."""
        file_list.delete(0, tk.END)
        try:
            png_files = [f for f in os.listdir(".") if f.startswith("graphe") and f.endswith(".png")]
            if not png_files:
                messagebox.showinfo("Info", "Aucun fichier PNG trouvé.")
            for file in png_files:
                file_list.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de lister les fichiers PNG : {e}")

    def open_selected_file(event=None):
        """Ouvrir le fichier PNG sélectionné."""
        selected_file = file_list.get(tk.ACTIVE)
        if not selected_file:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier.")
            return
        try:
            img = Image.open(selected_file)
            img.show()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier PNG : {e}")

    file_list = tk.Listbox(explorer_root, width=70, height=20)
    file_list.pack()
    file_list.bind("<Double-Button-1>", open_selected_file)
    list_png_files()


def open_file_explorer_prompt():
    """Explorer fichiers 'prompt'."""
    explorer_root = tk.Toplevel(root)
    explorer_root.title("Explorer fichiers 'prompt'")
    center_window(explorer_root, 600, 400)

    def list_prompt_files():
        """Lister les fichiers contenant 'prompt'."""
        file_list.delete(0, tk.END)
        try:
            prompt_files = [f for f in os.listdir(".") if "prompt" in f and f.endswith(".txt")]
            if not prompt_files:
                messagebox.showinfo("Info", "Aucun fichier 'prompt' trouvé.")
            for file in prompt_files:
                file_list.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de lister les fichiers 'prompt' : {e}")

    def open_selected_file(event=None):
        """Ouvrir le fichier texte sélectionné."""
        selected_file = file_list.get(tk.ACTIVE)
        if not selected_file:
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier.")
            return
        try:
            with open(selected_file, "r", encoding="utf-8") as file:
                content = file.read()
            content_window = tk.Toplevel(explorer_root)
            content_window.title(f"Contenu de {selected_file}")
            text_widget = tk.Text(content_window, wrap=tk.WORD)
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(expand=True, fill=tk.BOTH)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")

    file_list = tk.Listbox(explorer_root, width=70, height=20)
    file_list.pack()
    file_list.bind("<Double-Button-1>", open_selected_file)
    list_prompt_files()


def center_window(window, width, height):
    """Centrer la fenêtre."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# Fenêtre principale
root = tk.Tk()
root.title("Interface professeur")
center_window(root, 900, 500)

try:
    verif_icon = ImageTk.PhotoImage(Image.open("gradiant.png").resize((80, 80)))
    transfo_icon = ImageTk.PhotoImage(Image.open("transfo.png").resize((80, 80)))
    graph_icon = ImageTk.PhotoImage(Image.open("icone_graphe.png").resize((80, 80)))
    prompt_icon = ImageTk.PhotoImage(Image.open("prompt.png").resize((80, 80)))
except Exception as e:
    verif_icon = transfo_icon = graph_icon = prompt_icon = None

main_frame = tk.Frame(root)
main_frame.pack(expand=True)

title_label = tk.Label(main_frame, text="Interface professeur", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

button_verif = tk.Button(button_frame, image=verif_icon, command=open_verif_interface, width=80, height=80, bd=0)
button_verif.grid(row=0, column=0, padx=20)
label_verif = tk.Label(button_frame, text="Vérification Résultats", font=("Arial", 10))
label_verif.grid(row=1, column=0, padx=20)

button_transfo = tk.Button(button_frame, image=transfo_icon, command=transform_excel_to_csv, width=80, height=80, bd=0)
button_transfo.grid(row=0, column=1, padx=20)
label_transfo = tk.Label(button_frame, text="Questions QCM", font=("Arial", 10))
label_transfo.grid(row=1, column=1, padx=20)

button_explorer = tk.Button(button_frame, image=graph_icon, command=open_file_explorer_graphs, width=80, height=80, bd=0)
button_explorer.grid(row=0, column=2, padx=20)
label_explorer = tk.Label(button_frame, text="Explorer les graphes", font=("Arial", 10))
label_explorer.grid(row=1, column=2, padx=20)

button_prompt = tk.Button(button_frame, image=prompt_icon, command=open_file_explorer_prompt, width=80, height=80, bd=0)
button_prompt.grid(row=0, column=3, padx=20)
label_prompt = tk.Label(button_frame, text="Explorer fichiers 'prompt'", font=("Arial", 10))
label_prompt.grid(row=1, column=3, padx=20)

root.mainloop()