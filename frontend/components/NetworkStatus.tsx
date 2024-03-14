import { useEffect, useState } from "preact/hooks";
import { networkinfo } from "../endpoints";

export function NetworkStatus() {
  useEffect(() => {
    networkinfo()
      .then(setNetworkString)
      .catch((reason) => {
        setNetworkString(`Unable to grab network information: ${reason}`);
      });
  }, []);

  const [networkString, setNetworkString] = useState("");

  return (
    <div>
      <p
        style={{
          whiteSpace: "pre-line",
          backgroundColor: "black",
          color: "white",
          fontFamily: "Courier New, monospaced,",
          fontSize: 11,
        }}
      >
        {networkString === "" ? "Grabbing network information" : networkString}
      </p>
    </div>
  );
}
