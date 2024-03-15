import { useEffect, useState } from 'preact/hooks';
import { networkinfo } from '../endpoints';

export function NetworkStatus() {
    const [netInfo, setNetInfo] = useState();

    useEffect(() => {
        networkinfo().then(setNetInfo);
    }, []);

    return (
        <div>
            <p
                style={{
                    whiteSpace: 'pre-line',
                    backgroundColor: 'black',
                    color: 'white',
                    fontFamily: 'Courier New, monospaced,',
                    fontSize: 22,
                }}
            >
                {JSON.stringify(netInfo)}
            </p>
        </div>
    );
}
