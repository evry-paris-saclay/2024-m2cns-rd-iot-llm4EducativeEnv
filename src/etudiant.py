import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from subprocess import run

def run_app_script():
    """Lancer le script app.py."""
    try:
        run(["python", "app.py"], check=True)
        messagebox.showinfo("Succès", "Le script app.py a été exécuté avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec lors de l'exécution de app.py : {e}")

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
            messagebox.showerror("Erreur", f"Erreur lors de la liste des fichiers PNG : {e}")

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

def center_window(window, width, height):
    """Centrer la fenêtre."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Fenêtre principale
root = tk.Tk()
root.title("Interface étudiante")
center_window(root, 500, 300)

try:
    app_icon = ImageTk.PhotoImage(Image.open("Apple_Intelligence.png").resize((80, 80)))
    graph_icon = ImageTk.PhotoImage(Image.open("icone_graphe.png").resize((80, 80)))
except Exception as e:
    app_icon = graph_icon = None

main_frame = tk.Frame(root)
main_frame.pack(expand=True)

title_label = tk.Label(main_frame, text="Interface étudiante", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

button_app = tk.Button(button_frame, text="Quiz", image=app_icon, compound=tk.TOP, command=run_app_script, width=100, height=100, bd=0)
button_app.grid(row=0, column=0, padx=20)

button_graph = tk.Button(button_frame, text="Graphes", image=graph_icon, compound=tk.TOP, command=open_file_explorer_graphs, width=100, height=100, bd=0)
button_graph.grid(row=0, column=1, padx=20)

root.mainloop()
