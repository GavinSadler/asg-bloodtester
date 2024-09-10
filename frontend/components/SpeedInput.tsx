import { Dispatch, StateUpdater, useRef } from 'preact/hooks';
import { FunctionalComponent } from 'preact';
import { setDispenseSpeed } from '../endpoints';

interface SpeedInputProps {
    dispenseSpeed: number;
    setDispenseSpeed: Dispatch<StateUpdater<number>>;
}

const SpeedInput: FunctionalComponent<SpeedInputProps> = (props) => {
    const inputRef = useRef<HTMLInputElement>(null);

    const updateSpeed = () => {
        if (!inputRef.current) return;

        // Reset input to 0 if the input is invalid (negative numbers)
        if (inputRef.current.valueAsNumber < 0) inputRef.current.value = '0';

        props.setDispenseSpeed(inputRef.current.valueAsNumber);
        setDispenseSpeed(inputRef.current.valueAsNumber);
    };

    return (
        <label className="control-options">
            <h2>Speed (µL/min):</h2>
            <input
                ref={inputRef}
                type="number"
                defaultValue={props.dispenseSpeed.toString()}
                // eslint-disable-next-line react/no-unknown-property
                onFocusOut={updateSpeed}
                onKeyDown={(e) => {
                    if (e.key === 'Enter') updateSpeed();
                }}
            />
            <button onClick={updateSpeed}>Set speed</button>
        </label>
    );
};

export default SpeedInput;
