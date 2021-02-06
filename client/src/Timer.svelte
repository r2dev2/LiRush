<script>
  import { onMount, onDestroy } from 'svelte';

  export let minutes = 3;
  export let seconds = 0;

  let interval;

  onMount(() => {
    interval = setInterval(() => {
      if (minutes == 0 && seconds == 0) {
        dispatchEvent(new Event('timeup'));
        clearInterval(interval);
      } else if (seconds == 0) {
        minutes--;
        seconds = 59;
      } else {
        seconds--;
      }
    }, 1000);
  });

  onDestroy(() => clearInterval(interval));
</script>

<div class="timer">
  <p>{minutes}:{`${seconds}`.padStart(2, '0')}</p>
</div>

<style>
  .timer {
    font-size: 3em;
    color: #D5D5D5;
  }
</style>
