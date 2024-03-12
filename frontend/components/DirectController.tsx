
import { dispenseContinuous, retractContinuous, stop } from "../endpoints"
import StepCounter from "./StepCounter";

export default function DirectControl({showSteps = false}) {
    return (
        <div className="control-options">
            <h2>Direct Control</h2>
            <div>
                <button
                    onTouchStart={(e) => { e.preventDefault(); retractContinuous() }}
                    onTouchEnd={(e) => { e.preventDefault(); stop() }}
                    onMouseDown={(e) => { e.preventDefault(); retractContinuous() }}
                    onMouseUp={(e) => { e.preventDefault(); stop() }}
                >
                    ◀
                </button>
                <button
                    onTouchStart={(e) => {e.preventDefault(); stop()}}
                    onMouseDown={(e) => {e.preventDefault(); stop()}}
                >
                    Stop
                </button>
                <button
                    onTouchStart={(e) => { e.preventDefault(); dispenseContinuous() }}
                    onTouchEnd={(e) => { e.preventDefault(); stop() }}
                    onMouseDown={(e) => { e.preventDefault(); dispenseContinuous() }}
                    onMouseUp={(e) => { e.preventDefault(); stop() }}
                >
                    ▶
                </button>
            </div>
            {showSteps ? <StepCounter /> : null}
        </div>
    )

}
