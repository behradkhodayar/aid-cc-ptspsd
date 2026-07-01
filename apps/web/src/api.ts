/**
 * The single boundary to the backend API. Components import typed functions from here
 * and never call `fetch` directly. Keep these types in sync with `apps/api/src/app/schemas.py`.
 */

const API_URL: string = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export interface Health {
  status: string;
  database: boolean;
}

export interface Item {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface ItemCreate {
  name: string;
  description?: string | null;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!response.ok) {
    throw new Error(`API ${response.status}: ${await response.text()}`);
  }
  return (await response.json()) as T;
}

export function getHealth(): Promise<Health> {
  return request<Health>('/health');
}

export function listItems(): Promise<Item[]> {
  return request<Item[]>('/items');
}

export function createItem(payload: ItemCreate): Promise<Item> {
  return request<Item>('/items', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
