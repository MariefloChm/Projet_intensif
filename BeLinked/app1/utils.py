import pandas as pd
import pickle
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor


data = pd.read_csv('data.csv')
data.head()

cols = ['MTE_Domaines','MTE_Diplôme','MTE_Compétences','MTE_Objectifs','MTE_Métier']

X = data.drop(columns=["Score"])[cols]
y = data["Score"]

from sklearn.preprocessing import OrdinalEncoder


ord = OrdinalEncoder()
encodedfeat=ord.fit_transform(X)


def transform_data(x):
    ord = OrdinalEncoder()
    encodedfeat=ord.fit_transform(x)
    return encodedfeat


X_train, X_test, y_train, y_test = train_test_split(encodedfeat,y,test_size=0.3)
model = RandomForestRegressor(random_state=0)
model.fit(X_train, y_train)

model.predict(X_test)

user_input = {k:[input(f"Please Enter {k}")] for  k in cols}
user_input_df =pd.DataFrame(user_input)


user_input_df

model.predict(transform_data(user_input_df))

pickle.dump(model, open('model.pkl', 'wb'))

pickled_model = pickle.load(open('model.pkl', 'rb'))
pickled_model.predict(X_test)