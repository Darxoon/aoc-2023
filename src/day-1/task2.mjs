import { readFile } from "fs/promises";

function strToNumber(str) {
    switch (str) {
        case "one":   return 1;
        case "two":   return 2;
        case "three": return 3;
        case "four":  return 4;
        case "five":  return 5;
        case "six":   return 6;
        case "seven": return 7;
        case "eight": return 8;
        case "nine":  return 9;
        default:
            if (/^\d*$/.test(str))
                return parseInt(str)
            else
                throw new Error(str)
    }
}
function strToNumberReversed(str) {
    switch (str) {
        case "eno":   return 1;
        case "owt":   return 2;
        case "eerht": return 3;
        case "ruof":  return 4;
        case "evif":  return 5;
        case "xis":   return 6;
        case "neves": return 7;
        case "thgie": return 8;
        case "enin":  return 9;
        default:
            if (/^\d*$/.test(str))
                return parseInt(str)
            else
                throw new Error(str)
    }
}

let input = await readFile('day-1/main.txt', 'utf8')

let inputLines = input.split('\n')

let accumulator = 0

for (let i = 0; i < inputLines.length; i++) {
    let line = inputLines[i]
    
    let firstDigit = line.match(/(one|two|three|four|five|six|seven|eight|nine|\d)/)
    let lastDigit = line.split('').reverse().join('').match(/(eno|owt|eerht|ruof|evif|xis|neves|thgie|enin|\d)/)

    if (firstDigit && lastDigit)
        accumulator += parseInt(strToNumber(firstDigit[0]) + "" + strToNumberReversed(lastDigit[0]))
}

console.log('accumulator', accumulator)
