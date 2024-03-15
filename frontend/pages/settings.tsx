import { Link, useNavigate } from 'react-router-dom';
import { NetworkStatus } from '../components/NetworkStatus';
import { setSettings } from '../endpoints';
import { iSettings, useSettings } from '../components/SettingsContext';
import { useRef } from 'preact/hooks';

export const Settings = () => {
    const settingsContext = useSettings();
    const navigate = useNavigate();
    const formRef = useRef<HTMLFormElement>(null);

    const handleSubmit = () => {
        if (!formRef.current) return;

        const formData = new FormData(formRef.current);
        const formJson = Object.fromEntries(formData.entries());

        setSettings(formJson as unknown as iSettings).then(settingsContext.updateSettings);
    };

    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            <form
                method="post"
                onSubmit={(e) => {
                    e.preventDefault();
                }}
                className="settings-form"
                style={{
                    display: 'flex',
                    flexDirection: 'column',
                }}
                ref={formRef}
            >
                <label>
                    Syringe diameter (mm):
                    <input
                        name="syringeDiameter"
                        min="0.01"
                        step="0.0000001"
                        type="number"
                        defaultValue={settingsContext.settings.syringeDiameter.toString()}
                    />
                </label>
                <label>
                    Motor calibration value (steps/mm):
                    <input name="stepsPerMm" type="number" min="0.001" step="0.0000001" defaultValue={settingsContext.settings.stepsPerMm.toString()} />
                </label>
                <label>
                    Default flow rate (uL/min):
                    <input
                        name="defaultFlowRate"
                        type="number"
                        min="0.01"
                        step="0.0000001"
                        defaultValue={settingsContext.settings.defaultFlowRate.toString()}
                    />
                </label>
                <label>
                    Direct control speed (cm/sec):
                    <input
                        name="directControlSpeed"
                        type="number"
                        min="0.01"
                        step="0.0000001"
                        defaultValue={settingsContext.settings.directControlSpeed.toString()}
                    />
                </label>
                <label>
                    DiscoveryQ Hostname:
                    <input name="discoveryqHostname" defaultValue={settingsContext.settings.discoveryqHostname} />
                </label>
                <label>
                    Show stepper motor steps:
                    <input
                        name="showSteps"
                        type="checkbox"
                        checked={settingsContext.settings.showSteps}
                        style={{
                            width: '25px',
                            height: '25px',
                        }}
                    />
                </label>

                <div>
                    <button
                        onClick={() => {
                            handleSubmit();
                        }}
                    >
                        Save settings
                    </button>
                    <button onClick={() => navigate('/')}>Back</button>
                </div>
            </form>

            <NetworkStatus />
            <Link to="/">Back</Link>
        </div>
    );
};
