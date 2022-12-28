<script>
    import { onMount } from "svelte";

    let bottles = {
        whiskeys: [],
        rums: [],
        other: [],
    }

    onMount(async () => {
        let resp = await fetch("/api/greet").then((res) => res.json());
        bottles.whiskeys = []
        bottles.rums = []
        bottles.other = []

        resp["bottles"].forEach(bottle => {
            console.log(bottle)
            if (bottle.kind == "whiskey") {
                bottles.whiskeys.push(bottle)
            } else if (bottle.kind == "rum") {
                bottles.rums.push(bottle)
            } else {
                bottles.other.push(bottle)
            }
        });

    })
</script>

<main>
	<h1>Bottles</h1>

    {#if bottles.whiskeys.length > 0}
    <h2>Whiskeys</h2>
    <ul>
    {#each bottles.whiskeys as bottle}
        <li> {bottle.name} </li>
    {/each}
    </ul>
    {/if}

    {#if bottles.rums.length > 0}
    <h2>Rums</h2>
    <ul>
    {#each bottles.rums as bottle}
        <li> {bottle.name} </li>
    {/each}
    </ul>
    {/if}

    {#if bottles.other.length > 0}
    <h2>Other</h2>
    <ul>
    {#each bottles.other as bottle}
        <li> {bottle.name} </li>
    {/each}
    </ul>
    {/if}

</main>

<style>
</style>
