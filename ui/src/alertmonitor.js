import { useAlert } from './AlertHook';

function AlertMonitor (props) {
    const alert = useAlert({})
    console.log(`Monitoring Alert ${props.alertId} ${props.pollRate}` )

    if (!props.alertId || !props.pollRate){
        console.log("Skipping... for now")
        return
    }
    
    setTimeout( () => {
        console.log("getting latest data")
        fetch(`/api/v1/alerts?id=${props.alertId}`).then((response) => {response.json().then(
            (data) => {alert.setAlert(
                data.num_passed,
                data.num_failed,
                data.remaining_msgs,
                data.poll_rate,
                data.num_senders,
            )
            console.log("got the latest data")}
        )})
    }, props.pollRate * 1000)

    return <>
        <p>Failed: {alert.numFailed}</p>
        <p>Passed: {alert.numPassed}</p>
        <p>Remaining: {alert.remainingMsgs}</p>
        <p>Poll Rate: {alert.pollRate}</p>
        <p>Number Senders: {alert.numSenders}</p>
    </>
    


}
export default AlertMonitor