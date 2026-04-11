<template>
    <section class="page-shell">
        <h1 class="page-title">About GitHubContrib</h1>

        <div class="content-panel about-panel">
            <p>
                GitHubContrib keeps a public list of repositories you
                contributed to and the commits loaded from GitHub.
            </p>
            <p>
                Add repositories from your account, refresh commits when you
                need current data, and share your contribution page with anyone.
            </p>
            <p>
                <a href="https://github.com/" target="_blank" rel="noopener"
                    >GitHub</a
                >
                is used for login and repository data.
            </p>
        </div>
    </section>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss">
.about-panel {
    max-width: 760px;
    padding: 24px;
}

.about-panel p {
    margin: 0 0 16px;
    color: #57606a;
    line-height: 1.65;
}

.about-panel p:last-child {
    margin-bottom: 0;
}
</style>
