import { FunctionalComponent, createContext } from 'preact';
import { useContext, useEffect, useState } from 'preact/hooks';
import { getSettings } from '../endpoints';

export interface iSettings {
    syringeDiameter: number;
    stepsPerMm: number;
    showSteps: boolean;
    defaultFlowRate: number;
    directControlSpeed: number;
    discoveryqHostname: string;
}

interface SettingsContextType {
    settings: iSettings;
    updateSettings: (updatedSettings: iSettings) => void;
}

const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

export const SettingsProvider: FunctionalComponent = ({ children }) => {
    const [settings, setSettings] = useState({} as iSettings);
    const [settingsLoaded, setSettingsLoaded] = useState(false);

    useEffect(() => {
        getSettings().then((set) => {
            setSettings(set);
            setSettingsLoaded(true);
        });
    }, []);

    if (!settingsLoaded) return <h2>One moment...</h2>;

    const updateSettings = (newSettings: iSettings) => {
        console.log('Settings state updated');
        setSettings(newSettings);
    };

    return <SettingsContext.Provider value={{ settings, updateSettings }}>{children}</SettingsContext.Provider>;
};

export const useSettings = () => {
    const settingsContext = useContext(SettingsContext);

    if (!settingsContext) throw new Error('Settings must be used within SettingsProvider');

    return settingsContext;
};
