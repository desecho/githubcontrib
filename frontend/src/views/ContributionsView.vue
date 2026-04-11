<template>
    <section class="page-shell">
        <v-progress-linear v-if="loading" color="primary" indeterminate />

        <template v-else-if="contributions !== null">
            <div class="profile-header">
                <a
                    :href="contributions.githubProfileUrl"
                    target="_blank"
                    rel="noopener"
                >
                    <img
                        class="profile-avatar"
                        :src="
                            contributions.avatar ??
                            githubAvatarUrl(contributions.username)
                        "
                        :alt="`${contributions.username} avatar`"
                    />
                </a>
                <div>
                    <h1 class="page-title">{{ title }}</h1>
                    <p v-if="own" class="profile-username">
                        {{ contributions.username }}
                    </p>
                    <div class="profile-links">
                        <a
                            :href="contributions.githubProfileUrl"
                            target="_blank"
                            rel="noopener"
                        >
                            <v-icon icon="mdi-github" />
                            GitHub
                        </a>
                        <span>
                            <v-icon color="warning" icon="mdi-star" />
                            {{ contributions.stars }}
                        </span>
                    </div>
                </div>
            </div>

            <div
                v-if="reposWithCommits.length === 0"
                class="content-panel empty-state"
            >
                No loaded commits yet.
            </div>

            <v-expansion-panels v-else variant="accordion">
                <v-expansion-panel
                    v-for="repo in reposWithCommits"
                    :key="repo.id"
                >
                    <v-expansion-panel-title>
                        {{ repo.name }}
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <v-list bg-color="transparent">
                            <v-list-item
                                v-for="commit in repo.commits"
                                :key="commit.id"
                            >
                                <template #title>
                                    <span>{{ commit.message }}</span>
                                </template>
                                <template #subtitle>
                                    {{ formatDate(commit.date) }}
                                </template>
                                <template #append>
                                    <v-btn
                                        :href="commit.url"
                                        icon="mdi-open-in-new"
                                        target="_blank"
                                        rel="noopener"
                                        variant="text"
                                    />
                                </template>
                            </v-list-item>
                        </v-list>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </template>
    </section>
</template>

<script setup lang="ts">
import axios from "axios";
import { computed, ref, watch } from "vue";
import { useToast } from "vue-toast-notification";

import type { Contributions } from "../types";

import { formatDate, githubAvatarUrl } from "../helpers";

const props = withDefaults(
    defineProps<{
        username?: string;
        own?: boolean;
    }>(),
    {
        own: false,
        username: undefined,
    },
);

const contributions = ref<Contributions | null>(null);
const loading = ref(true);
const toast = useToast();

const reposWithCommits = computed(() =>
    (contributions.value?.repos ?? []).filter(
        (repo) => repo.commits.length > 0,
    ),
);

const title = computed(() =>
    props.own ? "My contributions" : contributions.value?.username,
);

async function loadContributions(): Promise<void> {
    loading.value = true;
    try {
        const url = props.own
            ? "my-contributions/"
            : `users/${props.username}/contributions/`;
        const response = await axios.get<Contributions>(url);
        contributions.value = response.data;
    } catch {
        toast.error("Error loading contributions");
    } finally {
        loading.value = false;
    }
}

watch(
    () => [props.own, props.username],
    () => {
        void loadContributions();
    },
    { immediate: true },
);
</script>

<style scoped lang="scss">
.profile-header {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 24px;
}

.profile-links {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    align-items: center;
}

.profile-username {
    margin: 0 0 8px;
    color: #5f6b7a;
    font-weight: 600;
}
</style>
