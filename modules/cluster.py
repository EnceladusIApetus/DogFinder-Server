from __future__ import division

from django.conf import settings
from sklearn.cluster import KMeans, AgglomerativeClustering, AffinityPropagation, MiniBatchKMeans
from collections import Counter
from sklearn.externals import joblib

from modules import data_manager

divider = None


def dump(path=settings.BASE_DIR + '/data/cluster/affinity_propagation.mdl'):
    global divider
    joblib.dump(divider, path)


def load(path=settings.BASE_DIR + '/data/cluster/affinity_propagation.mdl'):
    global divider
    divider = joblib.load(path)


def fit(instances):
    global divider
    divider = AffinityPropagation()
    labels = divider.fit_predict(instances)
    return labels


def predict(instances):
    global divider
    labels = []
    for label in divider.predict(instances):
        labels.append(label)
    return labels


def get_accuracy(ordered_data, ratio=0.5):
    training_set, testing_set = data_manager.separate_data(ratio, ordered_data)
    training_labels = predict(training_set['instances'])
    testing_labels = predict(testing_set['instances'])
    training_start = 0
    training_end = 0
    testing_start = 0
    testing_end = 0
    correct = 0
    incorrect = 0
    testing_labels_size = len(testing_set['original_labels'])
    training_labels_size = len(training_set['original_labels'])
    max_label = max([max(testing_set['original_labels']), max(training_set['original_labels'])])
    for index in range(1, max_label):
        while training_end < training_labels_size and training_set['original_labels'][training_end] == index :
            training_end += 1
        while testing_end < testing_labels_size and testing_set['original_labels'][testing_end] == index:
            testing_end += 1
        mode = Counter(training_labels[training_start:training_end]).most_common(1)[0][0]
        training_start = training_end
        for i in range(testing_start, testing_end):
            if testing_labels[i] == mode:
                correct += 1
            else:
                incorrect += 1
        testing_start = testing_end

    return (correct/(correct + incorrect)) * 100


def get_purity(sorted_data):
    items = 0
    accumulated_cluster = 0
    for index in range(0, len(sorted_data)):
        items += len(sorted_data[index])
        accumulated_cluster += Counter(sorted_data[index]).most_common(1)[0][1] if len(sorted_data[index]) > 0 else 0

    return (1/items) * accumulated_cluster
