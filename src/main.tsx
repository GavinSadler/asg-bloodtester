import { render } from 'preact';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import './index.css';
import { App } from './pages/app.tsx';
import { Calibrate } from './pages/calibrate.tsx';
import { Settings } from './pages/settings.tsx';

const router = createBrowserRouter([
    {
        path: "/",
        element: <App/>,
    },
    {
        path: "/calibrate/",
        element: <Calibrate />
    },
    {
        path: "/settings/",
        element: <Settings />
    }

]);


render(<RouterProvider router={router} />, document.getElementById('app')!)
