<template>
  <div>
    <!-- Section des statistiques clés -->
    <KeyStatsSection />

    <!-- Section héro -->
    <HeroSection />

    <!-- Section detection -->
    <DiseaseDetectionSection />

    <!-- Community Ecosystem -->
    <CommunityEcosystem />

    <!-- Blog Section -->
<!--    <BlogSection />-->

    <!-- Forum Section -->
<!--    <ForumSection />-->

    <!-- Faq Section -->
    <FaqSection />
  </div>
</template>

<script setup>
// Configuration de la page
definePageMeta({
  title: 'Accueil',
  description: 'Protection des cultures avec l\'intelligence artificielle'
})

// Configuration SEO
useSeoMeta({
  title: 'AgriTech AI - Protection des cultures',
  ogTitle: 'AgriTech AI - Protection des cultures',
  description: 'Protégez vos cultures avec l\'intelligence artificielle. Solution pour les agriculteurs camerounais.',
  ogDescription: 'Protégez vos cultures avec l\'intelligence artificielle. Solution pour les agriculteurs camerounais.',
  ogImage: '/logo.png',
  twitterCard: 'summary_large_image'
})
</script>