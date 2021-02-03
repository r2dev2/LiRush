<script>
        import Board from './Board.svelte';
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

        function getPuzzzle(...args) {
          return new Promise((res, rej) => {
            setTimeout(() => {
              getPuzzzle(...args).then(res).catch(rej);
            }, 2000);
          });
        }

        function onPuzzle(e) {
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
        }

        removeEventListener('puzzle', onPuzzle);
        addEventListener('puzzle', onPuzzle);
</script>

<main>
        {#if wrong < 30}
          <div class="flex-container">
            <div class="board-container">
              {#await getPuzzle(minPuzzle, maxPuzzle) then { fen, moves }}
                <Board {fen} {moves} />
              {/await}
            </div>
            <div class="correct-description">
              <span class="correct">
                {count}
              </span>
              correct and
              <span class="incorrect">
                {wrong}
              </span>
              incorrect
            </div>
          </div>
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

        .flex-container {
          display: flex;
          flex-direction: row;
        }

        .flex-container > * {
          padding: 50px;
          padding-top: 0px;
        }

        .correct {
          color: green;
        }

        .incorrect {
          color: red;
        }

        .correct-description {
          font-size: 3em;
        }

        .board-container {
          background-image: url("/public/extimg/board.svg");
          background-size: contain;
          padding-top: 0px;
          padding-left: 0px;
          width: calc(41rem - 2px);
          height: calc(41rem - 2px);
        }

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
