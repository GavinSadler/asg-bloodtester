import { Link } from "react-router-dom";
import { getSteps } from "../endpoints";
import { useEffect, useState } from "preact/hooks";
import SpeedController from "../components/SpeedController";
import DirectControl from "../components/DirectController";

export function Calibrate() {

  const [steps, setSteps] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      getSteps().then((value) => {
        setSteps(value.steps)
      })
    }, 1000 * 0.5);

    return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
  }, [])

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row"
      }}
    >
      <p>Calibrate Device</p>
      <p>{steps}</p>
      <div
        style={{
          display: "flex",
          flexDirection: "column"
        }}
      >
        <SpeedController />
        <DirectControl />
      </div>
      <form
      style={{
        display: "flex",
        flexDirection: "column"
      }}
      >
        <label>
          Initial fluid (mL):
          <input />
        </label>
        <label>
          Final fluid (mL):
          <input />
        </label>
        <label>
          Initial steps:
          <input />
        </label>
        <label>
          Final steps:
          <input />
        </label>
        <button>Calibrate</button>
      </form>
      <Link to="/">Back</Link>
    </div>
  )
}
