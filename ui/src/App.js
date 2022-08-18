import AlertForm from './form';
import AlertMonitor from './alertmonitor'
import StartButton from './startButton'
import './App.css';
import { useState } from 'react';

function App() {
  const [currentAlertId, setCurrentAlertId] = useState(undefined);
  const [pollRate, setPollRate] = useState(undefined);
  
  return (
    <div className="App">
      <AlertForm 
        setAlertId={setCurrentAlertId}
        setPollRate={setPollRate}
      />
      <StartButton 
        alertId={currentAlertId}
      />
      <AlertMonitor
        alertId={currentAlertId}
        pollRate={pollRate}
      />
    </div>
  );
}

export default App;
