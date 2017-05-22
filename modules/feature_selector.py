from sklearn.externals import joblib
from django.conf import settings
from sklearn.decomposition import PCA
from sklearn import linear_model
import numpy as np
import math

model = None
pca = None

def fit(ordered_instances):
    global model, pca
    model = linear_model.LinearRegression() if model is None else model
    pca = PCA(n_components=0.896) if pca is None else pca

    internal_matching = []
    cross_matching = []
    groups_size = len(ordered_instances)

    for i in range(1, groups_size):
        for j in range(1, groups_size):
            for k in range(0, len(ordered_instances[i])):
                if i == j:
                    for l in range(0, len(ordered_instances[j])):
                        internal_matching.append(ordered_instances[i][k] + ordered_instances[j][l])
                else:
                    for l in range(0, len(ordered_instances[j])):
                        cross_matching.append(ordered_instances[i][k] + ordered_instances[j][l])

    cross_matching = cross_matching[::2] # opt only even like 0, 2, 4
    labels = [1] * len(internal_matching) + [0] * len(cross_matching)
    model.fit(internal_matching + cross_matching, labels)

    instances = []
    for group_instances in ordered_instances:
        instances += group_instances

    mask = get_mask()

    for index in range(0, len(instances)):
        instances[index] = [(weight / mask[index2]) for index2, weight in enumerate(instances[index]) if
                            mask[index2] != 0]

    X = np.array(instances)
    pca.fit(X)


def get_coeff():
    global model
    return model.coef_[0:4096]


def load(path='data/feature_selector'):
    global model, pca
    model = joblib.load(path + '/linear_regression.mdl')
    pca = joblib.load(path + '/PCA.mdl')


def dump(path='data/feature_selector'):
    global model, pca
    joblib.dump(model, path + '/linear_regression.mdl')
    joblib.dump(pca, path + '/PCA.mdl')


def get_mask(filters=41000000000):
    coef = get_coeff()
    for index, weight in enumerate(coef):
        if math.fabs(weight) < filters:
            coef[index] = 0
    return coef


def reduce_features(instances):
    global pca
    mask = get_mask()

    for index in range(0, len(instances)):
        instances[index] = [(weight/mask[index2]) for index2, weight in enumerate(instances[index]) if mask[index2] != 0]

    instances = pca.transform(instances)
    return instances
