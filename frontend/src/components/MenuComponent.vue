<template>
    <v-app-bar class="app-header" color="surface" elevation="0" height="64">
        <v-app-bar-title class="brand-title">
            <router-link
                aria-label="GitHubContrib home"
                class="brand-link"
                to="/"
            >
                <img :src="logoUrl" alt="" class="brand-logo" />
                <span class="brand-text">GitHubContrib</span>
            </router-link>
        </v-app-bar-title>

        <v-spacer />

        <div class="nav-actions">
            <v-btn class="nav-button" to="/" variant="text">Users</v-btn>
            <v-btn
                v-if="auth.user.isLoggedIn"
                class="nav-button"
                to="/my-contributions"
                variant="text"
            >
                My contributions
            </v-btn>
            <v-btn
                v-if="auth.user.isLoggedIn"
                class="nav-button"
                to="/repositories"
                variant="text"
            >
                Repositories
            </v-btn>
            <v-btn class="nav-button" to="/about" variant="text">About</v-btn>
            <v-btn
                v-if="auth.user.isLoggedIn"
                class="nav-button"
                to="/account"
                variant="text"
            >
                {{ auth.user.username }}
            </v-btn>
            <v-btn
                v-if="auth.user.isLoggedIn"
                class="nav-button"
                to="/logout"
                variant="text"
                >Log out</v-btn
            >
            <v-btn
                v-else
                class="login-button"
                color="primary"
                to="/login"
                variant="flat"
                >Log in</v-btn
            >
        </div>
    </v-app-bar>
</template>

<script setup lang="ts">
import logoUrl from "../assets/logo.png";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
</script>

<style scoped lang="scss">
.app-header {
    border-bottom: 1px solid #d0d7de;
}

.brand-title {
    min-width: 178px;
}

.brand-link {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: #24292f;
    font-weight: 700;
    text-decoration: none;
}

.brand-logo {
    width: 40px;
    height: 38px;
    flex: 0 0 auto;
    object-fit: contain;
}

.brand-text {
    line-height: 1;
}

.nav-actions {
    display: flex;
    max-width: calc(100vw - 220px);
    align-items: center;
    gap: 4px;
    overflow-x: auto;
    scrollbar-width: none;
}

.nav-actions::-webkit-scrollbar {
    display: none;
}

.nav-button,
.login-button {
    flex: 0 0 auto;
}

.nav-button {
    color: #57606a;
}

.nav-button:hover,
.nav-button.active {
    color: #116329;
    background: #dafbe1;
}

.login-button {
    box-shadow: none;
}

@media (max-width: 720px) {
    .brand-title {
        min-width: 52px;
    }

    .brand-text {
        display: none;
    }

    .nav-actions {
        max-width: calc(100vw - 88px);
    }
}
</style>
