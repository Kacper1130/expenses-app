import axios, { AxiosError } from 'axios';

const TOKEN_KEY = 'jwt_token';

export const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8080',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10_000,
});

/* ---------- Request interceptor — attach JWT ---------- */
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(TOKEN_KEY);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error),
);

/* ---------- Response interceptor — handle 401 globally ---------- */
apiClient.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
        const url = error.config?.url ?? ''
        const isAuthEndpoint = url.includes('/api/auth/')

        if (error.response?.status === 401 && !isAuthEndpoint) {
            localStorage.removeItem(TOKEN_KEY)
            window.location.replace('/login')
        }
        return Promise.reject(error)
    },
)

/* ---------- Token helpers (used by useAuth hook) ---------- */
export const tokenStorage = {
    get: (): string | null => localStorage.getItem(TOKEN_KEY),
    set: (token: string): void  => localStorage.setItem(TOKEN_KEY, token),
    clear: (): void              => localStorage.removeItem(TOKEN_KEY),
};