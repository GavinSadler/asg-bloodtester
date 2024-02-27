import { render } from 'preact';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import './index.css';
import { App } from './pages/app.tsx';
import { DiscoveryQ } from './pages/discoveryq.tsx';
import { Settings } from './pages/settings.tsx';

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
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

render(<RouterProvider router={router} />, document.getElementById('app')!)
