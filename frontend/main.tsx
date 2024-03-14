import { render } from 'preact';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import './index.css';
import { Control } from './pages/control.tsx';
import { DiscoveryQ } from './pages/discoveryq.tsx';
import { Settings } from './pages/settings.tsx';
import { SettingsProvider } from './SettingsContext.tsx';

const router = createBrowserRouter([
    {
        path: "/",
        element: <Control />,
    },
    {
        path: "/settings/",
        element: <Settings />
    },
    {
        path: "/discoveryq/",
        element: <DiscoveryQ />
    }
]);

render(
    <SettingsProvider>
        <RouterProvider router={router} />
    </SettingsProvider>
    , document.getElementById('app')!
)
