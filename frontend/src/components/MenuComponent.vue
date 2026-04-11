<template>
    <v-app-bar color="surface" elevation="1">
        <v-app-bar-title>
            <router-link class="brand-link" to="/">GitHubContrib</router-link>
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
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
</script>

<style scoped lang="scss">
.brand-link {
    color: #1f2933;
    font-weight: 700;
    text-decoration: none;
}
</style>
