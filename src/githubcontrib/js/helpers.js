export function param(params) {
  const paramsOutput = new URLSearchParams();
  for (const key in params) {
    if (Object.prototype.hasOwnProperty.call(params, key)) {
      paramsOutput.append(key, params[key]);
    }
  }
  return paramsOutput;
}
