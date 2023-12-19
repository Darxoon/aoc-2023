use anyhow::Result;

mod part1;
mod part2;

fn main() -> Result<()> {
    println!("---- Part 1 ----");
    part1::main()?;
    println!("\n---- Part 2 ----");
    part2::main()?;
    
    Ok(())
}
