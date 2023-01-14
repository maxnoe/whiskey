export function to_hex(integer) {
    var str = Number(integer).toString(16);
    return str.length == 1 ? "0" + str : str;
}

export function rgb2hex(r, g, b) {
    if (arguments.length == 1) {
        g = r[1];
        b = r[2];
        r = r[0];
    }
    return "#" + to_hex(r) + to_hex(g) + to_hex(b);
}

export function hsv2rgb(h, s, v) {
  if (arguments.length == 1) {
      s = h[1];
      v = h[2];
      h = h[0];
  }

  h = h / (1/6);
  let c = s * v;
  let x = c * (1 - Math.abs(h % 2 - 1));
  let m = v - c;

  let r = 0;
  let g = 0;
  let b = 0;

  switch (Math.floor(h) % 6) {
      case 0: r = c; g = x; break;
      case 1: r = x; g = c; break;
      case 2: g = c; b = x; break;
      case 3: g = x; b = c; break;
      case 4: r = x; b = c; break;
      case 5: r = c; b = x; break;
  }

  return [Math.round((r + m) * 255), Math.round((g + m) * 255), Math.round((b + m) * 255)]
}


export function rgb2hsv(r, g, b) {
  if (arguments.length == 1) {
      g = r[1];
      b = r[2];
      r = r[0];
  }
  let x_max = Math.max(r, g, b);
  let x_min = Math.min(r, g, b);
  let c = x_max - x_min;
  let v = 0.5 * (c + (x_max + x_min));
  let h = 0;
  if (v == r) {
    h = (1/6) * (0 + (g - b) / c);
  } else if (v == g) {
    h = (1/6) * (2 + (b - r) / c);
  } else if (v == b) {
    h = (1/6) * (4 + (r - g) / c)
  }

  let s = 0;
  if (v != 0) {
    s = c / v;
  }
  return [h, s, v];
}

export function hex2rgb(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return [r, g, b];
}
