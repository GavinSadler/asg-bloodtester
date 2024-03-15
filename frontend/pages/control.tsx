import { Link } from 'react-router-dom';
import DirectControl from '../components/DirectController';
import DispenseController from '../components/DispenseController';
import SpeedInput from '../components/SpeedInput';
import { useSettings } from '../components/SettingsContext';
import { useState } from 'preact/hooks';

export function Control() {
    const settingsContext = useSettings();
    const [dispenseSpeed, setDispenseSpeed] = useState(settingsContext.settings.defaultFlowRate);

    return (
        <div
            className={'main-container'}
            style={{
                display: 'flex',
                flexDirection: 'column',
                // flexWrap: "wrap",
                alignItems: 'center',
                justifyContent: 'space-evenly',
            }}
        >
            <div
                style={{
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'row',
                    flexWrap: 'wrap',
                    alignItems: 'center',
                    justifyContent: 'space-evenly',
                }}
            >
                <SpeedInput dispenseSpeed={dispenseSpeed} setDispenseSpeed={setDispenseSpeed} />
                <DispenseController dispenseSpeed={dispenseSpeed} />
                <DirectControl />
            </div>
            <div
                className="links"
                style={{
                    display: 'flex',
                    flexDirection: 'row',
                    flexWrap: 'wrap',
                    justifyContent: 'center',
                }}
            >
                <Link to="/settings/">Settings</Link>
                <Link to="/discoveryq/">Discovery Q Homepage</Link>
            </div>
        </div>
    );
}
