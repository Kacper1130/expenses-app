import { AxiosError } from 'axios';
import { apiClient } from './client';
import type {
    LoginRequest,
    RegistrationRequest,
    AuthResponse,
    ErrorResponse,
    ApiResult,
} from '../types/auth';

/** Extract a human-readable message from any axios error */
function extractMessage(error: unknown): { message: string; status?: number } {
    if (error instanceof AxiosError) {
        const data = error.response?.data as ErrorResponse | undefined;
        return {
            message: data?.message ?? error.message ?? 'Nieoczekiwany błąd serwera.',
            status:  error.response?.status,
        };
    }
    return { message: 'Nie można połączyć się z serwerem.' };
}

export async function login(
    payload: LoginRequest,
): Promise<ApiResult<AuthResponse>> {
    try {
        const { data } = await apiClient.post<AuthResponse>('/api/auth/login', payload);
        return { ok: true, data };
    } catch (err) {
        return { ok: false, ...extractMessage(err) };
    }
}

export async function register(
    payload: RegistrationRequest,
): Promise<ApiResult<AuthResponse>> {
    try {
        const { data } = await apiClient.post<AuthResponse>('/api/auth/register', payload);
        return { ok: true, data };
    } catch (err) {
        return { ok: false, ...extractMessage(err) };
    }
}