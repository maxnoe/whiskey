<script>

async function sendCommand(cmd) {
    const response = await fetch("/api/pixels", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(cmd)
    })
    return response
}


function toggle(event) {
    let cmd = "off"
    if (event.target.checked) {
        cmd = "on"
    }
    let data = {"cmd": cmd};
    sendCommand(data).then(response => {console.log(response.json());});
}

let color = "#400000";
let pixel = 0;

function hex2rgb(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return [r, g, b];
}

function setColor(event) {
    const cmd = {"cmd": "set", "pix": pixel, "color": hex2rgb(color)}
    sendCommand(cmd).then(response => {console.log(response.json());});
}

</script>

<main>
	<h1>Pixels</h1>

    <div class="form-check form-switch mb-3">
      <input class="form-check-input" on:change="{toggle}" type="checkbox" id="power">
      <label class="form-check-label" for="power">Pixels on/off</label>
    </div>

    <form on:submit|preventDefault="{setColor}" class="form form-inline">
      <div class="row">
        <label class="col-auto col-form-label" for="pixel">Pixel</label>
        <div class="col-auto">
          <input bind:value="{pixel}" type="number" min=0 max=13 id="pixel">
        </div>

        <label class="col-auto col-form-label" for="color">Color</label>
        <div class="col col-2">
          <input class="form-control" bind:value="{color}" type="color" id="color">
        </div>

        <div class="col-auto">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </div>

    </form>

</main>

<style>

</style>
