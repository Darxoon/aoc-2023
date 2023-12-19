use std::{fs, time::Instant};

use anyhow::Result;

#[derive(Clone, Copy, PartialEq, Eq)]
enum SpringType {
    Ok,
    Damaged,
    Unknown,
}

impl SpringType {
    fn from_char(input: char) -> SpringType {
        match input {
            '.' => Self::Ok,
            '#' => Self::Damaged,
            '?' => Self::Unknown,
            _ => panic!(),
        }
    }
}

#[derive(Clone)]
struct Segment {
    spring_type: SpringType,
    count: i32,
}

struct Record {
    segments: Vec<Segment>,
    sizes: Vec<i32>,
}

impl Record {
    fn from_line(input: &str) -> Record {
        let first_char = input.chars().next().unwrap();
        
        let mut spring_type = SpringType::from_char(first_char);
        let mut spring_count = 1;
        
        let mut segments = Vec::new();
        
        let mut sizes: Vec<i32> = Vec::new();
        
        for (i, c) in input.chars().skip(1).enumerate() {
            if c == ' ' {
                sizes = input[i + 2..].split(',').map(|x| x.parse().unwrap()).collect();
                
                segments.push(Segment {
                    spring_type,
                    count: spring_count,
                });
                
                break;
            }
            
            if SpringType::from_char(c) == spring_type {
                spring_count += 1;
            } else {
                segments.push(Segment {
                    spring_type,
                    count: spring_count,
                });
                
                spring_type = SpringType::from_char(c);
                spring_count = 1;
            }
        }
        
        Record { segments, sizes }
    }
}

fn get_possibilities(segments: &[Segment], sizes: &[i32], follows_damaged: bool, must_start_with_damaged: bool) -> i32 {
    if sizes.len() == 0 {
        if segments.iter().all(|segment| segment.spring_type != SpringType::Damaged) {
            return 1;
        } else {
            return 0;
        }
    }
    
    if segments.len() == 0 {
        return 0;
    }
    
    match segments[0].spring_type {
        SpringType::Ok => 
            if must_start_with_damaged {
                0
            } else {
                get_possibilities(&segments[1..], sizes, false, false)
            },
        SpringType::Damaged =>
            if (follows_damaged && !must_start_with_damaged) || segments[0].count > sizes[0] {
                0
            } else if segments[0].count == sizes[0] {
                get_possibilities(&segments[1..], &sizes[1..], true, false)
            } else {
                let mut new_sizes: Vec<i32> = sizes.to_owned();
                new_sizes[0] -= segments[0].count;
                
                get_possibilities(&segments[1..], &new_sizes, true, true)
            },
        SpringType::Unknown => {
            if follows_damaged && !must_start_with_damaged && segments[0].count == 1 {
                return get_possibilities(&segments[1..], sizes, false, false);
            }
            
            let damaged_offset_range = if must_start_with_damaged {
                0..=0
            } else if follows_damaged {
                1..=segments[0].count
            } else {
                0..=segments[0].count
            };
            
            let mut accumulator: i32 = 0;
            
            for damaged_offset in damaged_offset_range {
                if segments[0].count == damaged_offset {
                    accumulator += get_possibilities(&segments[1..], &sizes, false, false)
                } else if sizes[0] + damaged_offset > segments[0].count {
                    let mut new_sizes: Vec<i32> = sizes.to_owned();
                    new_sizes[0] -= segments[0].count - damaged_offset;
                    
                    accumulator += get_possibilities(&segments[1..], &new_sizes, true, true);
                } else if sizes[0] + damaged_offset == segments[0].count {
                    accumulator += get_possibilities(&segments[1..], &sizes[1..], true, false);
                } else {
                    let mut new_segments: Vec<Segment> = segments.to_owned();
                    new_segments[0].count -= damaged_offset + sizes[0];
                    
                    accumulator += get_possibilities(&new_segments, &sizes[1..], true, false);
                }
            }
            
            accumulator
        },
    }
}

pub fn main() -> Result<()> {
    let input_file = fs::read_to_string("input.txt")?;
    
    let now = Instant::now();
    
    let records: Vec<Record> = input_file.lines().map(Record::from_line).collect();
    
    let x: i32 = records.iter()
        .map(|record| get_possibilities(&record.segments, &record.sizes, false, false))
        .sum();
    
    let elapsed = now.elapsed();
    
    println!("{} (finished in {:?})", x, elapsed);
    
    Ok(())
}
