<script>
  import { CBoard } from './board.js';
  import Piece from './Piece.svelte';
  export let fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  export let moves = [];
  const rows = [...Array(8).keys()];
  const columns = [...rows]; 
  let board = new CBoard(fen);
  let moveNumber = 0;
  if (moves[0]) {
    board = board.move_uci(moves[0]);
    moveNumber++;
  }
  let flipped = !board.turn;
  let hasEnded = false;
  let wasCorrect = false;

  function flipBoard() {
    flipped = !flipped;
  }

  function hasNextMove() {
    return moveNumber + 1 < moves.length;
  }

  function nextMove() {
    board = board
      .move_uci(moves[moveNumber])
      .move_uci(moves[moveNumber + 1]);
    moveNumber += 2;
  }

  function nextPuzzle(wasSuccess) {
    const detail = {
      success: wasSuccess
    };
    hasEnded = true;
    wasCorrect = wasSuccess;
    setTimeout(() => dispatchEvent(new CustomEvent('puzzle', { detail })), 100);
  }

  addEventListener('move', e => {
    if (board.validate(e.detail)) {
      const newBoard = board.move(e.detail);
      if (moveNumber < moves.length
        && board.move_uci(moves[moveNumber]).fen === newBoard.fen) {
        if (hasNextMove())
          nextMove();
        else
        {
          nextPuzzle(true);
          board = newBoard;
        }
      } else {
        nextPuzzle(false);
        board = newBoard;
      }
    }
  });
</script>

{#if !hasEnded}
  <div class="grid board">
    {#each board.pieces as piece}
      <Piece {...piece} {flipped} />
    {/each}
  </div>
{:else if wasCorrect}
  <div class="status correct" />
{:else}
  <div class="status incorrect" />
{/if}

<!--
<button on:click={flipBoard}>
  Flip board
</button>
-->


<style>
:root {
  --square-width: 5.5rem;
}

.board {
  background-image: url("/public/extimg/board.svg");
  background-size: contain;
  width: calc(8*var(--square-width));
  height: calc(8*var(--square-width));
}

.grid {
  display: grid;
  grid-template-columns: repeat(8, var(--square-width));
  grid-template-rows: repeat(8, var(--square-width));
}

.status {
  width: calc(8*var(--square-width));
  height: calc(8*var(--square-width));
  transition: .1s ease-in-out;
  opacity: .75;
}

.correct {
  background-color: #36B039;
}

.incorrect {
  background-color: #FF0000;
}

</style>
