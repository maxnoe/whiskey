<script>

import { onMount } from 'svelte';
import { hsv2rgb, rgb2hex, hex2rgb } from './colors.js';
import ColorPicker from './ColorPicker.svelte';


let color = "#400000";
let color_all = "#400000";
let pixel = 0;
let on = false;
let hue = 0.0;
let value = 0.5;


async function sendCommand(cmd) {
    console.log(cmd);
    const response = await fetch("/api/pixels", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(cmd)
    })
    return await response.json()
}


function toggle(event) {
    let cmd = {"cmd": event.target.checked ? "on" : "off"};
    sendCommand(cmd).then(data => console.log(data));
}

function setColor(event) {
    const cmd = {"cmd": "set_pix", "pix": pixel, "color": hex2rgb(color)};
    sendCommand(cmd).then(data => console.log(data));
}

function setAll(event) {
    const cmd = {"cmd": "set_all", "color": hex2rgb(color_all)};
    sendCommand(cmd).then(data => console.log(data));
}

function rainbow(event) {
    const cmd = {"cmd": "rainbow"}
    sendCommand(cmd).then(data => console.log(data));
}

function clock(event) {
    const cmd = {"cmd": "clock"}
    sendCommand(cmd).then(data => console.log(data));
}

function sine(event) {
    const cmd = {"cmd": "sine"}
    sendCommand(cmd).then(data => console.log(data));
}

onMount(async () => {
    const data = await sendCommand({"cmd": "get"});
    on =  data["on"];
})

</script>

<main>
	<h1>Pixels</h1>


    <div class="form-check form-switch mb-3">
      <input class="form-check-input" bind:checked={on} on:change={toggle} type="checkbox" id="power">
      <label class="form-check-label" for="power">Pixels on/off</label>
    </div>

    <button type="button" on:click={rainbow} class="btn btn-primary">Rainbow</button>

    <button type="button" on:click={clock} class="btn btn-primary">Clock</button>

    <button type="button" on:click={sine} class="btn btn-primary">Sine-Wave</button>

    <ColorPicker />

</main>

<style>

main {
  max-width: 80rem;
}

</style>
