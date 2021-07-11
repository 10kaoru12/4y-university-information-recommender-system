from sklearn import datasets, model_selection, metrics
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

iris = datasets.load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3, shuffle=True, random_state=0)

clf = LogisticRegression(random_state=0, solver="lbfgs", multi_class="multinomial")
clf.fit(X_train, y_train)

joblib.dump(clf, "iris_regression_clf.joblib")

y_pred = clf.predict(X_test)
print(metrics.accuracy_score(y_test, y_pred))
