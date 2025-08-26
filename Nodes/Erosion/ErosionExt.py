"""
Erosion Extension Module
Author: Arnaud Cassone

"""

from TDStoreTools import StorageManager
import TDFunctions as TDF
import CraftGGenUtils

class ErosionExt:
	"""
	ErosionExt is an extension for the GGen node.
	This extension manages erosion effects on terrain.

	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def OnStart(self):
		pass
	
	def OnCreate(self):

		# Manage params of the cloned operator
		if "GGenFamily" not in parent().tags:

			CraftGGenUtils.SetCloneParameters(parent())

		pass
	
	def OnPulse(self, name):
		if name == 'Help':
			# open html browser
			mod.webbrowser.open('https://github.com/CraftKontrol/GroundGen-for-Touchdesigner/wiki/erosion')

		pass
	
	def OnChange(self, name, value, prev):
		pass