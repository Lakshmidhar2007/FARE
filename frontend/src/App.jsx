import React, { useEffect, useState } from 'react'
import { checkBackendHealth } from './api'

function App() {
  const [backendStatus, setBackendStatus] = useState('Checking...')
  const [error, setError] = useState('')

  useEffect(() => {
    checkBackendHealth()
      .then((data) => {
        if (data.status === 'ok') {
          setBackendStatus('Backend Connected')
        } else {
          setBackendStatus('Backend Error')
        }
      })
      .catch((err) => {
        console.error(err)
        setBackendStatus('Backend Disconnected')
        setError('Could not connect to FastAPI')
      })
  }, [])

  return (
    <div>
      <h1>FARE</h1>

      <p>
        Faithfulness & Abstention Rate Evaluation
      </p>

      <p>
        Frontend is running
      </p>

      <h2>{backendStatus}</h2>

      {error && (
        <p>{error}</p>
      )}
    </div>
  )
}

export default App