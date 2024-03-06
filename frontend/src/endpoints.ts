
export const toplevel = `${window.location.protocol}//${window.location.hostname}/endpoints`

export interface settings {
    syringeDiameter: number;
    maxFlowRate: number;
    defaultFlowRate: number;
    discoveryqHostname: string;
    networkMode: string;
}

export function networkinfo(): Promise<string> {
    return new Promise((ret, rej) => {
        fetch(`${toplevel}/networkinfo`)
            .then(res => {
                res.text()
                    .then(ret)
                    .catch(rej)
            })
            .catch(rej)
    })
}

export function dispense(amount: number) {
    fetch(toplevel + "/dispense?amount=" + String(amount))
}

export function retract(amount: number) {
    fetch(toplevel + "/retract?amount=" + String(amount))
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
    return fetch(toplevel + "/setDispenseSpeed?speed=" + String(speed))
}

export function getSteps(): Promise<{ steps: number; }> {
    return new Promise((ret, rej) => {
        fetch(`${toplevel}/getSteps`)
            .then(res => {
                res.json()
                    .then(ret)
                    .catch(rej)
            })
            .catch(rej)
    })
}

export function getSettings() {
    return fetch(`${toplevel}/settings`)
        .then(res => res.json())
        .then(res => {
            return res as settings
        })
}

export function setSettings(newSettings: settings) {
    const headers: Headers = new Headers()
    headers.set('Content-Type', 'application/json')
    headers.set('Accept', 'application/json')

    const request: RequestInfo = new Request(`${toplevel}/settings`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(newSettings)
    })

    return fetch(request)
        .then(res => res.json())
        .then(res => res as settings)
}

// =====================
// Discovery Q endpoints
// =====================

export function getLastAcquisitionInformation() {
    return fetch(`${toplevel}/discoveryqproxy/php/LastAcquisitionID.php`)
        .then(res => res.json())
        .then(res => {
            return res as { id: string; sweep_mode: string; }
        })
}

export function getChannelData(id: number, timestamp_min: number, timestamp_nth: number, device: number, well: number) {
    return fetch(`${toplevel}/discoveryqproxy/php/ChannelData.php?id=${id}&timestamp_min=${timestamp_min}&timestamp_nth=${timestamp_nth}&device=${device}&well=${well}`)
        .then(res => res.json())
        .then(res => {
            return res as [{ "timestamp": number, "frequency": number, "resistance": number, "phase": number }]
        })
}

export function getRecentTemperatureData() {
    return fetch(`${toplevel}/discoveryqproxy/php/mysql2json.php?database=View&table=temperature_recent`)
        .then(res => res.json())
        .then(res => {
            return res as [{ "timestamp": string, "device": string, "temperature": string }]
        })
}
