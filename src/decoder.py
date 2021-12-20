import sys

from src.memory_map import MemoryMap
from src.instruction_set import InstructionSet

class Decoder:
	_pc = 0
	_output = []
	_demiliter = ","

	def __init__(self, file):
		self._file = file
		self._mem = MemoryMap()
		self._iss = InstructionSet()
	

	def handle(self, output_file=None):
		for line in self._file:
			# remove '\n' char
			line = line.strip()
			if len(line) == 0:		
				continue
			# check if is define a label
			if line[:3].upper() == "LAB":
				if len(line.split(" ")) > 1:
					print(f"{line}\nMust to have no spaces in label declarations.")
					sys.exit(1)
				self._mem.def_label(line.upper(), self._pc)
			elif line[:3].upper() == "VAR":
					if "=" not in line:
						print(f"failed: {line}")
						print("You must to have '=' to declare variables address")
						sys.exit(1)
					name, value = list(map(lambda x: x.replace(" ", "").upper(), line.split("=")))
					self._mem.def_variable(name, int(value), self._pc)
					self._output.append([hex(self._pc)[2:].zfill(3).upper(), self._mem._def_var[name][1]])
					self._pc = self._pc + 1
			else:
				# separate instructions and remove empty elements.
				instructions = list(filter(lambda y: y, map(lambda x: x.replace(" ", "").upper(), line.split(self._demiliter))))
				if len(instructions) == 2:
					self.build_instruction_string(instructions)
					self._pc = self._pc + 1
				else:
					print("Erro: Your code need 2 instructions per line, separeted by ','. Variables must to be declared in one line and set a default value like 0.")
					sys.exit(1)

		if self._mem.is_valid():
			for code in self._output:
				if len(code) == 5:
					# verify memory address unfilled
					if code[2][:3] == "LAB":
						code[2] = self._mem.addr_label(code[2])
					elif code[2][:3] == "VAR":
						code[2] = self._mem.addr_variable(code[2])
					if code[4][:3] == "LAB":
						code[4] = self._mem.addr_label(code[4])
					elif code[4][:3] == "VAR":
						code[4] = self._mem.addr_variable(code[4])
					if output_file == None:
						print(" ".join(list(map(lambda x: str(x), code))))
					else:
						output_file.write(" ".join(list(map(lambda x: str(x), code))))
						output_file.write("\n")
					continue
				if output_file == None:
					print(" ".join(code))
				else:
					output_file.write(" ".join(code))
					output_file.write("\n")
		else:
			print("Error: missing label or variable declarations.")
			print("Must do declare this labels/variables: ", [x for x in self._mem._ghost_label], [y for y in self._mem._ghost_var])
			sys.exit(1)


	def build_instruction_string(self, instructions):
		# setting the line of instruction
		line = [hex(self._pc)[2:].zfill(3).upper()]
		
		for i in range(2):
			# verify instructions with no memory access to append default value
			if instructions[i] == "RSH" or instructions[i] == "LSH" or instructions[i] == "LOADMQ" or instructions[i] == "ABORT":
				line.append(self._iss.handle(instructions[i]))
				line.append("000")
			else:
				if "=" not in instructions[i]:
					print(f"Unrecognized instruction: {instructions[i]}")
					sys.exit(1)
				# destructuring instructions and memory IAS set 
				ins, mem = instructions[i].split('=')
				line.append(self._iss.handle(ins))
				if mem[:3] == "LAB":
					# create a tempory label that must be created
					self._mem.decl_label(mem)
				else:
					# create a tempory variable that must be created
					self._mem.decl_variable(mem)
				line.append(mem)

		self._output.append(line)
			