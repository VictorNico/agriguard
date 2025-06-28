<template>
    <div class="card flex justify-center mr-2">
        <Select v-model="selectedCountry" :options="countries" optionLabel="name" placeholder="Select a Country"
            class="w-full md:w-56">
            <template #value="slotProps">
                <div v-if="slotProps.value" class="flex items-center">
                    <i :class="`fi fi-${slotProps.value.icon.toLowerCase()}`"></i>
                    <div>{{ t(slotProps.value.name) }}</div>
                </div>
                <span v-else>
                    {{ slotProps.placeholder }}
                </span>
            </template>
            <template #option="slotProps">
                <div class="flex items-center">
                    <i :class="`fi fi-${slotProps.option.icon.toLowerCase()}`"></i>
                    <div>{{ t(slotProps.option.name) }}</div>
                </div>
            </template>
            <template #dropdownicon>
                <i class="pi pi-language" />
            </template>
        </Select>
    </div>
</template>
<script setup>
import { useLocaleStore } from '~/stores/locale';
const localeStore = useLocaleStore();

const { locale, t } = useI18n()
const selectedCountry = ref();
console.log(locale.value, localeStore.language)
selectedCountry.value= localeStore.language === 'en'?{ name: 'english', icon: 'gb', code: 'en' }:{ name: 'french', icon: 'fr', code: 'fr' }

const countries = ref([
    { name: 'french', icon: 'fr', code: 'fr' },
    { name: 'english', icon: 'gb', code: 'en' },
    // { name: 'german', icon: 'de', code: 'de' }
]);


// Initialiser la langue d'i18n avec celle du store
locale.value = localeStore.language;

// Watcher pour détecter le changement de pays sélectionné
watch(selectedCountry, (newValue) => {
    if (newValue && newValue.code) {
      localeStore.setLanguage(newValue.code);
    }
});
</script>

<style>
.fi {
    margin-right: 5px;
}

.p-select {
    width: 150px;
    height: 30px;
}

.p-placeholder {
    padding: 6px 10px;
    font-size: 11px;
}

.p-select-label {
    padding: 6px 10px;
    font-size: 11px;
}

.p-select-option {
    font-size: 11px;
}
</style>
