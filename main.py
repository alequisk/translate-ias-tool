import sys
# NAO PRECISA DE '=': LOAD_MQ, LSH, RSH

OP_CODE_TEXT = [
    'LOAD_MQ', 'LOAD_MQ_M', 'STOR', 'LOAD', 'LOAD_NEG', 'LOAD_MOD',
    'LOAD_NEG_MOD', 'JUMP_NOIF_LEFT', 'JUMP_NOIF_RIGHT', 'JUMP_IF_LEFT',
    'JUMP_IF_RIGHT', 'ADD', 'ADD_MOD', 'SUB', 'SUB_MOD', 'MUL', 'DIV', 'LSH',
    'RSH', 'STOR_REPL_LEFT', 'STOR_REPL_RIGHT', 'ABORT_PROGRAM'
]

OP_CODE_HEX = [
    '0A', '09', '21', '01', '02', '03', '04', '0D', '0E', '0F', '10', '05',
    '07', '06', '08', '0B', '0C', '14', '15', '12', '13', '00'
]

VARIABLES_NAME = []
VARIABLES_MEMORY = []

LABELS_NAME = []
LABELS_MEMORY = []

LINE_CURRENT = 0

OUTPUT = []


def create_variable(var_name):
    global VARIABLES_MEMORY
    global VARIABLES_NAME
    global LINE_CURRENT

    if var_name in VARIABLES_NAME:
        if VARIABLES_MEMORY[VARIABLES_NAME.index(var_name)] != -1:
            print("Error: Duplicate variable statement")
            sys.exit()
        else:
            VARIABLES_MEMORY[VARIABLES_NAME.index(var_name)] = LINE_CURRENT
    else:
        VARIABLES_NAME.append(var_name)
        VARIABLES_MEMORY.append(LINE_CURRENT)


def create_tempory_variable(var_name):
    global VARIABLES_MEMORY
    global VARIABLES_NAME

    if var_name in VARIABLES_NAME:
        print("Error: Duplicate variable statement")
        sys.exit()
    VARIABLES_NAME.append(var_name)
    VARIABLES_MEMORY.append(-1)


def get_variable_memory(var_name):
    global VARIABLES_MEMORY
    global VARIABLES_NAME

    if var_name not in VARIABLES_NAME:
        print("Error: Address to memory is invalid")
        sys.exit()
    position = VARIABLES_MEMORY[VARIABLES_NAME.index(var_name)]
    return position


def create_label(label_name):
    global LABELS_NAME
    global LABELS_MEMORY
    global LINE_CURRENT

    if label_name in LABELS_NAME:
        position = LABELS_MEMORY[LABELS_NAME.index(label_name)]
        if position == -1:
            LABELS_MEMORY[LABELS_NAME.index(label_name)] = LINE_CURRENT
        else:
            print("Error: The label name already exists! Name:{}".format(
                label_name))
            sys.exit()
    else:
        LABELS_NAME.append(label_name)
        LABELS_MEMORY.append(LINE_CURRENT)


def create_tempory_label(label_name):
    global LABELS_NAME
    global LABELS_MEMORY

    if label_name in LABELS_NAME:
        print(f"Error: Duplicate label name {label_name}")
        sys.exit()
    LABELS_NAME.append(label_name)
    LABELS_MEMORY.append(-1)


def get_label_memory(label_name):
    global LABELS_NAME
    global LABELS_MEMORY

    if label_name not in LABELS_NAME:
        print("Error: Label name not exists")
        sys.exit()
    return LABELS_MEMORY[LABELS_NAME.index(label_name)]


def hex_number(number, tam):
    return (str(hex(int(number)))[2:].zfill(tam)).upper()


def decode_instruction(inst):
    global OP_CODE_HEX
    global OP_CODE_TEXT
    global VARIABLES_MEMORY
    global VARIABLES_NAME
    global LABELS_MEMORY
    global LABELS_NAME

    inst = inst.split('=')
    if len(inst) == 1:
        return OP_CODE_HEX[OP_CODE_TEXT.index(inst[0])] + ' 000'
    else:
        ret = OP_CODE_HEX[OP_CODE_TEXT.index(inst[0])]
        if inst[1][:3] == 'VAR':
            if inst[1] not in VARIABLES_NAME:
                create_tempory_variable(inst[1])
                ret += ' ' + inst[1]
            else:
                position = VARIABLES_MEMORY[VARIABLES_NAME.index(inst[1])]
                if position != -1:
                    ret += ' ' + hex_number(position, 3)
                else:
                    ret += ' ' + inst[1]

        elif inst[1][:3] == 'LAB':
            if inst[1] not in LABELS_NAME:
                create_tempory_label(inst[1])
                ret += ' ' + inst[1]
            else:
                position = LABELS_MEMORY[LABELS_NAME.index(inst[1])]
                if position != -1:
                    ret += ' ' + hex_number(position, 3)
                else:
                    ret += ' ' + inst[1]
        else:
            print("Error: Wrong Syntex Detected")
            sys.exit()

        return ret


def decode(line):
    #remove '\n' from string
    if line[-1] == '\n':
        line = line[:-1]

    #output variable
    output = ''

    #define global variable
    global LINE_CURRENT
    global OUTPUT

    if len(line) == 0:
        OUTPUT.append('')
        return

    #create a new label
    if line[:3] == 'LAB':
        create_label(line)
        return
    elif line[:3] == 'VAR':
        line = line.split(' ')
        create_variable(line[0])
        output = hex_number(get_variable_memory(line[0]),
                            3) + ' ' + hex_number(line[1], 3)
        LINE_CURRENT += 1
    else:
        instructions = line.split(' ')
        output = hex_number(LINE_CURRENT, 3) + ' ' + decode_instruction(
            instructions[0]) + ' ' + decode_instruction(instructions[1])
        LINE_CURRENT += 1

    OUTPUT.append(output)


file = open(sys.argv[1], 'r')

for x in file:
    decode(x)

for x in OUTPUT:
    line = x.split(' ')
    new_line = []
    for i in line:
        if i[:3] == 'VAR':
            new_line.append(
                hex_number(VARIABLES_MEMORY[VARIABLES_NAME.index(i)], 3))
        elif i[:3] == 'LAB':
            new_line.append(hex_number(LABELS_MEMORY[LABELS_NAME.index(i)], 3))
        else:
            new_line.append(i)

    print(' '.join(new_line))
