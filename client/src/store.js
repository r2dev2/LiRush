import { writable } from 'svelte/store';

export const squareWidth = writable(updateSquareWidth());

function computeSquareWidth() {
  const fontSize = getComputedStyle(document.body)
    .getPropertyValue('font-size');
  return Math.min(window.innerHeight, window.innerWidth) / parseFloat(fontSize) / 8.65;
}

function updateSquareWidth() {
  const width = computeSquareWidth();
  document.querySelector(':root').style
    .setProperty('--square-width', `${computeSquareWidth()}rem`);
  return width;
}

addEventListener('resize', () => {
  squareWidth.update(updateSquareWidth);
});
