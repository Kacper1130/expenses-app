import React, { forwardRef, useState } from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'ghost' | 'danger'
    loading?: boolean
    fullWidth?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    ({ variant = 'primary', loading = false, fullWidth = false, children, disabled, className, ...rest }, ref) => (
        <button
            ref={ref}
            disabled={disabled || loading}
            className={['btn', `btn-${variant}`, fullWidth ? 'btn-full' : '', className ?? ''].filter(Boolean).join(' ')}
            {...rest}
        >
            {loading ? <Spinner size={16} /> : null}
            {children}
        </button>
    ),
)
Button.displayName = 'Button'

interface TextInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string
    error?: string
    iconLeft?: React.ReactNode
    revealable?: boolean
}

export const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
    ({ label, error, iconLeft, revealable = false, type, id, ...rest }, ref) => {
        const [revealed, setRevealed] = useState(false)
        const inputId   = id ?? label.toLowerCase().replace(/\s+/g, '-')
        const inputType = revealable ? (revealed ? 'text' : 'password') : type

        const inputClasses = [
            'input',
            !iconLeft  ? 'input-no-icon'    : '',
            revealable ? 'input-revealable' : '',
            error      ? 'input-error'      : '',
        ].filter(Boolean).join(' ')

        return (
            <div className="input-field">
                <label htmlFor={inputId} className="input-label">{label}</label>
                <div className="input-wrap">
                    {iconLeft && <span className="input-icon">{iconLeft}</span>}
                    <input ref={ref} id={inputId} type={inputType} className={inputClasses} {...rest} />
                    {revealable && (
                        <button
                            type="button"
                            className="eye-btn"
                            onClick={() => setRevealed((v) => !v)}
                            tabIndex={-1}
                            aria-label={revealed ? 'Ukryj hasło' : 'Pokaż hasło'}
                        >
                            <EyeIcon open={revealed} />
                        </button>
                    )}
                </div>
                {error && <span className="field-error">{error}</span>}
            </div>
        )
    },
)
TextInput.displayName = 'TextInput'

interface ErrorBannerProps {
    message: string | null
    onDismiss?: () => void
}

export function ErrorBanner({ message, onDismiss }: ErrorBannerProps) {
    if (!message) return null
    return (
        <div className="error-banner" role="alert">
            <AlertIcon />
            <span style={{ flex: 1 }}>{message}</span>
            {onDismiss && (
                <button type="button" onClick={onDismiss} aria-label="Zamknij">✕</button>
            )}
        </div>
    )
}

export function Spinner({ size = 18 }: { size?: number }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="animate-spin" aria-hidden>
            <path d="M21 12a9 9 0 11-6.219-8.56" />
        </svg>
    )
}

function EyeIcon({ open }: { open: boolean }) {
    return (
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            {open ? (
                <><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" /><circle cx="12" cy="12" r="3" /></>
            ) : (
                <><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94" /><path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19" /><line x1="1" y1="1" x2="23" y2="23" /></>
            )}
        </svg>
    )
}

function AlertIcon() {
    return (
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ flexShrink: 0 }}>
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
    )
}