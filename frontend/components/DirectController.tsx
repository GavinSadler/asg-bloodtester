import { dispenseContinuous, retractContinuous, stop } from "../endpoints"

export default function DirectControl() {

    return (
        <div>
            <button
                onMouseDown={retractContinuous}
                onMouseUp={retractContinuous}
            >
                ◀
            </button>
            <button
                onClick={stop}
            >
                Stop
            </button>
            <button
                onMouseDown={dispenseContinuous}
                onMouseUp={dispenseContinuous}
            >
                ▶
            </button>
        </div>
    )

}
