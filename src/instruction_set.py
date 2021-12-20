import sys

class InstructionSet:
	_dictionary = {
		'LOADMQ': 10,
		'LOADMMQ': 9,
		'STOR': 33,
		'LOAD': 1,
		'LOADN': 2,
		'LOADABS': 3,
		'LOADNABS': 4,
		'JUMPL': 13,
		'JUMPR': 14,
		'JUMPIL': 15,
		'JUMPIR': 16,
		'ADD': 5,
		'ADDABS': 7,
		'SUB': 6,
		'SUBABS': 8,
		'MUL': 11,
		'DIV': 12,
		'LSH': 20,
		'RSH': 21,
		'STORREPLL': 18,
		'STORREPLR': 19,
		'ABORT': 0
	}

	def handle(self, instruction):
		try:
			code = hex(self._dictionary[instruction.upper()])
			return code[2:].zfill(2).upper()
		except KeyError:
			print(f"Error: Instruction '{instruction}' don't exists.")
			sys.exit(1)