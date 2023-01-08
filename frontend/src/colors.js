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

    c = Math.floor(255 * c)
    x = Math.floor(255 * x)

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

    return [r, g, b]
}

export function hex2rgb(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return [r, g, b];
}
