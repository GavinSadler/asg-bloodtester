
const toplevel = "http://127.0.0.1:5000"

export function dispense(amount: number) {
    fetch(toplevel + "/dispenseContinuous?amount=" + String(amount))
}

export function dispenseContinuous() {
    fetch(toplevel + "/dispenseContinuous")
}

export function retractContinuous() {
    fetch(toplevel + "/retractContinuous")
}

export function stop() {
    fetch(toplevel + "/stop")
}

export function setDispenseSpeed(speed: number) {
    fetch(toplevel + "/setDispenseSpeed?speed=" + String(speed))
}

// =====================
// Discovery Q endpoints
// =====================

export function getLastAcquisitionInformation(debug = false): Promise<{ id: string; sweep_mode: string; }> {
    return new Promise((ret, rej) => {
        fetch(`${toplevel}/php/LastAcquisitionID.php?debug=${debug}`)
            .then(res => {
                res.json()
                    .then(ret)
                    .catch(rej)
            })
            .catch(rej)
    })
}

export function getChannelData(id: number, timestamp_min: number, timestamp_nth: number, device: number, well: number, debug = false):
    Promise<[{ "timestamp": number, "frequency": number, "resistance": number, "phase": number }]> {
    return new Promise((ret, rej) => {
        fetch(`${toplevel}/php/ChannelData.php?id=${id}&timestamp_min=${timestamp_min}&timestamp_nth=${timestamp_nth}&device=${device}&well=${well}&debug=${debug}`)
            .then(res => {
                res.json()
                    .then(ret)
                    .catch(rej)
            })
            .catch(rej)
    })
}

export function getRecentTemperatureData(debug = false):
    Promise<[{ "timestamp": string, "device": string, "temperature": string }]> {
    return new Promise((ret, rej) => {
        fetch(`${toplevel}/php/mysql2json.php?database=View&table=temperature_recent&debug=${debug}`)
            .then(res => {
                res.json()
                    .then(ret)
                    .catch(rej)
            })
            .catch(rej)
    })
}
