
import { useEffect, useState } from 'preact/hooks';
import Plot from 'react-plotly.js';
import { getLastAcquisitionInformation, getChannelData, getRecentTemperatureData } from "../endpoints.ts";

export default function DataDisplay() {

    let [graphData, setGraphData] = useState({ timestamp: [] as number[], frequency: [] as number[], phase: [] as number[], resistance: [] as number[] })
    let [temperatureData, setTemperatureData] = useState({ timestamp: [] as number[], temperature: [] as number[] })

    useEffect(() => {
        getLastAcquisitionInformation(true)
            .then(acquisitionInfo => {
                getChannelData(Number(acquisitionInfo.id), 0, 1, 0, 0, true)
                    .then(data => {

                        let timestamp: number[] = [];
                        let frequency: number[] = [];
                        let phase: number[] = [];
                        let resistance: number[] = [];

                        data.forEach(point => {
                            timestamp.push(point.timestamp)
                            frequency.push(point.frequency)
                            phase.push(point.phase)
                            resistance.push(point.resistance)
                        })

                        setGraphData({ timestamp, frequency, phase, resistance })
                    })
            })

        getRecentTemperatureData(true)
            .then(temperatureData => {

                let timestamp: number[] = [];
                let temperature: number[] = [];

                temperatureData.forEach(point => {
                    timestamp.push(Number(point.timestamp))
                    temperature.push(Number(point.temperature))
                })

                setTemperatureData({temperature, timestamp})
            })
    }, [])

    return (
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                backgroundColor: "#cccccc",
                borderRadius: "10px",
                // width: WIDTH + "px",
                // height: HEIGHT + "px"
            }}
        >
            <Plot
                data={[
                    {
                        y: graphData.resistance,
                        x: graphData.timestamp,
                        xaxis: 'x1',
                        yaxis: 'y1',
                        mode: 'markers',
                        type: 'scatter'
                    },
                    {
                        y: graphData.frequency,
                        x: graphData.timestamp,
                        xaxis: 'x2',
                        yaxis: 'y2',
                        mode: 'markers',
                        type: 'scatter'
                    },
                    {
                        y: graphData.phase,
                        x: graphData.timestamp,
                        xaxis: 'x3',
                        yaxis: 'y3',
                        mode: 'markers',
                        type: 'scatter'
                    },
                    {
                        y: temperatureData.temperature,
                        x: temperatureData.timestamp,
                        xaxis: 'x4',
                        yaxis: 'y4',
                        mode: 'markers',
                        type: 'scatter'
                    }
                ]}
                layout={{
                    title: 'Discovery-Q Data',
                    height: 600,
                    showlegend: false,
                    grid: {
                        rows: 4,
                        columns: 1,
                        pattern: 'independent'
                    },
                    yaxis: {title: 'Resistance'},
                    yaxis2: {title: 'Frequency'},
                    yaxis3: {title: 'Phase'},
                    yaxis4: {title: 'Temperature'},
                    xaxis4: {title: 'Time'}
                }}
                config={{
                    responsive: true
                }}
            />
        </div>
    )
}
