from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from .models import Mentor  # Remplacez "VotreModeleDeMentor" par le nom de votre modèle

# Redéfinir la fonction calculate_matching_score
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

    mentors = Mentor.objects.all()  # Récupérer tous les objets de mentor depuis la base de données

    for mentor in mentors:
        # Comparaison de chaque paire de colonnes pour le mentor actuel
        scores = []
        vectorizer = TfidfVectorizer()
        for col in weights.keys():
            mentor_text = str(getattr(mentor, col))  # Utilisez getattr pour accéder aux champs du modèle
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
            'FirstName': mentor.first_name,
            'LastName': mentor.last_name,
            'Skills': mentor.Skills,
            'Job': mentor.Job,
            'Rating': mentor.Rating,
            'ID': mentor.id
        }

        # Ajoutez le score au tableau des meilleurs scores
        top_scores.append(matching_score)

    # Triez les scores de manière décroissante
    top_scores = sorted(top_scores, reverse=True)

    # Sélectionnez les 3 meilleurs scores et leurs informations associées
    top_scores = top_scores[:3]
    top_mentors = {score: top_mentors[score] for score in top_scores}

    return top_mentors

# Initialisez le vectorizer une seule fois et réutilisez-le
vectorizer = TfidfVectorizer()

def calculate_matching_score_optimized(mentore, vectorizer):
    weights = {
        'Fields': 0.9,
        'Degree': 0.9,
        'Skills': 0.9,
        'Objectives': 0.9,
        'Job': 0.9,
        'PersonalityDescription': 1
    }

    # Préparez les textes des mentores pour la vectorisation
    mentore_texts = [str(mentore[col]) for col in weights.keys()]
    vectorizer.fit(mentore_texts)  # Fit une seule fois sur les textes du mentore
    mentore_vectors = vectorizer.transform(mentore_texts)

    top_mentors = []  # Liste pour stocker les meilleurs mentors avec leurs scores

    mentors = Mentor.objects.all()  # Récupérer tous les objets de mentor depuis la base de données
    for mentor in mentors:
        mentor_texts = [str(getattr(mentor, col)) for col in weights.keys()]
        mentor_vectors = vectorizer.transform(mentor_texts)

        # Calcul de la similarité cosinus pour tous les champs en une seule fois
        similarity_scores = cosine_similarity(mentor_vectors, mentore_vectors)

        # Calcul du score global pondéré pour ce mentor
        weighted_scores = similarity_scores.diagonal() * np.array(list(weights.values()))
        matching_score = np.mean(weighted_scores)

        # Ajoutez le mentor et son score dans la liste
        top_mentors.append((matching_score, mentor))

    # Triez les mentors en fonction de leur score de manière décroissante
    top_mentors.sort(reverse=True, key=lambda x: x[0])

    # Sélectionnez les 3 meilleurs scores et leurs informations associées
    top_3_mentors = top_mentors[:3]
    top_3_mentors_info = [{
        'Score': score,
        'FirstName': mentor.first_name,
        'LastName': mentor.last_name,
        'Skills': mentor.Skills,
        'Job': mentor.Job,
        'Rating': mentor.Rating,
        'ID': mentor.id
    } for score, mentor in top_3_mentors]

    return top_3_mentors_info