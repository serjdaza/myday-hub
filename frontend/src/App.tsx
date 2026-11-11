import { useEffect, useState } from "react";

type Event = {
  id: number;
  source: "google" | "outlook";
  title: string;
  start_at: string;
  end_at: string;
  all_day: boolean;
};

export default function App() {
  const [health, setHealth] = useState("checking…");
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    fetch("/api/health")
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then((d) => setHealth(d.status))
      .catch(() => setHealth("unavailable"));

    fetch("/api/events")
      .then((r) => (r.ok ? r.json() : []))
      .then(setEvents)
      .catch(() => setEvents([]));
  }, []);

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: "1rem", maxWidth: 640 }}>
      <h1>myday-hub</h1>
      <p>Backend health: <strong>{health}</strong></p>
      <h2>Events</h2>
      {events.length === 0 ? (
        <p>No events yet.</p>
      ) : (
        <ul>
          {events.map((e) => (
            <li key={e.id}>
              [{e.source}] {e.title} — {new Date(e.start_at).toLocaleString()}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
