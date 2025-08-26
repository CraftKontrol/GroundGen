"""
Shape Extension Module
Author: Arnaud Cassone

"""

from TDStoreTools import StorageManager
import TDFunctions as TDF
import CraftGGenUtils

class ShapeExt:
	"""
	ShapeExt is an extension for the Shape node.
	This extension manages shape effects and parameters.
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp


	def OnStart(self):
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
			mod.webbrowser.open('https://github.com/CraftKontrol/GroundGen-for-Touchdesigner/wiki/shape')
		pass
	
	def OnChange(self, name, value, prev):
		if name == 'Compositemode':
			if value == 'Add':
				op('mathcombine1').par.comb1oper = 35
				pass
			elif value == 'Substract':
				op('mathcombine1').par.comb1oper = 36
				pass
			elif value == 'Multiply':
				op('mathcombine1').par.comb1oper = 38
				pass
			elif value == 'Divide':
				op('mathcombine1').par.comb1oper = 39
				pass
			elif value == 'Average':
				op('mathcombine1').par.comb1oper = 43
				pass

		pass
	


	