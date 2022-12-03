#![allow(clippy::needless_return)]
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
            if line == "" {
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


fn main() {
    // day1("../day1/test.txt".to_string());
    day1("../day1/input.txt".to_string());
}
