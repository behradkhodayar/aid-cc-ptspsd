import { render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import { App } from './App.tsx';
import * as api from './api.ts';

beforeEach(() => {
  vi.spyOn(api, 'getHealth').mockResolvedValue({ status: 'ok', database: true });
  vi.spyOn(api, 'listItems').mockResolvedValue([
    { id: 1, name: 'widget', description: null, created_at: '', updated_at: '' },
  ]);
});

afterEach(() => {
  vi.restoreAllMocks();
});

test('renders the API status and item list', async () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: 'ccaidtemplate' })).toBeInTheDocument();

  await waitFor(() => expect(screen.getByText('ok')).toBeInTheDocument());
  expect(screen.getByText('widget')).toBeInTheDocument();
});
