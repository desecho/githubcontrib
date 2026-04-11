<template>
    <section class="page-shell login-page">
        <h1 class="page-title">Log in</h1>

        <div class="content-panel login-panel">
            <p>
                Use your GitHub account to manage repositories and load commits.
            </p>
            <v-btn
                :href="loginUrl"
                color="primary"
                size="large"
                prepend-icon="mdi-github"
            >
                Log in with GitHub
            </v-btn>
        </div>
    </section>
</template>

<script setup lang="ts">
import { getUrl } from "../helpers";

const loginUrl = getUrl("auth/login/github/");
</script>

<style scoped lang="scss">
.login-panel {
    max-width: 480px;
    padding: 22px;
}
</style>
