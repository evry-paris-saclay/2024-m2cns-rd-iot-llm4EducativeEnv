import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import time

# Charger les résultats d'une feuille spécifique dans un fichier Excel
def load_quiz_results(filename, sheet_name):
    try:
        data = pd.read_excel(filename, sheet_name=sheet_name)
        return data
    except Exception as e:
        print(f"Erreur lors du chargement du fichier Excel ou de la feuille : {e}")
        return None

# Créer un graphe ordonné avec des valeurs sous forme de fractions
def create_ordered_graph(data, student_name, prompt_created, results_filename, sheet_name):
    try:
        G = nx.DiGraph()
        G.add_node("Réseau", value=0, max_value=18)

        # Calcul des scores par concept
        concept_scores = data.groupby("Concept")["Score"].sum().to_dict()

        for _, row in data.iterrows():
            concept = row["Concept"]
            detailed_concept = row["Detailed Concept"]
            score = row["Score"]

            if not G.has_node(concept):
                G.add_node(concept, value=concept_scores.get(concept, 0), max_value=2)
                G.add_edge("Réseau", concept)

            G.add_node(detailed_concept, value=score, max_value=1)
            G.add_edge(concept, detailed_concept)

        total_network_value = sum(G.nodes[child]["value"] for child in G.neighbors("Réseau"))
        G.nodes["Réseau"]["value"] = total_network_value

        pos = nx.nx_agraph.graphviz_layout(G, prog="dot", args="-Grankdir=LR -Gnodesep=1.5")

        # Générer un nom unique pour le fichier graphique
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        graph_filename = f"graphe_{results_filename}_{sheet_name}_{timestamp}.png"

        # Générer et sauvegarder le graphe
        plt.figure(figsize=(16, 8))
        nx.draw(
            G, pos, with_labels=False, node_size=300, node_color="lightblue",
            font_size=8, font_weight="normal", edge_color="gray", arrowsize=15
        )

        for node, (x, y) in pos.items():
            plt.text(x, y + 60, s=node, horizontalalignment='center', fontsize=8)

        for node, (x, y) in pos.items():
            score_fraction = f"{G.nodes[node]['value']}/{G.nodes[node]['max_value']}"
            plt.text(x, y, s=score_fraction, horizontalalignment='center', verticalalignment='center', fontsize=10, color="black")

        plt.title(f"Arborescence de Concepts et Scores (Fraction) - {student_name}", fontsize=14)
        plt.savefig(graph_filename)
        plt.close()
        print(f"Graphe enregistré : {graph_filename}")

    except Exception as e:
        print(f"Erreur lors de la création du graphe : {e}")

# Créer un fichier .txt avec les concepts non maîtrisés et une consigne
def create_prompt_txt(data, student_name):
    try:
        # Calcul des scores par concept
        concept_scores = data.groupby("Concept")["Score"].sum().to_dict()
        low_score_concepts = {
            concept: concept_scores[concept]
            for concept in concept_scores
            if concept_scores[concept] < 2
        }

        if not low_score_concepts:
            print("Tous les concepts sont maîtrisés. Aucun fichier .txt n'est nécessaire.")
            return

        # Contenu du fichier
        prompt_content = "Génère un nouveau PDF basé sur les concepts non maîtrisés par l’étudiant.\n"
        prompt_content += "Ce PDF extrait les informations de l’ancien PDF, reformule les explications, ajoute des images, et structure les contenus en chapitres pour chaque concept concerné.\n\n"
        prompt_content += "Concepts non maîtrisés :\n"
        for concept, score in low_score_concepts.items():
            prompt_content += f"- {concept} (Score : {score})\n"

        # Générer un nom unique pour le fichier
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        base_filename = f"prompt_cours_pdf_{student_name}_{timestamp}"
        filename = f"{base_filename}.txt"
        counter = 1
        while os.path.exists(filename):
            filename = f"{base_filename}_{counter}.txt"
            counter += 1

        # Sauvegarder le fichier
        with open(filename, "w", encoding="utf-8") as file:
            file.write(prompt_content)

        print(f"Fichier .txt créé : {filename}")

    except Exception as e:
        print(f"Erreur lors de la création du fichier .txt : {e}")

# Main
if __name__ == "__main__":
    print("Liste des fichiers disponibles :")
    for file in os.listdir("."):
        if file.startswith("quiz_results_") and file.endswith(".xlsx"):
            print(file)

    filename = input("Entrez le nom du fichier (ex: quiz_results_Momo.xlsx) : ")
    if not os.path.exists(filename):
        print("Fichier introuvable.")
        exit()

    # Charger les noms des feuilles dans le fichier Excel
    try:
        sheet_names = pd.ExcelFile(filename).sheet_names
        print("Feuilles disponibles (date-heure) :")
        for sheet in sheet_names:
            print(f" - {sheet}")
    except Exception as e:
        print(f"Erreur lors de la lecture des feuilles : {e}")
        exit()

    sheet_name = input("Entrez le nom de la feuille (date-heure ex: 2025-01-16-10-15) : ")
    if sheet_name not in sheet_names:
        print("Feuille introuvable.")
        exit()

    student_name = filename.split("_")[2].split(".")[0]

    data = load_quiz_results(filename, sheet_name)

    if data is not None:
        create_ordered_graph(data, student_name, False, filename.split(".")[0], sheet_name)
        create_prompt_txt(data, student_name)
    else:
        print("Aucune donnée à afficher.")