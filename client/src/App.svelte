<script>
        import { squareWidth } from './store.js';
        import Board from './Board.svelte';
        import Timer from './Timer.svelte';
        let server = squareWidth === squareWidth ? "" : "";
        let minPuzzle = 700;
        let maxPuzzle = 800;
        let count = 0;
        let wrong = 0;
        let timesUp = false;
        let hasStarted = false;

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

        function start() {
          minPuzzle = 700;
          maxPuzzle = 800;
          count = 0;
          wrong = 0;
          hasStarted = true;
          timesUp = false;
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

        function onTimeup() {
          console.log("received times up");
          timesUp = true;
        }

        removeEventListener('puzzle', onPuzzle);
        addEventListener('puzzle', onPuzzle);
        removeEventListener('timeup', onTimeup);
        addEventListener('timeup', onTimeup);
</script>

<main
  on:click={() => window.dispatchEvent(new Event('mainclick'))} >
  {#if hasStarted}
    {#if wrong < 3 && !timesUp}
      <div class="flex-container">
        <div class="board-container">
          {#await getPuzzle(minPuzzle, maxPuzzle) then { fen, moves }}
            <Board {fen} {moves} />
          {/await}
        </div>
        <div class="info">
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
          <Timer />
        </div>
      </div>
    {:else}
      <h1>{count}</h1>
      <button on:click={start}>Start new rush</button>
    {/if}
  {:else}
    <h1>LiRush</h1>
    <button on:click={start}>Start rush</button>
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
          font-size: 4em;
          font-weight: 100;
        }

        button {
          background-color: #252525;
          border-color: #151515;
          color: #E5E5E5;
          font-size: 1.2em;
          font-weight: 50;
          transition: .2s ease-in-out;
        }

        button:hover {
          cursor: pointer;
          transform: scale(1.05);
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
          color: #D5D5D5;
        }

        .board-container {
          background-image: url("/public/extimg/board.svg");
          background-size: contain;
          padding-top: 0px;
          padding-left: 0px;
          padding-right: 0px;
          padding-bottom: 0px;
          width: calc(8*var(--square-width));
          height: calc(8*var(--square-width));
        }

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
        }

        @media (max-width: 800px) {

                .flex-container {
                        flex-direction: column;
                }
	}
</style>
