import numpy 
from matplotlib import pyplot as plt

def circle_around_aclockwise(x, y):
	r = 1
	i, j = x-1, y-1
	while True:
		while i < x + r:
			i += 1
			yield r, (i, j)
		while j < y + r:
			j += 1
			yield r, (i, j)
		while i > x - r:
			i -= 1
			yield r, (i, j)
		while j > y - r:
			j -= 1
			yield r, (i, j)
		r += 1
		j -= 1
		yield r, (i, j)

def circle_around_clockwise(x, y):
	r = 1
	i, j = x-1, y-1
	while True:
		while j < y + r:
			j += 1
			yield r, (i, j)

		while i < x + r:
			i += 1
			yield r, (i, j)

		while j > y - r:
			j -= 1
			yield r, (i, j)

		while i > x - r:
			i -= 1
			yield r, (i, j)

		r += 1
		j -= 1
		yield r, (i, j)

if __name__=="__main__":
	M = numpy.random.rand(100, 100) 
	plt.axis([0, 100, 0, 100])

	ax = plt.gca()
	ax.yaxis.grid(color='gray')
	ax.xaxis.grid(color='gray')
	X = []
	Y = []
	# for (i, j) in M
	i, j = 20, 50
	X.append(i)
	Y.append(j)
	import pudb; pudb.set_trace();
	for (radius, (cx, cy)) in circle_around_clockwise(i, j):
		print str(cx) + " " + str(cy)
		if cx < 0 or cx >= M.shape[0] or cy >= M.shape[0] or cy < 0:
			break
		else:
			X.append(cx)
			Y.append(cy)
	plt.plot(X, Y, 'r-', linewidth=2.0)
	plt.show()

#        if not circle_around(M[i][j], M[cx][cy]):
#           R[cx][cy] = radius - 1
#           break
