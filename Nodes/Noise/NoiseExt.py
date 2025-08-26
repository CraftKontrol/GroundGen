"""
Noise Extension Module
Author: Arnaud Cassone

"""

from TDStoreTools import StorageManager
import TDFunctions as TDF
import CraftGGenUtils as CraftGGenUtils

class NoiseExt:
	"""
	NoiseExt is an extension module for the Noise node.
	The class provides methods to handle initialization, parameter changes, and pulse actions for the Noise node. 
	It manages parameter synchronization, composite mode operations, and integration with the CraftGGenUtils utilities.
	
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	
	def OnStart(self):
		#print("NoiseExt started")
		op('noise1').par.noiseoutputattscope = parent().par.Paramname
		pass
	
	def OnCreate(self):
		# Manage params of the cloned operator
		if "GGenFamily" not in parent().tags:
			CraftGGenUtils.SetCloneParameters(parent())

		# Initialize the extension
		self.OnStart()


		pass

	def OnChange(self, name, value, prev):
		if name == 'Paramname':
			self.changeParamName(value)

	
		if name == 'Compositemode':
			if value == 'Add':
				op('mathcombine1').par.comb2oper = 35
				pass
			elif value == 'Substract':
				op('mathcombine1').par.comb2oper = 36
				pass
			elif value == 'Multiply':
				op('mathcombine1').par.comb2oper = 38
				pass
			elif value == 'Divide':
				op('mathcombine1').par.comb2oper = 39
				pass
			elif value == 'Average':
				op('mathcombine1').par.comb2oper = 43
				pass
			
		pass
	
	def OnPulse(self, name):
		if name == 'Help':
			# open html browser
			mod.webbrowser.open('https://github.com/CraftKontrol/GroundGen-for-Touchdesigner/wiki/noise')

		pass
	
	def changeParamName(self, name):
		op('noise1').par.noiseoutputattscope = name

	def Update(self):
		if len(parent().inputConnectors[0].connections) > 0:
			parent().par.Compositemode.readOnly = False
		else:
			parent().par.Compositemode = 'Add'
			parent().par.Compositemode.readOnly = True