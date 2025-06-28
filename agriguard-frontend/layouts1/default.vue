<template>
      <main>
        <slot />
      </main>
</template>

<script>
export default {
  name: 'DefaultLayout',
  mounted() {
    console.log('mounted');
  }
}
</script>
  <style>
    
  </style>
  