<script>
  import { onDestroy } from 'svelte';
  import { CPiece } from './piece.js';

  export let file = 0;
  export let rank = 0;
  export let color = true;
  export let move = null;

  let squareWidth = 5.5;

  $: rrank = rank;

  $: flipped = rank === 0
  $: hide = {
    file: move.from.file,
    rank: move.from.rank,
    hide: true
  };

  $: unHide = {
    file: move.from.file,
    rank: move.from.rank,
    hide: false
  };
  const pt = () => color ? 'QNRB' : 'qnrb';

  let renderTargets = [];

  function translate({ file, rank }) {
    const r = (flipped ? rank : (7 - rank)) * squareWidth;
    const f = (flipped ? (7 - file) : file) * squareWidth;
    return `transform: translate(${f}rem, ${r}rem);`;
  }

  function notifyPromo(piece) {
    const detail = {...move};
    detail.promoPiece = piece.toLowerCase();
    dispatchEvent(new CustomEvent('move', { detail }));
    dispatchEvent(new CustomEvent('hide', { detail: unHide }));
  }

  function newRenderTargets(updateR) {
    let r = rank;
    let z = 200;
    let renderTargets = [];
    for (const c of pt()) {
      renderTargets.push({
        file, rank: r, src: new CPiece(c).getImg(), z, alt: c,
        click: () => notifyPromo(c)
      });
      r = updateR(r);
      z += 20;
    }
    return renderTargets;
  }

  if (flipped) {
    renderTargets = newRenderTargets(r => r + 1);
  } else {
    renderTargets = newRenderTargets(r => r + 1);
  }

  $: containerTrans = translate(renderTargets[0], file);
  $: x = dispatchEvent(new CustomEvent('hide', { detail: hide }));
  onDestroy(() => {
    dispatchEvent(new CustomEvent('hide', { detail: unHide }));
  });
</script>

<div class="container" style={containerTrans}>
  {#each renderTargets as { alt, src, click }}
    <img {alt} {src} class="promo-target" on:click={click} />
  {/each}
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    z-index: 200;
  }

  .promo-target {
    width: var(--square-width);
    height: var(--square-height);
    z-index: 200;
    background-color: silver;
    transition: .1s ease-in-out;
  }

  .promo-target:hover {
    background-color: purple;
    transition: .1s ease-in-out;
    cursor: pointer;
  }
</style>
