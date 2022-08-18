import { useAlert } from './AlertHook';

function AlertMonitor (props) {
    const alert = useAlert({})
    if (!props.alertId || !props.pollRate){
        return
    }
    setTimeout( () => {
        fetch(`/api/v1/alerts?id=${props.alertId}`).then((response) => {response.json().then(
            (data) => {alert.setAlert(
                data.num_passed,
                data.num_failed,
                data.remaining_msgs,
                data.poll_rate,
                data.num_senders,
            )}
        )})
    }, alert.pollRate * 1000)
    


}
export default AlertMonitor