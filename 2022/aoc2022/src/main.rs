#![allow(clippy::needless_return)]
#![allow(dead_code)]
use std::fs::File;
use std::path::Path;
// Needed for read_to_string?
use std::io::{prelude::*, BufReader};

/**
 * Generic helper functions.
 */

// https://stackoverflow.com/questions/30801031/read-a-file-and-get-an-array-of-strings
fn get_lines(input_path: String) -> Vec<String> {
    let path = Path::new(&input_path);
    // Open the path in read-only mode, returns `io::Result<File>`
    let file = File::open(path)
        .unwrap_or_else(|_| panic!("no such file: {}", path.display()));
    let buf = BufReader::new(file);
    return buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect();
}

/// An iterator that returns a group lines separated by empty lines.
struct Grouped<'a> {
    list: &'a Vec<String>,
    curr_idx: usize,
}

impl<'a> Grouped<'a> {
    /// Constructor
    fn new(list: &'a Vec<String>) -> Grouped<'a> {
        Self {
           list,
           curr_idx: 0
        }
    }
}

impl Iterator for Grouped<'_> {
    type Item = Vec<String>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.curr_idx >= self.list.len() {
            return None;
        }
        let mut new_group: Vec<String> = Vec::new();
        while self.curr_idx < self.list.len() {
            let line = &self.list[self.curr_idx];
            self.curr_idx += 1;
            if line.is_empty() {
                break;
            }
            new_group.push(line.clone());
        }
        return Some(new_group);
    }
}

/**
 * Experimentation.
 */

#[allow(dead_code)]
fn day0(input_path: String) {
    let _lines = get_lines(input_path);
    // println!("{:?}", lines);
    // println!("{:#?}", lines);
    // for line in lines {
    //     println!("{}", line);
    // }
}

/**
 * Actual solutions (with their own helper functions).
 */

fn day1(input_path: String) {
    let lines = get_lines(input_path);
    let mut elves = Vec::new();
    for elf_items in Grouped::new(&lines) {
        let summ: i32 = elf_items.iter().map(|l| l.parse::<i32>().unwrap()).sum();
        elves.push(summ);
    }
    elves.sort();
    println!("{:?}", elves.last().unwrap());
    println!("{:?}", elves.iter().rev().take(3).sum::<i32>());
}


fn day4(input_path: String) {
    let lines = get_lines(input_path);

    let mut part1 = 0;
    let mut part2 = 0;
    for line in lines {
        let mut elves = line.split(',');
        let (elf1_str, elf2_str) = (elves.next(), elves.next());
        let elf1: [i32; 2] = elf1_str.unwrap().split('-').map(|n| n.parse::<i32>().unwrap()).collect::<Vec<_>>()
            // convert Vec<i32> to [i32; 2]
            .try_into().unwrap();
        let elf2: [i32; 2] = elf2_str.unwrap().split('-').map(|n| n.parse::<i32>().unwrap()).collect::<Vec<_>>()
            .try_into().unwrap();
        // println!("{:?}, {:?}", elf1, elf2);

        if (elf1[0] >= elf2[0] && elf1[1] <= elf2[1]) || (elf2[0] >= elf1[0] && elf2[1] <= elf1[1]){
            part1 += 1;
        }
        if (elf2[0] <= elf1[0] && elf1[0] <= elf2[1])
          || (elf2[0] <= elf1[1] && elf1[1] <= elf2[1])
          || (elf1[0] <= elf2[0] && elf2[0] <= elf1[1])
          || (elf1[0] <= elf2[1] && elf2[1] <= elf1[1]) {
            part2 += 1;
        }
    }
    println!("{}", part1);
    println!("{}", part2);
}


fn main() {
    // day1("../day1/test.txt".to_string());
    // day1("../day1/input.txt".to_string());
    // day4("../day4/test.txt".to_string());
    day4("../day4/input.txt".to_string());
}
