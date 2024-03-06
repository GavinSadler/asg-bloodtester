import { Link } from "react-router-dom";
import { toplevel } from "../endpoints";

export function DiscoveryQ() {

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%"
      }}
    >
      <iframe src={`${toplevel}/discoveryq`} style={{ height: "100%" }}></iframe>
      <Link to="/">Back</Link>
    </div>
  )
}
