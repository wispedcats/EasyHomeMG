import { useEffect, useState } from "react"

export default function Dashboard() {
  const [temperature, setTemperature] = useState(null)
  const [fan, setFan] = useState(null)

  useEffect(() => {
    
    const apiUrl = `http://${window.location.hostname}:8000/temperature`

    function getTemp() {
      fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
          setTemperature(data.temperature)
          setFan(data.fan_state)
        })
        .catch(error => {
          console.error("API Fehler:", error)
        })
    };

    const interval = setInterval(getTemp, 1000)

    return () => {
      clearInterval(interval)
    }
  }, [])
function TemperatureGauge({ temperature }) {
  const maxTemp = 100
  const radius = 45
  const circumference = 2 * Math.PI * radius

  const percent = Math.min(temperature / maxTemp, 1)
  const offset = circumference * (1 - percent)

  return (
    <div className="relative w-32 h-32">
      <svg
        viewBox="0 0 100 100"
        className="w-full h-full -rotate-90"
      >
        <circle
          cx="50"
          cy="50"
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth="8"
          className="text-slate-700"
        />

        <circle
          cx="50"
          cy="50"
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="text-red-400 transition-all duration-500"
        />
      </svg>

      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-2xl font-bold text-white">
          {temperature ?? "--"}°C
        </span>
      </div>
    </div>
  )
}

return (
  <div>
    <TemperatureGauge temperature={temperature} />
    <p className="text-2lg font-mono text-center">Fan Speed: {fan}</p>
  </div>
)
}