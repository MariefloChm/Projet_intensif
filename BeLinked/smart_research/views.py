from django.shortcuts import render

# Create your views here.
import joblib
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from register.models import Mentor
from smart_research.forms import SearchingForm

# Chemin relatif au dossier de base de votre projet Django
model_path = 'smart_research/models_ml/mon_modele.joblib'
tfid = joblib.load('smart_research/models_ml/mon_transformer.joblib')


def load_model():
    model = joblib.load(model_path)
    return model

# Dans une vue Django
from django.shortcuts import render

def evaluate_score(score):
    if score > 0.7:
        return 'High'
    elif 0.5 <= score <= 0.7:
        return 'Middle'
    else:
        return 'Low'

def train_model(data_matrix,raw_df,n_optimal_cluster):
    kmeans = KMeans(n_clusters=n_optimal_cluster)
    prediction = kmeans.fit_predict(data_matrix)
    raw_df["cluster"]=prediction
    return raw_df, kmeans
def process_data(mentors, main_features):
    tfidf_vectorizer = TfidfVectorizer(stop_words=["french", "english"])
    combined_texts = []

    for mentor in mentors:
        text_elements = []
        for feature in main_features:
            attr = getattr(mentor, feature, '')
            text_elements.append(str(attr))
        combined_text = ' '.join(text_elements).lower()
        combined_texts.append(combined_text)

    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_texts)
    return tfidf_matrix, tfidf_vectorizer



def recommend_mentors(mentee_profile, model, tfid, raw_data, data_matrix, top_n=3):
    # Assurez-vous que mentee_profile est un dictionnaire avec des valeurs sous forme de chaînes
    if mentee_profile is not None:
        # Créer une chaîne de caractères à partir des valeurs du dictionnaire
        profile_text = ' '.join([str(value) for value in mentee_profile.values()]).lower()
        mentee_tfidf = tfid.transform([profile_text])


    # Predict the cluster for the mentee
    mentee_cluster = model.predict(mentee_tfidf)[0]

    # Filter mentors in the same cluster
    mentors_in_cluster = [mentor for mentor in raw_data if getattr(mentor, 'cluster', None) == mentee_cluster]

    # Get the indices of mentors in the same cluster
    mentor_indices = [i for i, mentor in enumerate(raw_data) if mentor in mentors_in_cluster]

    # Check if mentor_indices is not empty
    if mentor_indices:
        # Calculate similarity within the cluster
        mentor_data_matrix = [data_matrix[i] for i in mentor_indices]
        similarity_scores = cosine_similarity(mentor_data_matrix, mentee_tfidf)
        # ... Reste de votre code pour attacher les scores de similarité et trier ...
        for i, mentor in enumerate(mentors_in_cluster):
            mentor['similarity'] = similarity_scores[i][0]
            mentor['Evaluation'] = evaluate_score(mentor['similarity'])

            # Sort mentors by similarity score
            top_mentors = sorted(mentors_in_cluster, key=lambda x: x['similarity'], reverse=True)[:top_n]
    else:

        return None, "No mentors found in the same cluster."

    return top_mentors

def recommend_view(request):
    return render(request, 'recommend.html')

def result_view(request):
    model = load_model()
    context = {}
    if request.method == 'POST':
        # Gérer la logique du formulaire ici
        form = SearchingForm(request.POST)

        if form.is_valid():
            # Access the cleaned data
            domains = form.cleaned_data['Fields']
            diplomas = form.cleaned_data['Degree']
            skills = form.cleaned_data['Skills']
            career = form.cleaned_data['Objectives']
            professions = form.cleaned_data['Job']
            personality = form.cleaned_data['PersonalityDescription']

            user_input = {
                'Fields': [domains],
                'Degree': [diplomas],
                'Skills': [skills],
                'Objectives': [career],
                'Job': [professions],
                'PersonalityDescription': [personality]
            }

        mentors = Mentor.objects.all()
        DATA_MATRIX, tf=process_data(mentors, user_input)


        top_n, message = recommend_mentors(user_input, model, tfid, mentors, DATA_MATRIX)
        context = {
            'top_n': top_n,
            'message': message
        }

    return render(request, 'result.html', context)