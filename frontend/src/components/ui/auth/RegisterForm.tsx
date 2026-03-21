import {useState} from 'react'
import {Button, ErrorBanner, TextInput} from '../index'
import {useAuth} from '../../../hooks/useAuth'

const EmailIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
        <polyline points="22,6 12,13 2,6"/>
    </svg>
)
const LockIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
        <path d="M7 11V7a5 5 0 0110 0v4"/>
    </svg>
)
const CheckLockIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M9 12l2 2 4-4"/>
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
        <path d="M7 11V7a5 5 0 0110 0v4"/>
    </svg>
)

const STRENGTH_LABEL = ['', 'Słabe', 'Przeciętne', 'Dobre', 'Silne'] as const
const STRENGTH_COLOR = ['', 'var(--color-error)', 'var(--color-warning)', 'var(--color-info)', 'var(--color-success)'] as const

function calcStrength(pw: string): number {
    if (!pw) return 0
    let s = 0
    if (pw.length >= 8) s++
    if (/[A-Z]/.test(pw)) s++
    if (/[0-9]/.test(pw)) s++
    if (/[^A-Za-z0-9]/.test(pw)) s++
    return s
}

function PasswordStrengthBar({password}: { password: string }) {
    if (!password) return null
    const score = calcStrength(password)
    return (
        <div className="strength-wrap">
            <div className="strength-bar">
                {[1, 2, 3, 4].map((i) => (
                    <div
                        key={i}
                        className="strength-segment"
                        style={{background: i <= score ? STRENGTH_COLOR[score] : 'var(--color-border-strong)'}}
                    />
                ))}
            </div>
            <span className="strength-label" style={{color: STRENGTH_COLOR[score]}}>
        {STRENGTH_LABEL[score]}
      </span>
        </div>
    )
}

export function RegisterForm() {
    const {register, loading, error, clearError} = useAuth()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        register({email, password, confirmPassword})
    }

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-5" noValidate>
            <TextInput label="Adres e-mail" type="email" value={email}
                       onChange={(e) => setEmail(e.target.value)}
                       placeholder="jan@kowalski.pl" iconLeft={<EmailIcon/>}
                       autoComplete="email" required/>
            <div className="flex flex-col gap-2">
                <TextInput label="Hasło" value={password}
                           onChange={(e) => setPassword(e.target.value)}
                           placeholder="••••••••" iconLeft={<LockIcon/>}
                           revealable autoComplete="new-password" required/>
                <PasswordStrengthBar password={password}/>
            </div>
            <TextInput label="Potwierdź hasło" value={confirmPassword}
                       onChange={(e) => setConfirmPassword(e.target.value)}
                       placeholder="••••••••" iconLeft={<CheckLockIcon/>}
                       revealable autoComplete="new-password" required
            />
            <ErrorBanner message={error} onDismiss={clearError}/>
            <Button type="submit" fullWidth loading={loading}>
                Utwórz konto
            </Button>
        </form>
    )
}