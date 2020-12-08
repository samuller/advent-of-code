#!/usr/bin/env python3
import os, json
from datetime import datetime


# A sort key to use for sorting Nones
def sk_nones_last(x):
    return (x is None, x)

def sort_nones_last(listy):
    return sorted(l, key=lambda x: sk_nones_last(x))


# Find first JSON file in current folder
json_fn = [f for f in os.listdir(".") if f.endswith('json')][0]
print('Found file', json_fn)
with open(json_fn) as f:
  data = json.load(f)


show_day = 8
last_day = show_day + 1

print('\nSubmission times for day {}:'.format(show_day))
member_times = {}
for member_id, member in sorted(data['members'].items()):
    print()
    print(member['name'], '({})'.format(member['local_score']))
    days = sorted(member['completion_day_level'].keys())
    for day in days:
        day_data = member['completion_day_level'][day]
        for part in sorted(day_data.keys()):
            ts = int(day_data[part]['get_star_ts'])
            # Local time (use utcfromtimestamp for UTC)
            time_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            if int(day) == show_day:
                print(day, '.', part, '=', time_str)

    times = []
    for num in range(1, last_day):
        if str(num) not in member['completion_day_level']:
            times.append(None)
            continue

        part1_time = member['completion_day_level'][str(num)].get(
            '1', {}).get('get_star_ts', None)
        part2_time = member['completion_day_level'][str(num)].get(
            '2', {}).get('get_star_ts', None)
        times.append(int(part1_time))
    member_times[member_id] = times
    # print(times)

print()
puzzle_times = {}
puzzle_order_idx = {}
member_ids = sorted(data['members'].keys())
for num in range(1-1, last_day-1):
    times = []
    for member_id in member_ids:
        times.append(member_times[member_id][num])
    puzzle_times[num] = times
    # print(num, times)

    # https://stackoverflow.com/questions/6422700/how-to-get-indices-of-a-sorted-array-in-python
    # print([i[0] for i in sorted(enumerate(times), key=lambda x: x[1])])
    # np.argsort()
    puzzle_order_idx[num] = [i[0] for i in sorted(
        enumerate(times), key=lambda x: sk_nones_last(x[1]))
    ]
    # print(num, puzzle_order_idx[num])

member_ranks = {}
for member_id in data['members']:
    ioi = member_ids.index(member_id)
    member_ranks[member_id] = []
    for num in range(1-1, last_day-1):
        rank = 1 + puzzle_order_idx[num].index(ioi)
        member_ranks[member_id].append(rank)

print('Ranks:')
for member_id, ranks in sorted(member_ranks.items()):
    name = data['members'][member_id]['name']
    print('{:<20}: {}'.format(name, str(ranks)))
