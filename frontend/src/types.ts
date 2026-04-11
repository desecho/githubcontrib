export interface JWTDecoded {
    exp: number;
}

export interface TokenRefreshData {
    access: string;
}

export interface AuthCallbackTokens {
    access: string;
    refresh: string;
    username: string;
}

export interface AuthUser {
    accessToken?: string;
    refreshToken?: string;
    username?: string;
    isLoggedIn: boolean;
}

export interface UserProfile {
    id: number;
    username: string;
    avatar: string | null;
    githubProfileUrl: string;
    stars: number;
}

export interface Repo {
    id: number;
    name: string;
    order: number;
}

export interface RepoOrder {
    id: number;
    order: number;
}

export interface Commit {
    id: number;
    url: string;
    date: string;
    message: string;
}

export interface ContributionRepo {
    id: number;
    name: string;
    commits: Commit[];
}

export interface Contributions {
    username: string;
    avatar: string | null;
    githubProfileUrl: string;
    stars: number;
    repos: ContributionRepo[];
}

export interface ApiErrorData {
    detail?: string;
    messageType?: "error" | "warning";
}
