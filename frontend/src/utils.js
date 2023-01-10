export function round(number, digits) {
  let factor = Math.pow(10, digits);
  return Math.round(factor * number) / factor;
}
