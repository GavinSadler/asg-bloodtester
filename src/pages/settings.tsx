
import { Link } from "react-router-dom";
import { NetworkStatus } from "../components/NetworkStatus";

export function Settings() {

  const handleSubmit = (e: SubmitEvent) => {
    // Prevent the browser from reloading the page
    e.preventDefault();

    // Read the form data
    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);

    // You can pass formData as a fetch body directly:
    fetch('/some-api', { method: form.method, body: formData });

    // Or you can work with it as a plain object:
    const formJson = Object.fromEntries(formData.entries());
    console.log(formJson);
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      <p>Settings page</p>
      <Link to="/">Back</Link>
      <form method="post" onSubmit={handleSubmit}>

      </form>
      <label>
        DiscoveryQ Hostname:
        <input defaultValue="imvx-discovery3.local"/>
      </label>
      
      <button>Save settings</button>
      <NetworkStatus />
    </div>
  )
}
