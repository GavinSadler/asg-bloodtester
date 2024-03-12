
import { Link } from "react-router-dom";
import { NetworkStatus } from "../components/NetworkStatus";
import { getSettings, setSettings, } from "../endpoints";
import { settings } from "../settingsContext";
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
      {!settingsFetched ?
        <h2>Fetching settings</h2>
        :
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
            Motor calibration value (steps/mm):
            <input name="stepsPerMm" defaultValue={fetchedSettings.stepsPerMm.toString()} />
          </label>
          <label>
            Default flow rate (uL/min):
            <input name="defaultFlowRate" defaultValue={fetchedSettings.defaultFlowRate.toString()} />
          </label>
          <label>
            Direct control speed (cm/sec):
            <input name="directControlSpeed" defaultValue={fetchedSettings.directControlSpeed.toString()} />
          </label>
          <label>
            DiscoveryQ Hostname:
            <input name="discoveryqHostname" defaultValue={fetchedSettings.discoveryqHostname} />
          </label>
          <label>
            Color theme:
            <input name="discoveryqHostname" defaultValue={fetchedSettings.colorTheme} />
          </label>

          <input type="submit" value="Save settings" />
        </form>
      }
      <NetworkStatus />
      <Link to="/">Back</Link>
    </div>
  )
}
