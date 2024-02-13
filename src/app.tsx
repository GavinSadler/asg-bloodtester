
import DataDisplay from "./components/DataDisplay";
import DirectControl from "./components/DirectController";
import Keypad from "./components/Keypad";
import SpeedController from "./components/SpeedController";


export function App() {
  return (
    <div
      className={"main-container"}
    >
      <SpeedController />
      <div
        style={{
          height: "400px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-around",
          
        }}
      >
        <Keypad />
        <DirectControl />
      </div>
      <DataDisplay />
    </div>
  )
}
