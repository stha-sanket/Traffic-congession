import React from 'react'
import { Route, Routes } from 'react-router-dom'
import Analytic from './Components/Analytic'
import Hero from './Components/Hero'
import TrafficSystem from './Components/TrafficSystem'

const App = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Hero />} />
        <Route path="/analytic" element={<Analytic />} />
        <Route path="/traffic-system" element={<TrafficSystem />} />
      </Routes>
    </div>
  )
}

export default App
