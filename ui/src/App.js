import AlertForm from './form';
import AlertMonitor from './alertmonitor'
import StartButton from './startButton'
import './App.css';
import { useState } from 'react';

function App() {
  const [currentAlertId, setCurrentAlertId] = useState(undefined);
  const [pollRate, setPollRate] = useState(undefined);
  const [startTime, setStartTime] = useState(undefined);
  const [alertLoaded, setAlertLoaded] = useState(false);
  
  return (
    <div className="App">
      <AlertForm 
        setAlertId={setCurrentAlertId}
        setPollRate={setPollRate}
        setAlertLoaded={setAlertLoaded}
      />
      <StartButton 
        alertId={currentAlertId}
        setStartTime={setStartTime}
        alertLoaded={alertLoaded}
      />
      <AlertMonitor
        alertId={currentAlertId}
        pollRate={pollRate}
        startTime={startTime}
      />
    </div>
  );
}

export default App;
