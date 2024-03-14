import { useEffect, useState } from "preact/hooks";
import { getSteps } from "../endpoints";

export default function StepCounter() {
  console.log("Rendered");

  const [steps, setSteps] = useState(0);

  useEffect(() => {
    const interval = setInterval(
      () => {
        getSteps().then(setSteps);
      },
      1000 / 10, // Run every 10th of a second
    );

    // Clean up timer so we don't leak memory
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
      }}
    >
      <h2>Steps:</h2>
      <h2>{steps}</h2>
    </div>
  );
}
