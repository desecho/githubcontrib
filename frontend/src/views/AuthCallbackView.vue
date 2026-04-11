<template>
    <section class="page-shell">
        <h1 class="page-title">Signing in</h1>
        <v-progress-linear color="primary" indeterminate />
    </section>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toast-notification";

import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const router = useRouter();
const toast = useToast();

function getParam(params: URLSearchParams, key: string): string | null {
    return params.get(key);
}

onMounted(async () => {
    const params = new URLSearchParams(window.location.hash.replace(/^#/, ""));
    const access = getParam(params, "access");
    const refresh = getParam(params, "refresh");
    const username = getParam(params, "username");

    if (access === null || refresh === null || username === null) {
        toast.error("Login failed");
        await router.replace("/login");
        return;
    }

    auth.setTokens({ access, refresh, username });
    await router.replace("/");
});
</script>
