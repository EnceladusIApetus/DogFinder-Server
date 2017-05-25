from __future__ import division
from sklearn import svm
from sklearn.externals import joblib


model = None
training_set = None
testing_set = None

def set_data(training_set, testing_set):
    globals()['training_set'] = training_set
    globals()['testing_set'] = testing_set

def fit(instances, labels):
    global training_set, model
    model = svm.SVC(kernel='poly', degree=5, C=1.0).fit(instances, labels)
    joblib.dump(model, 'classifier.clf')

def predict(data):
    global model
    return model.predict(data)

def evaluate():
    global testing_set, model
    predicted_data = model.predict(testing_set['instances'])
    correct = 0
    incorrect = 0
    correct_data = []
    incorrect_data = []
    for index in range(0, len(predicted_data)):
        temp = {}
        temp['instance'] = testing_set['instances'][index]
        temp['label'] = testing_set['labels'][index]
        temp['file_name'] = testing_set['file_names'][index]
        if testing_set['labels'][index] == predicted_data[index]:
            correct += 1
            correct_data.append(temp)
        else:
            incorrect += 1
            incorrect_data.append(temp)

    accuracy = (correct / (correct + incorrect)) * 100

    return (accuracy, correct_data, incorrect_data)