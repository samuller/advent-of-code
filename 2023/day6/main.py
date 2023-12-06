#!/usr/bin/env python3
import fileinput


def calc(times, distances):
    ans = 1
    for idx in range(len(distances)):
        time = times[idx]
        min_dist = distances[idx]
        ways_to_win = 0
        for i in range(time+1):
            new_dist = (time-i) * (i)
            # print(i, new_dist)
            if new_dist > min_dist:
                ways_to_win += 1
        # print(ways_to_win)
        ans *= ways_to_win
    return ans


def main():
    lines = [line.strip() for line in fileinput.input()]
    # Part 1
    times = [int(n) for n in lines[0].split(": ")[1].strip().split()]
    distances = [int(n) for n in lines[1].split(": ")[1].strip().split()]
    print(calc(times, distances))
    # Part 2
    times = [int("".join(lines[0].split(": ")[1].strip().split()))]
    distances = [int("".join(lines[1].split(": ")[1].strip().split()))]
    print(calc(times, distances))


if __name__ == '__main__':
    main()
