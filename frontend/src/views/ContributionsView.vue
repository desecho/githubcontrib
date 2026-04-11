<template>
    <section class="page-shell">
        <v-progress-linear v-if="loading" color="primary" indeterminate />

        <template v-else-if="contributions !== null">
            <div class="content-panel profile-header">
                <a
                    class="profile-avatar-link"
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
                <div class="profile-summary">
                    <h1 class="page-title profile-title">{{ title }}</h1>
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

            <v-expansion-panels
                v-else
                class="contrib-panels"
                variant="accordion"
            >
                <v-expansion-panel
                    v-for="repo in reposWithCommits"
                    :key="repo.id"
                    class="contrib-panel"
                >
                    <v-expansion-panel-title>
                        <div class="repo-panel-title">
                            <span>{{ repo.name }}</span>
                            <span class="commit-count">
                                {{ repo.commits.length }}
                                {{
                                    repo.commits.length === 1
                                        ? "commit"
                                        : "commits"
                                }}
                            </span>
                        </div>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <v-list bg-color="transparent">
                            <v-list-item
                                v-for="commit in repo.commits"
                                :key="commit.id"
                                class="commit-row"
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
                                        class="commit-link"
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
    padding: 20px;
}

.profile-avatar-link {
    display: inline-flex;
    flex: 0 0 auto;
}

.profile-summary {
    min-width: 0;
}

.profile-title {
    margin-bottom: 8px;
    overflow-wrap: anywhere;
}

.profile-links {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    align-items: center;
}

.profile-links a,
.profile-links span {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #57606a;
    font-weight: 650;
}

.profile-links a:hover {
    color: #1a7f37;
}

.profile-username {
    margin: 0 0 8px;
    color: #57606a;
    font-weight: 600;
}

.contrib-panels {
    gap: 10px;
}

.contrib-panel {
    border: 1px solid #d0d7de;
    border-radius: 8px;
    background: #ffffff;
    box-shadow: 0 1px 2px rgba(27, 31, 36, 0.04);
}

.contrib-panel :deep(.v-expansion-panel-title) {
    min-height: 58px;
    color: #24292f;
    font-weight: 700;
}

.contrib-panel :deep(.v-expansion-panel-text__wrapper) {
    padding: 0;
    border-top: 1px solid #d8dee4;
}

.repo-panel-title {
    display: flex;
    width: 100%;
    min-width: 0;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.repo-panel-title > span:first-child {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.commit-count {
    flex: 0 0 auto;
    padding: 3px 8px;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    color: #57606a;
    font-size: 0.82rem;
    font-weight: 650;
}

.commit-row {
    border-bottom: 1px solid #d8dee4;
}

.commit-row:last-child {
    border-bottom: 0;
}

.commit-row :deep(.v-list-item-title) {
    color: #24292f;
    line-height: 1.35;
    white-space: normal;
}

.commit-row :deep(.v-list-item-subtitle) {
    color: #57606a;
    opacity: 1;
}

.commit-link {
    color: #57606a;
}

@media (max-width: 720px) {
    .profile-header {
        align-items: flex-start;
        padding: 16px;
    }

    .profile-avatar {
        width: 72px;
        height: 72px;
    }

    .repo-panel-title {
        align-items: flex-start;
        flex-direction: column;
        gap: 6px;
    }

    .repo-panel-title > span:first-child {
        white-space: normal;
    }
}
</style>
