"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
import TDFunctions as TDF
import json
import os
class TerrainNetworkExt:
	"""
	TerrainNetworkExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		TDF.createProperty(self, 'HeightList', value=[], dependable=True,readOnly=False)

	def OnStart(self):
		op.GGenLogger.Info("TerrainNetwork started")
		# Load parameters from config.json
		path = op.GGen.par.Ggenfolder + "/config.json"
		if os.path.exists(path):
			op.GGenLogger.Info("Loading Terrain config from " + path)
			with open(path, 'r') as f:
				config = json.load(f)
				if 'Terrain' in config:
					for terrain in config['Terrain']:
						for node in op('UserNetwork').findChildren(tags=["Splatmap", "GGen2d", "GGen3d"]):
							if str(node) == terrain['op']:
								if terrain['inputs']:
									for input in terrain['inputs']:
										node.par[input[0]] = input[1]
								if terrain['outputs']:
									for output in terrain['outputs']:
										node.par[output[0]] = output[1]

		self.ownerComp.par.opshortcut = "TerrainNetwork"
		self.HeightList.clear()
		pass
	
	def OnChange(self, v):
		pass
	 
	def OnPulse(self):
		pass
		
	def Update(self):

		#print("heights =" + str(len(self.HeightList)) + " nodes = " + str(len(op('UserNetwork').findChildren(tags=["heightGGen"]))))

		for node in op('UserNetwork').findChildren(tags=["heightGGen"]):
			
			try:
				newItem = ({'name': node.par.Paramname.eval(),'node': node + "/outValue"})
				
				ishere = 0
				for item in self.HeightList:
					if item['name'] == newItem['name']:
						ishere = 1
						break
				if ishere == 0:
					self.HeightList.append(newItem)
					#print("Added new item:", newItem) 
			except:
				pass
			
				
		
		
		try:
			for item in self.HeightList:
				if item['name'] not in [node.par.Paramname.eval() for node in op('UserNetwork').findChildren(tags=["heightGGen"])]:
					self.HeightList.remove(item)
					#print("Removed item:", item)
		except:
			pass
		
		
		pass