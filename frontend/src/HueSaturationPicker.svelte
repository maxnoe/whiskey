<script>
import { onMount } from 'svelte';
import { hsv2rgb } from './colors.js';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();
export let hue;
export let saturation;
export let value = 1.0;
export let open = false;

let dragging = false;

let canvas;
let ctx;
let colors;
let img_data;


$: if (open == true) {
    ctx = canvas.getContext("2d");
    colors = ctx.createImageData(canvas.width, canvas.height);
    img_data = colors.data;
    update();
}


function setColor(event) {
    if (event.type == "mousemove" && !dragging) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    let [h, s] = xy2hs(x, y);
    hue = h;
    saturation = Math.min(s, 1.0);
    dispatch("change", {hue: hue, saturation: saturation, value: value});
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

function toggle() {
    open = !open;
}

</script>

<div class="background" style="--display: {open ? 'block' : 'none'};"></div>
<div class="modal" style="--display: {open ? 'block' : 'none'};">
    <div class="wrapper">
        <canvas
            width="300" height="300"
            class="popup"
            on:mousemove={setColor}
            on:click={setColor}
            on:mousedown={(event) => {dragging = true; setColor(event)}}
            on:mouseup={() => {dragging = false;}}
            on:mouseleave={() => {dragging = false;}}
            bind:this={canvas}
        ></canvas>
        <button class="btn btn-primary" on:click={toggle}>Close</button>
    </div>
</div>


<style>
.wrapper {
    display: flex;
    flex-direction: column;
}

.background {
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: var(--display);
    background: rgba(0, 0, 0, 0.3);
}
button {
    margin: 0.5rem;
}
canvas {
    display: block;
    margin: 0.5rem;
}

.modal {
    position: fixed;
    z-index: 2;
    width: min-content;
    height: min-content;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #fff;
    filter: drop-shadow(0 0 20px #333);
    display: var(--display);
}
</style>
