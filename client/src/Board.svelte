<script>
  import { CBoard } from './board.js';
  import Piece from './Piece.svelte';
  export let fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  export let moves = [];
  const rows = [...Array(8).keys()];
  const columns = [...rows]; 
  let board = new CBoard(fen);
  if (moves[0])
    board = board.move_uci(moves[0]);
  let flipped = !board.turn;

  function flipBoard() {
    flipped = !flipped;
  }

  addEventListener('move', e => {
    if (board.validate(e.detail)) {
      board = board.move(e.detail);
    }
  });
</script>

<div class="grid board">
  {#each board.pieces as piece}
    <Piece {...piece} {flipped} />
  {/each}
</div>

<button on:click={flipBoard}>
  Flip board
</button>


<style>
:root {
  --square-width: 3.5rem;
}

.board {
  background-image: url("https://lichess1.org/assets/_4hHVpp/images/board/svg/brown.svg");
  width: calc(8*var(--square-width));
  height: calc(8*var(--square-width));
}

.grid {
  display: grid;
  grid-template-columns: repeat(8, var(--square-width));
  grid-template-rows: repeat(8, var(--square-width));
}

</style>
