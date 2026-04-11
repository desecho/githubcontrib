<template>
    <section class="page-shell">
        <h1 class="page-title">Users</h1>

        <v-progress-linear v-if="loading" color="primary" indeterminate />

        <div v-else class="content-panel">
            <div v-if="users.length === 0" class="empty-state">
                No users yet.
            </div>
            <v-list v-else bg-color="transparent">
                <v-list-item
                    v-for="username in users"
                    :key="username"
                    :to="`/users/${username}`"
                    prepend-icon="mdi-github"
                    :title="username"
                />
            </v-list>
        </div>
    </section>
</template>

<script setup lang="ts">
import axios from "axios";
import { onMounted, ref } from "vue";
import { useToast } from "vue-toast-notification";

const users = ref<string[]>([]);
const loading = ref(true);
const toast = useToast();

async function loadUsers(): Promise<void> {
    loading.value = true;
    try {
        const response = await axios.get<string[]>("users/");
        users.value = response.data;
    } catch {
        toast.error("Error loading users");
    } finally {
        loading.value = false;
    }
}

onMounted(() => {
    void loadUsers();
});
</script>
