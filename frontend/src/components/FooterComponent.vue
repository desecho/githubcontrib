<template>
    <v-footer class="footer" color="surface">
        <div class="footer-content">
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
    border-top: 1px solid #d0d7de;
    color: #57606a;
}

.footer-content {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 8px 0;
    font-size: 0.92rem;
}

.footer-separator {
    margin: 0 10px;
    color: #8c959f;
}

@media (max-width: 520px) {
    .footer-content {
        padding: 8px 0;
    }
}
</style>
