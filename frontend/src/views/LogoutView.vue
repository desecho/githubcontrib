<template>
    <section class="page-shell status-page">
        <div class="content-panel status-panel">
            <h1 class="page-title">Logging out</h1>
            <v-progress-linear color="primary" indeterminate />
        </div>
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

<style scoped lang="scss">
.status-panel {
    max-width: 520px;
    padding: 24px;
}
</style>
