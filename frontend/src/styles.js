export function cssVariables(node, variables) {
  setCssVariables(node, variables);
  
  return {
    update(variables) {
      setCssVariables(node, variables);
    }
  }
}

export function setCssVariables(node, variables) {
  for (const name in variables) {
    node.style.setProperty(`--${name}`, variables[name]);
  }
}
