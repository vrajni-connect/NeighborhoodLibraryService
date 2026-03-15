import { useEffect, useState } from 'react'

// Backend URL used by frontend. Can be overridden with VITE_API_URL.
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  // Local state for books and members.
  const [books, setBooks] = useState([])
  const [members, setMembers] = useState([])

  // Load initial lists on mount.
  useEffect(() => {
    fetch(`${API_URL}/books`)
      .then((r) => r.json())
      .then(setBooks)
      .catch((err) => console.error('Failed to load books:', err))

    fetch(`${API_URL}/members`)
      .then((r) => r.json())
      .then(setMembers)
      .catch((err) => console.error('Failed to load members:', err))
  }, [])

  return (
    <div style={{ margin: '2rem', fontFamily: 'system-ui, sans-serif' }}>
      <h1>Neighborhood Library</h1>
      <p>Backend API: <code>{API_URL}</code></p>
      <section>
        <h2>Books</h2>
        <ul>
          {books.map((b) => (
            <li key={b.id}>
              {b.title} by {b.author} (copies {b.total_copies})
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h2>Members</h2>
        <ul>
          {members.map((m) => <li key={m.id}>{m.name} ({m.email})</li>)}
        </ul>
      </section>
    </div>
  )
}

export default App
