#!/usr/bin/env python3
import math
import fileinput
import itertools
from collections import defaultdict
# import sys; sys.path.append("../..")
# from lib import *

INSTRUCTIONS = ['inp', 'add', 'mul', 'div', 'mod', 'eql']
curr_value = None

# https://www.geeksforgeeks.org/find-number-contain-digit-d/
def contains_digit(num, digit):
    """Returns true if d is present as digit in number x."""
    # Breal loop if d is present as digit
    while (num > 0):
        if (num % 10 == digit):
            break
        # Fix bug in their code
        num = int(num / 10)
    # If loop broke
    return (num > 0)


def alu(commands, input, debug=False):
    count_matches = 0
    input_idx = 0
    locals = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    for cmd_str in commands:
        cmd_list = cmd_str.split()
        assert len(cmd_list) in [1,2,3]
        cmd = cmd_list[0]
        assert cmd in INSTRUCTIONS
        params = cmd_list[1:]
        assert params[0] in ['w', 'x', 'y', 'z']

        values = []
        for param in params:
            if param in ['w', 'x', 'y', 'z']:
                values.append(locals[param])
            else:
                values.append(int(param))

        if cmd in INSTRUCTIONS[1:]:
            assert (params[1] in ['w', 'x', 'y', 'z']) or int(params[1]) < 100

        result = 0
        if cmd == 'inp':
            result = input[input_idx]
            input_idx += 1
        elif cmd == 'add':
            result = values[0] + values[1]
        elif cmd == 'mul':
            result = values[0] * values[1]
        elif cmd == 'div':
            result = values[0] // values[1]
        elif cmd == 'mod':
            result = values[0] % values[1]
        elif cmd == 'eql':
            result = 1 if values[0] == values[1] else 0
        locals[params[0]] = result
        if debug:
            if cmd_str.startswith("inp"):
                print()
            print(cmd_str, locals)
        if cmd_str == 'add z y' and locals['x'] == 0 and locals['z'] != 0:
            count_matches += 1
    # if count_matches > 2:
    #     print('X!', count_matches, input)
    #     return None
    return locals


def num_to_chars(num):
    chars = []
    while num > 0:
        chars.append(chr(65 + num % 26))
        num = num // 26
    return ''.join(reversed(chars))


def fpga(input):
    input = [int(n) for n in list('99919765949498')]
    # 999[1]9[76]594[9498]
    # 9-1, 9-7, 9-6, 4-9, 9-4, 5-9, 9-8
    # -8,   -2,  -3,   5,  -5,   4,  -1
    # thus: 249[1]3[11]161[6151]
    input = [int(n) for n in list('24913111616151')]

    divs = [1,1,1,26,1,26,26,1,1,1,26,26,26,26]
    matches = [14,15,13,-10,14,-3,-14,12,14,12,-6,-6,-2,-9]
    offset = [8,11,2,11,1,5,10,6,1,11,9,14,11,2]
    z = 0
    zz = []
    for idx, w in enumerate(input):
        # x = (z % 26) + matches[idx]
        # z = z // divs[idx]
        # x = 1 if x != w else 0
        # y = 25*x + 1
        # z = z*y + x*(w + offset[idx])
        # 
        # x = (z % 26) + matches[idx]
        # z = z // divs[idx]
        # if x != w:
        #     z = 26*z + w + offset[idx]
        #
        # It's a stack!
        prev_z = zz[-1] if len(zz) > 0 else 0
        x = prev_z + matches[idx]
        if divs[idx] == 26:
            zz.pop()
        print(f'W({w}) != X({x}) [{prev_z} + {matches[idx]}]')
        if w != x:
            zz.append(w + offset[idx])
            print('Push:', zz, '=', [chr(65 + num % 26) for num in zz])
        print(num_to_chars(z))

    # w1 != 14
    # w2 != (w1 + 8)%26 + 15
    # w3 != (w2 + 11)%26 + 13
    # Diff of -8 ('91') mandatory
    # w4 == (w3 + 2)%26 - 10
    # w5 != (w2 + 11)%26 + 14
    # Diff of -2 mandatory
    # w6 == (w5 + 1)%26 - 3
    # Diff of -3 mandatory
    # w7 == (w2 + 11)%26 - 14
    # w8 != (w1 + 8)%26 + 12
    # w9 != (w8 + 6)%26 + 14
    # w10 != (w9 + 1)%26 + 12
    # Diff of 5 mandatory
    # w11 == (w10 + 11)%26 - 6
    # Diff of -5 mandatory
    # w12 == (w9 + 1)%26 - 6
    # Diff of 4 mandatory
    # w13 == (w8 + 6)%26 - 2
    # Diff of -1 mandatory
    # w14 == (w1 + 8)%26 - 9
    return z, len(zz)


# 999[1]9[76]594[9498]

# inp w    # 1 to 9
# mul x 0  # clear x
# add x z  # x = z [previous step?]
# mod x 26 # x = x % 26 [NOP on 1st step]
# When to decrease Z on schedule
# div z 1  # [diff] NOP     [1,1,1,26,1,26,26,1,1,1,26,26,26,26]
# What value to match
# add x 14 # [diff] x += 14 [14,15,13,-10,14,-3,-14,12,14,12,-6,-6,-2,-9]
# eql x w  # x == w
# eql x 0  # x != w
# mul y 0  # clear
# add y 25 # y = 25
# mul y x  # y = 25*x
# add y 1  # y += 1
# mul z y  # z = 0 ?
# mul y 0  # clear y
# add y w  # y = w
# What offset to add to to Z for mismatches
# add y 8  # [diff] y += 8  [8,11,2,11,1,5,10,6,1,11,9,14,11,2]
# mul y x  #
# add z y  # (1 or 0) * y

# x1 = (z % 26) + [14]
# y = 25*x + 1
# x = 1 if x1 != w else 0
# z = z*y + x*(inp+) = (z/[1])*(25*x + 1) + x*(inp + [8])
# if x != w: z = (z * 26) + (inp+[])
# else: z = (z * 1) + 0
# z == 0 and x == 0

# Step 1: w1 == 14
# Step 2: w2 == (w1+8)+15


def search_numerical(commands):
    """Search in numerical order."""
    global curr_value
    # 21111111111111-21111125949493, 27272727272727-27272735999975
    for model_number in range(99919765949498+1, 99919769999999+1):
        curr_value = model_number
    # 99999985949499-99999913765488
    # 99919769999999-99919763949479 
    # for model_number in range(99919763949479, 11111111111111-1, -1):
    # for model_number in range(99919763949479, 11111111111111-1, -1):
        if model_number % 10 == 0:
            if model_number % 10000 == 0:
                print('.', end="", flush=True)
            continue
        if contains_digit(model_number, 0):
            continue
        # if model_number % 100 < 80:
        #     continue
        # if (model_number % 10000)//1000 not in [16, 27, 38, 49]:
        #     continue
        # if (model_number % 1000)//10 not in [14, 25, 36, 47, 58, 69]:71,82,93
        #     continue
        if (model_number % 10000)//100 not in [94]:
            continue

        vars = alu(commands, [int(ch) for ch in str(model_number)])
        # x**26 = y
        # x = log(y)/log(26)
        # value = math.log(vars['z'])/math.log(26)
        # if value < 1:
        #     print(f"{model_number} ({math.log(vars['z'])/math.log(26)})")

        valid = vars['z'] == 0
        if valid:
            print(model_number)
            exit()


def search_progressive(commands):
    global curr_value
    closest = 2**32
    lock_numbers = []
    # (1, 1, 1, 4, 1, 3, 1, 7, 3, 9, 6, 1, 1, 9)
    for model_number in itertools.product(range(1, 10), repeat=14):
        curr_value = model_number
        # Algorithm processes left to right, so we increment numbers
        # in that order to find patterns that "unlock" code
        model_number = tuple(reversed(model_number))
        if model_number[0:6] == tuple([9]*6):
            print('.', end="", flush=True)

        if model_number[2:2+2] != (9,1):
            continue
        if model_number[4] != model_number[5]+2:
        # if model_number[4:4+2] != (3,1):
            continue
        if model_number[-1] == 2:
            exit()

        vars = alu(commands, model_number)
        assert fpga(model_number) == vars['z']
        if vars['z'] < closest:
            print(f"{model_number} ({vars['z']})")
            closest = vars['z']

        valid = vars['z'] == 0
        if valid:
            print(model_number)
            exit()


# Step 1: z = 0 + (w1 + 8)
# Step 2: z = (w1+8)*26 + (w2 + 11)
# Step 3: z = ((w1+8)*26 + (w2 + 11))*26 + (w3 + 2)
# End: z = (((w1+8)*26 + (w2 + 11))*26 + (w3 + 2))*26 + (w4 + 11)

# Model number looks for correct "letter" in correct location?
# but "letters" are 1 to 9 to map to 26 and thus there are a few duplicates?
# only ~30 possible valid model numbers? (10 or 26)
# 7 non-matches required? (because matches increase by 26 and there's 7 div's by 26)

# 47min - 99999999999999 - too high
# 99919763949478 - too low
# 99[91](97)6594(94)98 (lower/before: 99919764949488)
def main():
    commands = [line.strip() for line in fileinput.input() if not line.startswith('#')]
    print(len(commands))

    # # Compare steps
    # step_cmds = 18
    # first_step = commands[0:step_cmds]
    # diffs = defaultdict(list)
    # for idx in range(0, len(commands), step_cmds):
    #     assert commands[idx].startswith('inp')
    #     curr_step = commands[idx:idx+step_cmds]
    #     for cmd_idx in range(len(curr_step)):
    #         if cmd_idx not in [4,5,15]:
    #             assert first_step[cmd_idx] == curr_step[cmd_idx], \
    #                 f'{cmd_idx}: {first_step[cmd_idx]} != {curr_step[cmd_idx]}'
    #         else:
    #             print(curr_step[cmd_idx])
    #             diffs[cmd_idx].append(int(curr_step[cmd_idx].split()[2]))
    #     print()
    #     # if cmd.startswith('inp'):
    #     #     print(idx, idx / 18)
    # print(str(diffs).replace(" ", ""))

    # step = 8-1  # 0-index
    # # for ijk in itertools.product(range(1,10), range(1,10)):
    # #     inp = [1,1,9,1,1,1,1,1,ijk[0],ijk[1]]
    # #     # print(inp)
    # #     alu(commands[0:18*(step+1)], inp)
    # for ijk in itertools.product(range(1,10), range(1,10), range(1,10), range(1,10),
    #         range(1,10), range(1,10)):
    #     inp = [ijk[0],ijk[1],9,1,ijk[2],ijk[3],ijk[4],ijk[5]] 
    #     # print(inp)
    #     alu(commands[0:18*(step+1)], inp)
    # exit()

    # print(alu(commands, [int(n) for n in list('13579246899999')], debug=True))
    # print(alu(commands, [int(n) for n in list('99919765949498')], debug=True))
    print(fpga([int(n) for n in list('99919765949498')]))
    exit()

    try:
        # search_numerical(commands)
        search_progressive(commands)
    # ...UVWXXYZZ
    # U = 1 or 2
    # V = 1,2,3,4
    # W = 6,7,8,9
    # XX = 16, 27, 38, 49
    # Y = 1,2,3,4
    # ZZ = 52,62,72 82 (2) ,83, 88 (8), 99 (9)
    #
    # [99]91(97)(69)
    except KeyboardInterrupt:
        print("Ended at", curr_value)
        exit()
    print()

if __name__ == '__main__':
    main()
