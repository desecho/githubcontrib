<template>
    <section class="page-shell">
        <h1 class="page-title">Logging out</h1>
        <v-progress-linear color="primary" indeterminate />
    </section>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const router = useRouter();

onMounted(async () => {
    auth.logout();
    await router.replace("/");
});
</script>
