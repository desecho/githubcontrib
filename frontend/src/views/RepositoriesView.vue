<template>
    <section class="page-shell">
        <h1 class="page-title">Repositories</h1>

        <v-form class="repo-form" @submit.prevent="addRepo">
            <v-text-field
                v-model="name"
                label="Repository"
                placeholder="user/project"
                :rules="repoRules"
                variant="outlined"
                density="comfortable"
            />
            <v-btn color="primary" type="submit" :loading="saving">Add</v-btn>
            <v-btn
                color="secondary"
                variant="tonal"
                :disabled="repos.length === 0"
                :loading="loadingCommits"
                @click="loadCommitData"
            >
                Load/Update commits
            </v-btn>
        </v-form>

        <v-progress-linear v-if="loading" color="primary" indeterminate />

        <div v-else class="content-panel">
            <div v-if="repos.length === 0" class="empty-state">
                Add a repository you contributed to. Then load commits from your
                repositories.
            </div>
            <draggable
                v-else
                v-model="repos"
                item-key="id"
                handle=".drag-handle"
                @end="saveReposOrder"
            >
                <template #item="{ element, index }">
                    <div class="repo-row">
                        <div>
                            <v-icon class="drag-handle" icon="mdi-drag" />
                            <span>{{ element.name }}</span>
                        </div>
                        <div class="repo-actions">
                            <v-btn
                                icon="mdi-refresh"
                                :loading="refreshingRepoId === element.id"
                                title="Load commits"
                                variant="text"
                                @click="loadCommitDataForRepo(element.id)"
                            />
                            <v-btn
                                icon="mdi-delete"
                                title="Delete"
                                variant="text"
                                @click="deleteRepo(element.id, index)"
                            />
                        </div>
                    </div>
                </template>
            </draggable>
        </div>
    </section>
</template>

<script setup lang="ts">
import axios from "axios";
import draggable from "vuedraggable";
import { onMounted, ref } from "vue";
import { useToast } from "vue-toast-notification";

import type { ApiErrorData, Repo, RepoOrder } from "../types";
import type { AxiosError } from "axios";

const repos = ref<Repo[]>([]);
const originalRepos = ref<Repo[]>([]);
const name = ref("");
const loading = ref(true);
const saving = ref(false);
const loadingCommits = ref(false);
const refreshingRepoId = ref<number | null>(null);
const toast = useToast();

const repoRules = [
    (value: string) => (/.+\/.+/.test(value) ? true : "Use user/project"),
];

function errorMessage(error: unknown, fallback: string): string {
    const axiosError = error as AxiosError<ApiErrorData>;
    return axiosError.response?.data.detail ?? fallback;
}

async function loadRepos(): Promise<void> {
    loading.value = true;
    try {
        const response = await axios.get<Repo[]>("repos/");
        repos.value = response.data;
        originalRepos.value = [...response.data];
    } catch {
        toast.error("Error loading repositories");
    } finally {
        loading.value = false;
    }
}

async function addRepo(): Promise<void> {
    saving.value = true;
    try {
        const response = await axios.post<Repo>("repos/", { name: name.value });
        repos.value = [response.data, ...repos.value];
        originalRepos.value = [...repos.value];
        name.value = "";
        toast.success("Repository added");
    } catch (error) {
        toast.error(errorMessage(error, "Error adding repository"));
    } finally {
        saving.value = false;
    }
}

async function deleteRepo(repoId: number, index: number): Promise<void> {
    try {
        await axios.delete(`repos/${repoId}/`);
        repos.value.splice(index, 1);
        originalRepos.value = [...repos.value];
        toast.success("Repository deleted");
    } catch (error) {
        toast.error(errorMessage(error, "Error deleting repository"));
    }
}

async function loadCommitData(): Promise<void> {
    loadingCommits.value = true;
    try {
        await axios.post("repos/load-commit-data/");
        toast.success("Commit data has been updated");
    } catch {
        toast.error("Error loading commit data");
    } finally {
        loadingCommits.value = false;
    }
}

async function loadCommitDataForRepo(repoId: number): Promise<void> {
    refreshingRepoId.value = repoId;
    try {
        await axios.post(`repos/${repoId}/load-commit-data/`);
        toast.success("Commit data has been updated");
    } catch {
        toast.error("Error loading commit data");
    } finally {
        refreshingRepoId.value = null;
    }
}

async function saveReposOrder(): Promise<void> {
    const payload: RepoOrder[] = repos.value.map((repo, index) => ({
        id: repo.id,
        order: index + 1,
    }));

    try {
        await axios.put("repos/save-order/", { repos: payload });
        originalRepos.value = [...repos.value];
    } catch {
        repos.value = [...originalRepos.value];
        toast.error("Error saving repositories order");
    }
}

onMounted(() => {
    void loadRepos();
});
</script>

<style scoped lang="scss">
.repo-form {
    display: grid;
    grid-template-columns: minmax(220px, 1fr) auto auto;
    gap: 12px;
    align-items: start;
    margin-bottom: 20px;
}

.repo-actions {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    gap: 4px;
}

@media (max-width: 720px) {
    .repo-form {
        grid-template-columns: 1fr;
    }
}
</style>
