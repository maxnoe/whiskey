<script>
import { cssVariables } from './styles.js';
import { hsv2rgb, rgb2hex } from './colors.js';
import HueSaturationPicker from './HueSaturationPicker.svelte';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

export let color = rgb2hex(hsv2rgb(hue, saturation, value));

let value255 = 64;
$: value = value255 / 255;
let hue = 0.0;
let saturation = 1.0;
$: color1 = rgb2hex(hsv2rgb(hue, saturation, 1.0));

let isPickerOpen = false;

function update() {
  color = rgb2hex(hsv2rgb(hue, saturation, value));
  dispatch("change", {"color": color});
}

</script>

<div class="wrapper" use:cssVariables={{ color, color1, value}}>
  <button class="field" on:click={() => {isPickerOpen=!isPickerOpen}}>
  </button>

  <HueSaturationPicker on:change={update} bind:open={isPickerOpen} bind:hue bind:saturation />

  <input class="form-range" on:change={update} id="value" type="range" bind:value={value255} min="0" max="255" />
  <label class="form-label" for="value">Lightness</label>
</div>

<style>

.field {
  width: 3rem;
  height: 3rem;
  border: 3px solid #505050;
  border-radius: 1rem;
  margin: 0.5rem;
  background-color: var(--color1);
}

.wrapper {
  display: flex;
  align-items: center;
}


input[type="range"] {
  margin: 0.5rem;
  width: 100px;
}

</style>
