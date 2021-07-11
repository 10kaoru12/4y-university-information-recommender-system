import hug
from sklearn.externals import joblib


mt = MeCabTokenize(pos_keep_filters=["名詞", "形容詞", "動詞"])
story_clf = joblib.load("story.pkl")
le = joblib.load("label.pkl")


@hug.get("/author_predict")
def api_example(text):
    X = mt.tokenize(text)
    pred = story_clf.predict(X)
    return le.inverse_transform(pred)
