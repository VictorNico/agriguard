<script setup lang="ts">
import { ShieldCheckIcon, UsersIcon, HomeIcon, UserGroupIcon, RocketLaunchIcon, Cog8ToothIcon, ChevronLeftIcon, ChevronDownIcon, AcademicCapIcon, SunIcon, BuildingLibraryIcon, TruckIcon, BeakerIcon, MapIcon, AdjustmentsHorizontalIcon, ChevronRightIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '~/stores/auth';
import { ref, computed, onMounted } from 'vue'

const authStore = useAuthStore();

const hasManagePermission = computed(() => {
    return authStore?.user?.permissions?.some(el => el.toLowerCase().includes(`find:user`) || el.toLowerCase().includes("manage:system"));
})
const isSidebarOpen = ref(true)
const isMobileSidebarOpen = ref(false)
const config = useRuntimeConfig()
const { t } = useI18n()
const route = useRoute();

// Gestion des liens principaux
const links = ref([
    { id: 'home', label: 'sidebar.menu.home', icon: HomeIcon, to: '/dashboard', tooltip: { text: 'Home', shortcuts: ['G', 'H'] }, hasSubMenu: false },
    {
        id: 'Education',
        label: 'sidebar.menu.education',
        icon: AcademicCapIcon,
        to: '',
        tooltip: { text: 'Education', shortcuts: ['G', 'E'] },
        hasSubMenu: true,
        isSubMenuOpen: false,  // État pour gérer l'ouverture/fermeture
        subLinks: [
            { label: 'sidebar.menu.school', to: '/analyse/ecoles' },
            { label: 'sidebar.menu.schoolinfirmiere', to: '/analyse/ecolesdeformationsciencesinfirmieres' },
            { label: 'sidebar.menu.institut', to: '/analyse/instituts' },
            { label: 'sidebar.menu.primaire', to: '/analyse/primaires' },
            { label: 'sidebar.menu.secondaire', to: '/analyse/secondaires' },
            { label: 'sidebar.menu.superieur', to: '/analyse/superieurs' },
        ]
    },
    {
        id: 'sante',
        label: 'sidebar.menu.sante',
        icon: BeakerIcon,
        to: '',
        tooltip: { text: 'Santé', shortcuts: ['G', 'S'] },
        hasSubMenu: true,
        isSubMenuOpen: false,
        subLinks: [
            { label: 'sidebar.menu.formationsSanitaires', to: '/analyse/formationsSanitaires' },
            { label: 'sidebar.menu.laboratoires', to: '/analyse/laboratoires' },
            { label: 'sidebar.menu.santes', to: '/analyse/santes' },
            { label: 'sidebar.menu.pharmacies', to: '/analyse/pharmacies' },
            { label: 'sidebar.menu.centresZooTechniquesEtVeterinaires', to: '/analyse/centresZooTechniquesEtVeterinaires' },
        ]
    },
    {
        id: 'tourism',
        label: 'sidebar.menu.tourism',
        icon: MapIcon,
        to: '',
        tooltip: { text: 'tourisme', shortcuts: ['G', 'T'] },
        hasSubMenu: true,
        isSubMenuOpen: false,
        subLinks: [
            { label: 'sidebar.menu.hotels', to: '/analyse/hotels' },
            { label: 'sidebar.menu.restaurants', to: '/analyse/restaurants' },
        ]
    },
    {
        id: 'roadnetwork',
        label: 'sidebar.menu.roadnetwork',
        icon: TruckIcon,
        to: '',
        tooltip: { text: 'reseau routier', shortcuts: ['G', 'R'] },
        hasSubMenu: true,
        isSubMenuOpen: false,
        subLinks: [
            { label: 'sidebar.menu.routesNationales', to: '/analyse/routesNationales' },
            { label: 'sidebar.menu.routesRegionales', to: '/analyse/routesRegionales' },
            { label: 'sidebar.menu.routesDepartementales', to: '/analyse/routesDepartementales' },
            { label: 'sidebar.menu.tronconsRoutesCentres', to: '/analyse/tronconsRoutesCentres' },
        ]
    },
    {
        id: 'PostOffice',
        label: 'sidebar.menu.postoffice',
        icon: BuildingLibraryIcon,
        to: '',
        tooltip: { text: 'post office', shortcuts: ['G', 'P'] },
        hasSubMenu: true,
        isSubMenuOpen: false,
        subLinks: [
            { label: 'sidebar.menu.posteDeTravailMinepias', to: '/analyse/posteDeTravailMinepias' },
        ]
    },
    {
        id: 'Agriculture',
        label: 'sidebar.menu.agriculture',
        icon: SunIcon,
        to: '',
        tooltip: { text: 'Agriculture', shortcuts: ['G', 'A'] },
        hasSubMenu: true,
        isSubMenuOpen: false,
        subLinks: [
            { label: 'sidebar.menu.postesAgricoles', to: '/analyse/postesAgricoles' },
            { label: 'sidebar.menu.siteagricoles', to: '/analyse/siteagricoles' },
        ]
    },
    {
        id: 'Autres',
        label: 'sidebar.menu.autre',
        icon: AdjustmentsHorizontalIcon,
        to: '',
        tooltip: { text: 'Autre', shortcuts: ['G', 'A','U'] },
        hasSubMenu: true,
        isSubMenuOpen: false,
        subLinks: [
            { label: 'sidebar.menu.consultations', to: '/analyse/consultations' },
            { label: 'sidebar.menu.slaughtering', to: '/analyse/abattages' },
            { label: 'sidebar.menu.deworming', to: '/analyse/deparasitages' },
            { label: 'sidebar.menu.production', to: '/analyse/productions' },
        ]
    },
    { id: 'GeoPortal', label: 'sidebar.menu.geoportal', icon: RocketLaunchIcon, to: `${config.public.geoportalUrl}`, target: '_blank', hasSubMenu: false }
]);
const footerLinks = [
    { label: 'sidebar.menu.setting', icon: Cog8ToothIcon, to: '/setting', show: () => { return authStore.isAuthenticated } },
    { label: 'sidebar.menu.usermanagement', icon: UsersIcon, to: '/usersmanagement', show: () => { return authStore.isAuthenticated } },
    { label: 'sidebar.menu.rgpd', icon: ShieldCheckIcon, to: '/privacy-policy', show: () => { return true } },

]
// Fonction pour basculer l'état du sous-menu
const toggleSubMenu = (link) => {
    link.isSubMenuOpen = !link.isSubMenuOpen;
};

// Computed pour vérifier si un sous-menu doit être ouvert en fonction de la route actuelle
const updatedLinks = computed(() => {
    return links.value.map(link => {
        // Si le lien contient un sous-menu, vérifier si l'un des sous-liens correspond à la route actuelle
        if (link.hasSubMenu) {
            link.isSubMenuOpen = link.subLinks.some(subLink => route.path.includes(subLink.to));
        }
        return link;
    });
});

const isExternal = (url: string) => {
  return /^https?:\/\//.test(url);
}
const handleLinkClick = (event: MouseEvent, link: any) => {
  if (link.hasSubMenu) {
    event.preventDefault();
    toggleSubMenu(link);
  }
};

</script>

<template>
    <div class="flex h-screen bg-gray-100">
        <!-- Sidebar -->
        <aside :class="isSidebarOpen ? (isMobileSidebarOpen ? 'w-64 gophone' : 'w-64') : 'w-20'"
            v-if="route.path !== '/'"
            class="bg-white border-r border-gray-200 flex flex-col transition-width duration-200 fixed md:static menn">

            <!-- Header -->
            <div class="h-[--header-height] h-soi flex-shrink-0 flex items-center border-b border-gray-200 px-4 gap-x-4
          min-w-0 !border-transparent">
                <div class="flex items-center justify-between flex-1 gap-x-1.5 min-w-0">
                    <div class="flex items-stretch gap-1.5 min-w-0 flex-1" style="align-items: center;">
                        <span class="relative inline-flex items-center justify-center flex-shrink-0 rounded-full
                h-5 w-5 text-[10px]">
                            <nuxt-link to="/">
<!--                                <img class="rounded-full h-5 w-5 text-[10px]" src="/logo.png">-->
                            </nuxt-link>
                        </span>
                        <span class="truncate text-gray-900 font-semibold"> <nuxt-link to="/"> CRCE </nuxt-link></span>
                        <button @click="isSidebarOpen = !isSidebarOpen" class="ml-auto p-2 ytt">
                            <ChevronLeftIcon class="w-5 h-5" :class="isSidebarOpen ? 'rotate-180' : ''" />
                        </button>
                        <button @click="isMobileSidebarOpen = false" class="ml-auto p-2 tyy">
                            <ChevronRightIcon class="w-5 h-5" :class="isMobileSidebarOpen ? 'rotate-180' : ''" />
                        </button>
                    </div>
                </div>
            </div>

            <!-- Links -->
            <nav class="flex-1 p-4 space-y-2 nav-aside"
                style="font-size: .9em;max-height: calc(100vh - 178px);overflow-y: auto;">
                <div class="menu-item" v-for="link in updatedLinks" :key="link.id">
                    <component
                        :is="isExternal(link.to) ? 'a' : 'NuxtLink'"
                        :href="isExternal(link.to) ? link.to : undefined"
                        :to="!isExternal(link.to) ? link.to : undefined"
                        :target="link.target"
                        :rel="isExternal(link.to) ? 'noopener noreferrer' : null"
                        @click="handleLinkClick($event, link)"
                        :class="link.isSubMenuOpen ? 'nuxt-link-active group relative flex items-center gap-1.5 px-2.5 py-1.5 w-full rounded-md font-medium text-sm focus:outline-none focus-visible:outline-none  focus-visible:before:ring-inset focus-visible:before:ring-2 focus-visible:before:ring-primary-500 before:absolute before:inset-px before:rounded-md disabled:cursor-not-allowed disabled:opacity-75 text-gray-500 hover:text-gray-900 cursor-pointer hover:bg-gray-100' : 'group relative flex items-center gap-1.5 px-2.5 py-1.5 w-full rounded-md font-medium text-sm focus:outline-none focus-visible:outline-none  focus-visible:before:ring-inset focus-visible:before:ring-2 focus-visible:before:ring-primary-500 before:absolute before:inset-px before:rounded-md disabled:cursor-not-allowed disabled:opacity-75 text-gray-500 hover:text-gray-900 cursor-pointer hover:bg-gray-100'"
                    >
                        <component :is="link.icon" class="w-5 h-5 mr-2" />
                        <span v-if="isSidebarOpen">{{ t(link.label) }}</span>
                        <ChevronDownIcon v-if="link.hasSubMenu" class="w-5 h-5 -rotate-90"
                            :class="link.isSubMenuOpen ? 'rotate-0 absolute right-0 top-1/2 transform -translate-y-1/2' : 'absolute right-0 top-1/2 transform -translate-y-1/2'" />
                    </component>
                    <!-- Sous-menu (Affiché au clic) -->
                    <div v-if="link.hasSubMenu && link.isSubMenuOpen" class="space-y-2 pl-4">
                        <NuxtLink v-for="subLink in link.subLinks" :key="subLink.label" :to="subLink.to" @click="isMobileSidebarOpen = false"
                            class="block px-2.5 py-1.5 rounded-md text-sm text-gray-700 hover:bg-gray-200">
                            {{ t(subLink.label) }}
                        </NuxtLink>
                    </div>
                </div>
            </nav>

            <!-- Footer Links -->
            <nav class="p-4 border-t border-gray-200">
                <NuxtLink v-for="link in footerLinks.filter(el => el.show() === true)" :key="link.label" :to="link.to"
                    class="flex items-center p-2 hover:bg-gray-100 rounded cursor-pointer">
                    <component :is="link.icon" class="w-5 h-5 mr-2" />
                    <span v-if="isSidebarOpen">{{ t(link.label) }}</span>
                </NuxtLink>
            </nav>
        </aside>

        <!-- Main Content Area -->
        <main class="flex-1 flex flex-col">
            <!-- Page Content -->
            <div class="flex-1 overflow-y-auto">
                <Menubar :model="[]">
                    <template #end>
                        <div class="flex items-center gap-2 justify-between">
                            <button type="button"
                                class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700 moid"
                                @click="isMobileSidebarOpen = true">
                                <span class="sr-only">Open main menu</span>
                                <i class="pi pi-align-left" style="font-size: 1.5rem"></i>
                            </button>
                            <InternationalisationButtons />
                            <auth />
                        </div>
                    </template>
                </Menubar>
                <slot />
            </div>
        </main>
    </div>
</template>

<style scoped>
.transition-width {
    transition-property: width;
}

.nav-aside::-webkit-scrollbar {
    width: 6px;
}

.h-soi {
    height: 64px;
}

.router-link-active {
    @apply bg-green-200/45 font-medium;
}

.router-link-active:hover {
    @apply bg-green-200 font-medium;
}

.p-button {
    padding: 0 15px;
}

/* Cible la scrollbar horizontale */
::-webkit-scrollbar:horizontal {
    height: 5px;
    /* Modifier la hauteur selon tes besoins */
}

/* Style pour les sous-menus */
.space-y-2 {
    margin-top: 8px;
}

.pl-4 {
    padding-left: 1rem;
}

.text-sm {
    font-size: 0.875rem;
}

.hover\:bg-gray-200:hover {
    background-color: #edf2f7;
}

.menn {
    z-index: 9;
}

.moid {
    display: none;
}

.tyy {
    display: none;
}

@media (max-width: 768px) {
    .menn {
        height: 100vh !important;
        transform: translateX(-100%);
        transition: .3s;
    }

    .menn.gophone {
        transform: translateX(0px);
        transition: .3s;
    }

    .moid {
        display: block;
        position: fixed;
        top: 16px;
        left: 15px;
    }

    .ytt {
        display: none;
    }

    .tyy {
        display: block;
    }
}
</style>
