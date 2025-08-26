"""
Combiner extension module
Author: Arnaud Cassone

"""

from TDStoreTools import StorageManager
import TDFunctions as TDF
import CraftGGenUtils

class CombineExt:
	"""
	CombineExt is an extension for the Combiner node.
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		TDF.createProperty(self, 'SourceAMenuNames', value=[], dependable=True,readOnly=False)
		TDF.createProperty(self, 'SourceBMenuNames', value=[], dependable=True,readOnly=False)
	
	def OnStart(self, ):

		# Initialize menu names for SourceA and SourceB from attributesA and attributesB DATs
		tempListA = []
		tempListB = []
		datmenu1 = op('attributesA')

		# Collect menu names from attributesA DAT
		for i in range(datmenu1.numRows - 1):
			tempListA.append(datmenu1[i+1, 0].val)
		datmenu2 = op('attributesB')
		# Collect menu names from attributesB DAT
		for i in range(datmenu2.numRows - 1):
			tempListB.append(datmenu2[i+1, 0].val)

		# Update SourceAMenuNames if the list has changed
		if self.SourceAMenuNames != tempListA:
			self.SourceAMenuNames = tempListA
			self.updateMenu()

		# Update SourceBMenuNames if the list has changed
		if self.SourceBMenuNames != tempListB:
			self.SourceBMenuNames = tempListB
			self.updateMenu()
		
		pass
	
	def OnChange(self, name, value, prev):
		if name == 'Paramname':
			pass

		if name == 'Source':
			self.changeSource(value)

		if name == 'Source2':
			self.changeSource(value)
		
		if name == 'Operation':
			self.changeOperation(value)

		pass
	
	def changeSource(self, value):
		# change the source parameter of the Combiner component
		

		pass
	
	def changeOperation(self, value):
		# change the operation parameter of the Combiner component
		if value == 'Add':
			op('mathcombine1').par.comb0oper = 'add'
		elif value == 'Sub':
			op('mathcombine1').par.comb0oper = 'asubb'
		elif value == 'Multiply':
			op('mathcombine1').par.comb0oper = 'mult'
		elif value == 'Divide':
			op('mathcombine1').par.comb0oper = 'adivb'
		elif value == 'Average':
			op('mathcombine1').par.comb0oper = 'avg'
			

	def OnCreate(self):
		# Manage params of the cloned operator
		if "GGenFamily" not in parent().tags:
			op = parent()
			if op:
				try:
					CraftGGenUtils.SetCloneParameters(op)
				except Exception:
					pass
		pass
	
	def OnPulse(self, name):
		if name == 'Help':
			# open html browser
			mod.webbrowser.open('https://github.com/CraftKontrol/GroundGen-for-Touchdesigner/wiki/combiner')
		pass

	def updateMenu(self):
		# update the menu of the sources parameters
		menuA = parent().par.Source
		menuA.menuNames = self.SourceAMenuNames
		menuA.menuLabels = self.SourceAMenuNames

		menuB = parent().par.Source2
		menuB.menuNames = self.SourceBMenuNames
		menuB.menuLabels = self.SourceBMenuNames 

		pass
	
	def Update(self):
		
		# Gather menu names from attributesA and attributesB DATs
		tempListA = []
		tempListB = []
		datmenu1 = op('attributesA')
		# Collect menu names from attributesA DAT, skipping header row
		for i in range(datmenu1.numRows - 1):
			tempListA.append(datmenu1[i+1, 0].val)
		datmenu2 = op('attributesB')
		# Collect menu names from attributesB DAT, skipping header row
		for i in range(datmenu2.numRows - 1):
			tempListB.append(datmenu2[i+1, 0].val)

		# Update SourceAMenuNames and refresh menu if changed
		if self.SourceAMenuNames != tempListA:
			self.SourceAMenuNames = tempListA
			self.updateMenu()

		# Update SourceBMenuNames and refresh menu if changed
		if self.SourceBMenuNames != tempListB:
			self.SourceBMenuNames = tempListB
			self.updateMenu()

		pass
