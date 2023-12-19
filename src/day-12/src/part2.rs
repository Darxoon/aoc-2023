use std::{fs, time::Instant, collections::{HashMap, hash_map::DefaultHasher}, hash::{Hash, Hasher}, rc::Rc, cell::RefCell, result};

use anyhow::Result;

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
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

#[derive(Clone, Copy, Hash)]
struct Segment {
    spring_type: SpringType,
    count: i32,
}

impl Segment {
    pub fn new(spring_type: SpringType, count: i32) -> Segment {
        Segment { spring_type, count }
    }
}

#[derive(Clone)]
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

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
enum Requirement {
    None,
    CantBeDamaged,
    MustBeDamaged,
}

struct Memo {
    // map: HashMap<(Option<Segment>, Option<i32>, Requirement, u64), u32>,
    map: HashMap<u64, u32>,
}

impl Memo {
    fn new() -> Memo {
        Memo {
            map: HashMap::new(),
            // map: RefCell::new(HashMap::new()),
        }
    }
    
    fn get_memo(&mut self, first_segment: Option<&Segment>, tail_segments: &[Segment],
                first_size: Option<i32>, tail_sizes: &[i32],
                requirement: Requirement) -> result::Result<u32, u64> {
        let mut hasher = DefaultHasher::new();
        first_segment.hash(&mut hasher);
        tail_segments.hash(&mut hasher);
        first_size.hash(&mut hasher);
        tail_sizes.hash(&mut hasher);
        requirement.hash(&mut hasher);
        
        let hash = hasher.finish();
        // let map = self.map.borrow_mut();
        
        if self.map.contains_key(&hash) {
            Ok(self.map.get(&hash).copied().unwrap())
        } else {
            Err(hash)
        }
    }
    
    fn put(&mut self, hash: u64, possibilities: u32) -> u32 {
        // let mut map = self.map.borrow_mut();
        self.map.insert(hash, possibilities);
        
        possibilities
    }
}

fn get_possibilities(first_segment: Option<&Segment>, tail_segments: &[Segment],
                     first_size: Option<i32>, tail_sizes: &[i32],
                     requirement: Requirement, memo: &mut Memo) -> u32 {
    if first_size.is_none() && first_segment.is_none() {
        return 1;
    }
    
    if first_size.is_none() {
        let first_segment_isnt_damaged = first_segment.unwrap().spring_type != SpringType::Damaged;
        
        if first_segment_isnt_damaged && tail_segments.iter().all(|segment| segment.spring_type != SpringType::Damaged) {
            return 1;
        } else {
            return 0;
        }
    }
    
    if first_segment.is_none() {
        return 0;
    }
    
    let memo_key = match memo.get_memo(first_segment, tail_segments, first_size, tail_sizes, requirement) {
        Ok(result) => return result,
        Err(key) => key,
    };
    
    let first_segment = first_segment.unwrap();
    let first_size = first_size.unwrap();
    
    let tail_segments_tail = if tail_segments.len() > 1 { &tail_segments[1..] } else { &[] };
    let tail_sizes_tail = if tail_sizes.len() > 1 { &tail_sizes[1..] } else { &[] };
    
    match first_segment.spring_type {
        SpringType::Ok => 
            if requirement == Requirement::MustBeDamaged {
                0
            } else {
                let result = get_possibilities(tail_segments.get(0), tail_segments_tail,
                    Some(first_size), tail_sizes, Requirement::None, memo);
                    
                memo.put(memo_key, result)
            },
        SpringType::Damaged =>
            if requirement == Requirement::CantBeDamaged || first_segment.count > first_size {
                0
            } else if first_segment.count == first_size {
                get_possibilities(tail_segments.get(0), tail_segments_tail,
                    tail_sizes.get(0).copied(), tail_sizes_tail, Requirement::CantBeDamaged, memo
                )
            } else {
                get_possibilities(tail_segments.get(0), tail_segments_tail,
                    Some(first_size - first_segment.count), tail_sizes, Requirement::MustBeDamaged, memo
                )
            },
        SpringType::Unknown => {
            if requirement == Requirement::CantBeDamaged && first_segment.count == 1 {
                let result = get_possibilities(tail_segments.get(0), tail_segments_tail,
                    Some(first_size), tail_sizes, Requirement::None, memo);
                return memo.put(memo_key, result);
            }
            
            let damaged_offset_range = match requirement {
                Requirement::None => 0..=first_segment.count,
                Requirement::CantBeDamaged => 1..=first_segment.count,
                Requirement::MustBeDamaged => 0..=0,
            };
            
            let mut accumulator: u32 = 0;
            
            for damaged_offset in damaged_offset_range {
                if first_segment.count == damaged_offset {
                    accumulator += get_possibilities(tail_segments.get(0), tail_segments_tail,
                        Some(first_size), tail_sizes, Requirement::None, memo);
                } else if first_size + damaged_offset > first_segment.count {
                    accumulator += get_possibilities(tail_segments.get(0), tail_segments_tail,
                        Some(first_size - first_segment.count + damaged_offset), tail_sizes, Requirement::MustBeDamaged, memo);
                } else if first_size + damaged_offset == first_segment.count {
                    accumulator += get_possibilities(tail_segments.get(0), tail_segments_tail,
                        tail_sizes.get(0).copied(), tail_sizes_tail, Requirement::CantBeDamaged, memo);
                } else {
                    let mut new_first_segment = first_segment.clone();
                    new_first_segment.count -= damaged_offset + first_size;
                    
                    accumulator += get_possibilities(Some(&new_first_segment), tail_segments,
                        tail_sizes.get(0).copied(), tail_sizes_tail, Requirement::CantBeDamaged, memo);
                }
            }
            
            memo.put(memo_key, accumulator)
        },
    }
}

fn unfold_record(mut record: Record) -> Record {
    let segment_count = record.segments.len();
    let size_count = record.sizes.len();
    
    record.segments.reserve(segment_count * 6);
    record.sizes.reserve(size_count * 6);
    
    for _ in 0..4 {
        if record.segments[0].spring_type == SpringType::Unknown {
            let mut new_segment = record.segments[0];
            new_segment.count += 1;
            
            record.segments.push(new_segment);
        } else {
            record.segments.push(Segment::new(SpringType::Unknown, 1));
            record.segments.push(record.segments[0]);
        }
        
        for i in 1..segment_count {
            record.segments.push(record.segments[i]);
        }
    }
    
    for _ in 0..4 {
        for i in 0..size_count {
            record.sizes.push(record.sizes[i]);
        }
    }
    
    record
}

pub fn main() -> Result<()> {
    let input_file = fs::read_to_string("input.txt")?;
    
    let now = Instant::now();
    
    let records: Vec<Record> = input_file.lines().map(Record::from_line).collect();
    
    let x: u32 = records.iter()
        .map(|record| unfold_record(record.clone()))
        .enumerate()
        .map(|(i, record)| {
            let now = Instant::now();
            let result = get_possibilities(Some(&record.segments[0]), &record.segments[1..],
                Some(record.sizes[0]), &record.sizes[1..], Requirement::None, &mut Memo::new());
            println!("finished {} in {:?}", i, now.elapsed());
            return result;
        })
        .sum();
    
    let elapsed = now.elapsed();
    
    println!("{} (finished in {:?})", x, elapsed);
    
    Ok(())
}
