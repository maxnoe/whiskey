<script>
import { onMount } from 'svelte';
import { hsv2rgb } from './colors.js';

export let hue;
export let saturation;
export let value = 1.0;

let dragging = false;

let canvas;
let ctx;
let colors;
let img_data;


onMount(() => {
    ctx = canvas.getContext("2d");
    colors = ctx.createImageData(canvas.width, canvas.height);
    img_data = colors.data;
    update();
});


function setColor(event) {
    if (event.type == "mousemove" && !dragging) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    let [h, s] = xy2hs(x, y);
    hue = h;
    saturation = Math.min(s, 1.0);
    update();
}


function hs2xy(h, s) {
    let phi = 2 * Math.PI * h;
    let x = 0.5 * canvas.width - 0.475 * s * Math.sin(phi) * canvas.width;
    let y = 0.5 * canvas.height - 0.475 * s * Math.cos(phi) * canvas.height;
    return [x, y];
}

function xy2hs(x, y) {
    let dy = (y - 0.5 * canvas.height) / (0.475 * canvas.height);
    let dx = (x - 0.5 * canvas.width) / (0.475 * canvas.width);

    let h = 0.5 + Math.atan2(dx, dy) / (2 * Math.PI);
    let s = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));
    return [h, s];
}


function fill() {
    for (let x=0; x < canvas.width; x++) {
        for (let y=0; y < canvas.height; y++) {
            let [h, s] = xy2hs(x, y);
            if (s > 1.02) continue;

            let [r, g, b] = hsv2rgb(h, s, value);
            let idx = y * canvas.width * 4 + x * 4;
            img_data[idx] = r;
            img_data[idx + 1] = g;
            img_data[idx + 2] = b;
            img_data[idx + 3] = 255;
        }
    }
    ctx.putImageData(colors, 0, 0);
}


function update() {
    fill();

    let [x, y] = hs2xy(hue, saturation);
    [-1, 1].forEach(sign => {
        ctx.beginPath();
        ctx.moveTo(x, y + sign * 2);
        ctx.lineTo(x, y + sign * 10);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(x + sign * 2, y);
        ctx.lineTo(x + sign * 10, y);
        ctx.stroke();
    })
}
</script>

<canvas
    width="300" height="300"
    class="popup"
    on:mousemove={setColor}
    on:click={setColor}
    on:mousedown={(event) => {dragging = true; setColor(event)}}
    on:mouseup={() => {dragging = false;}}
    bind:this={canvas}
></canvas>

<style>
canvas {
    border: 3px solid darkgray;
    border-radius: 5px;
}
</style>
