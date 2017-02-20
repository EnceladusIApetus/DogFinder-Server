from sklearn.neighbors import NearestNeighbors

model = None
neighbor_num = None
radius = None


def set(neighbor_num, radius):
    global model
    globals()['neighbor_num'] = neighbor_num
    globals()['radius'] = radius
    model = NearestNeighbors(neighbor_num, radius)


def fit(data):
    global model, neighbor_num, radius
    if len(data) < neighbor_num:
        model = NearestNeighbors(len(data), radius) # if number of neighbor is less than defined
    model.fit(data)


def neighbors(data):
    global model
    return model.kneighbors(data, return_distance=False)[0]
