<template>
  <div class="flex items-center space-x-4">
    <!-- Notifications -->
    <NotificationBell />

    <!-- Menu utilisateur -->
    <UserDropdown :user="user" />
  </div>
</template>

<script setup>
defineProps({
  user: Object
})
</script>