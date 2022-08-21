import { useState } from "react"


function StartButton(props) {
    const [disabled, setDisabled] = useState(false)
    return <button disabled={disabled || !props.alertLoaded} onClick = {() => {
        setDisabled(true)
        fetch('/api/v1/execute', {
            body: JSON.stringify({'id': props.alertId}),
            headers: {'content-type': 'application/json'},
            method: 'POST',
        }).then((rsp) => {
            setDisabled(false);
            props.setStartTime(new Date()/ 1000);
        })
    }}> SEND IT! </button>
}

export default StartButton
  