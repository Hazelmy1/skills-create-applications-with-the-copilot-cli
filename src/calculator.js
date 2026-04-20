/**
 * Node.js CLI Calculator App
 *
 * Supports the following operations:
 *   - addition
 *   - subtraction
 *   - multiplication
 *   - division
 *   - modulo
 *   - power (exponentiation)
 *   - squareRoot
 */

/**
 * addition - Returns the sum of a and b.
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function addition(a, b) {
  return a + b;
}

/**
 * subtraction - Returns the difference of a minus b.
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function subtraction(a, b) {
  return a - b;
}

/**
 * multiplication - Returns the product of a and b.
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function multiplication(a, b) {
  return a * b;
}

/**
 * division - Returns the quotient of a divided by b.
 * Throws an error if b is zero.
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function division(a, b) {
  if (b === 0) {
    throw new Error('Division by zero is not allowed');
  }
  return a / b;
}

/**
 * modulo - Returns the remainder of a divided by b.
 * Throws an error if b is zero.
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function modulo(a, b) {
  if (b === 0) {
    throw new Error('Modulo by zero is not allowed');
  }
  return a % b;
}

/**
 * power - Returns base raised to the given exponent.
 * @param {number} base
 * @param {number} exponent
 * @returns {number}
 */
function power(base, exponent) {
  return Math.pow(base, exponent);
}

/**
 * squareRoot - Returns the square root of n.
 * Throws an error if n is negative.
 * @param {number} n
 * @returns {number}
 */
function squareRoot(n) {
  if (n < 0) {
    throw new Error('Cannot take square root of a negative number');
  }
  return Math.sqrt(n);
}

module.exports = {
  addition,
  subtraction,
  multiplication,
  division,
  modulo,
  power,
  squareRoot,
};
