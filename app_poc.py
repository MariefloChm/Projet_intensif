
import pandas as pd
from sklearn.metrics.cluster import silhouette_score
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, kmeans_plusplus
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st
import pickle

st.set_page_config("pi_poc",layout="wide", initial_sidebar_state="expanded")
st.title("POC")
RAW_DATA=pd.read_csv("full_dataset.csv")
with st.expander("Show data"):
    st.dataframe(RAW_DATA)
    
# Définition des seuils pour l'évaluation
def evaluate_score(score):
    if score > 0.7:
        return 'High'
    elif 0.5 <= score <= 0.7:
        return 'Middle'
    else:
        return 'Basse'


def process_df(df:pd.DataFrame):
    main_feat=["Domaines","Diplôme","Compétences","Objectifs","Métier","Description de la personnalité","Langue parlée"]
    tfidf_vectorizer = TfidfVectorizer(stop_words=["french","english"])
    df_work =df.copy()
    df_work['combined_text'] = df_work[main_feat].apply(lambda x: ' '.join(x), axis=1)
    df_work['combined_text'] =df_work["combined_text"].apply(lambda x:x.lower())
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_work['combined_text'])
    return tfidf_matrix, tfidf_vectorizer

def find_optimal_k(data_matrix):
    wcss = []
    add_wcss = wcss.append
    shs_score = []
    add_shs = shs_score.append
    K_range = range(2, 20) 
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=0)
        cluster_labels = kmeans.fit_predict(data_matrix)
        add_wcss(kmeans.inertia_)
        silhouette_avg = silhouette_score(data_matrix, cluster_labels)
        add_shs(silhouette_avg)
    res = pd.DataFrame({"K":K_range,"WCSS":wcss,"Silhouette Score":shs_score})
    return res

def train_model(data_matrix,raw_df,n_optimal_cluster):
    kmeans = KMeans(n_clusters=n_optimal_cluster)
    prediction = kmeans.fit_predict(data_matrix)
    raw_df["cluster"]=prediction
    return raw_df, kmeans

def get_user_input_df():
    col1, col2 =st.columns(2)
    with col1:
        domain =st.text_input("domain", value="Mathématiques")
        compétences =st.text_input("compétences", value="Analyse de données")
        métier =st.text_input("métier",value="Scientifique des données")
    with col2:
        diplome =st.text_input("diplome", value="Master en mathématiques")
        objectifs = st.text_input("objectifs",value="Devenir Data Scientist")
        personalité =st.text_input("personalité",value="Ethousiaste, Sympathique et Patient")
        feat=["Domaines","Diplôme","Compétences","Objectifs","Métier","ID"]
    user_inp = {"Domaines":[domain],"Diplôme":[diplome],"Compétences":[compétences],"Objectifs":[objectifs],"Métier":[métier]}
    user_input_df = pd.DataFrame(user_inp)
    return user_input_df

def recommend_mentors(mentee_profile,model:KMeans,transformer:TfidfVectorizer,raw_df:pd.DataFrame,data_matrix,top_n=3):
    # Transform mentee profile text to TF-IDF
    if mentee_profile is not None:
        if isinstance(mentee_profile, pd.DataFrame):
            corpus= mentee_profile.apply(lambda x:' '.join(x),axis=1)
            # corpus = [col.lower() for col in corpus]
            mentee_tfidf = transformer.transform(corpus)
        else:
            mentee_tfidf = transformer.transform([mentee_profile])
    else:
        st.warning("Pleaser enter your information")

    # Predict the cluster for the mentee
    mentee_cluster =model.predict(mentee_tfidf)
    # Filter mentors in the same cluster
    mentors_in_cluster = raw_df[raw_df['cluster'] == mentee_cluster[0]]

    # Calculate similarity within the cluster
    similarity_scores = cosine_similarity(data_matrix[mentors_in_cluster.index], mentee_tfidf)
    # Sort mentors by similarity score
    mentors_in_cluster['similarity'] = similarity_scores.flatten()
    mentors_in_cluster["Evaluation"] = mentors_in_cluster['similarity'].apply(evaluate_score)
    top_mentors = mentors_in_cluster.sort_values(by='similarity', ascending=False).head(top_n)
    return top_mentors

DATA_MATRIX, tfid=process_df(RAW_DATA)
best_k_res = find_optimal_k(data_matrix=DATA_MATRIX)
df,kmeans = train_model(DATA_MATRIX,RAW_DATA,10)

import matplotlib.pyplot as plt 
with st.sidebar:
    st.write("Settings")
    menu =st.radio("Select Menu",options=("Train","Recommandation"))

if menu=="Train":
    st.write("You can train model here")
    fig,(ax,ax2)= plt.subplots(nrows=2)
    best_k_res.plot(x="K",y="WCSS", ax=ax)
    best_k_res.plot(x="K",y="Silhouette Score", ax=ax2)
    st.pyplot(fig)
else:
    mentee_information = None
    inp_option = st.radio("Select the input format",options=("Forumalaire","Text"))
    # user_inp = st.text_input("Enter your description")
    mentee_information= st.text_input("Enter your description") if inp_option=="Text" else get_user_input_df()
    
    top_n = recommend_mentors(mentee_information,model=kmeans,transformer=tfid,raw_df=RAW_DATA,data_matrix=DATA_MATRIX)
    if st.button("Find mentors"):
        st.dataframe(top_n)

            
                
