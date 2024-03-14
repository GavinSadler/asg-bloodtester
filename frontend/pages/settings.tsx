
import { Link } from "react-router-dom";
import { NetworkStatus } from "../components/NetworkStatus";
import { setSettings } from "../endpoints";
import { iSettings, useSettings } from "../SettingsContext";

export const Settings = () => {

  const settingsContext = useSettings();

  const handleSubmit = (e: SubmitEvent) => {
    // Prevent the browser from reloading the page
    e.preventDefault();

    // Read the form data
    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);

    // Or you can work with it as a plain object:
    const formJson = Object.fromEntries(formData.entries());

    setSettings(formJson as unknown as iSettings)
      .then(settingsContext.updateSettings)
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      <p>Settings page</p>
      <form method="post" onSubmit={handleSubmit}
        style={{
          display: "flex",
          flexDirection: "column"
        }}
      >
        <label>
          Syringe diameter (mm):
          <input name="syringeDiameter" defaultValue={settingsContext.settings.syringeDiameter.toString()} />
        </label>
        <label>
          Motor calibration value (steps/mm):
          <input name="stepsPerMm" defaultValue={settingsContext.settings.stepsPerMm.toString()} />
        </label>
        <label>
          Default flow rate (uL/min):
          <input name="defaultFlowRate" defaultValue={settingsContext.settings.defaultFlowRate.toString()} />
        </label>
        <label>
          Direct control speed (cm/sec):
          <input name="directControlSpeed" defaultValue={settingsContext.settings.directControlSpeed.toString()} />
        </label>
        <label>
          DiscoveryQ Hostname:
          <input name="discoveryqHostname" defaultValue={settingsContext.settings.discoveryqHostname} />
        </label>
        <label>
          Color theme:
          <input name="discoveryqHostname" defaultValue={settingsContext.settings.colorTheme} />
        </label>

        <input type="submit" value="Save settings" />
      </form>

      <NetworkStatus />
      <Link to="/">Back</Link>
    </div>
  )
}
