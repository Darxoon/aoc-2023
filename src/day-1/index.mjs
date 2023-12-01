import { readFile } from "fs/promises";

let input = await readFile('day-1/main.txt', 'utf8')

let inputLines = input.split('\n')

let accumulator = 0

for (let i = 0; i < inputLines.length; i++) {
    let digits = inputLines[i].matchAll(/\d/g)

    if (digits)
        accumulator += parseInt(digits.at(0) + digits.at(-1))
}

console.log('accumulator', accumulator)
