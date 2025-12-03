// frontend/src/Room.tsx
import React, { useEffect, useRef, useState } from 'react';

function useDebounced(value: string, delay = 600) {
  const [deb, setDeb] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDeb(value), delay);
    return () => clearTimeout(t);
  }, [value, delay]);
  return deb;
}

export default function Room({ roomId }: { roomId: string }) {
  const [code, setCode] = useState('');
  const [suggestion, setSuggestion] = useState('');
  const wsRef = useRef<WebSocket | null>(null);
  const debCode = useDebounced(code, 600);

  useEffect(() => {
    const host = location.hostname;
    const port = '8000';
    const scheme = location.protocol === 'https:' ? 'wss' : 'ws';
    const ws = new WebSocket(`${scheme}://${host}:${port}/ws/${roomId}`);

    ws.onopen = () => {
      console.log('ws open');
    };

    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.type === 'init') setCode(data.code || '');
        if (data.type === 'update') setCode(data.code || '');
      } catch (e) {
        console.warn(e);
      }
    };

    ws.onerror = (err) => {
      console.warn('ws error', err);
    };

    wsRef.current = ws;
    return () => {
      try {
        ws.close();
      } catch {}
      wsRef.current = null;
    };
  }, [roomId]);

  // send updates (only when socket is open)
  useEffect(() => {
    const ws = wsRef.current;
    if (!ws) return;
    try {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'update', code }));
      }
      // if not open, we silently ignore — the server sends init on connect anyway
    } catch (e) {
      console.warn('ws send error', e);
    }
  }, [code]);

  // autocomplete on debounced code
  useEffect(() => {
    async function callAC() {
      try {
        const res = await fetch(`http://localhost:8000/autocomplete`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            code: debCode,
            cursorPosition: debCode.length,
            language: 'python',
          }),
        });
        if (!res.ok) {
          console.warn('autocomplete failed', res.status);
          return;
        }
        const j = await res.json();
        setSuggestion(j.suggestion);
      } catch (e) {
        console.warn(e);
      }
    }
    if (debCode.trim().length > 0) callAC();
    else setSuggestion('');
  }, [debCode]);

  return (
    <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
      <textarea
        style={{ width: 700, height: 500 }}
        value={code}
        onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
          setCode(e.target.value)
        }
      />
      <div style={{ width: 320 }}>
        <h4>Autocomplete</h4>
        <pre>{suggestion}</pre>
      </div>
    </div>
  );
}
