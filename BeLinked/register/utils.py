import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Chargez le fichier CSV contenant les données des mentors
data = pd.read_csv('register/mentors_dataset.csv')

# Redéfinir la fonction calculate_matching_score après avoir importé les bibliothèques nécessaires
def calculate_matching_score(mentore):
    weights = {
        'Fields': 0.9,
        'Degree': 0.9,
        'Skills': 0.9,
        'Objectives': 0.9,
        'Job': 0.9,
        'PersonalityDescription': 1
    }

    # Initialisation de la liste des meilleurs scores
    top_scores = []

    top_mentors = {}  # Un dictionnaire pour stocker les informations associées aux scores

    for index, mentor in data.iterrows():  # Utilisez data au lieu de merged_data
        # Comparaison de chaque paire de colonnes pour le mentor actuel
        scores = []
        vectorizer = TfidfVectorizer()
        for col in weights.keys():
            mentor_text = str(mentor[col])
            mentore_text = str(mentore[col])

            vectorizer.fit([mentor_text, mentore_text])
            mentor_vector = vectorizer.transform([mentor_text])
            mentore_vector = vectorizer.transform([mentore_text])
            score = cosine_similarity(mentor_vector, mentore_vector)[0][0]
            scores.append(score * weights[col])

        # Calcul du score global pour ce mentor
        matching_score = np.mean(scores)

        # Stockez le score et les informations associées dans le dictionnaire
        top_mentors[matching_score] = {
            'FirstName': mentor['FirstName'],
            'LastName': mentor['LastName'],
            'Skills': mentor['Skills'],
            'Job': mentor['Job'],
            'Rating': mentor['Rating'],
            'ID': mentor['ID']
        }

        # Ajoutez le score au tableau des meilleurs scores
        top_scores.append(matching_score)

    # Triez les scores de manière décroissante
    top_scores = sorted(top_scores, reverse=True)

    # Sélectionnez les 3 meilleurs scores et leurs informations associées
    top_scores = top_scores[:3]
    top_mentors = {score: top_mentors[score] for score in top_scores}

    return top_mentors









