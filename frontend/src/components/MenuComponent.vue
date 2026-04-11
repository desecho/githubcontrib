<template>
    <v-app-bar color="surface" elevation="1">
        <v-app-bar-title>
            <router-link
                aria-label="GitHubContrib home"
                class="brand-link"
                to="/"
            >
                <img :src="logoUrl" alt="" class="brand-logo" />
            </router-link>
        </v-app-bar-title>

        <v-spacer />

        <v-btn to="/" variant="text">Users</v-btn>
        <v-btn
            v-if="auth.user.isLoggedIn"
            to="/my-contributions"
            variant="text"
        >
            My contributions
        </v-btn>
        <v-btn v-if="auth.user.isLoggedIn" to="/repositories" variant="text"
            >Repositories</v-btn
        >
        <v-btn to="/about" variant="text">About</v-btn>
        <v-btn v-if="auth.user.isLoggedIn" to="/account" variant="text">
            {{ auth.user.username }}
        </v-btn>
        <v-btn v-if="auth.user.isLoggedIn" to="/logout" variant="text"
            >Log out</v-btn
        >
        <v-btn v-else to="/login" color="primary" variant="flat">Log in</v-btn>
    </v-app-bar>
</template>

<script setup lang="ts">
import logoUrl from "../assets/logo.png";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
</script>

<style scoped lang="scss">
.brand-link {
    display: inline-flex;
    align-items: center;
    text-decoration: none;
}

.brand-logo {
    width: 44px;
    height: 40px;
    flex: 0 0 auto;
    object-fit: contain;
}
</style>
