import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn import linear_model
from sklearn.linear_model import SGDRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn import svm


connection = sqlite3.connect('ComicChron.db')
cursor = connection.cursor()

def read_db(keyword):
    # statement = "SELECT units, month, issue FROM comicTable WHERE title LIKE '%" + keyword + "%' ORDER BY units DESC"
    statement = "SELECT units, month, issue FROM comicTable ORDER BY units DESC"
    myFrames = pd.read_sql_query(statement, connection)
    nparray = np.array(myFrames.values)
    return nparray

def main():
    # keyword = input('Enter a keyword or character name: \n')
    keyword = 'batman'

    data_set = read_db(keyword)

    data_set = data_set.reshape(len(data_set), 3)

    X = data_set[:, [1, 2]]
    y = data_set[:, [0]]

    # model
    regr = linear_model.LinearRegression()
    # regr = MLPRegressor(hidden_layer_sizes=60)
    #clf = svm.SVR(verbose=True)
    # clf = SGDRegressor(max_iter=100, verbose=True, penalty='elasticnet', shuffle=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Robust Scaler
    scaler = RobustScaler().fit(X_train)
    rescaledX = scaler.transform(X_train)
    scalerTest = RobustScaler().fit(X_test)
    rescaledTestX = scalerTest.transform(X_test)

    # Fitting model
    regr.fit(rescaledX, y_train.ravel())
    # clf.fit(rescaledX, y_train.ravel())

    prediction = regr.predict(rescaledTestX)
    # prediction = clf.predict(rescaledTestX)

    # MSE
    print("Mean squared error: %.2f"
          % mean_squared_error(y_test, prediction))



    # Explained variance score: 1 is perfect prediction
    print('Variance score on test: %.4f' % regr.score(rescaledTestX, y_test))
    print('Variance score on train: %.4f' % regr.score(rescaledX, y_train))

    # print('Variance score on test: %.4f' % clf.score(rescaledTestX, y_test))
    # print('Variance score on train: %.4f' % clf.score(rescaledX, y_train))
    cursor.close()

    # Plot outputs
    # plt.scatter(rescaledTestX, y_test, color='black')
    # plt.plot(rescaledTestX, prediction, color='blue', linewidth=3)
    #
    # plt.xticks(())
    # plt.yticks(())


main()
