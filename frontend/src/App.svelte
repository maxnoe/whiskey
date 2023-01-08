<script>
import { onMount } from 'svelte';

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

let color = "#400000";
let pixel = 0;
let on = false;

function to_hex(integer) {
    var str = Number(integer).toString(16);
    return str.length == 1 ? "0" + str : str;
};

function rgb2hex(r, g, b) {
    return "#" + to_hex(r) + to_hex(g) + to_hex(b);
}

function hex2rgb(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    console.log(color)
    console.log([r, g, b]);
    return [r, g, b];
}

function setColor(event) {
    const cmd = {"cmd": "set_pix", "pix": pixel, "color": hex2rgb(color)};
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
