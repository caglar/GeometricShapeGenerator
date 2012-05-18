import numpy

def circle_around(x, y):
    r = 1
    i, j = x-1, y-1
    while True:
        while i < x+r:
            i += 1
            yield r, (i, j)
        while j < y+r:
            j += 1
            yield r, (i, j)
        while i > x-r:
            i -= 1
            yield r, (i, j)
        while j > y-r:
            j -= 1
            yield r, (i, j)
        r += 1
        j -= 1
        yield r, (i, j)

if __name__=="__main__":
    M = numpy.random.rand(100, 100)
    R = numpy.zeros(M.shape, dtype=numpy.int)
    # for (i, j) in M
    i, j = 0, 0
    for (radius, (cx, cy)) in circle_around(i, j):
        print str(cx) + " " + str(cy)
        
        if not circle_around(M[i][j], M[cx][cy]):
           R[cx][cy] = radius - 1
           break

