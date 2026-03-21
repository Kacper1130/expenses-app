import { redirect } from '@tanstack/react-router'
import { tokenStorage } from '../api/client'

export function isAuthenticated(): boolean {
    return !!tokenStorage.get()
}

export function requireAuth() {
    if (!isAuthenticated()) {
        throw redirect({ to: '/login' })
    }
}