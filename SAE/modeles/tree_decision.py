from sklearn import tree

def tree_decision(X_train, y_train):
    
    # charger le modèle
    clf = tree.DecisionTreeClassifier(criterion='gini', max_depth=7, max_features='log2', min_samples_leaf=4, min_samples_split=5)
                    
    # Entrainer le modèle
    clf = clf.fit(X_train, y_train)

    return clf