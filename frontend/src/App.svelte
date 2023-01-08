<script>

import { onMount } from 'svelte';
import { hsv2rgb, rgb2hex, hex2rgb } from './colors.js';


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

    <div id="test" style="display: block; height: 20px; width: 20px; background-color: black; border: solid 1px black;">
    </div>


    <form on:submit|preventDefault={setAll} class="form form-inline">
      <div class="row">
        <label class="col-auto col-form-label" for="color">Hue</label>
        <div class="col col-2">
          <input class="form-control" style="background-color: {rgb2hex(hsv2rgb(hue, 1.0, 1.0))};" bind:value={hue} type="range" on:change={console.log(hue)} id="hue" min="0.0" max="1.0" step="{1/255}">
        </div>

        <div class="col-auto">
          <button type="submit" class="btn btn-primary">Set All Pixels</button>
        </div>
      </div>
    </form>

    <form on:submit|preventDefault={setAll} class="form form-inline">
      <div class="row">
        <label class="col-auto col-form-label" for="color">Color</label>
        <div class="col col-2">
          <input class="form-control" bind:value={color_all} type="color" id="color">
        </div>

        <div class="col-auto">
          <button type="submit" class="btn btn-primary">Set All Pixels</button>
        </div>
      </div>
    </form>

    <form on:submit|preventDefault={setColor} class="form form-inline">
      <div class="row">
        <label class="col-auto col-form-label" for="pixel">Pixel</label>
        <div class="col-auto">
          <input bind:value={pixel} type="number" min=0 max=13 id="pixel">
        </div>

        <label class="col-auto col-form-label" for="color">Color</label>
        <div class="col col-2">
          <input class="form-control" bind:value={color} type="color" id="color">
        </div>

        <div class="col-auto">
          <button type="submit" class="btn btn-primary">Set Pixel Color</button>
        </div>
      </div>
    </form>

</main>

<style>

main {
  max-width: 80rem;
}

</style>
