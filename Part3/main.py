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

df = pd.read_excel(r'Excel.xlsx')
df = df[["Type", "m1", "m2", "m3", "m4","SRT", "nQ1","nQ2","nQ3","nQ4" ,"label"]]
"""
print(df.head)
print(df.columns)
"""

x = df.values[:, 0:10]
y = df.values[:,10]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1 - train_ratio, random_state = 100)

"""
decisionTree = DecisionTreeClassifier()
grid = GridSearchCV(decisionTree, param_grid=param_dict, cv=10, verbose=1, n_jobs=-1)
grid.fit(x_train,y_train)

# Best model is parameters {'criterion': 'entropy', 'max_depth': 7, 'min_samples_leaf': 4, 'min_samples_split': 2} with score 0.649
print(grid.best_params_)
print(grid.best_score_)
"""

model = DecisionTreeClassifier(criterion="entropy", max_depth=7, min_samples_leaf=4, min_samples_split=2)
model.fit(x_train,y_train)
y_pred_en = model.predict(x_test)
# Score is 63.2
print(("Accuracy is"), accuracy_score(y_test,y_pred_en)*100)
print("Confusion matrix")
print(confusion_matrix(y_test, y_pred_en))
print("Report")
print(classification_report(y_test, y_pred_en))


feature_names = df.columns[:10]
target_names = df['label'].unique().tolist()

plot_tree(model, 
          feature_names = feature_names, 
          class_names = target_names, 
          filled = True, 
          rounded = True)

plt.savefig('tree_visualization.png',dpi=600) 