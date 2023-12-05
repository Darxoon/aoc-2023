use std::{fs, error::Error};

use once_cell::sync::Lazy;
use itertools::{Itertools, Chunks};
use regex::Regex;

struct Rule {
    source_start: u32,
    destination_start: u32,
    count: u32,
}

impl Rule {
    fn get_match(&self, input: u32) -> Option<u32> {
        let is_in_bounds = input >= self.source_start && input < self.source_start + self.count;
        
        if is_in_bounds {
            Some(input - self.source_start + self.destination_start)
        } else {
            None
        }
    }
}

struct AlmanacMap {
    from: String,
    to: String,
    rules: Vec<Rule>,
}

impl AlmanacMap {
    fn new(input: &str) -> Self {
        static TITLE_REGEX: Lazy<Regex> = Lazy::new(|| Regex::new("^(\\w+)-to-(\\w+) map:").unwrap());
        
        let (full, [from, to]) = TITLE_REGEX
            .captures_iter(input)
            .map(|caps| caps.extract())
            .next()
            .unwrap();
        
        let mut rules: Vec<Rule> = Vec::new();
        
        let lines: Vec<&str> = input.split('\n').collect();
        
        for line in &lines[1..] {
            let numbers: Vec<u32> = line.split(' ').map(|x| x.parse::<u32>().unwrap()).collect();
            
            if let [destination_start, source_start, count] = numbers[..] {
                rules.push(Rule { source_start, destination_start, count });
            }
        }
        
        AlmanacMap { from: from.to_owned(), to: to.to_owned(), rules }
    }
    
    fn map(&self, number: u32) -> u32 {
        for rule in &self.rules {
            let rule_match = rule.get_match(number);
            
            if let Some(rule_match) = rule_match {
                return rule_match
            }
        }
        number
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let input_file = fs::read_to_string("input.txt")?;
    
    let find_char = |c: char| {
        input_file.chars().position(|x| x == c).unwrap()
    };
    
    let seed_rules_strings = input_file[
        find_char(':') + 2
        ..find_char('\n')
    ].split(' ');
    
    let maps: Vec<AlmanacMap> = input_file[find_char('\n') + 2..]
        .split("\n\n")
        .map(|block| AlmanacMap::new(block))
        .collect();
    
    println!("Seeds and maps parsed");
    
    let mut min_location: u32 = u32::MAX;
    
    for chunk in &seed_rules_strings.chunks(2) {
        let seed_rule: Vec<u32> = chunk.map(|string| string.parse::<u32>().unwrap()).collect();
        
        let mut current_map_index: usize = 0;
        let mut resources: Vec<u32> = (seed_rule[0]..seed_rule[0] + seed_rule[1]).collect();
        
        let map_amount: usize = maps.len().try_into().unwrap();
        
        while current_map_index < map_amount {
            let current_map: &AlmanacMap = &maps[current_map_index];
            
            println!("Going from {} to {}", current_map.from, current_map.to);
            
            current_map_index += 1;
            
            for resource in &mut resources {
                *resource = current_map.map(*resource);
            }
            
        }
        
        let min = *resources.iter().min().unwrap();
        
        println!("Local minimum: {}", min);
        
        if min_location > min {
            min_location = min;
            println!("New total minimum!");
        }
    }
    
    println!("Min: {}", min_location);
    
    Ok(())
}
