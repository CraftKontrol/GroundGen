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

class SplatmapsNetworkExt:
	"""
	SplatmapsNetworkExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# properties
		TDF.createProperty(self, 'SplatList', value=[], dependable=True,readOnly=False)



	def OnCreate(self):
		self.ownerComp.par.opshortcut = "SplatmapsNetwork"
	def OnStart(self):
		op.GGenLogger.Info("SplatmapsNetwork started")
		# Load parameters from config.json
		path = op.GGen.par.Ggenfolder + "/config.json"
		if os.path.exists(path):
			op.GGenLogger.Info("Loading Splatmaps config from " + path)
			with open(path, 'r') as f:
				config = json.load(f)
				if 'Splatmaps' in config:
					for splat in config['Splatmaps']:
						for node in op('UserNetwork').findChildren(tags=["Splatmap", "GGen2d", "GGen3d"]):
							if str(node) == splat['op']:
								
								if splat['inputs']:
									for input in splat['inputs']:
										
										node.par[input[0]] = input[1]
								if splat['outputs']:
									for output in splat['outputs']:
										
										node.par[output[0]] = output[1]

		# update the SplatList
		self.SplatList.clear()
		for splat in op('UserNetwork').findChildren(tags=["Splatmap"]):
			
			newItem = {'name': splat.par.Paramname ,'node': splat + "/out1"}
			if newItem not in self.SplatList:
				self.SplatList.append(newItem)

		combiner = op('InputTerrain/mathcombine1')
		if len(self.SplatList) == 0:
			combiner.seq.input.numBlocks = 1
			combiner.seq.comb.numBlocks = 1
		pass
	
	def OnChange(self, v):
		pass
	
	def OnPulse(self):
		pass
		
	def Update(self):
		try:
			
			heights = op.TerrainNetwork.HeightList
		except Exception as e:
			heights = []

		self.SplatList.clear()
		
		combiner = op('InputTerrain/mathcombine1')
		
		for splat in op('UserNetwork').findChildren(tags=["Splatmap"]):
			
			newItem = {'name': splat.par.Paramname ,'node': splat + "/out1"}
			if newItem not in self.SplatList:
				self.SplatList.append(newItem)

			

		if len(heights) > 0 :
			# for each heights, verify if seq.input block is present.
			# if not, add it
			# for each block, verify if is present in heights.
			# if not delete it
			for i in range(len(heights)-1):
				# verify if input block is present
				ishere = -1
				for j in range(1,combiner.seq.input.numBlocks):
					if combiner.par["input" + str(j) + "pop"] == heights[i]['name']:
						ishere = j
						break
				if ishere == 0:
					# add block
					
					combiner.par["input" + str(j) + "pop"] = heights[i]['name']
					combiner.par["input" + str(j) + "attrs"] = heights[i]['name']
					combiner.par["comb" + str(j) + "oper"] = 'copya'
					combiner.par["comb" + str(j) + "scopea"] = heights[i]['name']

			for i in range (combiner.seq.input.numBlocks-1):
				ishere = -1
				for j in range(len(heights)):
					if combiner.par["input" + str(i+1) + "attrs"] == heights[j]['name']:
						ishere = j
						break
				if ishere == -1:
					# block is not present, delete it
					print("try deleting :", i+1)
					combiner.seq.input.destroyBlock(i+1)

			for i in range(combiner.seq.comb.numBlocks):
				ishere = -1
				for j in range(len(heights)):
					if combiner.par["comb" + str(i) + "scopea"] == heights[j]['name']:
						ishere = j
						break
				if ishere == -1:
					# block is not present, delete it
					print("try deleting :", i)
					combiner.seq.comb.destroyBlock(i)


			# remove duplicate from input and comb
			input_names = [combiner.par["input" + str(i) + "attrs"] for i in range(combiner.seq.input.numBlocks)]
			comb_names = [combiner.par["comb" + str(i) + "scopea"] for i in range(combiner.seq.comb.numBlocks)]
			unique_inputs = list(set(input_names))
			unique_combs = list(set(comb_names))
			for i in range(combiner.seq.input.numBlocks):
				if combiner.par["input" + str(i) + "attrs"] not in unique_inputs:
					combiner.par["input" + str(i) + "attrs"] = None
			for i in range(combiner.seq.comb.numBlocks):
				if combiner.par["comb" + str(i) + "scopea"] not in unique_combs:
					combiner.par["comb" + str(i) + "scopea"] = None


			#delete empty for input and comb
			for i in range(combiner.seq.input.numBlocks):
				if combiner.par["input" + str(i) + "attrs"] is None:
					combiner.seq.input.destroyBlock(i)
			for i in range(combiner.seq.comb.numBlocks):
				if combiner.par["comb" + str(i) + "scopea"] is None:
					combiner.seq.comb.destroyBlock(i)

			self.UpdateInputs(combiner,heights)
			self.UpdateCombiners(combiner,heights)

		pass
	
	
	
	def UpdateInputs(self,combiner,heights):

		for i in range(len(heights)):

			combiner.par["input" + str(i+1) + "pop"] = heights[i]['node']
			combiner.par["input" + str(i+1) + "attrs"] = heights[i]['name']

	def UpdateCombiners(self,combiner,heights):
			
		#print("UpdateCombiners: number of heights: ", len(heights))
		for i in range(len(heights)): 
			
			combiner.par["comb" + str(i) + "oper"] = 'copya'
			combiner.par["comb" + str(i) + "scopea"] = heights[i]['name']

	def DeleteBlock(self, combiner, index):
		print("try deleting :", index)
		combiner.seq.input.destroyBlock(index)
		combiner.seq.comb.destroyBlock(index)

