<template>
    <section class="page-shell login-page">
        <h1 class="page-title">Log in</h1>

        <div class="content-panel login-panel">
            <p>
                Use your GitHub account to manage repositories and load commits.
            </p>
            <v-btn
                :href="loginUrl"
                class="github-login-button"
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
    padding: 24px;
}

.login-panel p {
    margin: 0 0 20px;
    color: #57606a;
    line-height: 1.55;
}

.github-login-button {
    box-shadow: none;
}
</style>
