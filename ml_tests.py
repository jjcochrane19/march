import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

X = train.drop(columns = ["TEAM", "YEAR", "ROUND", "Unnamed: 0"])
y = train["ROUND"]

X_predict = test.drop(columns = ["TEAM", "YEAR", "ROUND", "Unnamed: 0"])
test_info = test[["TEAM", "YEAR"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

classifiers = [
    SVC(),
    DecisionTreeClassifier(criterion='entropy'),
    KNeighborsClassifier(),
    RandomForestClassifier(),
    LogisticRegression(max_iter=1000) 
]

param_grid = [
    {'kernel': ['linear', 'rbf'], 'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]},  
    {'max_depth': [None] + list(range(1, 31))},  
    {'n_neighbors': list(range(1, 31))}, 
    {"n_estimators": list(range(1,201)), "max_depth": [None] + list(range(1, 51))},  
    {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]} 
]

best_accuracy = -1
best_classifier_index = -np.Inf
best_classifier = None

for i, classifier in enumerate(classifiers):
    grid_search = GridSearchCV(classifier, param_grid[i], cv = 5, scoring='accuracy')
    grid_search.fit(X_train_scaled, y_train)
    
    if grid_search.best_score_ > best_accuracy:
        best_accuracy = grid_search.best_score_
        best_classifier_index = i
        best_classifier = grid_search.best_estimator_

print("Best classifier:", best_classifier)
print("Best accuracy:", best_accuracy)

X_predict_scaled = scaler.transform(X_predict)
preds = best_classifier.predict(X_predict_scaled)

test_info["PREDICTED_ROUND"] = preds

test_info.to_csv("preds.csv")