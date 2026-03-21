import { useState, useCallback } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { login as apiLogin, register as apiRegister } from '../api/authApi.ts';
import { tokenStorage } from '../api/client';
import type { LoginRequest, RegistrationRequest } from '../types/auth';

interface AuthState {
    loading: boolean;
    error: string | null;
    isAuthenticated: boolean;
}

export function useAuth() {
    const navigate = useNavigate();

    const [state, setState] = useState<AuthState>({
        loading: false,
        error: null,
        isAuthenticated: !!tokenStorage.get(),
    });

    const clearError = useCallback(() => {
        setState((s) => ({ ...s, error: null }));
    }, []);

    const login = useCallback(
        async (payload: LoginRequest) => {
            setState((s) => ({ ...s, loading: true, error: null }));
            const result = await apiLogin(payload);

            if (!result.ok) {
                setState((s) => ({ ...s, loading: false, error: result.message }));
                return;
            }

            tokenStorage.set(result.data.jwtToken);
            setState({ loading: false, error: null, isAuthenticated: true });

            await navigate({to: '/dashboard'});
        },
        [navigate],
    );

    const register = useCallback(
        async (payload: RegistrationRequest) => {

            setState((s) => ({ ...s, loading: true, error: null }));
            const result = await apiRegister(payload);

            if (!result.ok) {
                setState((s) => ({ ...s, loading: false, error: result.message }));
                return;
            }

            tokenStorage.set(result.data.jwtToken);
            setState({ loading: false, error: null, isAuthenticated: true });

            await navigate({to: '/dashboard'});
        },
        [navigate],
    );

    const logout = useCallback(() => {
        tokenStorage.clear();
        setState({ loading: false, error: null, isAuthenticated: false });
        navigate({ to: '/login' });
    }, [navigate]);

    return {
        ...state,
        clearError,
        login,
        register,
        logout,
    };
}