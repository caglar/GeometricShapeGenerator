import numpy as np
import math
from citerator import circle_around_aclockwise

tau = 1
n0 = 2

def get_exp_decay(r, n):
	tau = r
	return n0 * math.exp(-tau/n)

def reconstruct_density_matrix(w, h, sprite):
	density_mat = np.zeros((w, h))
	for i in xrange(w):
		for j in xrange(h):
			for r, (cx, cy) in circle_around_aclockwise(i, j):
				if cx < 0 or cx >= w or cy >= h or cy < 0:
					break
				else:
					if i>=1 and j>=1 and density_mat[i - 1][j - 1] != 0:
						density_mat[i][j] += sprite[i][j] + get_exp_decay(r, density_mat[i-1][j-1])
					else:
						density_mat[i][j] = sprite[i][j]
	return density_mat

def weighted_choice(weights, seed=12411):
	R = np.random.RandomState(seed)
	totals = np.cumsum(weights)
	norm = totals[-1]
	throw = R.rand()*norm
	return np.searchsorted(totals, throw)

def get_random_loc(w, h, seed=34551):
	R = np.random.RandomState(seed)
	initx, inity = R.random_integers(0, w - 1), R.random_integers(0, h - 1)
	return initx, inity

def get_neighbour_random(w, h, x, y, walk_matrix, seed=3451):
	R = np.random.RandomState(seed)
	i, j = R.random_integers(0, walk_matrix.shape[0] - 1), R.random_integers(0, walk_matrix.shape[1] - 1)
	print "i %s j %s" % (i, j)
	walk_x, walk_y = walk_matrix[i][j][0] + x, walk_matrix[i][j][1] + y

	while walk_x <0 or walk_x >= w or walk_y < 0 or walk_y >= h:
		i, j  = R.random_integers(0, walk_matrix.shape[0] - 1), R.random_integers(0, walk_matrix.shape[1] - 1)
		walk_x, walk_y = walk_matrix[i][j][0] + x, walk_matrix[i][j][1] + y
	return walk_x, walk_y

def get_random_loc_w_transition(w, h, x, y, transition_vec, walk_matrix, seed=3451):
	print transition_vec
	idx = weighted_choice(transition_vec)
	row = idx / 3
	col = idx % 3
	walk_x = x + walk_matrix[row][col][0]
	walk_y = y + walk_matrix[row][col][1]

	while walk_x < 0 or walk_x >= w or walk_y < 0 or walk_y >= h:
		row = idx / 3
		col = idx % 3
		walk_x = x + walk_matrix[row][col][0]
		walk_y = y + walk_matrix[row][col][1]

	return walk_x, walk_y

def get_point_density(x, y, walk_matrix, sprite):
	density_matrix = reconstruct_density_matrix(sprite.shape[0], sprite.shape[1], sprite)
	print density_matrix
	print x, y
	density = density_matrix[x][y]
	return density

def update_transition_matrix(x, y, transition_matrix, walk_matrix, sprite):
	import pudb; pudb.set_trace()
	f, s = transition_matrix.shape
	for i in xrange(f):
		for j in xrange(s):
			walk_x, walk_y = x + walk_matrix[i][j][0], y + walk_matrix[i][j][1]
			if not (walk_x < 0 or walk_x >= sprite.shape[0] or walk_y < 0 or walk_x >= sprite.shape[1]):
				if get_point_density(walk_x, walk_y, walk_matrix, sprite) == 0:
					transition_matrix[i][j] = 0
				else:
					transition_matrix[i][j] = get_point_density(walk_x, walk_y, walk_matrix, sprite)
	max = np.max(transition_matrix)
	if max != 0:
		transition_matrix /= max
	return transition_matrix

def gen_rnd_walk_shape(w, h, fill=0.5, seed=123112):
	x, y = get_random_loc(w, h, seed)
	sprite = np.zeros((w, h))
	walk_matrix = np.array([[(-1, 1), (0, 1), (1, 1)], [(-1, 0), (0, 0), (1, 0)], [(-1, -1), (0, -1), (1, -1)]])
	transition_matrix = np.ones((3, 3))
	filled = 0

	xflag_start, xflag_end = False, False
	yflag_start, yflag_end = False, False

	while not (xflag_start and xflag_end) or not (yflag_start and yflag_end) or filled < 0.5:
		print "x: %s, y:%s\n" % (x, y)
		if x == 0:
			xflag_start = True
		if x == w:
			xflag_end = True
		if y == 0:
			yflag_start = True
		if y == h:
			yflag_end = True
		if sprite[x][y] == 1:
			continue

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
			x, y = get_random_loc_w_transition(w, h, x, y, transition_vec, walk_matrix)
		filled = np.count_nonzero(sprite)/(w * h)
	return sprite

print gen_rnd_walk_shape(8, 8)
