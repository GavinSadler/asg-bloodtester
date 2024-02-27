
import { Link } from "react-router-dom";
import { NetworkStatus } from "../components/NetworkStatus";
import { getSettings, setSettings, settings, } from "../endpoints";
import { useEffect, useState } from "preact/hooks";

export function Settings() {

  const [fetchedSettings, setFetchedSettings] = useState({} as settings)
  const [settingsFetched, setSettingsFetched] = useState(false)

  useEffect(() => {
    getSettings().then((grabbedSettings) => {
      setFetchedSettings(grabbedSettings)
      setSettingsFetched(true)
    })
  }, [])

  const handleSubmit = (e: SubmitEvent) => {
    // Prevent the browser from reloading the page
    e.preventDefault();

    // Read the form data
    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);

    // Or you can work with it as a plain object:
    const formJson = Object.fromEntries(formData.entries());

    setSettings(formJson as unknown as settings)
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      <p>Settings page</p>
      {settingsFetched ?
        <form method="post" onSubmit={handleSubmit}
        style={{
          display: "flex",
          flexDirection: "column"
        }}
        >
          <label>
            Syringe diameter (mm):
            <input name="syringeDiameter" defaultValue={fetchedSettings.syringeDiameter.toString()} />
          </label>
          <label>
            Default flow rate (uL/min):
            <input name="defaultFlowRate" defaultValue={fetchedSettings.defaultFlowRate.toString()} />
          </label>
          <label>
            Syringe max flow rate (uL/min):
            <input name="maxFlowRate" defaultValue={fetchedSettings.maxFlowRate.toString()} />
          </label>
          <label>
            DiscoveryQ Hostname:
            <input name="discoveryqHostname" defaultValue={fetchedSettings.discoveryqHostname} />
          </label>
          <label>
            Wifi Mode:
            <select name="wifiMode" defaultValue={fetchedSettings.networkMode}>
              <option value="Eduroam">Eduroam</option>
              <option value="Access Point">Access Point</option>
            </select>
          </label>

          <input type="submit" value="Save settings" />
        </form>
        :
        <p>Fetching settings</p>
      }
      <NetworkStatus />
      <Link to="/">Back</Link>
    </div>
  )
}
