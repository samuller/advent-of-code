#!/usr/bin/env python3
import fileinput
from collections import Counter


def get_unique_digit(wires):
    stats = Counter(wires)
    if len(stats) == 2:
        return 1
    if len(stats) == 3:
        return 7
    if len(stats) == 4:
        return 4
    if len(stats) == 7:
        return 8
    return None


DISPLAY_WIRES = {
    0: 'abcefg', # 6
    1: 'cf',
    2: 'acdeg', # 5
    3: 'acdfg', # 5
    4: 'bcdf',
    5: 'abdfg', # 5
    6: 'abdefg', # 6
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg', # 6
}
# Check all values are unique
assert len(set(DISPLAY_WIRES.values())) == len(DISPLAY_WIRES)

def list_in_list(small_list, big_list):
    return all([val in big_list for val in small_list])


def decode_wires(inputs):
    assert len(inputs) == 10
    mapping = {}
    rev_mapping = {}
    # 1/4/7/8
    for wires_str in inputs:
        wires_str = ''.join(sorted(wires_str))
        digit = get_unique_digit(wires_str)
        if digit is not None:
            mapping[wires_str] = digit
            rev_mapping[digit] = wires_str
    # 0/2/3/5/6/9
    maybe_25 = []
    for wires_str in inputs:
        # sort wires
        wires_str = ''.join(sorted(wires_str))
        wires = list(wires_str)
        # 0/6/9
        if len(wires) == 6:
            one_wires = list(rev_mapping[1])
            # 0/9
            if list_in_list(one_wires, wires):
                four_wires = list(rev_mapping[4])
                # 9
                if list_in_list(four_wires, wires):
                    mapping[wires_str] = 9
                    rev_mapping[9] = wires
                # 0
                else:
                    mapping[wires_str] = 0
                    rev_mapping[0] = wires
            # 6
            else:
                mapping[wires_str] = 6
                rev_mapping[6] = wires
        # 2/3/5
        if len(wires) == 5:
            one_wires = list(rev_mapping[1])
            # 3
            if list_in_list(one_wires, wires):
                mapping[wires_str] = 3
                rev_mapping[3] = wires
            # 2/5
            else:
                mapping[wires_str] = 2
                rev_mapping[2] = wires
                # for later
                maybe_25.append(wires_str)
    # 2/5
    for wires_str in maybe_25:
        six_wires = list(rev_mapping[6])
        if list_in_list(wires_str, six_wires):
            mapping[wires_str] = 5
            rev_mapping[5] = wires
        else:
            mapping[wires_str] = 2
            rev_mapping[2] = wires
    # Check there are no conflicting mappings (i.e. each unique)
    assert len(set(mapping.values())) == len(mapping)
    return mapping


def wires_to_digits(wires, wire_mapping):
    digits = []
    for unk in wires:
        unk = ''.join(sorted(unk))
        assert unk in wire_mapping, f"{unk} in {wire_mapping}"
        digits.append(wire_mapping[unk])
    return digits


test_inp = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split(' ')
test_out = "cdfeb fcadb cdfeb cdbaf".split(' ')
assert wires_to_digits(test_inp, decode_wires(test_inp)) == [8, 5, 2, 3, 7, 9, 6, 4, 0, 1]
assert wires_to_digits(test_out, decode_wires(test_inp)) == [5, 3, 5, 3]


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    # Part 1
    # decoded = []
    # for line in lines:
    #     inputs, outputs = line.split(' | ')
    #     inputs = inputs.split(' ')
    #     outputs = outputs.split(' ')
    #     print(outputs)
    #     for wires in outputs:
    #         print(wires)
    #         digit = get_unique_digit(wires)
    #         if digit is not None:
    #             print(wires, '->', digit)
    #         decoded.append(digit)
    # print(decoded)
    # digit_counts = Counter(decoded)
    # print(digit_counts)
    # print(digit_counts[1] + digit_counts[4] + digit_counts[7] + digit_counts[8])


    # Part 2
    decoded = []
    summ = 0
    for line in lines:
        # Split
        inputs, outputs = line.split(' | ')
        inputs = inputs.split(' ')
        outputs = outputs.split(' ')
        # Use input to determine wiring
        wire_mapping = decode_wires(inputs)

        # print(line)
        # Use wiring to determine whole output digits and sum them
        mapping = decode_wires(inputs)
        # print(mapping)
        input_digits = wires_to_digits(inputs, mapping)
        output_digits = wires_to_digits(outputs, mapping)
        # print(input_digits)
        # print(output_digits)
        output_num = int(''.join([str(d) for d in output_digits]))
        # print(output_num)
        summ += output_num
        # exit()
    print(summ)


if __name__ == '__main__':
    main()
