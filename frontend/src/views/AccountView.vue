<template>
    <section class="page-shell">
        <h1 class="page-title">Account</h1>

        <v-progress-linear v-if="loading" color="primary" indeterminate />

        <div v-else-if="profile !== null" class="content-panel account-panel">
            <div class="profile-header">
                <img
                    class="profile-avatar"
                    :src="profile.avatar ?? githubAvatarUrl(profile.username)"
                    :alt="`${profile.username} avatar`"
                />
                <div>
                    <h2 class="account-username">{{ profile.username }}</h2>
                    <a
                        class="profile-url"
                        :href="profile.githubProfileUrl"
                        target="_blank"
                        rel="noopener"
                    >
                        {{ profile.githubProfileUrl }}
                    </a>
                </div>
            </div>

            <v-divider />

            <div class="danger-zone">
                <div>
                    <h2>Delete Account</h2>
                    <p class="muted">
                        Your repositories and commits will be deleted with your
                        account.
                    </p>
                </div>
                <v-btn color="error" :loading="deleting" @click="deleteAccount"
                    >Delete Account</v-btn
                >
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toast-notification";

import type { UserProfile } from "../types";

import { githubAvatarUrl } from "../helpers";
import { useAuthStore } from "../stores/auth";

const profile = ref<UserProfile | null>(null);
const loading = ref(true);
const deleting = ref(false);
const toast = useToast();
const router = useRouter();
const auth = useAuthStore();

async function loadProfile(): Promise<void> {
    loading.value = true;
    try {
        const response = await axios.get<UserProfile>("me/");
        profile.value = response.data;
    } catch {
        toast.error("Error loading account");
    } finally {
        loading.value = false;
    }
}

async function deleteAccount(): Promise<void> {
    deleting.value = true;
    try {
        await axios.delete("me/");
        auth.logout();
        toast.success("Your account has been deleted");
        await router.push("/");
    } catch {
        toast.error("Error deleting account");
    } finally {
        deleting.value = false;
    }
}

onMounted(() => {
    void loadProfile();
});
</script>

<style scoped lang="scss">
.account-panel {
    max-width: 760px;
    padding: 24px;
}

.profile-header,
.danger-zone {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
}

.profile-header {
    justify-content: flex-start;
    padding-bottom: 22px;
}

.account-username {
    margin: 0 0 6px;
    color: #24292f;
    font-size: 1.35rem;
    line-height: 1.25;
    overflow-wrap: anywhere;
}

.profile-url {
    overflow-wrap: anywhere;
}

.danger-zone {
    padding-top: 22px;
}

.danger-zone h2 {
    margin: 0 0 6px;
    color: #24292f;
    font-size: 1.15rem;
}

.danger-zone p {
    margin: 0;
}

@media (max-width: 720px) {
    .profile-header,
    .danger-zone {
        align-items: flex-start;
        flex-direction: column;
    }
}
</style>
