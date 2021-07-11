import json
import numpy as np
from sklearn.externals import joblib

clf = joblib.load("iris_regression_clf.joblib")
label = ('setosa', 'versicolor', 'virginica')


def lambda_handler(event, context):
    query = event["queryStringParameters"]

    x = np.array([(
            query["sepal_length"],
            query["sepal_width"],
            query["petal_length"],
            query["petal_width"]
    )], dtype="f2")

    pred = label[clf.predict(x)[0]]

    return {
        "statusCode": 200,
        "body": json.dumps({"predicted": pred})
	}
