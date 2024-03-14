import { useState } from "preact/hooks";
import { dispense, retract } from "../endpoints";

const keySymbols = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0", ".", "C"];

let createButtons = (onClickCallback: (value: string) => void) => {
  let elements = [];

  for (const k of keySymbols) {
    elements.push(<button onClick={() => onClickCallback(k)}>{k}</button>);
  }
  return elements;
};

export default function Keypad() {
  let [value, setValue] = useState("1.0");

  let handleKey = (key: string) => {
    if (key == "C") setValue("");
    else if (key == "." && value.indexOf(".") == -1)
      if (value == "") setValue("0.");
      else setValue(value + key);
    else if (key != ".") setValue(value + key);
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        flexDirection: "column",
        justifyContent: "space-between",
        height: "300px",
      }}
    >
      <h4>{value} mL</h4>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr",
          gap: "10px",
        }}
      >
        {createButtons(handleKey)}
      </div>
      <button onClick={() => dispense(Number(value))}>Dispense</button>
      <button onClick={() => retract(Number(value))}>Retract</button>
    </div>
  );
}
