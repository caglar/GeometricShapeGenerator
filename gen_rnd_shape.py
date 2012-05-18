import numpy as np

tau = 0.1
n0 = 2

def reconstruct_density_matrix(sprite):
    pass

def weighted_choice(weights, seed=1241):
    R = np.random.RandomState(seed)
    totals = np.cumsum(weights)
    norm = totals[-1]
    throw = R.rand()*norm
    return np.searchsorted(totals, throw)

def get_random_loc(w, h, seed=3451):
    R = np.random.RandomState(seed)
    initx, inity = R.random_integers(0, w), R.random_integers(0, h)
    return get_random_loc

def get_neighbour_random(w, h, x, y, walk_matrix, seed=3451):
    R = np.random.RandomState(seed)
    walk_x, walk_y = R.random_integers(0, walk_matrix.shape[0]), R.random_integers(0, walk_matrix.shape[1])
    while walk_x <0 or walk_x > w or walk_y < 0 or walk_y > h:
        walk_x, walk_y = R.random_integers(0, walk_matrix.shape[0]), R.random_integers(0, walk_matrix.shape[1])
    return walk_x, walk_y

def get_random_loc_w_transition(x, y, transition_vec, walk_matrix, seed=3451):
    idx = weighted_choice(transition_vec)
    row = idx / 3
    col = idx % 3
    x += walk_matrix[row][col][0]
    y += walk_matrix[row][col][1]
    return x, y

def get_point_density(x, y, walk_matrix, sprite):
    density_matrix = reconstruct_density_matrix(sprite)
    density = density_matrix[x][y]
    return density

def update_transition_matrix(x, y, transition_matrix, walk_matrix, sprite):
    f, s = transition_matrix.shape
    for i in xrange(f):
        for j in xrange(s):
            transition_matrix[i][j] = get_point_density(x + walk_matrix[i][j][0], y + walk_matrix[i][j][1], walk_matrix, sprite)
    transition_matrix /= np.max(transition_matrix)
    return transition_matrix

def gen_rnd_walk_shape(w, h, fill=0.5, seed=3412):
    x, y = get_random_loc(w, h, seed)
    sprite = np.zeros((w, h))
    walk_matrix = np.array([[(-1, 1), (0, 1), (1, 1)], [(-1, 0), (0, 0), (1, 0)], [(-1, -1), (0, -1), (1, -1)]])
    transition_matrix = np.ones((3, 3))
    filled = 0

    xflag_start, xflag_end = False, False
    yflag_start, yflag_end = False

    while not (xflag_start and xflag_end) or not (yflag_start and yflag_end) or filled < 0.5:
        if x == 0:
            xflag_start = True
        if x == w:
            xflag_end = True
        if y == 0:
            yflag_start = True
        if y == h:
            yflag_end = True
        sprite[x][y] = 1
        transition_matrix = update_transition_matrix(x, y, transition_matrix, 
                walk_matrix, sprite)
        if np.all(transition_matrix==0):
            x, y = get_random_loc(w, h, seed)
            while sprite[x][y] == 1:
                x, y = get_random_loc(w, h, seed)
        elif np.all(transition_matrix==1):
            x, y = get_neighbour_random(w, h, x, y, walk_matrix)
        else:
            transition_vec = transition_matrix.flatten()
            x, y = get_random_loc_w_transition(x, y, transition_vec, walk_matrix)
        filled = np.count_non_zeros(sprite)/(w * h)
    return sprite

print gen_rnd_walk_shape(100, 100)
