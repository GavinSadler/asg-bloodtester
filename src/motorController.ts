
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
