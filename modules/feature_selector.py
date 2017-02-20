from sklearn.externals import joblib
from django.conf import settings
import math

model = None


def fit(ordered_instances):
    global model
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


def get_coeff():
    global model
    return model.coef_[0:4096]


def load(path=settings.BASE_DIR + '/data/feature_selector/linear_regression.mdl'):
    global model
    model = joblib.load(path)


def dump(path=settings.BASE_DIR + '/data/feature_selector/linear_regression.mdl'):
    global model
    joblib.dump(model, path)


def get_mask(filters=41000000000):
    coef = get_coeff()
    for index, weight in enumerate(coef):
        if math.fabs(weight) < filters:
            coef[index] = 0
    return coef


def reduce_features(instances):
    mask = get_mask()

    for index in range(0, len(instances)):
        instances[index] = [(weight/mask[index2]) for index2, weight in enumerate(instances[index]) if mask[index2] != 0]

    return instances
