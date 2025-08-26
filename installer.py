"""

This file contains code that is based on or derived from the MIT-licensed work by Josef Pelz.

MIT License
Copyright (c) 2024 Josef Pelz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class GenericInstallerEXT:
    """
    GenericInstallerEXT is a flexible installer extension for TouchDesigner that allows
    the installation and uninstallation of custom operator families dynamically.
    
    It replicates the functionality of specific installers like LOPExt but is designed
    to handle any operator family by specifying parameters such as family name and color.
    """
    def __init__(self, ownerComp, family_name, color, compatible_types=None, connection_map=None):
        """
        Initializes the installer extension.

        Args:
            ownerComp (COMP): The component to which this extension is attached.
            family_name (str): The name of the operator family (e.g., 'LOP', 'CHATTD').
            color (list or tuple): The color to associate with the operator family.
        """
        #print(f"Initializing GenericInstallerEXT for {family_name}")
        op.GGenLogger.Info(f"Initializing GenericInstallerEXT for {family_name}")


        self.ownerComp = ownerComp
        self.family_name = family_name
        self.color = color
        self.compatible_types = compatible_types or []
        self.connection_map = connection_map or {}
        self.find_other_installers(op, self.family_name)

        run(
			"args[0].postInit() if args[0] "
					"and hasattr(args[0], 'postInit') else None",
			self,
			endFrame=True,
			delayRef=op.TDResources
		)

    def postInit(self):
        op('GGenExecute').par.startpulse.pulse()
        pass

    def find_other_installers(self, op, name):
        """
        Checks for existing installers with the same family name to prevent duplicates.

        Args:
            op (function): The operator function from TouchDesigner.
            name (str): The family name to check for existing installers. 
        """
        self.ownerComp.par.opshortcut = ''
        if hasattr(op, name):
            print(f"Found existing {name} installer, destroying this one.")
            try:
                ui.messageBox(name, f"{name} exists already ! !")
            except:
                pass

            run("args[0].selfDestroy()", self, endFrame=True, delayRef=op.TDResources)
            return 

        if self.ownerComp.parent() != op('/'):
            newInstaller = op('/').copy(self.ownerComp)
            newInstaller.cook(force=True)
            run("args[0].selfDestroy()", self, endFrame=True, delayRef=op.TDResources)
            return

        self.ownerComp.expose = True
        self.ownerComp.nodeX = 0
        self.ownerComp.nodeY = 0

        self.ownerComp.par.opshortcut = name

        if self.ownerComp.par.Install == 1:
            self.Install()
        return

    def Install(self):
        """
        Installs the operator family by configuring UI elements, menu operations,
        and compatibility settings.
        """
        self.ownerComp.par.Install = 1
        #print(f"Installing {self.family_name}")
        op.GGenLogger.Info(f"Start {self.family_name} Nodes Injection") 

        toggle_path = f"/ui/dialogs/bookmark_bar/{self.family_name}_toggle"
        if op('/ui/dialogs/bookmark_bar/' + f"{self.family_name}_toggle") is None:
            # print(f"Creating toggle button at {toggle_path}")
            op(f"install_scripts/fam_toggle/button/text1").par.text = self.family_name
            toggle = op('/ui/dialogs/bookmark_bar').copy(
                self.ownerComp.op('install_scripts/fam_toggle'),
                name=f"{self.family_name}_toggle"
            )
            toggle.allowCooking = True
            toggle.inputCOMPConnectors[0].connect(op('/ui/dialogs/bookmark_bar/emptypanel'))
            toggle.op('button').par.value0.bindExpr = f"op.{self.family_name}.par.Install"
            
            # Update the opexec1 text to use the correct family name
            opexec1 = toggle.op('opexec1')
            if opexec1:
                opexec1.par.op.expr = f"op.{self.family_name}"
                opexec1.text = opexec1.text.replace('LOP', self.family_name)

        self.ownerComp.par.opshortcut = self.family_name
        menuOp = op('/ui/dialogs/menu_op')
        nodeTable = op('/ui/dialogs/menu_op/nodetable')

        # Insert family into the families table
        if menuOp.op(f'{self.family_name}_insert') is None:
            # print(f"Creating family insert DAT for {self.family_name}")
            familyInsert = menuOp.create(insertDAT, f'{self.family_name}_insert')
            familyInsert.par.insert = 'col'
            familyInsert.par.at = 'index'
            familyInsert.par.index = self.ownerComp.par.Index
            familyInsert.par.index.expr = f'op.{self.family_name}.par.Index'
            familyInsert.par.contents = self.family_name
            current_output = menuOp.op('insert1').outputs[0]
            menuOp.op('insert1').outputConnectors[0].disconnect()
            menuOp.op('insert1').outputConnectors[0].connect(familyInsert)
            familyInsert.outputConnectors[0].connect(current_output)
            familyInsert.nodeX = menuOp.op('insert1').nodeX + 150
            familyInsert.nodeY = menuOp.op('insert1').nodeY

        # Update colors table directly instead of using a colorInsert DAT
        colors_table = menuOp.op('colors')
        if colors_table:
            # Check if the family already exists in the colors table
            family_exists = False
            for i in range(colors_table.numRows):
                if colors_table[i, 0].val == f"'{self.family_name}'":
                    # Family exists, update its color values
                    for j in range(1, min(len(self.color) + 1, colors_table.numCols)):
                        colors_table[i, j] = self.color[j-1]
                    family_exists = True
                    break
            # If family doesn't exist, add a new row
            if not family_exists:
                new_row = [f"'{self.family_name}'"]
                for c in self.color:
                    new_row.append(c)
                colors_table.appendRow(new_row)       
        # Create and modify the set_last_node_type DAT
        if menuOp.op('set_last_node_type') is None:
            setLastNodeType = menuOp.copy(op('install_scripts/set_last_node_type'))
            setLastNodeType.nodeX, setLastNodeType.nodeY = (
                menuOp.op('launch_menu_op').nodeX - 200,
                menuOp.op('launch_menu_op').nodeY
            )
        else:
            setLastNodeType = menuOp.op('set_last_node_type')

        compatible_types_check = ' or '.join([f"menu_type=='{t}'" for t in self.compatible_types])
        set_last_node_type_script = f'''varTable = op('local/set_variables')
lastnode = op(varTable['nodepath',1])
source = varTable['source',1].val
menu_type = varTable['menu_type',1].val
if(lastnode and source == 'output'):
    type = lastnode.family
    if ('{self.family_name}' in lastnode.tags):
        type = '{self.family_name}'
    varTable['lasttype',1] = type
elif(source == 'input' and ({compatible_types_check})):
    pane = ui.panes.current
    zoom = pane.zoom
    currentParent = pane.owner
    mousePos = [varTable['xpos',1],varTable['ypos',1]]
    type = menu_type
    for child in currentParent.findChildren(maxDepth=1):
        if (-5<(mousePos[0]-child.nodeX)*zoom<15 and child.nodeY+child.nodeHeight>mousePos[1] and mousePos[1]>child.nodeY):
            if('{self.family_name}' in child.tags):
                type = '{self.family_name}'
                varTable['lastnode',1] = child.name
                varTable['nodepath',1] = child.path
                break
    varTable['lasttype',1] = type'''

        setLastNodeType.text = set_last_node_type_script
        launch_menu_op = menuOp.op('launch_menu_op')
        code = launch_menu_op.text
        key = 'if($type != "none")'
        replacement = (
            f"{key}\n\tcvar menu_type=$type\n\trun set_last_node_type\n\tset type = $lasttype"
        )
        launch_menu_op.text = code.replace(key, replacement)
        # Set color for all children components- this could be removed
        for o in self.ownerComp.findChildren():
            if 'License' not in o.name and o.OPType != 'annotateCOMP':
                o.color = self.color
        self.ownerComp.color = self.color 


        families_op = nodeTable.op('families')
        families_op.bypass = False 

        inject_op_name = f'inject_{self.family_name}_fam'
        if nodeTable.op(inject_op_name) is None:            
            families_op = nodeTable.op('families')
            original_input = families_op.inputs[0]  
            inject_op = nodeTable.copy(families_op, name=inject_op_name, includeDocked=True)
            inject_op.par.callbacks.expr = f"op.{self.family_name}.op('install_scripts/fam_script_callbacks')"
            inject_op.nodeX = families_op.nodeX + 150 
            inject_op.nodeY = families_op.nodeY
            if original_input:
                original_input.outputConnectors[0].disconnect()
                original_input.outputConnectors[0].connect(inject_op)
                inject_op.outputConnectors[0].connect(families_op)
            families_op.cook(force=True)
            inject_op.cook(force=True)
        else:
            # debug(menuOp.op(inject_op_name))
            families_op = nodeTable.op('families')
            families_op.bypass = False  
        eval4 = nodeTable.op('eval4')
        current_expr = eval4.par.expr.eval()
        if current_expr:
            if current_expr != "[x for x in families.keys()]":
                if self.family_name not in current_expr:
                    eval4.par.expr = f"{current_expr[:-1]}, '{self.family_name}']"
            else:
                eval4.par.expr = f"[x for x in families.keys()] + ['{self.family_name}']"
        else:
            eval4.par.expr = f"[x for x in families.keys()] + ['{self.family_name}']"
        createNode = menuOp.op('create_node')
        if f"if($type=='{self.family_name}')" not in createNode.text:
            insertion_key = 'set type = `tab("current",0,0)`\n'
            insert_code = (
                f"if($type=='{self.family_name}')\n\texit\nendif\n"
            )
            index = createNode.text.index(insertion_key)
            createNode.text = (
                createNode.text[:index + len(insertion_key)]
                + insert_code
                + createNode.text[index + len(insertion_key):]
            )

        searchExec = menuOp.op('search/panelexec1')
        if self.family_name not in searchExec.text:
            key = "if parent.OPCREATE.op('nodetable/destil').numRows > 1:\n"
            unique_id = -abs(hash(self.family_name) % 10000)  # Creates a unique negative number between -1 and -9999
            insert_code = (
                f"\t\t\tif(op('/ui/dialogs/menu_op/current')[0,0].val=='{self.family_name}'):\n"
                f"\t\t\t\tparent.OPCREATE.op('nodetable').clickID({unique_id})\n"
                f"\t\t\t\treturn\n"
            )
            index = searchExec.text.index(key)
            searchExec.text = (
                searchExec.text[:index + len(key)]
                + insert_code
                + searchExec.text[index + len(key):]
            )

        panel_execute_path = f'{self.family_name}_panel_execute'
        if menuOp.op(panel_execute_path) is None:
            panel_execute = menuOp.copy(
                self.ownerComp.op('install_scripts/fam_panel_execute'),
                name=panel_execute_path
            )
            panel_execute.nodeX = menuOp.op('node_script').nodeX
            panel_execute.nodeY = menuOp.op('node_script').nodeY + 100
            # Generate the same unique ID used in the search panel
            unique_id = -abs(hash(self.family_name) % 10000)
            panel_execute_script = panel_execute.text.replace('OPNAME', self.family_name)
            panel_execute_script = panel_execute_script.replace('-9999', str(unique_id))
            panel_execute.text = panel_execute_script

        compatibleTable = menuOp.op('compatible')
        row_entry = [self.family_name]
        for index in range(1, compatibleTable.numCols):
            col_type = compatibleTable[0, index].val
            connection_key = (self.family_name, col_type)
            if connection_key in self.connection_map:
                row_entry.append(self.connection_map[connection_key])
            elif col_type in self.compatible_types:
                row_entry.append('x')
            else:
                row_entry.append('')
                
        col_entry = [self.family_name]
        for row in compatibleTable.rows()[1:]:  
            row_type = row[0].val
            connection_key = (row_type, self.family_name)
            if connection_key in self.connection_map:
                col_entry.append(self.connection_map[connection_key])
            elif row_type in self.compatible_types:
                col_entry.append('x')
            else:
                col_entry.append('')        

        # Add the row and column first
        if not compatibleTable.rows(self.family_name):
            compatibleTable.appendRow(row_entry)
        if not compatibleTable.cols(self.family_name):
            compatibleTable.appendCol(col_entry)

        # Now set the intersection point to 'x'
        try:
            # Get row and column indices by searching through the table
            row_index = None
            col_index = None
            
            # Find row index
            for i in range(compatibleTable.numRows):
                if compatibleTable[i, 0].val == self.family_name:
                    row_index = i
                    break
                    
            # Find column index
            for i in range(compatibleTable.numCols):
                if compatibleTable[0, i].val == self.family_name:
                    col_index = i
                    break
                    
            if row_index is not None and col_index is not None:
                compatibleTable[row_index, col_index] = 'x'
        except Exception as e:
            print(f"Error setting self-compatibility: {e}")
                
       
      
    
        #print(f"{self.family_name} installation complete")
        op.GGenLogger.Info(f"{self.family_name} Nodes Injection complete")

    def Uninstall(self):
        print(f"Beginning uninstall of {self.family_name}")
        self.ownerComp.par.Install = 0
        menuOp = op('/ui/dialogs/menu_op')
        nodeTable = op('/ui/dialogs/menu_op/nodetable')
        # toggle_path = f"/ui/dialogs/bookmark_bar/{self.family_name}_toggle"
        # if op(toggle_path):
        #     op(toggle_path).destroy()
        if menuOp.op(f'{self.family_name}_insert'):
            menuOp.op(f'{self.family_name}_insert').destroy()
        
        # Remove the family from the colors table instead of using colorInsert DAT
        colors_table = menuOp.op('colors')
        if colors_table:
            for i in range(colors_table.numRows):
                if colors_table[i, 0].val == f"'{self.family_name}'":
                    colors_table.deleteRow(i)
                    break
                    
        inject_op_name = f'inject_{self.family_name}_fam'
        if nodeTable.op(inject_op_name):
            nodeTable.op(inject_op_name).destroy()
        families_op = nodeTable.op('families')
        families_op.bypass = False 
        panel_execute_path = f'{self.family_name}_panel_execute'
        if menuOp.op(panel_execute_path):
            menuOp.op(panel_execute_path).destroy()
        launch_menu_op = menuOp.op('launch_menu_op')
        code = launch_menu_op.text
        key = f'if($type != "none")\n\tcvar menu_type=$type\n\trun set_last_node_type\n\tset type = $lasttype'
        replacement = 'if($type != "none")'
        launch_menu_op.text = code.replace(key, replacement)
        if menuOp.op('set_last_node_type'):
            menuOp.op('set_last_node_type').destroy()
        # eval4 = nodeTable.op('eval4')
        # eval4.par.expr = "[x for x in families.keys()]"
        compatibleTable = menuOp.op('compatible')
        if compatibleTable.rows(self.family_name):
            compatibleTable.deleteRow(self.family_name)
        if compatibleTable.cols(self.family_name):
            compatibleTable.deleteCol(self.family_name)
        print(f"{self.family_name} uninstallation complete")

    def selfDestroy(self):
        """
        Destroys the owner component.
        """
        print(f"Destroying {self.family_name} installer component")
        self.ownerComp.destroy()
        return
    


    def getElement(self, s):
        """Returns the first element of a set/list or None if empty."""
        for e in s:
            return e
        return None
    def createStub(self, comp):
        """
        Creates a lightweight stub of a component, preserving its connections and parameters.
        
        Args:
            comp (COMP): The component to create a stub from.
        """
        name = comp.name
        print(f"createStub: Creating stub for {comp.path} with tags {comp.tags}")
        
        # IMPORTANT: Extract the operator type before copying
        # First look for a tag that matches {type}{familyName} pattern
        op_type = None
        for tag in comp.tags:
            if tag.endswith(self.family_name) and tag != self.family_name:
                op_type = tag.removesuffix(self.family_name)
                print(f"createStub: Found operator type '{op_type}' from tag '{tag}'")
                break
        
        # If no type-specific tag was found, use the component name as the type
        if not op_type:
            op_type = comp.name
            print(f"createStub: No type tag found, using component name '{op_type}' as type")
        
        copy = comp.parent().copy(comp)
        copy.allowCooking = False
        
        # Preserve node position and size
        copy.nodeX = comp.nodeX
        copy.nodeY = comp.nodeY
        copy.nodeWidth = comp.nodeWidth
        copy.nodeHeight = comp.nodeHeight
        
        # Remove all children to make it lightweight
        children = copy.findChildren(depth=1)
        while children:
            if children[-1]:
                children[-1].destroy()
            else:
                children = children[:-1]
        
        # Store the operator type explicitly
        stub_tag = f"{op_type}{self.family_name}stub"
        print(f"createStub: Setting stub tag to '{stub_tag}'")
        copy.tags = [stub_tag]
        
        # Also store the type directly for easier retrieval
        copy.store('op_type', op_type)
        
        # Name it with _stub suffix
        copy.name = f"{name}_stub"
        
        # Store important properties
        copy.store('cooking', comp.allowCooking)
        copy.store('bypass', comp.bypass)
        
        # Store input connections
        inputs = [(i.connections[0].outOP if i.connections[0].owner.isCOMP else i.connections[0].owner) 
                if i.connections else None for i in comp.inputConnectors]
        copy.store('inputs', inputs)
        
        # Store output connections
        outputs = [[(con.owner, con.index) for con in o.connections] for o in comp.outputConnectors]
        copy.store('outputs', outputs)
        
        # Store parameter values
        params = {}
        for p in comp.pars():
            if hasattr(p, 'sequence') and p.sequence:
                # Special handling for sequence parameters
                seq = p.sequence
                seq_data = {
                    'name': seq.name if hasattr(seq, 'name') else '',
                    'numBlocks': seq.numBlocks,
                    'blocks': []
                }
                
                # Store each block's parameters using direct name access instead of iteration
                common_par_names = ['name', 'label', 'value', 'index', 'enable', 'display', 
                                    'top', 'dat', 'text', 'op', 'ops', 'mode', 'active',
                                    'parameters', 'pages', 'info', 'shortcut']
                
                for i in range(seq.numBlocks):
                    block = seq.blocks[i]
                    block_data = {}
                    
                    # Try each parameter name directly
                    for par_name in common_par_names:
                        try:
                            if hasattr(block.par, par_name):
                                par = block.par[par_name]
                                if par.mode == ParMode.CONSTANT:
                                    block_data[par_name] = par.val
                                elif par.mode == ParMode.EXPRESSION:
                                    block_data[par_name] = {'mode': 'expr', 'expr': par.expr}
                                elif par.mode == ParMode.BIND:
                                    block_data[par_name] = {'mode': 'bind', 'expr': par.bindExpr}
                        except Exception as e:
                            # Silently continue if a particular parameter access fails
                            pass
                    
                    seq_data['blocks'].append(block_data)
                
                params[p.name] = {'type': 'sequence', 'data': seq_data}
            else:
                # Regular parameter handling (existing code)
                if p.mode == ParMode.CONSTANT:
                    params[p.name] = p.val
                elif p.mode == ParMode.EXPRESSION:
                    params[p.name] = {'mode': 'expr', 'expr': p.expr}
                elif p.mode == ParMode.BIND:
                    params[p.name] = {'mode': 'bind', 'expr': p.bindExpr}
        
        copy.store('params', params)
        
        return copy

    def Createstubs(self):
        """
        Replaces all components of this family with lightweight stubs.
        Shows a confirmation dialog with stub count information.
        First warns about operators without specific type tags.
        """
        # print(f"Createstubs: Starting for {self.family_name}")
        # Find all operators of this family type, excluding the installer and its children
        familyOps = op('/').findChildren(type=COMP, key=lambda o: (
            self.family_name in o.tags and 
            not hasattr(o.parent, self.family_name) and 
            not hasattr(o.parent, f"{self.family_name}OPs") and
            o != self.ownerComp and  # Exclude the installer component itself
            self.ownerComp.path not in o.path  # Exclude children of the installer
        ))
        
        if not familyOps:
            print("Createstubs: No family operators found.")
            ui.messageBox(
                f"No {self.family_name} Operators Found",
                f"No {self.family_name} operators found to create stubs.",
                buttons=["OK"]
            )
            return
        
        # Check which operators don't have proper type tags
        ops_without_type_tags = []
        for comp in familyOps:
            has_type_tag = False
            for tag in comp.tags:
                # Check if the tag follows the pattern {type}{familyName} but isn't just the family name
                if tag.endswith(self.family_name) and tag != self.family_name:
                    has_type_tag = True
                    break
            
            if not has_type_tag:
                ops_without_type_tags.append(comp)
        
        # Show warning if any operators lack proper type tags
        if ops_without_type_tags:
            warning_message = f"WARNING: {len(ops_without_type_tags)} of {len(familyOps)} operators don't have proper type tags.\n\n"
            warning_message += "These operators will be stubbed but may not be able to be properly recreated later.\n\n"
            
            # List up to 5 problem operators
            warning_message += "Problem operators:\n"
            for i, op_comp in enumerate(ops_without_type_tags[:5]):
                warning_message += f"• {op_comp.path} (Tags: {op_comp.tags})\n"
            
            if len(ops_without_type_tags) > 5:
                warning_message += f"• ...and {len(ops_without_type_tags) - 5} more\n\n"
            else:
                warning_message += "\n"
            
            warning_message += "It's recommended to cancel and ensure all operators have proper type tags first.\n"
            warning_message += "Do you want to proceed anyway?"
            
            warning_buttons = ['Proceed Anyway', 'Cancel']
            warning_choice = ui.messageBox(f'Missing Type Tags Warning', warning_message, buttons=warning_buttons)
            
            if warning_choice != 0:  # Not "Proceed Anyway"
                print("Createstubs: User cancelled due to missing type tags.")
                return
        
        # Show confirmation dialog with count information
        message = f"""
This will create lightweight stubs for {len(familyOps)} {self.family_name} operator(s).

Creating stubs will:
• Preserve operator connections
• Preserve parameter values
• Remove internal components
• Reduce memory usage
• Improve performance

To restore full functionality later, use Replacestubs.

Do you want to continue?
    """
        
        buttons = ['Create Stubs', 'Cancel']
        choice = ui.messageBox(f'Create {self.family_name} Stubs', message, buttons=buttons)
        
        if choice != 0:  # Not "Create Stubs"
            print("Createstubs: User cancelled stub creation.")
            return
        
        # Proceed with stub creation
        ui.undo.startBlock(f'Create {self.family_name} Stubs')
        
        created_stubs = []
        for comp in familyOps:
            try:
                stub = self.createStub(comp)
                created_stubs.append(stub)
            except Exception as e:
                print(f"Createstubs: Error creating stub for {comp.path}: {e}")
        
        # After creating all stubs, destroy the originals
        for comp in familyOps:
            try:
                comp.destroy()
            except Exception as e:
                print(f"Createstubs: Error destroying original component {comp.path}: {e}")
        
        ui.undo.endBlock()
        
        # Show completion message
        completion_message = f"""
    Successfully created {len(created_stubs)} stub(s) for {self.family_name} operators.

    Stubs preserve connections and parameter values while reducing memory usage.
    Use Replacestubs to restore full functionality when needed.
        """
        
        ui.messageBox(f'{self.family_name} Stubs Created', completion_message, buttons=["OK"])
        print(f"Createstubs: Completed creating {len(created_stubs)} stubs.")
        return

    def Replacestubs(self):
        """
        Regenerates full components from stubs.
        """
        print(f"Replacestubs: Starting for {self.family_name}")
        stubs = op('/').findChildren(type=COMP, key=lambda o: len(o.tags) == 1 and f"{self.family_name}stub" in self.getElement(o.tags))
        
        if not stubs:
            print("Replacestubs: No stubs found.")
            ui.messageBox(
                f"No {self.family_name} Stubs Found",
                f"No {self.family_name} stubs found to regenerate.",
                buttons=["OK"]
            ) 
            return
        
        print(f"Replacestubs: Found {len(stubs)} stubs")
        for s in stubs:
            print(f"Replacestubs: Stub: {s.path}, Tags: {s.tags}")
        
        # Show confirmation dialog
        message = f"""
This will regenerate {len(stubs)} {self.family_name} operator(s) from stubs.

Regenerating will:
• Restore full functionality
• Reconnect all connections
• Restore parameter values
• Increase memory usage

Do you want to continue?
    """
        
        buttons = ['Regenerate', 'Cancel']
        choice = ui.messageBox(f'Regenerate {self.family_name} Operators', message, buttons=buttons)
        
        if choice != 0:  # Not "Regenerate"
            print("Replacestubs: User cancelled regeneration.")
            return
        
        ui.undo.startBlock(f'Regenerate {self.family_name} from Stubs')
        
        operators_folder = self.ownerComp.op('custom_operators')
        if not operators_folder:
            print("Replacestubs: custom_operators folder not found.")
            ui.messageBox(
                "Error",
                f"Error: 'custom_operators' folder not found in the installer component.",
                buttons=["OK"]
            )
            ui.undo.endBlock()
            return
        
        regenerated = []
        errors = []
        
        # First pass - create the components and set their parameters
        for stub in stubs:
            try:
                # Get the operator type - first try from stored value, then from tag
                op_type = stub.fetch('op_type', None)
                if not op_type:
                    # Extract from tag as fallback
                    tag = self.getElement(stub.tags)
                    if not tag or not tag.endswith(f"{self.family_name}stub"):
                        errors.append(f"Invalid tag format on {stub.path}: {tag}")
                        continue
                    op_type = tag.removesuffix(f"{self.family_name}stub")
                
                # print(f"Replacestubs: Using operator type '{op_type}' for {stub.path}")
                
                # Find the master component to copy
                master_ops = operators_folder.findChildren(name=op_type, maxDepth=1)
                if not master_ops:
                    print(f"Replacestubs: No master component found for type '{op_type}'")
                    errors.append(f"No master component found for type {op_type}")
                    continue
                
                master_op = master_ops[0]
                # print(f"Replacestubs: Found master component: {master_op.path}")
                
                # Create the new component
                new_comp = stub.parent().copy(master_op)
                new_comp.nodeX = stub.nodeX
                new_comp.nodeY = stub.nodeY
                new_comp.nodeWidth = stub.nodeWidth
                new_comp.nodeHeight = stub.nodeHeight
                new_comp.name = stub.name.removesuffix('_stub')
                
                # Restore parameters from stub
                params = stub.fetch('params', {})
                for name, value in params.items():
                    dest_pars = new_comp.pars(name)
                    if not dest_pars:
                        continue
                        
                    dest_par = dest_pars[0]
                    
                    # Check if this is a sequence parameter
                    if isinstance(value, dict) and value.get('type') == 'sequence':
                        seq_data = value.get('data', {})
                        
                        # Only proceed if the destination has a sequence
                        if hasattr(dest_par, 'sequence') and dest_par.sequence:
                            seq_dest = dest_par.sequence
                            
                            # Set the number of blocks
                            if seq_dest.numBlocks != seq_data.get('numBlocks', 0):
                                seq_dest.numBlocks = seq_data.get('numBlocks', 0)
                            
                            # Restore each block's parameters
                            blocks_data = seq_data.get('blocks', [])
                            for i, block_data in enumerate(blocks_data):
                                if i < seq_dest.numBlocks:
                                    dest_block = seq_dest.blocks[i]
                                    
                                    # Restore all parameters in this block using direct access
                                    for par_name, par_value in block_data.items():
                                        try:
                                            if hasattr(dest_block.par, par_name):
                                                dest_block_par = dest_block.par[par_name]
                                                
                                                if isinstance(par_value, dict):
                                                    if par_value.get('mode') == 'expr':
                                                        dest_block_par.mode = ParMode.EXPRESSION
                                                        dest_block_par.expr = par_value.get('expr', '')
                                                    elif par_value.get('mode') == 'bind':
                                                        dest_block_par.mode = ParMode.BIND
                                                        dest_block_par.bindExpr = par_value.get('expr', '')
                                                else:
                                                    dest_block_par.mode = ParMode.CONSTANT
                                                    dest_block_par.val = par_value
                                        except Exception as e:
                                            # Silently handle parameter restoration errors
                                            pass
                    else:
                        # Regular parameter handling (existing code)
                        if isinstance(value, dict):
                            if value.get('mode') == 'expr':
                                dest_par.mode = ParMode.EXPRESSION
                                dest_par.expr = value.get('expr', '')
                            elif value.get('mode') == 'bind':
                                dest_par.mode = ParMode.BIND
                                dest_par.bindExpr = value.get('expr', '')
                        else:
                            dest_par.mode = ParMode.CONSTANT
                            dest_par.val = value
                
                regenerated.append(new_comp)
            except Exception as e:
                errors.append(f"Error regenerating from stub {stub.path}: {e}")
        
        # Second pass - restore connections
        for stub in stubs:
            try:
                new_comp = op(f"{stub.parent().path}/{stub.name.removesuffix('_stub')}")
                if not new_comp:
                    continue
                    
                # Restore input connections 
                stored_inputs = stub.fetch('inputs')
                if stored_inputs:
                    for i, input_op in enumerate(stored_inputs):
                        if i < len(new_comp.inputConnectors) and input_op:
                            new_comp.inputConnectors[i].connect(input_op)
                
                # Restore output connections
                stored_outputs = stub.fetch('outputs')
                if stored_outputs:
                    for o_idx, connections in enumerate(stored_outputs):
                        if o_idx < len(new_comp.outputConnectors):
                            for con in connections:
                                if con[0].op() and con[1] < len(con[0].inputConnectors):
                                    new_comp.outputConnectors[o_idx].connect(con[0].inputConnectors[con[1]])
                
                # Restore cooking and bypass state
                new_comp.allowCooking = stub.fetch('cooking', 1)
                new_comp.bypass = stub.fetch('bypass')
                
                # Remove the stub
                stub.destroy()
            except Exception as e:
                errors.append(f"Error restoring connections for {stub.path}: {e}")
        
        ui.undo.endBlock()
        
        # Show completion message with any errors
        completion_message = f"Successfully regenerated {len(regenerated)} {self.family_name} component(s) from stubs."
        
        if errors:
            error_list = "\n".join([f"• {err}" for err in errors[:5]])
            if len(errors) > 5:
                error_list += f"\n• And {len(errors) - 5} more errors..."
            completion_message += f"\n\nThe following errors occurred:\n{error_list}"
        
        ui.messageBox(f'{self.family_name} Regeneration Complete', completion_message, buttons=["OK"])
        # print(f"Replacestubs: Completed with {len(regenerated)} regenerated components.")
        return

    def copyPar(self, destPar, sourcePar):
        """
        Copies parameter values and settings from one parameter to another,
        with proper support for sequence parameters.
        
        Args:
            destPar (Par): The destination parameter.
            sourcePar (Par): The source parameter.
        """
        # Handle sequence parameters
        if hasattr(destPar, 'sequence') and destPar.sequence and hasattr(sourcePar, 'sequence') and sourcePar.sequence:
            seq_dest = destPar.sequence
            seq_source = sourcePar.sequence
            
            # First set the number of blocks
            if seq_dest.numBlocks != seq_source.numBlocks:
                # print(f"Copying sequence: {sourcePar.name} - setting numBlocks from {seq_dest.numBlocks} to {seq_source.numBlocks}")
                seq_dest.numBlocks = seq_source.numBlocks
            
            # Copy each block individually using direct parameter access by name
            # Rather than trying to iterate over the parameters
            for i in range(min(seq_source.numBlocks, seq_dest.numBlocks)):
                try:
                    # Instead of trying to iterate over parameters, use a direct approach
                    # by trying common parameter names found in sequences
                    common_par_names = ['name', 'label', 'value', 'index', 'enable', 'display', 
                                       'top', 'dat', 'text', 'op', 'ops', 'mode', 'active',
                                       'parameters', 'pages', 'info', 'shortcut']
                    
                    source_block = seq_source.blocks[i]
                    dest_block = seq_dest.blocks[i]
                    
                    # Try each parameter name directly
                    for name in common_par_names:
                        try:
                            if hasattr(source_block.par, name) and hasattr(dest_block.par, name):
                                self.copySimplePar(dest_block.par[name], source_block.par[name])
                        except Exception as e:
                            # Silently continue if a particular parameter access fails
                            pass
                        
                except Exception as e:
                    print(f"Error processing sequence block {i}: {e}")
            
            return  # We've handled the sequence parameter, no need to continue
        
        # Handle regular parameters
        self.copySimplePar(destPar, sourcePar)

    def copySimplePar(self, destPar, sourcePar):
        """Helper function to copy a simple (non-sequence) parameter."""
        destPar.mode = sourcePar.mode
        
        if sourcePar.mode == ParMode.CONSTANT:
            destPar.val = sourcePar.val
        elif sourcePar.mode == ParMode.EXPRESSION:
            destPar.expr = sourcePar.expr
        elif sourcePar.mode == ParMode.BIND:
            destPar.bindExpr = sourcePar.bindExpr

    def find_matching_master_op(self, comp, operators_folder):
        """
        Find a matching master operator for a component using multiple matching methods.
        
        Args:
            comp (COMP): The component to find a match for
            operators_folder (COMP): The folder containing master operators
        
        Returns:
            tuple: (master_op, match_method) where master_op is the matching operator or None,
                   and match_method is a string describing how the match was made
        """
        # First try matching by type tag
        comp_type = next((s for s in comp.tags if s.endswith(self.family_name) and len(s) > len(self.family_name)), None)
        if comp_type:
            comp_type = comp_type.removesuffix(self.family_name)
            master_ops = operators_folder.findChildren(name=comp_type, maxDepth=1)
            if master_ops:
                return (master_ops[0], "type_tag")
        
        # If no match found by tag, try using ext0object
        if hasattr(comp.par, 'ext0object'):
            ext_obj = comp.par.ext0object.eval()
            if ext_obj:
                # Look for master operators with matching ext0object
                for master_op in operators_folder.findChildren(type=COMP, maxDepth=1):
                    if hasattr(master_op.par, 'ext0object') and master_op.par.ext0object.eval() == ext_obj:
                        return (master_op, "ext0object")
        
        # No match found
        return (None, "none")

    def update_comp(self, old_comp):
        """
        Updates a single component to the newest version.
        
        Args:
            old_comp (COMP): The component to update.
        Returns:
            tuple: (success, message) indicating if update was successful and status message
        """
        operators_folder = self.ownerComp.op('custom_operators')
        if not operators_folder:
            return (False, f"Error: 'custom_operators' folder not found in the installer component.")

        master_comp, match_method = self.find_matching_master_op(old_comp, operators_folder)
        if not master_comp:
            return (False, f"Couldn't update {old_comp.path}, no matching master component found.")

        try:
            # print(f"Updating {old_comp.path} using match method: {match_method}")

            new_comp = old_comp.parent().copy(master_comp)
            old_name = old_comp.name

            # Preserve attributes
            new_comp.nodeX = old_comp.nodeX
            new_comp.nodeY = old_comp.nodeY
            new_comp.nodeWidth = old_comp.nodeWidth
            new_comp.nodeHeight = old_comp.nodeHeight
            new_comp.allowCooking = old_comp.allowCooking
            new_comp.bypass = old_comp.bypass
            new_comp.activeViewer = old_comp.activeViewer
            new_comp.viewer = old_comp.viewer

            # Copy parameters, avoiding certain ones
            for p in new_comp.pars():
                if p.name in ('Version', 'Copyright') or (hasattr(p, 'sequence') and p.sequence and p.sequence.name == 'ext'):
                    continue
                old_pars = old_comp.pars(p.name)
                if old_pars:
                    self.copyPar(p, old_pars[0])

            # Restore connections
            for i in range(min(len(new_comp.inputConnectors), len(old_comp.inputConnectors))):
                old_in = old_comp.inputConnectors[i]
                if old_in.connections:
                    new_comp.inputConnectors[i].connect(old_in.connections[0])

            for o in range(min(len(new_comp.outputConnectors), len(old_comp.outputConnectors))):
                old_out = old_comp.outputConnectors[o]
                for conn in old_out.connections:
                    new_comp.outputConnectors[o].connect(conn)

            old_comp.destroy()
            new_comp.name = old_name

            return (True, f"Successfully updated {new_comp.path} (matched via {match_method})")

        except Exception as e:
            return (False, f"Error updating {old_comp.path}: {e}")

    def Updateall(self):
        """
        Updates all components of this family type to the newest version.
        """
        # print(f"Updateall: Starting for {self.family_name}")

        family_ops = op('/').findChildren(type=COMP, key=lambda o: (
            self.family_name in o.tags and
            not hasattr(o.parent, self.family_name) and
            not hasattr(o.parent, f"{self.family_name}OPs") and
            o != self.ownerComp and
            self.ownerComp.path not in o.path
        ))

        if not family_ops:
            ui.messageBox(
                "No Operators Found",
                f"No {self.family_name} operators found to update.",
                buttons=["OK"]
            )
            return

        operators_folder = self.ownerComp.op('custom_operators')
        if not operators_folder:
            ui.messageBox(
                "Folder Not Found",
                "Error: 'custom_operators' folder not found in the installer component.",
                buttons=["OK"]
            )
            return

        ops_without_type_tags = []
        ops_with_ext_object = []
        ops_without_matches = []

        for comp in family_ops:
            has_type_tag = any(tag.endswith(self.family_name) and tag != self.family_name for tag in comp.tags)

            if not has_type_tag:
                ops_without_type_tags.append(comp)

                if hasattr(comp.par, 'ext0object') and comp.par.ext0object.eval():
                    ops_with_ext_object.append(comp)
                else:
                    master_comp, _ = self.find_matching_master_op(comp, operators_folder)
                    if not master_comp:
                        ops_without_matches.append(comp)

        if ops_without_matches:
            warning_message = f"WARNING: {len(ops_without_matches)} of {len(family_ops)} operators cannot be matched to any master operator.\n\n"
            warning_message += "These operators will be skipped during the update process.\n\n"

            warning_message += "Operators without matches:\n"
            for i, op_comp in enumerate(ops_without_matches[:5]):
                warning_message += f"• {op_comp.path} (Tags: {op_comp.tags})\n"

            if len(ops_without_matches) > 5:
                warning_message += f"• ...and {len(ops_without_matches) - 5} more\n\n"
            else:
                warning_message += "\n"

            warning_buttons = ['Continue Anyway', 'Cancel']
            warning_choice = ui.messageBox('Missing Matches Warning', warning_message, buttons=warning_buttons)

            if warning_choice != 0:
                #print("Updateall: User cancelled due to missing matches.")
                return

        updateable_count = len(family_ops) - len(ops_without_matches)
        message = f"""
This will update {updateable_count} {self.family_name} operator(s) to the latest version.

Of these operators:
• {len(family_ops) - len(ops_without_type_tags)} have type tags
• {len(ops_with_ext_object)} will be matched using ext0object
• {len(ops_without_matches)} cannot be matched (will be skipped)

Updating will:
• Preserve connections
• Preserve parameter values
• Replace internal components with the latest version

Do you want to continue?
    """

        buttons = ['Update All', 'Cancel']
        choice = ui.messageBox(f'Update {self.family_name} Operators', message, buttons=buttons)

        if choice != 0:
            return

        ui.undo.startBlock(f'Update {self.family_name} operators')

        updated = []
        skipped = []
        errors = []
        match_methods = {"type_tag": 0, "ext0object": 0, "none": 0}

        for op_comp in family_ops:
            try:
                # print(f"Updateall: Processing {op_comp.path}")

                success, message = self.update_comp(op_comp)

                if success:
                    updated.append(op_comp.path)
                    if "matched via type_tag" in message:
                        match_methods["type_tag"] += 1
                    elif "matched via ext0object" in message:
                        match_methods["ext0object"] += 1
                else:
                    if "no matching master component found" in message:
                        skipped.append(op_comp.path)
                    else:
                        errors.append(message)
            except Exception as e:
                error_msg = f"Error updating {op_comp.path}: {e}"
                print(error_msg)
                errors.append(error_msg)

        ui.undo.endBlock()

        completion_message = f"Successfully updated {len(updated)} {self.family_name} operator(s) to the latest version.\n\n"

        if updated:
            completion_message += "Match methods used:\n"
            if match_methods["type_tag"] > 0:
                completion_message += f"• {match_methods['type_tag']} operators matched by type tag\n"
            if match_methods["ext0object"] > 0:
                completion_message += f"• {match_methods['ext0object']} operators matched by ext0object\n"
            completion_message += "\n"

        if skipped:
            completion_message += f"{len(skipped)} operators were skipped (no matching master found):\n"
            for i, path in enumerate(skipped[:3]):
                completion_message += f"• {path}\n"
            if len(skipped) > 3:
                completion_message += f"• ...and {len(skipped) - 3} more\n"
            completion_message += "\n"

        if errors:
            completion_message += f"{len(errors)} errors occurred:\n"
            for i, err in enumerate(errors[:3]):
                completion_message += f"• {err}\n"
            if len(errors) > 3:
                completion_message += f"• ...and {len(errors) - 3} more\n"

        ui.messageBox(f'{self.family_name} Update Complete', completion_message, buttons=["OK"])
        return