const {
  addition,
  subtraction,
  multiplication,
  division,
  modulo,
  power,
  squareRoot,
} = require('../calculator');

// Basic arithmetic tests

// addition tests
console.assert(addition(2, 3) === 5, 'addition: 2 + 3 should equal 5');
console.assert(addition(-1, 1) === 0, 'addition: -1 + 1 should equal 0');
console.assert(addition(0, 0) === 0, 'addition: 0 + 0 should equal 0');

// subtraction tests
console.assert(subtraction(5, 3) === 2, 'subtraction: 5 - 3 should equal 2');
console.assert(subtraction(0, 5) === -5, 'subtraction: 0 - 5 should equal -5');
console.assert(subtraction(-3, -3) === 0, 'subtraction: -3 - -3 should equal 0');

// multiplication tests
console.assert(multiplication(3, 4) === 12, 'multiplication: 3 * 4 should equal 12');
console.assert(multiplication(-2, 5) === -10, 'multiplication: -2 * 5 should equal -10');
console.assert(multiplication(0, 99) === 0, 'multiplication: 0 * 99 should equal 0');

// division tests
console.assert(division(10, 2) === 5, 'division: 10 / 2 should equal 5');
console.assert(division(7, 2) === 3.5, 'division: 7 / 2 should equal 3.5');
try {
  division(1, 0);
  console.assert(false, 'division: should throw on division by zero');
} catch (e) {
  console.assert(e.message.includes('zero'), 'division: error message should mention zero');
}

// modulo tests
console.assert(modulo(10, 3) === 1, 'modulo: 10 % 3 should equal 1');
console.assert(modulo(15, 5) === 0, 'modulo: 15 % 5 should equal 0');
console.assert(modulo(7, 4) === 3, 'modulo: 7 % 4 should equal 3');
try {
  modulo(5, 0);
  console.assert(false, 'modulo: should throw on modulo by zero');
} catch (e) {
  console.assert(e.message.includes('zero'), 'modulo: error message should mention zero');
}

// power (exponentiation) tests
console.assert(power(2, 10) === 1024, 'power: 2^10 should equal 1024');
console.assert(power(3, 3) === 27, 'power: 3^3 should equal 27');
console.assert(power(5, 0) === 1, 'power: 5^0 should equal 1');
console.assert(power(2, -1) === 0.5, 'power: 2^-1 should equal 0.5');

// square root tests
console.assert(squareRoot(9) === 3, 'squareRoot: sqrt(9) should equal 3');
console.assert(squareRoot(0) === 0, 'squareRoot: sqrt(0) should equal 0');
console.assert(squareRoot(2) === Math.SQRT2, 'squareRoot: sqrt(2) should equal Math.SQRT2');
try {
  squareRoot(-1);
  console.assert(false, 'squareRoot: should throw on negative number');
} catch (e) {
  console.assert(e.message.includes('negative'), 'squareRoot: error message should mention negative');
}

console.log('All calculator tests passed!');
