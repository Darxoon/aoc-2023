use std::{fs, error::Error, time::Instant, char};

use once_cell::sync::Lazy;
use itertools::Itertools;
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};
use regex::Regex;

struct Rule {
    source_start: u32,
    destination_start: u32,
    count: u32,
}

impl Rule {
    fn is_in_bounds(&self, input: u32) -> bool {
        input >= self.source_start && input < self.source_start + self.count
    }
    
    fn get_match_unchecked(&self, input: u32) -> u32 {
        input - self.source_start + self.destination_start
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
        match self.rules.iter().find(|rule| rule.is_in_bounds(number)) {
            Some(rule) => rule.get_match_unchecked(number),
            None => number,
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let input_file = fs::read_to_string("input.txt")?;
    
    let instant = Instant::now();
    
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
    
    
    let handle_seed_range = |chunk: &Vec<&str>| {
        let instant = Instant::now();
        
        let seed_rule: Vec<u32> = chunk.iter().map(|string| string.parse::<u32>().unwrap()).collect();
        
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
        
        println!("Local minimum: {}, finished in {:.2?}", min, instant.elapsed());
        
        min
    };
    
    let chunks: Vec<Vec<&str>> = seed_rules_strings
        .chunks(2)
        .into_iter()
        .map(|x| x.collect_vec())
        .collect();
    
    let min = chunks.par_iter().map(handle_seed_range).min().unwrap();
    
    println!("Min: {}, finished in {:.2?}", min, instant.elapsed());
    
    Ok(())
}
