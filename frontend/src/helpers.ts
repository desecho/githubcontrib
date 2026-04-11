const defaultBackendUrl = "http://localhost:8000/";

export function getBackendUrl(): string {
    const backendUrl =
        (import.meta.env.VITE_BACKEND_URL as string | undefined) ??
        defaultBackendUrl;
    return backendUrl.endsWith("/") ? backendUrl : `${backendUrl}/`;
}

export function getUrl(path: string): string {
    return `${getBackendUrl()}${path.replace(/^\/+/, "")}`;
}

export function formatDate(value: string): string {
    return new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
    }).format(new Date(value));
}

export function githubAvatarUrl(username: string): string {
    return `https://github.com/${username}.png?size=160`;
}
