function param(params){
  const paramsOutput = new URLSearchParams();
  for (const key in params) {
    paramsOutput.append(key, params[key]);
  }
  return paramsOutput;
}

export default param
