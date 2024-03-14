
import { dispenseContinuous, retractContinuous, setCarriageSpeed, stop } from "../endpoints"
import StepCounter from "./StepCounter";
import { useSettings } from "../SettingsContext";

export default function DirectControl() {

    const settings = useSettings()

    return (
        <div className="control-options">
            <h2>Direct Control</h2>
            <div>
                <button
                    onTouchStart={(e) => { e.preventDefault(); setCarriageSpeed(settings.settings.directControlSpeed); retractContinuous() }}
                    onTouchEnd={(e) => { e.preventDefault(); stop() }}
                    onMouseDown={(e) => { e.preventDefault(); setCarriageSpeed(settings.settings.directControlSpeed); retractContinuous() }}
                    onMouseUp={(e) => { e.preventDefault(); stop() }}
                >
                    ◀
                </button>
                <button
                    onTouchStart={(e) => { e.preventDefault(); stop() }}
                    onMouseDown={(e) => { e.preventDefault(); stop() }}
                >
                    Stop
                </button>
                <button
                    onTouchStart={(e) => { e.preventDefault(); setCarriageSpeed(settings.settings.directControlSpeed); dispenseContinuous() }}
                    onTouchEnd={(e) => { e.preventDefault(); stop() }}
                    onMouseDown={(e) => { e.preventDefault(); setCarriageSpeed(settings.settings.directControlSpeed); dispenseContinuous() }}
                    onMouseUp={(e) => { e.preventDefault(); stop() }}
                >
                    ▶
                </button>
            </div>
            {settings.settings.showSteps ? <StepCounter /> : null}
        </div>
    )

}
