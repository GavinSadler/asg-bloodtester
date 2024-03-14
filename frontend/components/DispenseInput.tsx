import { useContext, useRef } from "preact/hooks";
import { dispense, retract, setDispenseSpeed } from "../endpoints";
import { SettingsContext } from "../SettingsContext";

export default function DispenseInput() {
  const settings = useContext(SettingsContext);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateInput = () => {
    // Reset input to 0 if the input is invalid (negative numbers)
    if (inputRef.current!.valueAsNumber < 0) inputRef.current!.value = "0";
  };

  return (
    <label className="control-options">
      <h2>Dispense liquid (mL):</h2>
      <input
        ref={inputRef}
        type="number"
        defaultValue="1.0"
        onfocusout={validateInput}
        onKeyDown={(e) => {
          if (e.key === "Enter") validateInput();
        }}
      />
      <button
        onClick={() => {
          validateInput();
          setDispenseSpeed(settings.settings.directControlSpeed);
          dispense(inputRef.current!.valueAsNumber);
        }}
      >
        Dispense
      </button>
      <button
        onClick={() => {
          validateInput();
          setDispenseSpeed(settings.settings.directControlSpeed);
          retract(inputRef.current!.valueAsNumber);
        }}
      >
        Retract
      </button>
    </label>
  );
}
