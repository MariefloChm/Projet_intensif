
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

st.set_page_config("pi_poc",layout="wide", initial_sidebar_state="expanded")
st.title("POC")
df=pd.read_csv("full_dataset.csv")

st.dataframe(df)

def get_similarity_data(data_arg, feature=["Domaines","Diplôme"]):
    #Encodage one-hot des caractéristiques catégorielles
    oH_encoder = OneHotEncoder(sparse=False, drop='first')
    # encoder.get
    oH_encoded_features = oH_encoder.fit_transform(data_arg[feature])
    # scaler = MinMaxScaler()
    # df_arg[num_feat] = scaler.fit_transform(df_work[num_feat])
    # Créer un DataFrame avec les caractéristiques encodées
    oH_encoded_df = pd.DataFrame(oH_encoded_features, columns=oH_encoder.get_feature_names_out(feature))
    combined_data_encoded = pd.concat([data_arg,oH_encoded_df], axis=1)
    mentors_data = combined_data_encoded.query("Profil=='Mentor'")
    # mentors_data = mentors_data[features]
    mentorees_data = combined_data_encoded.query("Profil=='Mentoré'")
    mentors_features =mentors_data.drop(columns=data_arg.columns)
    mentorees_features =mentorees_data.drop(columns=data_arg.columns)
    similarity_score = cosine_similarity(mentors_features,mentorees_features, dense_output=True) 
    return mentors_data, mentorees_data, similarity_score

# Définition des seuils pour l'évaluation
def evaluate_score(score):
    if score > 0.7:
        return 'High'
    elif 0.5 <= score <= 0.7:
        return 'Middle'
    else:
        return 'Basse'


    
def get_full_matching_df(mtr_df, mte_df,mat_score,feature=["Domaines","Diplôme","Compétences","Objectifs","Métier","ID"]):
    n_repeats = len(mte_df)
    mtr_df_repeated = pd.concat([mtr_df[feature]] * n_repeats, ignore_index=True)
    mte_df_repeated = pd.concat([mte_df[feature]] * len(mtr_df), ignore_index=True)
    # Rename columns with prefixes
    mtr_df_repeated.columns = ["mtr_" + col for col in mtr_df_repeated.columns]
    mte_df_repeated.columns = ["mte_" + col for col in mte_df_repeated.columns]
    scores = [mat_score[i][j] for i in range(len(mtr_df)) for j in range(len(mte_df))]
    eval_score = [evaluate_score(score) for score in scores]
    # Combine the two DataFrames
    res_data = pd.concat([mtr_df_repeated, mte_df_repeated], axis=1)
    res_data["Score"] = scores
    res_data["eval_score"] = eval_score
    return res_data.sort_values(by="Score",ascending=False)
        

def add_new_mentee_data(raw_df, domaine:str,diplome:str,compétences:str,objectifs:str,métier:str, profil="Mentoré"):
    new_mentee_data =  pd.DataFrame({"Domaines":[domaine],"Diplôme":[diplome],"Compétences":[compétences],"Objectifs":[objectifs],"Métier":[métier],"Profil":[profil]})
    # new_mentee_data.index[-1]= new_mentee_data.index[-1]+1
    id_number  = int(raw_df.query("Profil=='Mentoré'")["ID"].iloc[-1].split("_")[1])+1
    new_mentee_data["ID"]=["MTE_"+str(id_number)]
    # new_mentee_data.reset_index(drop=True, inplace=True)
    res_df =pd.concat([raw_df,new_mentee_data], axis=0)
    res_df.reset_index(inplace=True, drop=True)
    return res_df

def recommand_best_mentor(new_data):
    new_mentee_id=  new_data['ID'].iloc[-1]
    mtr_df, mte_df, mat = get_similarity_data(new_data,new_data.columns)
    res= get_full_matching_df(mtr_df,mte_df,mat)
    top_n_mtr = res.query("mte_ID==@new_mentee_id").dropna(axis=1)
    return top_n_mtr
    
with st.sidebar:
    "test"
with st.form("New mentee Data"):
    col1, col2 =st.columns(2)
    with col1:
        domain =st.text_input("domain", value="Mathématiques")
        compétences =st.text_input("compétences", value="Analyse de données")
        métier =st.text_input("métier",value="Scientifique des données")
    with col2:
        diplome =st.text_input("diplome", value="Master en mathématiques")
        objectifs = st.text_input("objectifs",value="Devenir Data Scientist")
        personalité =st.text_input("personalité",value="Ethousiaste, Sympathique et Patient")
    new_input_data =add_new_mentee_data(df,domaine=domain,diplome=diplome,compétences=compétences,objectifs=objectifs,métier=métier)
    if st.form_submit_button("show matching mentors", use_container_width=True):
        st.dataframe(recommand_best_mentor(new_input_data))
        
