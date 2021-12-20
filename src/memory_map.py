import sys

class MemoryMap:
	_def_var = dict()
	_ghost_var = set()
	_def_label = dict()
	_ghost_label = set()


	def def_variable(self, var_name, var_value, address):
		if var_name in self._def_var:
			print(f"Error: variable '{var_name}' already defined.")
			sys.exit(1)
		hex_address = hex(address)
		self._def_var[var_name] = [hex_address[2:].zfill(3).upper(), hex(var_value)[2:].upper()]
		if var_name in self._ghost_var:
			self._ghost_var.remove(var_name)


	def def_label(self, label_name, address):
		if label_name in self._def_label:
			print(f"Error: label '{label_name}' already defined.")
			sys.exit(1)
		hex_address = hex(address)
		self._def_label[label_name] = [hex_address[2:].zfill(3).upper()]
		if label_name in self._ghost_label:
			self._ghost_label.remove(label_name)


	def decl_variable(self, var_name):
		if var_name in self._def_label:
			return
		self._ghost_var.add(var_name)
	

	def decl_label(self, label_name):
		if label_name in self._def_label:
			return
		self._ghost_label.add(label_name)
	

	def addr_variable(self, var_name):
		if var_name in self._def_var:
			return self._def_var[var_name][0]
		else:
			return -1
	

	def addr_label(self, label_name):
		if label_name in self._def_label:
			return self._def_label[label_name][0]
		else:
			return -1


	def is_valid(self):
		return not(len(self._ghost_var) > 0 or len(self._ghost_label) > 0)