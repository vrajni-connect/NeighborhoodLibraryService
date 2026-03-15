import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

// Main entrypoint: render React tree into root element.
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
