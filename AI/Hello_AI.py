from sklearn import tree

# Let's "smooth" ---> 1 and "bumpy" ---> 0
features = [ [140, 1],
             [130, 1],
             [150, 0],
             [170, 0] ]

# Here also "apple" ---> 0 and "orange" ---> 1
labels = [ 0, 0, 1, 1]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)

print( clf.predict([[150, 1]]) )
