export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegistrationRequest {
    email: string;
    password: string;
    confirmPassword: string;
    name: string;
}

export interface AuthResponse {
    jwtToken: string;
}

export interface ErrorResponse {
    status: number;
    message: string;
}

/* ============================================================
   types/api.ts — Generic API wrapper types
   ============================================================ */

/** Wraps every API call result — no raw axios bleeding into components */
export type ApiResult<T> =
    | { ok: true;  data: T }
    | { ok: false; message: string; status?: number };