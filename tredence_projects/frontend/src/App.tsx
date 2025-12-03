import React, { useState } from 'react'
import Room from './Room'

export default function App(){
  const [roomId, setRoomId] = useState('')
  const [joined, setJoined] = useState(false)

  return (
    <div style={{padding:20,fontFamily:'sans-serif'}}>
      <h1>Realtime Pair</h1>
      {!joined ? (
        <div style={{display:'flex',gap:8}}>
          <input placeholder="Enter or create room id" value={roomId} onChange={e=>setRoomId(e.target.value)} />
          <button onClick={async ()=>{ if(!roomId){ const res = await fetch('http://localhost:8000/rooms/', { method:'POST' }); const j = await res.json(); setRoomId(j.roomId); } setJoined(true)}}>Create / Join</button>
        </div>
      ) : (
        <Room roomId={roomId} />
      )}
    </div>
  )
}
