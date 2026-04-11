<template>
    <v-app>
        <MenuComponent />
        <v-main>
            <router-view />
        </v-main>
        <FooterComponent />
    </v-app>
</template>

<script setup lang="ts">
import FooterComponent from "./components/FooterComponent.vue";
import MenuComponent from "./components/MenuComponent.vue";
</script>
