sides, rows, cols = 6, 11, 11
worldsize = rows #size of edge
sectorsPerEdge = cols
sectorsize = worldsize/sectorsPerEdge #four by four sectors per face
sectorCenter = sectorsize/2.0 #helps you find the center point of each sector

def convertIndexToLoc(i):
    if i != None:
        side = i//(rows*cols)
        indexWithinSide = i%(rows*cols)
        row = indexWithinSide//rows
        col = indexWithinSide%cols
        return (side, row, col)

def convertLocToIndex(side, row, col):
	return side*(rows*cols) + row*cols + col

def returnSectorCoords(): #returns relative locations and orientations of sector centers
    dist = worldsize/2.0 #one-dimensional distance away from origin
    coords = [[[None for i in range(cols)] for j in range(rows)] for k in range(sides)]
    sideNames = ["front", "back", "top", "bottom", "left", "right"] #as seen from the "front" orientation
    for side in range(sides):
        for row in range(rows):
            for col in range(cols):
                if sideNames[side] == "front":
                    coords[side][row][col] = ((-dist+col+sectorCenter, -dist, dist-row-sectorCenter), (0, 90, 0))
                elif sideNames[side] == "back":
                    coords[side][row][col] = ((dist-col-sectorCenter, dist, dist-row-sectorCenter), (0, -90, 0))
                elif sideNames[side] == "top":
                    coords[side][row][col] = ((-dist+col+sectorCenter, dist-row-sectorCenter, dist), (0, 0, 0))
                elif sideNames[side] == "bottom":
                    coords[side][row][col] = ((dist-col-sectorCenter, dist-row-sectorCenter, -dist), (0, 180, 0))
                elif sideNames[side] == "left":
                    coords[side][row][col] = ((-dist, dist-col-sectorCenter, dist-row-sectorCenter), (0, 0, -90))
                elif sideNames[side] == "right":
                    coords[side][row][col] = ((dist, -dist+col+sectorCenter, dist-row-sectorCenter), (0, 0, 90))
    
    return coords

def moveSides(side, row, col): #returns new coordinates when event coords move off of one side onto another
    sideNames = ["front", "back", "top", "bottom", "left", "right"]
    if sideNames[side] == "front":
        if row<0:
            side, row = sideNames.index("top"), rows+row
        elif row>=rows:
            side, row, col = sideNames.index("bottom"), rows-(row-rows)-1, cols-col-1
        elif col<0:
            side, col = sideNames.index("left"), cols+col
        elif col>=cols:
            side, col = sideNames.index("right"), col-cols
    elif sideNames[side] == "back":
        if row<0:
            side, row, col = sideNames.index("top"), -row-1, cols-col-1
        elif row>=rows:
            side, row = sideNames.index("bottom"), row-rows
        elif col<0:
            side, col = sideNames.index("right"), cols+col
        elif col>=cols:
            side, col = sideNames.index("left"), col-cols
    elif sideNames[side] == "top":
        if row<0:
            side, row, col = sideNames.index("back"), -row-1, cols-col-1
        elif row>=rows:
            side, row = sideNames.index("front"), row-rows
        elif col<0:
            side, row, col = sideNames.index("left"), -col-1, row
        elif col>=cols:
            side, row, col = sideNames.index("right"), col-cols, rows-row-1
    elif sideNames[side] == "bottom":
        if row<0:
            side, row = sideNames.index("back"), rows+row
        elif row>=rows:
            side, row, col = sideNames.index("front"), rows-(row-rows)-1, cols-col-1
        elif col<0:
            side, row, col = sideNames.index("right"), cols+col, rows-row-1
        elif col>=cols:
            side, row, col = sideNames.index("left"), rows-(col-cols)-1, row
    elif sideNames[side] == "left":
        if row<0:
            side, row, col = sideNames.index("top"), col, -row-1
        elif row>=rows:
            side, row, col = sideNames.index("bottom"), col, cols-(row-rows)-1
        elif col<0:
            side, col = sideNames.index("back"), cols+col
        elif col>=cols:
            side, col = sideNames.index("front"), col-cols
    elif sideNames[side] == "right":
        if row<0:
            side, row, col = sideNames.index("top"), cols-col-1, rows+row
        elif row>=rows:
            side, row, col = sideNames.index("bottom"), cols-col-1, row-rows
        elif col<0: 
            side, col = sideNames.index("front"), cols+col
        elif col>=cols:
            side, col = sideNames.index("back"), col-cols
    return (side, row, col)

def returnDirs(radius):
    sums = set()
    dirs = set()
    for arg in range(radius+1):
        sums.add((arg, radius-arg))
    for coordSum in sums:
        x,y = coordSum
        dirs.add((x,y))
        dirs.add((-x,y))
        dirs.add((x,-y))
        dirs.add((-x,-y))
    return dirs