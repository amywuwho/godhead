import random

def getRGBA(r, g, b): #converts rgb colors to panda3D's rgba coloring system
	return (r/255.0, g/255.0, b/255.0, 1)

def personHealthColor(hp): #sets person's color based on health
    healthyToAverageR = 245/50.0        #increments of colors based on hp
    healthyToAverageG = (229-60)/50.0
    healthyToAverageB = 26/50.0
    avgToDyingG = 229/25.0
    dyingToDeadR = 255/25.0

    healthyR, healthyG, healthyB = (10, 60, 26)
    avgR, avgG, avgB = (255, 229, 0)
    dyingR, dyingG, dyingB = (255, 0, 0)

    if hp > 50: (r, g, b) = (healthyR+healthyToAverageR*(100-hp), healthyG+healthyToAverageG*(100-hp), healthyB-healthyToAverageB*(100-hp))
    if 25 < hp <= 50: (r, g, b) = (avgR, avgG-avgToDyingG*(50-hp), avgB)
    if hp <= 25: (r, g, b) = (dyingR-dyingToDeadR*(25-hp), dyingG, dyingB)

    return getRGBA(r, g, b)

def colorScheme():       #grass color           #sand color            #water color
    colorSchemes = {1: (getRGBA(5, 100, 20),   getRGBA(100, 75, 0),    getRGBA(4, 121, 136)),   #default
                    2: (getRGBA(181, 6, 21),  getRGBA(242, 66, 128),  getRGBA(120, 184, 168)),  #peppermint
                    3: (getRGBA(201/1.5, 106/1.5, 46/1.5), getRGBA(219/1.5, 147/1.5, 75/1.5), getRGBA(107/1.5, 135/1.5, 107/1.5)),  #dune
                    4: (getRGBA(184/2.0, 220/2.0, 150/2.0), getRGBA(255/2.0, 255/2.0, 157/2.0), getRGBA(2/2.0, 164/2.0, 137/2.0)),  #light swamp
                    5: (getRGBA(27, 150, 5),   getRGBA(131, 230, 56),  getRGBA(25, 63, 40)),    #the world is lava
                    6: (getRGBA(166/2.0, 156/2.0, 173/2.0), getRGBA(245/2.0, 235/2.0, 235/2.0), getRGBA(192/2.0, 246/2.0, 250/2.0))}  #pastels
    index = random.randint(1, 6)
    return colorSchemes[index]

# grassCol = getRGBA(5, 100, 20)
# sandCol = getRGBA(100, 75, 0)
# waterCol = getRGBA(4, 121, 136)
selectCol = getRGBA(236, 1, 253)
highlightCol = getRGBA(255, 255, 255)
healthyCol = getRGBA(10, 60, 26)
averageCol = getRGBA(255, 229, 0)
dyingCol = getRGBA(255, 0, 0)
skyCol = getRGBA(61, 88, 86)
darkSkyCol = getRGBA(30, 59, 89)
evenDarkerSky = getRGBA(3, 6, 9)
white = getRGBA(255, 255, 255)
black = getRGBA(0, 0, 0)