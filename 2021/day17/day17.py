#!/usr/bin/env python3
import fileinput


def simulate(dx, dy, xlim, ylim):
    # print("speed:", dx, dy)
    # simulate
    x, y = 0, 0
    highest = 0
    for step in range(1000):
        x += dx
        y += dy
        # drag
        if dx > 0:
            dx -= 1
        elif dx < 0:
            dx += 1
        dy -= 1
        if y > highest:
            highest = y
        # print(x,y)
        # TODO: simulate further for higher points?
        if xlim[0]<=x<=xlim[1] and ylim[0]<=y<=ylim[1]:
            return highest
    return None


def search(xlim, ylim):
    # dx/s
    dx, dy = 0, 0
    answers = []
    for dx in range(200):
        for dy in range(-150,150):
            highest = simulate(dx, dy, xlim, ylim)
            # highest = simulate(7, 2, xlim, ylim)
            if highest is not None:
                answers.append((highest, dx, dy))
            # print(highest)
            # exit()
    answers = sorted(answers, key=lambda x: x[0], reverse=True)
    return answers

# assert simulate(7, 2, [20, 30], [-10, -5]) is not None
# assert simulate(6, 3, [20, 30], [-10, -5]) is not None
# assert simulate(9, 0, [20, 30], [-10, -5]) is not None
# assert simulate(17, -4, [20, 30], [-10, -5]) is None
# example = search([20, 30], [-10, -5])
# assert (45,6,9) in example

# 1176 @ 7:22
# 4950 @ 7:28 - right for someone else? (17,99)
# P2: 1523 @ 7:31, 2183 @ 7:32
def main():
    lines = [line.strip() for line in fileinput.input()]
    limits = lines[0].split(": ")[1]
    xlim, ylim = limits.split(", ")
    assert xlim.startswith("x=")
    assert ylim.startswith("y=")
    xlim = [int(x) for x in xlim[2:].split("..")]
    ylim = [int(y) for y in ylim[2:].split("..")]
    print(xlim, ylim)

    answers = search(xlim, ylim)
    print(len(answers))
    print(answers[0])


if __name__ == '__main__':
    main()
