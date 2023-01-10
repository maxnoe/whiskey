<script>
import { cssVariables } from './styles.js';
import { hsv2rgb, rgb2hex } from './colors.js';
import HueSaturationPicker from './HueSaturationPicker.svelte';


let value255 = 255;
$: value = value255 / 255;
let hue = 0.0;
let saturation = 1.0;
$: color = rgb2hex(hsv2rgb(hue, saturation, value));
$: color1 = rgb2hex(hsv2rgb(hue, saturation, 1.0));


</script>

<p class="mono">
  HSV: ({hue.toFixed(3)}, {saturation.toFixed(3)}, {value.toFixed(3)})<br>
  RGB: {color}
</p>

<div class="wrapper" use:cssVariables={{ color, color1, value}}>
  <div class="field"></div>

  <HueSaturationPicker bind:hue bind:saturation bind:value />

  <input type="range" bind:value={value255} min="0" max="255" />
</div>

<style>

.mono {
  font-family: "Fira Mono", monospace;
}

.field {
  width: 3rem;
  height: 3rem;
  border: 3px solid darkgray;
  border-radius: 1rem;
  margin: 0.5rem;
  background-color: var(--color);
}

.wrapper {
  display: flex;
}


input[type="range"] {
  margin: 0.5rem;
  width: 100px;
}

</style>
