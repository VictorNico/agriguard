<template>
  <div class="py-12 bg-green-600 text-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
        <StatCard
            v-for="stat in stats"
            :key="stat.id"
            :value="stat.value"
            :description="t(stat.descriptionKey)"
            :source-link="stat.sourceLink"
            :source-title="stat.sourceTitle"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
const { t } = useI18n()

const stats = [
  {
    id: 1,
    value: '5%',
    descriptionKey: 'stats.agricultural_losses',
    sourceTitle: 'FAO',
    sourceLink:'https://www.fao.org/newsroom/detail/first-ever-global-estimation-of-the-impact-of-disasters-on-agriculture'
  },
  {
    id: 2,
    value: '600 000',
    descriptionKey: 'stats.cocoa_families',
    sourceTitle: 'CIRAD 2023',
    sourceLink:'https://www.cirad.fr/en/cirad-news/news/2024/2023-cirad-annual-report'
  },
  {
    id: 3,
    value: '100M+',
    descriptionKey: 'stats.corn_weevil_losses',
    sourceTitle: 'FAO',
    sourceLink:'https://www.fao.org/newsroom/detail/first-ever-global-estimation-of-the-impact-of-disasters-on-agriculture'
  }
]
</script>