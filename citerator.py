#Taken from the SO's post:
#http://stackoverflow.com/questions/8979214/iterate-over-2d-array-in-an-expanding-circular-spiral
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


