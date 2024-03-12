
import { Link } from "react-router-dom";
import DirectControl from "../components/DirectController";
import DispenseInput from "../components/DispenseInput";
import SpeedInput from "../components/SpeedInput";

export function App() {
  return (
    <div
      className={"main-container"}
      style={{
        display: "flex",
        flexDirection: "column",
        // flexWrap: "wrap",
        alignItems: "center",
        justifyContent: "space-evenly"
      }}
    >
      <div style={{
        width: "100%",
        display: "flex",
        flexDirection: "row",
        flexWrap: "wrap",
        alignItems: "center",
        justifyContent: "space-evenly"
      }}>
        <SpeedInput />
        <DispenseInput />
        <DirectControl />
      </div>
      <div
        className="links"
        style={{
          display: "flex",
          flexDirection: "row",
          flexWrap: "wrap",
          justifyContent: "center"
      }}>
        <Link to="/settings/">Settings</Link>
        <Link to="/discoveryq/">Discovery Q Homepage</Link>
      </div>
    </div>
  )
}
