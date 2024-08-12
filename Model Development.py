import sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def feedback():

    data = pd.read_csv(r'C:\Users\msaur\Documents\projects python\GUI\userdevelopment.csv')

    X= data[['Hint','Formulae','Solution']]
    Y= data['Proficiency']

    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=5)


    model=LinearRegression()
    model.fit(X_train,Y_train)


    Y_pred = model.predict(X_test)


feedback()