"""
HeightMap Extension Module
Author: Arnaud Cassone

"""

from TDStoreTools import StorageManager
import TDFunctions as TDF
import CraftGGenUtils

class HeightMapExt:
	"""
	HeightMapExt is an extension for the HeightMap node.

	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def OnStart(self):
		pass

	def OnChange(self, name, value, prev):
		
		pass
	
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
			mod.webbrowser.open('https://github.com/CraftKontrol/GroundGen-for-Touchdesigner/wiki/heightmap')
		pass
	
