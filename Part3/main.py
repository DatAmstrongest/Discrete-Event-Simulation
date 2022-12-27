import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import matplotlib.pyplot as plt
import numpy as np
from sklearn import tree
from sklearn.tree import _tree

def get_rules(tree, feature_names, class_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    paths = []
    path = []
    
    def recurse(node, path, paths):
        
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {np.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {np.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            path += [(tree_.value[node], tree_.n_node_samples[node])]
            paths += [path]
            
    recurse(0, path, paths)

    # sort by samples count
    samples_count = [p[-1][1] for p in paths]
    ii = list(np.argsort(samples_count))
    paths = [paths[i] for i in reversed(ii)]
    
    rules = []
    for path in paths:
        rule = "if "
        
        for p in path[:-1]:
            if rule != "if ":
                rule += " and "
            rule += str(p)
        rule += " then "
        if class_names is None:
            rule += "response: "+str(np.round(path[-1][0][0][0],3))
        else:
            classes = path[-1][0][0]
            l = np.argmax(classes)
            rule += f"class: {class_names[l]} (proba: {np.round(100.0*classes[l]/np.sum(classes),2)}%)"
        rule += f" | based on {path[-1][1]:,} samples"
        rules += [rule]
        
    return rules



df = pd.read_excel(r'data.xlsx',skiprows=1,)
df = df[["Type","SRT4","WIP","k","label"]]

x = df[["Type","SRT4","WIP"]]
y = df[["label"]]


# Training model
model = DecisionTreeClassifier(min_samples_leaf=50, max_depth=10,max_leaf_nodes=10)
model.fit(x,y)

# Getting training score: 0.68001
y_pred = model.predict(x)
print(accuracy_score(y,y_pred))

# Printing rules of the tree
text_representation = tree.export_text(model, feature_names=["Type", "SRT4", "WIP"])
print(text_representation)

# Printing rules (human readable form)
rules = get_rules(model, ["Type","SRT4","WIP"], ["A","B","C","D","E","F"])
for r in rules:
    print(r)


fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(model, 
                   feature_names=["Type","SRT4","WIP","label"],  
                   class_names=["A", "B", "C", "D", "E", "F"],
                   filled=True)
fig.savefig("decision_tree.png")


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
    


