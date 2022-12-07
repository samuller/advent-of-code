#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


def root_add(contents, path, file=None, size=0):
    # print("ADD", contents, path)
    assert path.startswith("/")
    curr = contents
    if path != "/":
        path = path[1:]
        path = path.split("/")
        for part in path:
            if part in curr:
                curr = curr[part]
                continue
            # Create new subdirectory
            curr[part]= {}
    if file is not None:
        curr[file] = size
    # return contents


def process_ls_output(root_contents, curdir, curdir_contents):
    for res_line in curdir_contents:
        res = res_line.split()
        if res[0] == "dir":
            deepdir = curdir.split("/")[-1]
            # assert res[1] == deepdir, f"'{res[1]}' vs '{deepdir}'"
            root_add(root_contents, f"{curdir}/{res[1]}".replace("//", "/"))
        else:
            root_add(root_contents, f"{curdir}", file=res[1], size=int(res[0]))
    # print(curdir_contents)


def recurse_size(contents, size_limit=None):
    assert type(contents) == dict
    total = 0
    dirsum = 0
    dir_sizes = []
    for key in contents:
        curr = contents[key]
        if type(curr) == dict:
            res, child_dirsum, child_dir_sizes = recurse_size(curr, size_limit)
            dir_sizes.append((key, res))
            dir_sizes.extend(child_dir_sizes)
            # print("SUB", key, res)
            if size_limit is not None:
                if res > size_limit:
                    # print("SKIP", key, res)
                    # continue
                    pass
                else:
                    # print("DIRSUM", key, res)
                    dirsum += res

            dirsum += child_dirsum
            total += res
            continue

        size = curr
        assert type(size) == int, type(size)
        total += size
    return total, dirsum, dir_sizes


# 2 hour power delay 
# part 2: 19935440 - too hight
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # print(lines)
    total_space = 70_000_000
    unused_space_needed = 30_000_000

    root_contents = {}
    curdir = None
    curdir_contents = []
    ls_results = False
    for line in lines:
        if line.startswith("$"):
            if ls_results:
                process_ls_output(root_contents, curdir, curdir_contents)
                ls_results = False
                curdir_contents = []
            # Split and dop dollar
            cmd = line.split()[1:]
            assert cmd[0] in ['ls', 'cd'], cmd[0]
            if cmd[0] == "cd":
                newdir = cmd[1]
                if ".." in newdir:
                    assert curdir is not None
                    assert newdir == "..", newdir
                    curdir = "/".join(curdir.split("/")[0:-1])
                    if len(curdir) == 0:
                        curdir = "/"
                    # curdir = f"{curdir}/"
                elif curdir is None or newdir == "/":
                    assert newdir == "/", newdir
                    curdir = "/"
                else:
                    curdir = f"{curdir}/{newdir}".replace("//", "/")
            if cmd[0] == "ls":
                ls_results = True
        elif ls_results:
            result = line.split()
            curdir_contents.append(line)
        # print(curdir)

    if ls_results:
        process_ls_output(root_contents, curdir, curdir_contents)
        ls_results = False
        curdir_contents = []

    # print(root_contents)
    # print(recurse_size(root_contents))
    total_used, smalldirs, alldirs = recurse_size(root_contents, size_limit=100_000)
    # print(smalldirs)
    total_unused = total_space - total_used
    space_need_to_free = unused_space_needed - total_unused
    # print(space_need_to_free)
    # print(alldirs)
    for dir_size in sorted(alldirs, key=lambda t: t[1]):
        dir, size = dir_size
        if size >= space_need_to_free:
            print(dir, size)
            break


if __name__ == '__main__':
    main()
