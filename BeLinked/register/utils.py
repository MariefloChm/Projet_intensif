import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Chargez le fichier CSV contenant les données des mentors
mentor_data = pd.read_csv('register/selected_mentor_data.csv', sep='\t')
mentor_info = pd.read_csv('register/info_mentor.csv', sep='\t')

merged_data = mentor_data.merge(mentor_info)

def calculate_matching_score(mentore):
    weights = {
        'Domain': 0.9,
        'Diploma': 0.9,
        'Skills': 0.9,
        'Career_objectives': 0.9,
        'Professions': 0.9,
        'Personality': 1
    }

    # Initialisation de la liste des meilleurs scores
    top_scores = []

    top_mentors = {}  # Un dictionnaire pour stocker les informations associées aux scores

    for index, mentor in merged_data.iterrows():  # Utilisez merged_data au lieu de mentor_data
        # Comparaison de chaque paire de colonnes pour le mentor actuel
        scores = []
        vectorizer = TfidfVectorizer()
        for col in mentor.index:
            if col in weights:
                if col in ['Skills', 'Career_objectives', 'Personality']:
                    mentor_text = str(mentor[col])
                    mentore_text = str(mentore[col])

                    vectorizer.fit([mentor_text, mentore_text])
                    mentor_vector = vectorizer.transform([mentor_text])
                    mentore_vector = vectorizer.transform([mentore_text])
                    score = cosine_similarity(mentor_vector, mentore_vector)[0][0]
                else:
                    score = int(mentor[col] == mentore[col])
                scores.append(score * weights[col])

        # Calcul du score global pour ce mentor
        matching_score = np.mean(scores)

        # Stockez le score et les informations associées dans le dictionnaire
        top_mentors[matching_score] = {
            'First_name': mentor['First_name'],
            'Last_name': mentor['Last_name'],
            'Skills': mentor['Skills'],
            'Professions': mentor['Professions'],
            'Rating': mentor['Rating']
        }

        # Ajoutez le score au tableau des meilleurs scores
        top_scores.append(matching_score)

    # Triez les scores de manière décroissante
    top_scores = sorted(top_scores, reverse=True)

    # Sélectionnez les 3 meilleurs scores et leurs informations associées
    top_scores = top_scores[:3]
    top_mentors = {score: top_mentors[score] for score in top_scores}

    return top_mentors






