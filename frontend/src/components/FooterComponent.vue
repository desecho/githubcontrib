<template>
    <v-footer class="footer" color="surface">
        <div>
            <span>© 2017-{{ currentYear }}</span>
            <span class="footer-separator">|</span>
            <router-link to="/about">About GitHubContrib</router-link>
            <span class="footer-separator">|</span>
            <a :href="`mailto:${adminEmail}`">{{ adminEmail }}</a>
        </div>
    </v-footer>
</template>

<script setup lang="ts">
const adminEmail =
    (import.meta.env.VITE_ADMIN_EMAIL as string | undefined) ??
    "admin@example.com";
const currentYear = new Date().getFullYear();
</script>

<style scoped lang="scss">
.footer {
    min-height: 56px;
    justify-content: center;
    border-top: 1px solid #d8e0e8;
    color: #4a5568;
}

.footer-separator {
    margin: 0 10px;
    color: #8a97a3;
}
</style>
