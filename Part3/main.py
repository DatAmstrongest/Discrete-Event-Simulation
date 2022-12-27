import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import matplotlib.pyplot as plt
from sklearn import tree


train_ratio = 0.8
test_ratio = 0.2

param_dict = {
    "criterion": ["gini", "entropy"],
    "max_depth": range(1,10),
    "min_samples_split": range(1,10),
    "min_samples_leaf":range(1,5)
}

df = pd.read_excel(r'data.xlsx',skiprows=1,)
df = df[["Type","SRT4","WIP","k","label"]]

x = df[["Type","SRT4","WIP"]]
y = df[["label"]]


# Training model
model = DecisionTreeClassifier()
model.fit(x,y)

# Getting training score: 0.68001
y_pred = model.predict(x)
print(accuracy_score(y,y_pred))

"""
fig = plt.figure(figsize=(25,20), dpi=1200)
_ = tree.plot_tree(model, 
                   feature_names=["Type","SRT4","WIP","label"],  
                   class_names=["A", "B", "C", "D", "E", "F"],
                   filled=True)
fig.savefig("decision_tree.png")
"""

# Getting average k values for each category
categories = dict({
    "A":0,
    "B":0,
    "C":0,
    "D":0,
    "E":0,
    "F":0
})

categories_frequency = dict({
    "A":0,
    "B":0,
    "C":0,
    "D":0,
    "E":0,
    "F":0
})

for ind in x.index:
    categories_frequency[y["label"][ind]] += 1
    categories[y["label"][ind]] += df["k"][ind]

for k in categories:
    categories[k] = categories[k]/categories_frequency[k]
for k,v in categories.items():
    print(k,v)
    


