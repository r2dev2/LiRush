<script>
  import { CPiece } from './piece.js';
  export let rank = 0;
  export let file = 0;
  export let piece = null;
  export let flipped = false;

  let moving = false;

  function flip(c) {
    return 3.5 * 8 - c;
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
  $: className = `piece ${piece.getClass()}`;
  $: backgroundStyle = `background-image: url(${src}); background-size: cover`;
  let movingStyle = '';
  const boardX = () => parent().getBoundingClientRect().left;
  const boardY = () => parent().getBoundingClientRect().top;
  $: dragx = 0 * flipped;
  $: dragy = 0 * flipped;
  $: ogRank = (flipped ? rank : 7 - rank) * 3.5;
  $: ogFile = (flipped ? 7 - file : file) * 3.5;
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

  function getFile() {
    const relativeFile = between(Math.ceil(pxToREM(pos3 - boardX()) / 3.5) - 1, 0, 7);
    return flipped ? 7 - relativeFile : relativeFile;
  }

  function getRank() {
    const relativeRank = between(Math.ceil(pxToREM(pos4 - boardY()) / 3.5) - 1, 0, 7);
    return flipped ? relativeRank : 7 - relativeRank;
  }

  function getMove() {
    return {
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
</script>

<div
 on:mousedown={dragMouseDown}
 {id}
 {style}
 class={className}/>

<style>
.piece {
  width: var(--square-width);
  height: var(--square-width);
  z-index: 10;
  position: absolute;
}

.piece:hover {
  z-index: 15;
}
</style>
