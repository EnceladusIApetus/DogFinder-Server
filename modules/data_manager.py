import copy
import os


def read_data(rootDir):
    instances = []  # for keeping instances, each contains its own features
    paths = []  # keep paths to each instance
    file_names = []
    original_labels = []  # keep original directory numbers of each files
    index = -1
    dirs = None
    for root, dir, files in os.walk(rootDir):
        if index == -1: dirs = dir
        for file in files:
            original_labels.append(int(dirs[index]))
            paths.append(root + '/' + file)
            file_names.append(file[:-9])
            sample = open(root + '/' + file, 'r')
            raw = sample.read()[9:-2].split(' ')
            features = [float(feature) for feature in raw][0:4096]
            instances.append(features)
            sample.close()
        index += 1
    return (instances, paths, file_names, original_labels)


def sort_data(labels, original_labels, instances, file_names, paths, separate=False):
    available_labels = labels if labels is not None else original_labels
    max_number = max(available_labels) + 1
    if separate is False:
        ordered_data = [[] for _ in xrange(max_number)]

        for index, label in enumerate(available_labels):
            temp = {}
            temp['instance'] = instances[index]
            temp['file_name'] = file_names[index]
            temp['original_label'] = original_labels[index]
            temp['path'] = paths[index]
            if labels is not None: temp['label'] = label
            ordered_data[label].append(temp)
    else:
        ordered_data = {}
        list = [[] for _ in xrange(max_number)]
        ordered_data['instances'] = copy.deepcopy(list)
        ordered_data['labels'] = copy.deepcopy(list)
        ordered_data['original_labels'] = copy.deepcopy(list)
        ordered_data['file_names'] = copy.deepcopy(list)
        ordered_data['paths'] = copy.deepcopy(list)

        for index, label in enumerate(available_labels):
            ordered_data['instances'][label].append(instances[index])
            ordered_data['file_names'][label].append(file_names[index])
            if original_labels:
                ordered_data['original_labels'][label].append(original_labels[index])
            ordered_data['paths'][label].append(paths[index])

    return ordered_data


def separate_data(ratio, ordered_data, file_name=True, original_label=True, label=True, path=True):
    testing_set = {'instances': [], 'labels': [], 'file_names': [], 'paths': [], 'original_labels': []}
    training_set = copy.deepcopy(testing_set)
    if type(ordered_data) is list:
        for i in range(0, len(ordered_data)):
            cluster_size = len(ordered_data[i])
            for j in range(0, cluster_size):
                if j < (cluster_size * ratio):
                    training_set['instances'].append(ordered_data[i][j]['instance'])
                    if label == True: training_set['labels'].append(i)
                    if file_name == True: training_set['file_names'].append(ordered_data[i][j]['file_name'])
                    if path == True: training_set['paths'].append(ordered_data[i][j]['path'])
                    if original_label == True: training_set['original_labels'].append(ordered_data[i][j]['original_label'])
                else:
                    testing_set['instances'].append(ordered_data[i][j]['instance'])
                    if label == True: testing_set['labels'].append(i)
                    if file_name == True: testing_set['file_names'].append(ordered_data[i][j]['file_name'])
                    if path == True: testing_set['paths'].append(ordered_data[i][j]['path'])
                    if original_label == True: testing_set['original_labels'].append(
                        ordered_data[i][j]['original_label'])
    else:
        for i in range(0, len(ordered_data['instances'])):
            cluster_size = len(ordered_data['instances'][i])
            separator = (cluster_size * ratio)
            training_set['instances'] += ordered_data['instances'][i][0:separator]
            testing_set['instances'] += ordered_data['instances'][i][separator:]
            if label == True:
                labels = [i for _ in xrange(cluster_size)]
                training_set['labels'] += labels[0:separator]
                testing_set['labels'] += labels[separator:]
            if file_name == True:
                training_set['file_names'] += ordered_data['file_names'][i][0:separator]
                testing_set['file_names'] += ordered_data['file_names'][i][separator:]
            if path == True:
                training_set['paths'] += ordered_data['paths'][i][0:separator]
                testing_set['paths'] += ordered_data['paths'][i][separator:]
            if original_label == True:
                training_set['original_labels'] += ordered_data['original_labels'][i][0:separator]
                testing_set['original_labels'] += ordered_data['original_labels'][i][separator:]

    return training_set, testing_set
