import { useState } from "react"


function StartButton(props) {
    const [disabled, setDisabled] = useState(false)
    return <button disabled={disabled} onClick = {() => {
        setDisabled(true)
        fetch('/api/v1/execute', {
            body: JSON.stringify({'id': props.alertId}),
            headers: {'content-type': 'application/json'},
            method: 'POST',
        }).then((rsp) => {setDisabled(false)})
    }}> SEND IT! </button>
}

export default StartButton
  