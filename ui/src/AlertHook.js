import { useMemo, useState } from "react";

export function useAlert() {
    const [numPassed, setNumPassed] = useState(0)
    const [numFailed, setNumFailed] = useState(0)
    const [remainingMsgs, setRemainingMsgs] = useState(0)
    const [pollRate, setPollRate] = useState(0)
    const [numSenders, setNumSenders] = useState(0)

    return useMemo(
        () => ({
            numPassed,
            numFailed,
            remainingMsgs,
            pollRate,
            numSenders,
            setAlert : (
                newNumPassed,
                newNumFailed,
                newRemainingMsgs,
                newPollRate,
                newNumSenders
            ) => {
                setNumPassed(newNumPassed);
                setNumFailed(newNumFailed);
                setRemainingMsgs(newRemainingMsgs);
                setPollRate(newPollRate);
                setNumSenders(newNumSenders);
            }
        }), [numPassed,
            numFailed,
            remainingMsgs,
            pollRate,
            numSenders]
    )


}