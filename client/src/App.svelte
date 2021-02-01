<script>
        import Board from './Board.svelte';
	export let name;
        let server = "";
        let minPuzzle = 700;
        let maxPuzzle = 800;
        let count = 0;
        let wrong = 0;
        async function getPuzzle(minPuzzle, maxPuzzle) {
          const r = await fetch(
            `${server}/puzzles?start=${minPuzzle}&end=${maxPuzzle}&pmax=1`
          );
          const j = await r.json().then(j => j[0]);
          j.moves = j.moves.split(' ');
          return j;
        }

        addEventListener('puzzle', e => {
          const { success } = e.detail;
          if (success) {
            minPuzzle += 50;
            maxPuzzle += 50;
            count++;
          } else {
            minPuzzle += 25;
            maxPuzzle += 25;
            wrong++;
          }
          console.log(`Solved ${count} puzzles, ${wrong} wrong`);
        });
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
        {#if wrong < 3}
          {#await getPuzzle(minPuzzle, maxPuzzle) then { fen, moves }}
            <Board {fen} {moves} />
          {/await}
          <span>{count} correct and {wrong} incorrect</span>
        {:else}
          <h1>You solved {count} correct.</h1>
        {/if}
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
