<script>
  import { onDestroy } from 'svelte';
  import { CBoard } from './board.js';
  import Piece from './Piece.svelte';
  import Promotion from './Promotion.svelte';
  export let fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  export let moves = [];
  const rows = [...Array(8).keys()];
  const columns = [...rows]; 
  let board = new CBoard(fen);
  let moveNumber = 0;
  setTimeout(() => {
    if (moves[0]) {
      board = board.move_uci(moves[0]);
      moveNumber++;
    }
  }, 100);
  let flipped = board.turn;
  let hasEnded = false;
  let wasCorrect = false;
  let isPromoting = false;
  let promoTarget = { rank: 0, file: 0, color: true };

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
    const { rank } = move.to;
    return move.piece == 'p' && rank == 0 || move.piece == 'P' && rank == 7;
  }

  function nextPuzzle(wasSuccess) {
    const detail = {
      success: wasSuccess,
    };
    hasEnded = true;
    wasCorrect = wasSuccess;
    setTimeout(() => dispatchEvent(new CustomEvent('puzzle', { detail })), 100);
  }

  function onMove(e) {
    if (board.validate(e.detail)) {
      if (isPromotion(e.detail) && !e.detail.promoPiece) {
        isPromoting = true;
        promoTarget = {
          ...e.detail.to,
          move: e.detail,
          color: e.detail.piece == 'P'
        };
      } else {
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
        isPromoting = false;
      }
    }
  }

  function onMainclick() {
    isPromoting = false;
  }

  addEventListener('move', onMove);
  addEventListener('mainclick', onMainclick);
  onDestroy(() => removeEventListener('move', onMove));
  onDestroy(() => removeEventListener('mainclick', onMainclick));

</script>


{#if !hasEnded}
  <div class="grid board">
    {#if isPromoting}
      <Promotion {...promoTarget}/>
    {/if}

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
