<script>
  import { onDestroy } from 'svelte';
  import { CBoard } from './board.js';
  import Piece from './Piece.svelte';
  export let fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  export let moves = [];
  fen = 'rn1qkbnr/pP1bpppp/8/8/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 4';
  moves = ['b8c6', 'b7a8q', 'd8c8'];
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

  function isPromotion(move) {
    const { rank } = move.to.rank;
    return move.piece == 'p' && rank == 1 || move.piece == 'P' && rank == 8;
  }

  function nextPuzzle(wasSuccess) {
    const detail = {
      success: wasSuccess
    };
    hasEnded = true;
    wasCorrect = wasSuccess;
    console.log("next puzzle");
    setTimeout(() => {
      console.log("dispatching puzzle");
      dispatchEvent(new CustomEvent('puzzle', { detail }))
    }, 100);
  }

  function onMove(e) {
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
  }

  addEventListener('move', onMove);
  onDestroy(() => removeEventListener('move', onMove));

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
