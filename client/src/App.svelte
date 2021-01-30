<script>
        import Board from './Board.svelte';
	export let name;
        let server = "";
        async function getPuzzle() {
          let r = await fetch(`${server}/puzzles?start=1000&end=1200&pmax=1`, {mode: "cors"});
          let j = await r.json().then(j => j[0]);
          j.moves = j.moves.split(' ');
          return j;
        }
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
        {#await getPuzzle() then { fen, moves }}
          <Board {fen} {moves} />
        {/await}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
