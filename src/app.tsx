
import DataDisplay from "./components/DataDisplay";
import DirectControl from "./components/DirectController";
import Keypad from "./components/Keypad";
import SpeedController from "./components/SpeedController";


export function App() {
  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between"
      }}
    >
      <SpeedController />
      <div
        style={{
          height: "100%",
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
