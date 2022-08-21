import { useAlert } from './AlertHook';

function AlertMonitor (props) {
    const alert = useAlert({})
    console.log(`Monitoring Alert ${props.alertId} ${props.pollRate}` )

    if (!props.alertId || !props.pollRate){
        return
    }
    
    setInterval( () => {
        fetch(`/api/v1/alerts?id=${props.alertId}`).then((response) => {response.json().then(
            (data) => {alert.setAlert(
                data.num_passed,
                data.num_failed,
                data.remaining_msgs,
                data.poll_rate,
                data.num_senders,
            )
        }
        )})
    }, props.pollRate * 1000)

    let msgRate = <></>
    if (props.startTime && (alert.numFailed + alert.numPassed)) {
        const rate = ((new Date()/1000) - props.startTime) / (alert.numFailed + alert.numPassed)
        msgRate = <p>Messages per sec: {rate}</p>
    }
    return <>
        <p>Failed: {alert.numFailed}</p>
        <p>Passed: {alert.numPassed}</p>
        <p>Remaining: {alert.remainingMsgs}</p>
        <p>Poll Rate: {alert.pollRate}</p>
        <p>Number Senders: {alert.numSenders}</p>
        {msgRate}
    </>
    


}
export default AlertMonitor