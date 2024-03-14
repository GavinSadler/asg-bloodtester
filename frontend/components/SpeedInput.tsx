
import { useEffect, useRef } from "preact/hooks";
import { setDispenseSpeed } from "../endpoints";
import {  useSettings } from "../SettingsContext";

export default function SpeedInput() {

  const settings = useSettings()
  const inputRef = useRef<HTMLInputElement>(null)

  const updateSpeed = () => {
    // Reset input to 0 if the input is invalid (negative numbers)
    if (inputRef.current!.valueAsNumber < 0)
      inputRef.current!.value = "0";
    
    setDispenseSpeed(inputRef.current!.valueAsNumber)
  }

  // This sends our default speed to the backend when the page is loaded
  useEffect(updateSpeed, [])

  return (
    <label className="control-options">
      <h2>Speed (µL/min):</h2>
      <input
        ref={inputRef}
        type="number"
        defaultValue={settings.settings.defaultFlowRate.toString()}
        onfocusout={updateSpeed}
        onKeyDown={(e) => {if (e.key === 'Enter') updateSpeed()}}
      />
      <button onClick={updateSpeed}>Set speed</button>
    </label>
  );
};
