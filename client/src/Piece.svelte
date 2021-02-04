<script>
  import { onDestroy } from 'svelte';
  import { CPiece } from './piece.js';
  export let rank = 0;
  export let file = 0;
  // export let piece = null;
  export let pieceL = '';
  export let flipped = false;

  $: piece = new CPiece(pieceL);

  let moving = false;
  let squareWidth = 5.5;
  let hidden = false;

  function flip(c) {
    return squareWidth * 8 - c;
  }

  function initDrag(mouseX, mouseY) {
    const newX = Math.ceil(mouseX - REMToPx(squareWidth));
    const newY = Math.ceil(mouseY - REMToPx(squareWidth));
    return {
      dragx: REMToPx(ogFile) - newX - boardX() + 3,
      dragy: REMToPx(ogRank) - newY - boardY() + 2,
    };
  }

  function translateStyle(x, y) {
    return `transform: translate(${x}, ${y});`;
  }

  function randInt(min, max) {
    min = Math.ceil(min)
    max = Math.floor(max)
    return Math.floor(Math.random() * (max - min) + min);
  }

  function randID() {
    const chars = Array.from("abcdefghijklmnopqrstuvwxyz");
    return chars.map(c => chars[randInt(0, chars.length)]).join('');
  }

  function self() {
    return document.querySelector(`#${id}`);
  }

  function parent() {
    return self().parentElement;
  }

  const id = randID();
  $: src = piece.getImg();
  $: className = `piece ${piece.getClass()}${moving ? ' moving' : ''}`;
  $: backgroundStyle = `background-image: url(${src}); background-size: cover;`;
  const boardX = () => parent().getBoundingClientRect().left + 2 * scrollX;
  const boardY = () => parent().getBoundingClientRect().top + 2 * scrollY;
  $: dragx = 0 * flipped;
  $: dragy = 0 * flipped;
  $: ogRank = (flipped ? rank : 7 - rank) * squareWidth;
  $: ogFile = (flipped ? 7 - file : file) * squareWidth;
  $: dispRank = `calc(${ogRank}rem - ${dragy}px)`;
  $: dispFile = `calc(${ogFile}rem - ${dragx}px)`;
  $: style = translateStyle(dispFile, dispRank, moving) + backgroundStyle;

  // from w3schools
  let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
    moving = true;
    const newPositions = initDrag(e.clientX, e.clientY);
    dragx = newPositions.dragx || dragx;
    dragy = newPositions.dragy || dragy;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    dragy += pos2;
    dragx += pos1;
  }

  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
    document.onmouseup = null;
    document.onmousemove = null;
    moving = false;
    const move = getMove();
    dispatchEvent(new CustomEvent('move', { detail: move }));
    dragx = 0, dragy = 0;
  }

  function fontSize() {
    return getComputedStyle(parent()).getPropertyValue('font-size');
  }

  function pxToREM(px) {
    return px / parseFloat(fontSize());
  }

  function REMToPx(rem) {
    return parseFloat(fontSize()) * rem;
  }

  function getFile() {
    const relativeFile = Math.ceil(pxToREM(pos3 - boardX()) / squareWidth) - 1;
    return flipped ? 7 - relativeFile : relativeFile;
  }

  function getRank() {
    const relativeRank = Math.ceil(pxToREM(pos4 - boardY()) / squareWidth) - 1;
    return flipped ? relativeRank : 7 - relativeRank;
  }

  function getMove() {
    return {
      piece: pieceL,
      from: {
        file,
        rank,
      },
      to: {
        file: getFile(),
        rank: getRank(),
      },
    }
  }

  function between(num, lower, upper) {
    return Math.min(Math.max(num, lower), upper);
  }

  function onHide(e) {
    if (e.detail.file == file && e.detail.rank == rank) {
      hidden = e.detail.hide;
    }
  }

  addEventListener('hide', onHide);
  onDestroy(() => removeEventListener('hide', onHide));
</script>

{#if !hidden}
  <div
   on:mousedown={dragMouseDown}
   {id}
   {style}
   class={className}/>
{/if}

<style>
.piece {
  background-size: contain;
  width: var(--square-width);
  height: var(--square-width);
  z-index: 10;
  position: absolute;
  /*transition: .2s;*/
}

.piece:hover {
  z-index: 15;
  cursor: grab;
}

.piece.moving {
  transition: 0s;
  cursor: grabbing;
}
</style>
