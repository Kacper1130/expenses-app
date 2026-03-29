export interface Group {
    id: string;
    name: string;
    description: string | null;
    owner_id: string;
    created_at: string;
    member_count: number;
}

export interface SplitDetail {
    user_name: string;
    amount: number;
}

export interface Expense {
    id: number;
    group_id: string;
    paid_by: string;
    amount: number;
    description: string;
    created_at: string;
    splits: SplitDetail[];
}

export interface DebtEntry {
    from_user: string;  // kto jest winny
    to_user: string;    // komu jest winny
    amount: number;
}

export interface BalanceSummary {
    debts: DebtEntry[];
    settled: boolean;
}

export interface CreateGroupRequest {
    name: string;
    description?: string;
}

export interface CreateExpenseRequest {
    amount: number;
    description: string;
}
