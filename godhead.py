import sys, math, os, random, copy
from panda3d.core import *
loadPrcFileData('', 'window-title godhead')
loadPrcFileData('', 'win-size 2500 1500')
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.task import Task
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.task.TaskManagerGlobal import taskMgr
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import *
from colors import *
from collections import deque
from positionCalculations import *
#I would like to thank the Panda3D manual, without which I would know nothing.

class godhead(ShowBase):

#######################
## splash screens/UI ##
#######################
	def __init__(self):
		ShowBase.__init__(self)
		self.accept('escape', sys.exit)
		self.width=2500
		self.height=1500
		self.splashScreen = True
		self.gameEnded = False
		self.startSittingByFire = False
		self.lostSittingByFire = False
		base.setBackgroundColor(darkSkyCol)
		self.textObj = OnscreenText(text='GODHEAD', pos = (0, .1), scale = .1, fg = white)
		self.instrObj = OnscreenText(text='click to begin.', pos=(0, .02), scale = .05, fg = white)
		if self.splashScreen == True:
			self.accept('mouse1', self.sitByFire)
			# self.accept('mouse1', self.sitByFire, [True, False]) #test win
			# self.accept('mouse1', self.sitByFire, [False, True]) #test loss

	def startSitByFire(self, count=0):
		if count == 0:
			self.textObj.destroy()
			self.instrObj.destroy()
			self.startSittingByFire = True
			base.setBackgroundColor(evenDarkerSky)
			self.fire = OnscreenImage(image = 'art/fire.png', pos = (0, 0, -.1), scale=(0.5, 1, 0.5))
			self.fire.setTransparency(TransparencyAttrib.MAlpha)
			self.fireSound = base.loader.loadSfx("music/fireSound.ogg") #from "FIRE Fire Sound Effect" by Audio Productions; https://www.youtube.com/watch?v=vOtzPWx7HXU
			self.textSound1 = base.loader.loadSfx("music/text1.ogg") #text and warp sound bites originally from the game Undertale by Toby Fox
			self.textSound2 = base.loader.loadSfx("music/text2.ogg")
			self.textSound3 = base.loader.loadSfx("music/text3.ogg")
			self.textSound5 = base.loader.loadSfx("music/text5.ogg")
			self.warpTransition = base.loader.loadSfx("music/warp.ogg")
			self.fireSound.setLoop(0)
			self.fireSound.play()
		elif count == 1:
			self.text1 = OnscreenImage(image = 'art/text1.png', scale = (0.4, 1, 0.13), pos=(-.85, 0, .8))
			self.text1.setTransparency(TransparencyAttrib.MAlpha)
			self.textSound1.play()
		elif count == 2:
			self.text2 = OnscreenImage(image = 'art/text2.png', scale = (0.2, 1, 0.1), pos=(.95, 0, .7))
			self.text2.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound1.status() == self.textSound1.PLAYING: self.textSound1.stop()
			self.textSound2.play()
		elif count == 3:
			self.text3 = OnscreenImage(image = 'art/text3.png', scale = (0.4, 1, 0.13), pos=(-.85, 0, .4))
			self.text3.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound2.status() == self.textSound2.PLAYING: self.textSound2.stop()
			self.textSound3.play()
		elif count == 4:
			self.text4 = OnscreenImage(image = 'art/text4.png', scale = (0.2, 1, 0.1), pos=(.95, 0, .2))
			self.text4.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound3.status() == self.textSound3.PLAYING: self.textSound3.stop()
			self.textSound2.play()
		elif count == 5:
			self.text5 = OnscreenImage(image = 'art/text5.png', scale = (0.4, 1, 0.18), pos=(-.85, 0, 0))
			self.text5.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound2.status() == self.textSound2.PLAYING: self.textSound2.stop()
			self.textSound5.play()
		elif count == 6:
			self.text6 = OnscreenImage(image = 'art/text6.png', scale = (0.4, 1, 0.13), pos=(-.85, 0, -.3))
			self.text6.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound5.status() == self.textSound5.PLAYING: self.textSound5.stop()
			self.textSound1.play()
		elif count == 7:
			self.text7 = OnscreenImage(image = 'art/text7.png', scale = (0.2, 1, 0.1), pos=(.95, 0, -.4))
			self.text7.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound1.status() == self.textSound1.PLAYING: self.textSound1.stop()
			self.textSound2.play()
		elif count == 8:
			self.text8 = OnscreenImage(image = 'art/text8.png', scale = (0.4, 1, 0.13), pos=(-.85, 0, -.6))
			self.text8.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound2.status() == self.textSound2.PLAYING: self.textSound2.stop()
			self.textSound1.play()
		elif count == 9:
			self.enterGame = DirectButton(relief=0, image='art/entergame.png', scale = (0.4, 1, 0.1), pos=(0, 0, -.8), 
											command = self.startGame, commandButtons=[DGG.RMB], clickSound = self.warpTransition)
		self.accept('mouse1', self.startSitByFire, [count+1])

	def lostSitByFire(self, count=0):
		if count == 0:
			self.lostSittingByFire = True
			base.setBackgroundColor(evenDarkerSky)
			self.fire = OnscreenImage(image = 'art/fire.png', pos = (0, 0, -.1), scale=(0.5, 1, 0.5))
			self.fire.setTransparency(TransparencyAttrib.MAlpha)
			self.fireSound = base.loader.loadSfx("music/fireSound.ogg") #from "FIRE Fire Sound Effect" by Audio Productions; https://www.youtube.com/watch?v=vOtzPWx7HXU
			self.textSound1 = base.loader.loadSfx("music/text1.ogg") #text and warp sound bites originally from the game Undertale by Toby Fox
			self.textSound2 = base.loader.loadSfx("music/text2.ogg")
			self.textSound3 = base.loader.loadSfx("music/text3.ogg")
			self.textSound5 = base.loader.loadSfx("music/text5.ogg")
			self.warpTransition = base.loader.loadSfx("music/warp.ogg")
			self.fireSound.setLoop(0)
			self.fireSound.play()
			if self.gameEnded == True:
				self.gameOverText.destroy()
				self.survivalText.destroy()
				self.restartText.destroy()
		elif count == 1:
			self.losttext1 = OnscreenImage(image = 'art/losttext1.png', scale = (0.4, 1, .13), pos=(-.85, 0, .8))
			self.losttext1.setTransparency(TransparencyAttrib.MAlpha)
			self.textSound1.play()
		elif count == 2:
			self.losttext2 = OnscreenImage(image = 'art/losttext2.png', scale = (0.25, 1, 0.1), pos=(.95, 0, .6))
			self.losttext2.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound1.status() == self.textSound1.PLAYING: self.textSound1.stop()
			self.textSound2.play()
		elif count == 3:
			self.losttext3 = OnscreenImage(image = 'art/losttext3.png', scale = (0.5, 1, 0.2), pos=(-.75, 0, .3))
			self.losttext3.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound2.status() == self.textSound2.PLAYING: self.textSound2.stop()
			self.textSound3.play()
		elif count == 4:
			self.losttext4 = OnscreenImage(image = 'art/losttext4.png', scale = (0.45, 1, 0.16), pos=(-.8, 0, -.1))
			self.losttext4.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound3.status() == self.textSound3.PLAYING: self.textSound3.stop()
			self.textSound1.play()
		elif count == 5:
			self.enterGame = DirectButton(relief=0, image='art/entergame.png', scale = (0.4, 1, 0.1), pos=(0, 0, -.8), 
												command = self.startGame, commandButtons=[DGG.RMB], clickSound = self.warpTransition)
		self.accept('mouse1', self.lostSitByFire, [count+1])

	def wonSitByFire(self, count=0):
		if count == 0:
			self.wonSittingByFire = True
			base.setBackgroundColor(evenDarkerSky)
			self.fire = OnscreenImage(image = 'art/fire.png', pos = (0, 0, -.1), scale=(0.5, 1, 0.5))
			self.fire.setTransparency(TransparencyAttrib.MAlpha)
			self.fireSound = base.loader.loadSfx("music/fireSound.ogg") #from "FIRE Fire Sound Effect" by Audio Productions; https://www.youtube.com/watch?v=vOtzPWx7HXU
			self.textSound1 = base.loader.loadSfx("music/text1.ogg") #text and warp sound bites originally from the game Undertale by Toby Fox
			self.textSound2 = base.loader.loadSfx("music/text2.ogg")
			self.textSound3 = base.loader.loadSfx("music/text3.ogg")
			self.textSound5 = base.loader.loadSfx("music/text5.ogg")
			self.warpTransition = base.loader.loadSfx("music/warp.ogg")
			self.fireSound.setLoop(0)
			self.fireSound.play()
		elif count == 1:
			self.wontext1 = OnscreenImage(image = 'art/wontext1.png', scale = (0.6, 1, .23), pos=(-1, 0, .7))
			self.wontext1.setTransparency(TransparencyAttrib.MAlpha)
			self.textSound1.play()
		elif count == 2:
			self.wontext2 = OnscreenImage(image = 'art/wontext2.png', scale = (.6, 1, 0.35), pos=(-1, 0, 0))
			self.wontext2.setTransparency(TransparencyAttrib.MAlpha)
			if self.textSound1.status() == self.textSound1.PLAYING: self.textSound1.stop()
			self.textSound5.play()
		self.accept('mouse1', self.wonSitByFire, [count+1])

	def sitByFire(self, gameWon = False, gameLost = False):
		if gameWon == False and gameLost == False:
			self.startSitByFire()
		elif gameLost == True:
			self.lostSitByFire()
		elif gameWon == True:
			self.wonSitByFire()

	def erase(self):
			self.timerText.destroy()
			self.helpMenuButton.destroy()
			self.eventText.destroy()
			self.world.remove_node()
			taskMgr.remove('grassSpread')
			taskMgr.remove('grassDie')
			taskMgr.remove('treeSpread')
			taskMgr.remove('treeDie')
			taskMgr.remove('personAI')
			taskMgr.remove('rotateWorld')
			taskMgr.remove('highlightSector')
			if self.moveOnPresent == True:
				self.moveOnButton.destroy()
			if self.imDonePresent == True:
				self.imDoneButton.destroy()

	def gameOver(self):
		if self.isEllisDead == True:
			self.splashScreen = True
			self.gameEnded = True
			self.erase()
			base.setBackgroundColor(darkSkyCol)
			self.soundtrack.stop()
			self.gameOverText = OnscreenText(text='life is extinguished.', pos=(0, .1), scale = .1, fg = white)
			self.survivalText = OnscreenText(text='humanity survived for '+str(self.time)+' years.', pos=(0, .02), scale = .06, fg = white)
			self.restartText = OnscreenText(text='click to continue.', pos=(0, -.05), scale = .05, fg = white)
			self.accept('mouse1', self.sitByFire, [False, True])

	def gameWon(self):
		self.splashScreen = True
		self.gameEnded = True
		self.erase()
		self.soundtrack.stop()
		self.sitByFire(gameWon=True)

#############	
## godhead ##
#############
	def startGame(self):
		if self.splashScreen == False: return
		self.splashScreen = False
		if self.gameEnded == False:
			self.loadBackground()
			self.soundtrack = base.loader.loadSfx("music/firewatchSoundtrack.ogg")
			self.helpMenu()
			self.movedOn = False
		if self.startSittingByFire == True:
			if self.fireSound.status() == self.fireSound.PLAYING: self.fireSound.stop()
			self.text1.destroy()
			self.text2.destroy()
			self.text3.destroy()
			self.text4.destroy()
			self.text5.destroy()
			self.text6.destroy()
			self.text7.destroy()
			self.text8.destroy()
			self.fire.destroy()
			self.enterGame.destroy()
			self.startSittingByFire = False
		if self.lostSittingByFire == True:
			if self.fireSound.status() == self.fireSound.PLAYING: self.fireSound.stop()
			self.losttext1.destroy()
			self.losttext2.destroy()
			self.losttext3.destroy()
			self.losttext4.destroy()
			self.fire.destroy()
			self.enterGame.destroy()
			self.lostSittingByFire = False
		base.setBackgroundColor(skyCol)
		self.soundtrack.play()
		self.grassCol, self.sandCol, self.waterCol = colorScheme()
		self.sides = 6
		self.rows = 11
		self.cols = self.rows
		self.pickedSector = None
		self.hiSect = None
		self.prevHiColor = None
		self.selSect = None
		self.selectorPresent = False
		self.camDistance = -3.75*self.rows
		self.moveDelay = 1
		self.loadWorld()
		self.camera.setPos(0, self.camDistance, 0)

		base.disableMouse()
		self.menuClosed = False
		self.helpMenuButton = DirectButton(relief=0, pos=(-1.6, 0, -.9), scale = (.03, 1, .03), image="art/questionmark.png", command=self.helpMenu)
		self.helpMenuButton.setTransparency(TransparencyAttrib.MAlpha)
		self.eventText = OnscreenText(text= '[1] flood; [2] drought; [3] sandstorm; [4] plant tree; [5] cut down tree', pos = (.9, .95), scale = .05, fg= white)
		self.moveOnPresent = False
		self.imDonePresent = False
		
		self.rotating  = False
		self.gameEnded = False
		self.lastX, self.lastY = 0, 0
		self.rotateWorld = taskMgr.add(self.rotateWorld, 'rotateWorld') #from Panda3D chessboard tutorial
		self.mousePressed()
		self.keyPressed()
		self.time = 0
		self.timerText = OnscreenText(text=str(self.time)+" years", pos = (1.25, 0), scale=.075, fg=white, mayChange=True)
		taskMgr.doMethodLater(2, self.worldTime, 'worldTime')
		taskMgr.add(self.worldTimer, 'worldTimer')
		self.highlightSector = taskMgr.add(self.highlightSector, 'highlightSector')


		self.picker = CollisionTraverser() #from Panda3D Manual: Clicking On 3D Objects
		self.pickerHandler = CollisionHandlerQueue()
		self.pickerNode = CollisionNode('mouseRay')
		self.pickerNP = camera.attachNewNode(self.pickerNode)
		self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
		self.pickerRay = CollisionRay()
		self.pickerNode.addSolid(self.pickerRay)
		self.picker.addCollider(self.pickerNP, self.pickerHandler)

		self.Person() #load character
		self.isEllisDead = False
		self.isEllisMoving = False
	
#############
## buttons ##
#############

	def helpMenu(self):
		helpText = """
		The world is in your hands. Help humanity survive as long as possible 
		by manipulating the landscape to give them access to trees and water...
		or hurt them by preventing them from doing either.

		Click and drag to rotate the globe. Mouse over a sector and hit SPACE
		to select it, then you can use arrow keys to switch sectors easily. Every
		event you enact on the world originates from your selected square, but be 
		careful: the terrain changes depending on its surroundings.

		Use the num keys to generate events. The tools at your disposal are:
		[1] flood  [2] drought  [3] sandstorm  [4] plant tree  [5] cut down tree

		Do what you will with this world, but there are consequences. Now go on.
		Go. Seriously.

		Hit escape to quit.
		"""
		self.helpMenuDialog = OkDialog(dialogName="help", text=helpText, command=self.helpMenuCleanup)

	def helpMenuCleanup(self, *args):
		self.menuClosed = True
		self.helpMenuDialog.cleanup()

	def moveOn(self):
		self.gameEnded = True
		self.splashScreen = True
		self.movedOn = True
		self.erase()
		self.startGame()


######################
## world generation ##
######################

	def loadWorld(self):
		self.terrainTypes = ["Sand", "Water", "Grass"]
		self.terrainBiasSand = ["Sand", "Sand", "Water", "Grass"] 
		self.terrainBiasWater = ["Water", "Water", "Sand", "Grass"]
		self.terrainBiasGrass = ["Grass", "Grass", "Sand", "Water"]
		self.prevTerrain = None

		self.worldsize = self.rows #size of edge
		self.sectorsPerEdge = self.cols
		self.sectorsize = self.worldsize/(self.sectorsPerEdge*1.0)
		self.sectorCenter = self.sectorsize/2.0 #helps you find the center point of each sector
		self.personSideStart, self.personRowStart, self.personColStart = 0, self.rows//2, self.cols//2

		self.world = self.loader.loadModel("models/cubeworld")
		self.world.reparentTo(render)
		self.world.setScale(1, 1, 1)
		self.world.setPos(0, 0, 0)
		self.worldH, self.worldP = 0, 0
		self.rotateX = 0
		self.rotateY = 0
		#randomly generate a terrain map
		self.sectorCoords = returnSectorCoords()
		self.sectors = [None for i in range(len(self.sectorCoords)*len(self.sectorCoords[0]*len(self.sectorCoords[0][0])))]
		self.sectorTypes = [[[None for col in range(self.cols)] for row in range(self.rows)] for side in range(self.sides)]
		self.treeLocs = [[[0 for col in range(self.cols)] for row in range(self.rows)] for side in range(self.sides)]
		i = 0
		for side in range(self.sides):
			for row in range(self.rows):
				for col in range(self.cols):
					pos, hpr = self.sectorCoords[side][row][col] #gives a list of xyz pos coordinates and hpr coordinates
					if self.prevTerrain == None:
						terrain = self.terrainTypes[random.randint(0, len(self.terrainTypes)-1)]
						self.prevTerrain = terrain
					elif (side, row, col) == (self.personSideStart, self.personRowStart, self.personColStart): 
						terrain = "Sand" #person always starts on sand
						self.prevTerrain = terrain
					else:
						if self.prevTerrain == "Sand": terrain = self.terrainBiasSand[random.randint(0, len(self.terrainBiasSand)-1)]
						elif self.prevTerrain == "Water": terrain = self.terrainBiasWater[random.randint(0, len(self.terrainBiasWater)-1)]
						elif self.prevTerrain == "Grass": terrain = self.terrainBiasGrass[random.randint(0, len(self.terrainBiasGrass)-1)]
						self.prevTerrain = terrain


					if terrain == "Sand":
						self.Sand(pos, hpr, i)
						self.sectorTypes[side][row][col] = "sand%d" % (i)
					elif terrain == "Water":
						self.Water(pos, hpr, i)
						self.sectorTypes[side][row][col] = "water%d" % (i)
					elif terrain == "Grass":
						treePresent = random.randint(0,1)
						self.treeLocs[side][row][col] = treePresent
						self.Grass(pos, hpr, i, treePresent)
						self.sectorTypes[side][row][col] = "grass%d" % (i)
					i += 1

		taskMgr.doMethodLater(2, self.grassSpread, 'grassSpread')

	def loadBackground(self):
		#light tutorial from Panda3D manual
	
		base.setBackgroundColor(skyCol)

		directionalLight = DirectionalLight('directionalLight')
		directionalLight.setColor(VBase4(0.5, 0.5, 0.5, 1))
		directionalLight.setSpecularColor((1, 1, 1, 1))
		directionalLightNP = render.attachNewNode(directionalLight)
		directionalLightNP.setHpr(120, 120, 0)
		render.setLight(directionalLightNP)

		directionalLight = DirectionalLight('directionalLight')
		directionalLight.setColor(VBase4(0.5, 0.5, 0.5, 1))
		directionalLight.setSpecularColor((1, 1, 1, 1))
		directionalLightNP = render.attachNewNode(directionalLight)
		directionalLightNP.setHpr(-120, -120, 0)
		render.setLight(directionalLightNP)

		directionalLight = DirectionalLight('directionalLight')
		directionalLight.setColor(VBase4(0.5, 0.5, 0.5, 1))
		directionalLight.setSpecularColor((1, 1, 1, 1))
		directionalLightNP = render.attachNewNode(directionalLight)
		directionalLightNP.setHpr(-45, 0, 0)
		render.setLight(directionalLightNP)

		directionalLight = DirectionalLight('directionalLight')
		directionalLight.setColor(VBase4(0.5, 0.5, 0.5, 1))
		directionalLight.setSpecularColor((1, 1, 1, 1))
		directionalLightNP = render.attachNewNode(directionalLight)
		directionalLightNP.setHpr(120, -120, 0)
		render.setLight(directionalLightNP)

		directionalLight = DirectionalLight('directionalLight')
		directionalLight.setColor(VBase4(0.5, 0.5, 0.5, 1))
		directionalLight.setSpecularColor((1, 1, 1, 1))
		directionalLightNP = render.attachNewNode(directionalLight)
		directionalLightNP.setHpr(-120, 120, 0)
		render.setLight(directionalLightNP)

		
###############
## character ##
###############

	def Person(self): #"Ellis"
		self.personscale = self.worldsize/32.0
		self.hp = 100
		self.person = self.loader.loadModel("models/ellis")
		self.person.reparentTo(self.world)
		self.person.setScale(self.personscale, self.personscale, self.personscale)
		self.personSide, self.personRow, self.personCol = self.personSideStart, self.personRowStart, self.personColStart
		pos, hpr = self.sectorCoords[self.personSide][self.personRow][self.personCol]
		self.person.setPos(pos)
		self.person.setHpr(hpr)
		taskMgr.doMethodLater(1, self.personAI, 'personAI')

	def personAI(self, task):
		if self.isPersonDying((self.personSide, self.personRow, self.personCol)):
			self.hp -= 2
			if self.hp <= 0: 
				self.isEllisDead = True
				self.gameOver()
			if self.isEllisMoving == False:
				self.movePerson()
		else: 
			if self.hp < 100: self.hp += 1

		self.person.setColor(personHealthColor(self.hp))
		return Task.again

	def isPersonDying(self, (side, row, col)):
		dirs = [(-1, -1), (-1, 0), (-1, +1),
				( 0, -1),		   ( 0, +1),
				(+1, -1), (+1, 0), (+1, +1)]
		treesFound = 0
		waterFound = 0
		minTrees = 3
		minWater = 2
		for direction in dirs:
			(drow, dcol) = direction
			checkSide, checkRow, checkCol = (side, row+drow, col+dcol)
			if checkRow<0 or checkRow>=self.rows or checkCol<0 or checkCol>=self.cols:
				checkSide, checkRow, checkCol = moveSides(checkSide, checkRow, checkCol)
				if (checkRow<0) or (checkRow>=self.rows) or (checkCol<0) or (checkCol >= self.cols): continue
			if self.sectorTypes[checkSide][checkRow][checkCol].startswith("water"): waterFound += 1
			if self.treeLocs[checkSide][checkRow][checkCol] == 1: treesFound+=1
		if (treesFound<minTrees) or (waterFound<minWater): #if not enough trees/water
			return True
		else:
			return False
	
	def search(self, (side, row, col), radius=1):
		if radius >= self.rows*4: return None #if you've searched all the way around the globe and there is nothing
		if not self.isPersonDying((side, row, col)):
			return (side, row, col)
		else:
			dirs = returnDirs(radius)
			for direction in dirs:
				drow, dcol = direction
				checkSide, checkRow, checkCol = moveSides(self.personSide, self.personRow+drow, self.personCol+dcol)
				if checkRow<0 or checkRow>=self.rows or checkCol<0 or checkCol>=self.cols: continue
				if self.isValid((checkSide, checkRow, checkCol)):
					if not self.isPersonDying((checkSide, checkRow, checkCol)):
						return (checkSide, checkRow, checkCol)
			return self.search((side, row, col), radius+1) 
	
	def findPath(self, origin, target): #breadth-first search algorithm suggested by Aaron Meyers
										#adapted from bfs explanation on http://bryukh.com/labyrinth-algorithms/
		dirs = [(-1, -1), (-1, 0), (-1, +1),
				( 0, -1),		   ( 0, +1),
				(+1, -1), (+1, 0), (+1, +1)]
		visited = set()
		starts = deque()
		starts.append(([], origin))
		while len(starts)>0:
			path, (side, row, col) = starts.popleft()
			for drow, dcol in dirs:
				newPath = copy.deepcopy(path)
				newSide, newRow, newCol = moveSides(side, row+drow, col+dcol)
				if newRow<0 or newRow>=self.rows or newCol<0 or newCol>=self.cols: continue
				if (newSide, newRow, newCol) in visited: continue
				newPath.append((newSide, newRow, newCol))
				visited.add((newSide, newRow, newCol))
				if (newSide, newRow, newCol) == target:
					return newPath
				if self.isValid((newSide, newRow, newCol)):
					starts.append((newPath, (newSide, newRow, newCol)))
		return None

	def movePerson(self): #finds path and prepares Ellis to move
		if not self.isPersonDying((self.personSide, self.personRow, self.personCol)): 
			return
		else:
			target = self.search((self.personSide, self.personRow, self.personCol))
			if target != None:
				path = self.findPath((self.personSide, self.personRow, self.personCol), target)
				if path != None:
					self.isEllisMoving = True
					taskMgr.doMethodLater(self.moveDelay, self.move, 'move', extraArgs = [path, target])
				else: self.randomMove()
	
	def move(self, path, target): #actual move function
		if len(path) == 0:
			self.isEllisMoving = False 
			return
		else:
			side, row, col = path[0]
			if self.isValid((side, row, col)):
				self.personSide, self.personRow, self.personCol = side, row, col
				pos, hpr = self.sectorCoords[self.personSide][self.personRow][self.personCol]
				self.person.setPos(pos)
				self.person.setHpr(hpr)
				taskMgr.doMethodLater(self.moveDelay, self.move, 'move', extraArgs = [path[1:], target])
			else: 
				self.isEllisMoving = False #no longer moving on a path
				self.randomMove()

	def randomMove(self, depth=0):
		if depth>50: return #prevent exceeding maximum recursion depth if there's a situation where Ellis can't move :(
		dirs = [(-1, -1), (-1, 0), (-1, +1),
				( 0, -1),		   ( 0, +1),
				(+1, -1), (+1, 0), (+1, +1)]
		randomDirection = dirs[random.randint(0, 7)] #just move in a random direction and hope for the best
		(drow, dcol) = randomDirection
		randSide, randRow, randCol = (self.personSide, self.personRow+drow, self.personCol+dcol)
		if randRow<0 or randRow>=self.rows or randCol<0 or randCol>=self.cols:
			(randSide, randRow, randCol) = moveSides(randSide, randRow, randCol)
			if (randRow<0) or (randRow>=self.rows) or (randCol<0) or (randCol>=self.cols): return
		if self.isValid((randSide, randRow, randCol)):
			self.personSide, self.personRow, self.personCol = randSide, randRow, randCol
			pos, hpr = self.sectorCoords[self.personSide][self.personRow][self.personCol]
			self.person.setPos(pos)
			self.person.setHpr(hpr)
			return
		else: self.randomMove(depth+1)

	def isValid(self, (side, row, col)):
		if not self.sectorTypes[side][row][col].startswith('water') and self.treeLocs[side][row][col] == 0:
			return True
		else: return False

#####################
## selection tasks ##
#####################

	def mousePressed(self):
		self.accept('mouse1', self.rotate)
		self.accept('mouse1-up', self.rotate)

	def keyPressed(self):
		self.accept('space', self.mouseSelectSector)
		self.accept('arrow_left', self.keySelectSector, [0, -1])
		self.accept('arrow_right', self.keySelectSector, [0, +1])
		self.accept('arrow_up', self.keySelectSector, [-1, 0])
		self.accept('arrow_down', self.keySelectSector, [+1, 0])
		self.accept('1', self.flood, [(None, None, None)])
		self.accept('2', self.drought, [(None, None, None)])
		self.accept('3', self.drought, [(None, None, None), 0, 0, 3])
		self.accept('4', self.growTree, [(None, None, None)])
		self.accept('5', self.destroyTree, [(None, None, None)])


	def keySelectSector(self, drow, dcol):
		if self.selSect == None: return
		side, row, col = convertIndexToLoc(self.selSect)
		row, col = row+drow, col+dcol
		if (row < 0) or (row >= self.rows) or (col < 0) or (col >= self.cols):
			(side, row, col) = moveSides(side, row, col)
		self.selSect = convertLocToIndex(side, row, col)
		selectPos, selectHpr = self.sectorCoords[side][row][col]
		self.selector.setPos(selectPos)
		self.selector.setHpr(selectHpr)

	def mouseSelectSector(self):
		if self.mouseWatcherNode.hasMouse():
			if self.selSect == None and self.selectorPresent == False:
				self.selSect = self.hiSect
				if self.selSect == None: return #if you're off the board and don't have a sector highlighted
				side, row, col = convertIndexToLoc(self.selSect)
				selectPos, selectHpr = self.sectorCoords[side][row][col]
				self.selector = loader.loadModel("models/selector")
				self.selector.reparentTo(self.world)
				self.selector.setPos(selectPos)
				self.selector.setHpr(selectHpr)
				self.selector.setScale(.5, .5, .5)
				self.selectorPresent = True
			else:
				if self.hiSect != None:
					self.selSect = self.hiSect
				side, row, col = convertIndexToLoc(self.selSect)
				selectPos, selectHpr = self.sectorCoords[side][row][col]
				self.selector.setPos(selectPos)
				self.selector.setHpr(selectHpr)

	def rotate(self): #toggles whether or not the world is rotating
		if self.startSittingByFire == True or self.lostSittingByFire: return
		if self.rotating == True: self.rotating = False
		else: 
			self.rotating = True
			if self.mouseWatcherNode.hasMouse():
				self.lastX, self.lastY = self.mouseWatcherNode.getMouse()
		if self.menuClosed == True or self.movedOn == True: #checks to make sure on-screen menu/buttons haven't toggled rotating
			self.rotating = False
			self.menuClosed = False
			self.movedOn = False

	def highlightSector(self, task): #referenced from Panda3D Manual: Clicking On 3D Objects 
									 #& Example for Clicking on 3D Objects
									 #and sample chessboard.py
		self.pickedSector = None #changes color of highlighted sector back to original color
		if self.hiSect != None:
			self.sectors[self.hiSect].setColor(self.prevHiColor)
			self.hiSect = None

		if self.mouseWatcherNode.hasMouse():
			mpos = self.mouseWatcherNode.getMouse()
			self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

			self.picker.traverse(render)
			if self.pickerHandler.getNumEntries() > 0:
				self.pickerHandler.sortEntries()
				self.pickedSector = self.pickerHandler.getEntry(0).getIntoNode().getTag('terrain')
				if self.pickedSector != None and self.hiSect == None and self.pickedSector != '':
					i = int(self.pickedSector)
					self.prevHiColor = self.sectors[i].getColor()
					self.sectors[i].setColor(highlightCol)
					self.hiSect = i
		return Task.cont
	
	def rotateWorld(self, task): #adapted from mouse-Modes demo (Panda3D samples)
		if self.rotating == True:
			if self.mouseWatcherNode.hasMouse():
				(mx, my) = self.mouseWatcherNode.getMouse()
				if mx != self.lastX and my != self.lastY:
					if 45 < self.worldH < 270:
						(dx, dy) = (mx-self.lastX, -(my-self.lastY))
						self.rotateX += dx
						self.rotateY -= dy
						self.worldDelta = (dx**2+dy**2)**0.5
						self.time += int(self.worldDelta*5//1) #makes time go faster when you rotate the world
						self.lastX, self.lastY = mx, my

						self.mouseMagnitude = 20
						self.worldH = (self.rotateX*self.mouseMagnitude)%360
						self.worldP = (self.rotateY*self.mouseMagnitude)%360
						self.world.setHpr(self.worldH, self.worldP, 0)
					else:
						(dx, dy) = (mx-self.lastX, -(my-self.lastY))
						self.rotateX += dx
						self.rotateY += dy
						self.worldDelta = (dx**2+dy**2)**0.5
						self.time += int(self.worldDelta*5//1)
						self.lastX, self.lastY = mx, my

						self.mouseMagnitude = 20
						self.worldH = (self.rotateX*self.mouseMagnitude)%360
						self.worldP = (self.rotateY*self.mouseMagnitude)%360
						self.world.setHpr(self.worldH, self.worldP, 0)
		return Task.cont
	
##########
## time ##
##########

	def worldTime(self, task):
		if self.gameEnded == False:
			self.time += 1
			if (self.time >= 100 and self.moveOnPresent == False and self.imDonePresent == False 
				and not self.isPersonDying((self.personSide, self.personRow, self.personCol)) and self.isEllisMoving == False):
				#adds 'continue' and 'quit' buttons
				self.moveOnButton = DirectButton(relief=0, pos=(1.2, 0, -.75), scale = (.12, 1, .04), image="art/moveon.png", command=self.moveOn)
				self.moveOnButton.setTransparency(TransparencyAttrib.MAlpha)
				self.imDoneButton = DirectButton(relief=0, pos=(1.2, 0, -.85), scale = (.12, 1, .04), image="art/imdone.png", command=self.gameWon)
				self.imDoneButton.setTransparency(TransparencyAttrib.MAlpha)
				self.moveOnPresent = True
				self.imDonePresent = True
			if (self.moveOnPresent == True and self.imDonePresent == True 
				and (self.isPersonDying((self.personSide, self.personRow, self.personCol)) or self.isEllisMoving == True)):
				self.moveOnButton.destroy()
				self.imDoneButton.destroy()
				self.moveOnPresent = False
				self.imDonePresent = False
			return Task.again

	def worldTimer(self, task):
		if self.gameEnded == False:
			self.timerText.setText(str(self.time)+" years elapsed")
			return Task.cont

################################
## terrains and terrain types ##
################################

	def Sand(self, pos, hpr, i):
		self.sectors[i] = loader.loadModel("models/terrain-base")
		self.sectors[i].reparentTo(self.world)
		self.sectors[i].setScale(.5, .5, .5)
		self.sectors[i].setPos(pos)
		self.sectors[i].setHpr(hpr)
		self.sectors[i].setColor(self.sandCol)
		self.sectors[i].find("**/Cube").node().setTag('terrain', str(i))


	def Water(self, pos, hpr, i):
		self.sectors[i] = loader.loadModel("models/terrain-base")
		self.sectors[i].reparentTo(self.world)
		self.sectors[i].setScale(.5, .5, .5)
		self.sectors[i].setPos(pos)
		self.sectors[i].setHpr(hpr)
		self.sectors[i].setColor(self.waterCol)
		self.sectors[i].find("**/Cube").node().setTag('terrain', str(i))


	def Grass(self, pos, hpr, i, treePresent):
		self.pos = pos
		self.hpr = hpr
		self.sectors[i] = loader.loadModel("models/terrain-base")
		self.sectors[i].reparentTo(self.world)
		self.sectors[i].setScale(.5, .5, .5)
		self.sectors[i].setPos(pos)
		self.sectors[i].setHpr(hpr)
		self.sectors[i].setColor(self.grassCol)
		self.sectors[i].find("**/Cube").node().setTag('terrain', str(i))
		if treePresent == True:
			self.Tree(i)
	
	def Tree(self, i):
		side, row, col = convertIndexToLoc(i)
		self.treeLocs[side][row][col] = 1
		self.generateBranch(random.uniform(1, 3), i)
	
	def generateBranch(self, length, i, origin = (0,0,0), angle = (0,0,0), scale=.65, depth=0):
		originX, originY, originZ = origin
		angleH, angleP, angleR = angle
		minLength = .05
		if length <= minLength:
			return None #if it's too small, don't make a tree
		else:
			self.branch = loader.loadModel("models/branch")
			self.branch.reparentTo(self.sectors[i])
			self.branch.setScale(scale, scale, scale)
			self.branch.setPos(origin) #fix the origin issues
			self.branch.setHpr(angle)

            #position calculations
			deltaZ = length*scale*math.cos(angleR)
			deltaXY = length*scale*math.sin(angleR)
			deltaY = deltaXY*math.sin(angleP)
			deltaX = deltaXY*math.cos(angleP)
			newOrigin = (originX+deltaX, originY+deltaY, originZ+deltaZ)

			if depth == 0 : branchNum = random.randint(2, 3)
			else: branchNum = random.randint(0, 2) #makes sure you don't have just trunks
			for branch in range(branchNum):
				deltaAngle = 30
				deltaScale = random.uniform(.5, 1)
				newAngleH = angleH + random.uniform(angleH-deltaAngle, angleH+deltaAngle)
				newAngleP = angleP + random.uniform(angleP-deltaAngle, angleP+deltaAngle)
				newAngle = (newAngleH, newAngleP, angleR)
				newScale = scale * deltaScale
				newLength = length * newScale
				taskMgr.doMethodLater(.15, self.generateBranch, 'branch', extraArgs = [newLength, i, newOrigin, newAngle, newScale, depth + 1])

############
## events ##
############

	def flood(self, (side, row, col), depth=0): #make flood less strong :-0
		if depth == 10: return
		if self.selSect == None: return
		if (side, row, col) == (None, None, None): (side, row, col) = convertIndexToLoc(self.selSect)
		if (row < 0) or (row >= self.rows) or (col < 0) or (col >= self.cols):
			(side, row, col) = moveSides(side, row, col) 
		if (row < 0) or (row >= self.rows) or (col < 0) or (col >= self.cols): return
		if (self.sectorTypes[side][row][col].startswith("water") or self.treeLocs[side][row][col] == 1): return
										#doesn't flood if there's already water or if there is a tree
		i = convertLocToIndex(side, row, col)
		self.sectors[i].setColor(self.waterCol)
		self.sectorTypes[side][row][col] = "water%d" % (i)
		if i == self.hiSect: self.prevHiColor = self.waterCol

		taskMgr.doMethodLater(.25, self.flood, 'flood', extraArgs = [(side, row-1, col), depth+1])
		taskMgr.doMethodLater(.25, self.flood, 'flood', extraArgs = [(side, row+1, col), depth+1])
		taskMgr.doMethodLater(.25, self.flood, 'flood', extraArgs = [(side, row, col-1), depth+1])
		taskMgr.doMethodLater(.25, self.flood, 'flood', extraArgs = [(side, row, col+1), depth+1])

	def drought(self, (side, row, col), drow=0, dcol=0, sunRadius=2, depth=0): #has a defined radius of...sunniness
		if drow+dcol > sunRadius: return
		if self.selSect == None: return
		if (side, row, col) == (None, None, None): (side, row, col) = convertIndexToLoc(self.selSect)
		if (row < 0) or (row >= self.rows) or (col < 0) or (col >= self.cols):
			(side, row, col) = moveSides(side, row, col)
		if (row < 0) or (row >= self.rows) or (col < 0) or (col >= self.cols): return
		if (self.sectorTypes[side][row][col].startswith("sand")): return
										 #doesn't dry up if it's already sand
		if self.treeLocs[side][row][col] == 1: 
			self.destroyTree((side, row, col))
		i = convertLocToIndex(side, row, col)
		self.sectors[i].setColor(self.sandCol)
		self.sectorTypes[side][row][col] = "sand%d" % (i)
		if i == self.hiSect: self.prevHiColor = self.sandCol

		taskMgr.doMethodLater(.25, self.drought, 'drought', extraArgs = [(side, row-1, col), drow+1, dcol, sunRadius, depth+1])
		taskMgr.doMethodLater(.25, self.drought, 'drought', extraArgs = [(side, row+1, col), drow+1, dcol, sunRadius, depth+1])
		taskMgr.doMethodLater(.25, self.drought, 'drought', extraArgs = [(side, row, col-1), drow, dcol+1, sunRadius, depth+1])
		taskMgr.doMethodLater(.25, self.drought, 'drought', extraArgs = [(side, row, col+1), drow, dcol+1, sunRadius, depth+1])
		taskMgr.doMethodLater(.25, self.drought, 'drought', extraArgs = [(side, row-1, col-1), drow+1, dcol+1, sunRadius, depth+1])
		taskMgr.doMethodLater(.25, self.drought, 'drought', extraArgs = [(side, row-1, col+1), drow+1, dcol+1, sunRadius, depth+1])
		taskMgr.doMethodLater(.25, self.drought, 'drought', extraArgs = [(side, row+1, col-1), drow+1, dcol+1, sunRadius, depth+1])
		taskMgr.doMethodLater(.25, self.drought, 'drought', extraArgs = [(side, row+1, col+1), drow+1, dcol+1, sunRadius, depth+1])

	def growTree(self, (side, row, col)):
		if self.selSect == None: return
		if (side, row, col) == (None, None, None): (side, row, col) = convertIndexToLoc(self.selSect)
		if (self.sectorTypes[side][row][col].startswith("grass") and self.treeLocs[side][row][col] == 0
			and convertLocToIndex(side, row, col) != convertLocToIndex(self.personSide, self.personRow, self.personCol)):
			i = convertLocToIndex(side, row, col)
			self.Tree(i)
			self.sectorTypes[side][row][col] = "grass%d" % (i)
	
	def destroyTree(self, (side, row, col)):
		if self.selSect == None: return
		if (side, row, col) == (None, None, None): (side, row, col) = convertIndexToLoc(self.selSect)
		if self.treeLocs[side][row][col] == 1:
			pos, hpr = self.sectorCoords[side][row][col]
			i = convertLocToIndex(side, row, col)
			self.sectors[i].removeNode()
			self.Grass(pos, hpr, i, treePresent = False)
			self.sectorTypes[side][row][col] = "grass%d" % (i)
			self.treeLocs[side][row][col] = 0

############################
## continuous world tasks ##
############################

	def isEnoughSurrounding(self, (side, row, col), substance, minSubstance): #general function for checking if enough of a certain kind of terrain is surrounding
		dirs = [(-1, -1), (-1, 0), (-1, +1),
				( 0, -1),		   ( 0, +1),
				(+1, -1), (+1, 0), (+1, +1)]
		surroundingSubstance = 0
		for direction in dirs:
			(drow, dcol) = direction
			(checkSide, checkRow, checkCol) = (side, row+drow, col+dcol)
			if (checkRow<0) or (checkRow>=rows) or (checkCol<0) or (checkCol>=cols):
				(checkSide, checkRow, checkCol) = moveSides(checkSide, checkRow, checkCol)
				if (checkRow<0) or (checkRow>=rows) or (checkCol<0) or (checkCol>=cols): continue
			if self.sectorTypes[checkSide][checkRow][checkCol].startswith(substance): surroundingSubstance += 1
		return (surroundingSubstance >= minSubstance)

	def grassSpread(self, task):
		dirs = [(-1, -1), (-1, 0), (-1, +1),
				( 0, -1),		   ( 0, +1),
				(+1, -1), (+1, 0), (+1, +1)]
		for side in range(len(self.sectorTypes)):
			for row in range(len(self.sectorTypes[0])):
				for col in range(len(self.sectorTypes[0][0])):
					if self.sectorTypes[side][row][col].startswith("sand"):
						waterFound = False
						grassFound = None
						for direction in dirs:
							(drow, dcol) = direction
							(checkSide, checkRow, checkCol) = (side, row+drow, col+dcol)
							if (checkRow<0) or (checkRow>=rows) or (checkCol<0) or (checkCol>=cols):
								(checkSide, checkRow, checkCol) = moveSides(checkSide, checkRow, checkCol)
								if (checkRow<0) or (checkRow>=rows) or (checkCol<0) or (checkCol>=cols): continue #if you've moved sides and it's still invalid, then you've reached
																										  #an invalid square (such as if the origin was a corner)
							if self.sectorTypes[checkSide][checkRow][checkCol].startswith("grass"): grassFound = (checkSide, checkRow, checkCol) #sand needs water and grass
							if self.sectorTypes[checkSide][checkRow][checkCol].startswith("water"): waterFound = True
						if waterFound==True and grassFound != None: #check to see if grass has sufficient water next to it to grow
							if self.isEnoughSurrounding(grassFound, "water", 2):
								i = convertLocToIndex(side, row, col)
								self.sectors[i].setColor(self.grassCol)
								self.sectorTypes[side][row][col] = "grass%d" % (i)
		taskMgr.doMethodLater(.5, self.treeSpread, 'treeSpread')  #continuous tasks all call another in succession with one initial call so that they won't overlap
		return task.again

	def treeSpread(self, task):
		dirs = [(-1, -1), (-1, 0), (-1, +1),
				( 0, -1),		   ( 0, +1),
				(+1, -1), (+1, 0), (+1, +1)]
		for side in range(len(self.sectorTypes)):
			for row in range(len(self.sectorTypes[0])):
				for col in range(len(self.sectorTypes[0][0])):
					if self.sectorTypes[side][row][col].startswith("grass") and self.treeLocs[side][row][col] == 0: #checks if there is a free grass sector
						treeFound = 0
						waterFound = 0
						sandFound = 0
						for direction in dirs:
							(drow, dcol) = direction
							(checkSide, checkRow, checkCol) = (side, row+drow, col+dcol)
							if (checkRow<0) or (checkRow>=rows) or (checkCol<0) or (checkCol>=cols):
								(checkSide, checkRow, checkCol) = moveSides(checkSide, checkRow, checkCol)
								if (checkRow<0) or (checkRow>=rows) or (checkCol<0) or (checkCol>=cols): continue #if you've moved sides and it's still invalid, then you've reached
																												#an invalid square (such as if the origin was a corner)
							if self.sectorTypes[checkSide][checkRow][checkCol].startswith("water"): 
								waterFound += 1
							if self.sectorTypes[checkSide][checkRow][checkCol].startswith("sand"): 
								sandFound += 1
							if self.sectorTypes[checkSide][checkRow][checkCol].startswith("grass") and self.treeLocs[checkSide][checkRow][checkCol] == 1:
								treeFound += 1
						if (waterFound>=2) and (3<=treeFound<4) and (sandFound<2):
							self.growTree((side, row, col))
		taskMgr.doMethodLater(.5, self.grassDie, 'grassDie')

	def grassDie(self, task):
		dirs = [(-1, 0), ( 0, -1), ( 0, +1), (+1, 0)]
		for side in range(len(self.sectorTypes)):
			for row in range(len(self.sectorTypes[0])):
				for col in range(len(self.sectorTypes[0][0])):
					if self.sectorTypes[side][row][col].startswith("grass"):
						waterFound = False
						for direction in dirs:
							(drow, dcol) = direction
							(checkSide, checkRow, checkCol) = (side, row+drow, col+dcol)
							if (checkRow<0) or (checkRow>=rows) or (checkCol<0) or (checkCol>=cols):
								(checkSide, checkRow, checkCol) = moveSides(checkSide, checkRow, checkCol)
								if (checkRow<0) or (checkRow>=rows) or (checkCol<0) or (checkCol>=cols): continue #if you've moved sides and it's still invalid, then you've reached
																												  #an invalid square (such as if the origin was a corner)
							if self.sectorTypes[checkSide][checkRow][checkCol].startswith("water"): 
								waterFound = True
						if not waterFound:
							i = convertLocToIndex(side, row, col)
							self.destroyTree((side, row, col))
							self.sectors[i].setColor(self.sandCol)
							self.sectorTypes[side][row][col] = "sand%d" % (i)
		taskMgr.doMethodLater(.5, self.treeDie, 'treeDie')

	def treeDie(self, task):
		dirs = [(-1, -1), (-1, 0), (-1, +1),
				( 0, -1),		   ( 0, +1),
				(+1, -1), (+1, 0), (+1, +1)]
		for side in range(len(self.sectorTypes)):
			for row in range(len(self.sectorTypes[0])):
				for col in range(len(self.sectorTypes[0][0])):
					if self.treeLocs[side][row][col] == 1: #checks if there is a tree
						if self.isEnoughSurrounding((side, row, col), "sand", 3) or not self.isEnoughSurrounding((side, row, col), "water", 1): 
							self.destroyTree((side, row, col))

			
app = godhead()
app.run()

