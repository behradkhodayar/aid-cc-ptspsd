import { useEffect, useState } from 'react';
import { getHealth, listItems, type Health, type Item } from './api.ts';

export function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [items, setItems] = useState<Item[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getHealth().then(setHealth).catch(handleError);
    listItems().then(setItems).catch(handleError);

    function handleError(err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
    }
  }, []);

  return (
    <main>
      <h1>ccaidtemplate</h1>
      <p>
        API status:{' '}
        <span className="status" data-ok={health?.status === 'ok'}>
          {health ? health.status : 'checking…'}
        </span>
      </p>

      {error && <p role="alert">Could not reach the API: {error}</p>}

      <h2>Items</h2>
      {items.length === 0 ? (
        <p>No items yet.</p>
      ) : (
        <ul>
          {items.map((item) => (
            <li key={item.id}>{item.name}</li>
          ))}
        </ul>
      )}
    </main>
  );
}
