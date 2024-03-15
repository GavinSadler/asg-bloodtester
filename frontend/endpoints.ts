import { iSettings } from './components/SettingsContext';

export const toplevel = `${window.location.protocol}//${window.location.hostname}:5000`;

export function networkinfo() {
    return fetch(`${toplevel}/networkinfo`).then((res) => res.json());
}

export function dispense(amount: number) {
    fetch(toplevel + '/dispense?amount=' + String(amount));
}

export function retract(amount: number) {
    fetch(toplevel + '/retract?amount=' + String(amount));
}

export function dispenseContinuous() {
    fetch(toplevel + '/dispenseContinuous');
}

export function retractContinuous() {
    fetch(toplevel + '/retractContinuous');
}
export function stop() {
    fetch(toplevel + '/stop');
}

export function setDispenseSpeed(speed: number) {
    return fetch(toplevel + '/setDispenseSpeed?speed=' + String(speed));
}

export function setCarriageSpeed(speed: number) {
    return fetch(`${toplevel}/setCarriageSpeed?speed=${String(speed)}`);
}

export function getSteps() {
    return fetch(`${toplevel}/getSteps`)
        .then((res) => res.text())
        .then((res) => Number(res));
}

export function getSettings() {
    return fetch(`${toplevel}/settings`)
        .then((res) => res.json())
        .then((res) => {
            return res as iSettings;
        });
}

export function setSettings(newSettings: iSettings) {
    const headers: Headers = new Headers();
    headers.set('Content-Type', 'application/json');
    headers.set('Accept', 'application/json');

    const request: RequestInfo = new Request(`${toplevel}/settings`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(newSettings),
    });

    return fetch(request)
        .then((res) => res.json())
        .then((res) => res as iSettings);
}

// =====================
// Discovery Q endpoints
// =====================

export function getLastAcquisitionInformation() {
    return fetch(`${toplevel}/discoveryqproxy/php/LastAcquisitionID.php`)
        .then((res) => res.json())
        .then((res) => {
            return res as { id: string; sweep_mode: string };
        });
}

export function getChannelData(id: number, timestamp_min: number, timestamp_nth: number, device: number, well: number) {
    return fetch(
        `${toplevel}/discoveryqproxy/php/ChannelData.php?id=${id}&timestamp_min=${timestamp_min}&timestamp_nth=${timestamp_nth}&device=${device}&well=${well}`,
    )
        .then((res) => res.json())
        .then((res) => {
            return res as [
                {
                    timestamp: number;
                    frequency: number;
                    resistance: number;
                    phase: number;
                },
            ];
        });
}

export function getRecentTemperatureData() {
    return fetch(`${toplevel}/discoveryqproxy/php/mysql2json.php?database=View&table=temperature_recent`)
        .then((res) => res.json())
        .then((res) => {
            return res as [{ timestamp: string; device: string; temperature: string }];
        });
}
