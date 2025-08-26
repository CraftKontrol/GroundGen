"""
Level Extension Module
Author: Arnaud Cassone

"""

from TDStoreTools import StorageManager
import TDFunctions as TDF
import CraftGGenUtils

class LevelExt:
	"""
	LevelExt is an extension for the Level node.
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		TDF.createProperty(self, 'SourceMenuNames', value=[], dependable=True,readOnly=False)
	
	def OnStart(self, ):

		# Initialize SourceMenuNames
		tempList = []
		datmenu = op('attributes')
		for i in range (datmenu.numRows - 1):
			tempList.append(datmenu[i+1, 0].val)

		# Update SourceMenuNames if it has changed
		if self.SourceMenuNames != tempList:
			self.SourceMenuNames = tempList
			self.updateMenu()	
		
		pass
	
	def OnChange(self, name, value, prev):
		pass

	def OnCreate(self):

		# Manage params of the cloned operator
		if "GGenFamily" not in parent().tags:
			op = parent()
			if op:
				CraftGGenUtils.SetCloneParameters(op)
		pass

	def OnPulse(self, name):
		if name == 'Help':
			# open html browser
			mod.webbrowser.open('https://github.com/CraftKontrol/GroundGen-for-Touchdesigner/wiki/level')
		pass

	def updateMenu(self):
		# update the menu of the source parameter
		menu = parent().par.Source
		menu.menuNames = self.SourceMenuNames
		menu.menuLabels = self.SourceMenuNames

		pass
	
	def Update(self):

		# Initialize tempList
		tempList = []
		datmenu = op('attributes')
		for i in range (datmenu.numRows - 1):
			tempList.append(datmenu[i+1, 0].val)

		# Update SourceMenuNames if it has changed
		if self.SourceMenuNames != tempList:
			self.SourceMenuNames = tempList
			self.updateMenu()	
	
		pass
