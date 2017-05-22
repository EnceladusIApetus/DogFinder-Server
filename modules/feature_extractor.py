import os


def extract(path):
    raw = os.popen('~/OverFeat/bin/linux_64/overfeat -f ' + path).read()[9:-2].split(' ')
    features = [float(feature) for feature in raw][0:4096]
    return features


def batch_extract(files_list):
    features_list = []
    for index in range(0, len(files_list)):
        features_list.append(extract(files_list[index]))
    return features_list


def convert_to_float(features):
    return [float(feature) for feature in features.split(', ')]


def convert_to_str(features):
    return ", ".join(str(x) for x in features)
