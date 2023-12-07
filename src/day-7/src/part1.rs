use std::{fs, iter::repeat, time::Instant, cmp::Ordering};

use anyhow::Result;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
enum Card {
    Two,
    Three,
    Four,
    Five,
    Six,
    Seven,
    Eight,
    Nine,
    Ten,
    J,
    Q,
    K,
    A,
    Length,
}

impl Card {
    fn from_char(c: char) -> Card {
        match c {
            '2' => Card::Two,
            '3' => Card::Three,
            '4' => Card::Four,
            '5' => Card::Five,
            '6' => Card::Six,
            '7' => Card::Seven,
            '8' => Card::Eight,
            '9' => Card::Nine,
            'T' => Card::Ten,
            'J' => Card::J,
            'Q' => Card::Q,
            'K' => Card::K,
            'A' => Card::A,
            _ => panic!(),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
enum Type {
    FiveKind,
    FourKind,
    FullHouse,
    ThreeKind,
    TwoPair,
    Pair,
    HighCard,
}

impl Type {
    fn cmp(self, other: Type) -> Ordering {
        (self as u32).cmp(&(other as u32))
    }
}

#[derive(Debug)]
struct Hand {
    cards: Vec<Card>,
    bid: u32,
    
    hand_type: Type,
}

impl Hand {
    fn from_line(line: &str) -> Hand {
        let cards_str = &line[..line.chars().position(|x| x == ' ').unwrap()];
        
        let cards: Vec<Card> = cards_str
            .chars()
            .map(Card::from_char)
            .collect();
        
        let mut index: Vec<u32> = repeat(0).take(Card::Length as usize).collect();
        
        for card in &cards {
            index[*card as usize] += 1;
        }
        
        index.sort_by(|a, b| b.cmp(a));
        
        Hand {
            bid: line.strip_prefix(cards_str).unwrap().trim().parse().unwrap(),
            cards,
            hand_type: match index[0] {
                1 => Type::HighCard,
                2 => if index[1] == 2 { Type::TwoPair } else { Type::Pair },
                3 => if index[1] == 2 { Type::FullHouse } else { Type::ThreeKind },
                4 => Type::FourKind,
                5 => Type::FiveKind,
                _ => panic!(),
            },
        }
    }
}

pub fn main() -> Result<()> {
    let input_file = fs::read_to_string("input.txt")?;
    let now = Instant::now();
    
    let mut hands: Vec<Hand> = input_file.lines().map(Hand::from_line).collect();
    hands.sort_by(|a, b| a.hand_type.cmp(b.hand_type).reverse().then_with(|| a.cards.cmp(&b.cards)));
    
    let winnings: u32 = hands.iter()
        .enumerate()
        .map(|(i, hand)| hand.bid * u32::try_from(i + 1).unwrap())
        .sum();
    
    let elapsed = now.elapsed();
    
    println!("winnings {:?}, took {:?}", winnings, elapsed);
    
    Ok(())
}
