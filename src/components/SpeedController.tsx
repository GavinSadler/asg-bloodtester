
import { useState } from 'preact/hooks';
import { Range, Direction, getTrackBackground } from 'react-range';
import { setDispenseSpeed } from '../motorController';

const STEP = 0.1;
const MIN = 0.1;
const MAX = 20.0;
const DEFAULT = 1.0

const HEIGHT = "450px";
const WIDTH = "36px";

let createMarkers = () => {
    let elements = [];

    for (let i = 0; i <= MAX; i += 2)
        elements.push(
            <h5
                style={{
                    height:"20px",
                    margin:"0px"
                }}
            >
                {i + ".0"}
            </h5>
        );

    return elements.reverse();
}

export default function SpeedController() {

    const [values, setValues] = useState([DEFAULT]);

    return (
        <div
            style={{
                display: "flex",
                alignItems: "center",
                height: HEIGHT
            }}
        >
            <h2
                style={{
                    transform: "rotate(180deg)",
                    writingMode: "vertical-lr"
                }}
            >
                Speed (mL/min)
            </h2>
            <Range
                direction={Direction.Up}
                values={values}
                step={STEP}
                min={MIN}
                max={MAX}
                onChange={(values) => { setValues(values); setDispenseSpeed(values[0]) }}
                renderTrack={({ props, children }) => (
                    <div
                        onMouseDown={props.onMouseDown}
                        onTouchStart={props.onTouchStart}
                        style={{
                            ...props.style,
                            marginLeft: "48px",
                            flexGrow: 1,
                            width: WIDTH,
                            display: 'flex',
                            height: HEIGHT,
                            left: "50px"
                        }}
                    >
                        <div
                            ref={props.ref}
                            style={{
                                width: WIDTH,
                                height: '100%',
                                borderRadius: '3px',
                                background: getTrackBackground({
                                    values: values,
                                    colors: ['#548BF4', '#ccc'],
                                    min: MIN,
                                    max: MAX,
                                    direction: Direction.Up,
                                }),
                                alignSelf: 'center'
                            }}
                        >
                            {children}
                        </div>
                    </div>
                )}
                renderThumb={({ props }) => (
                    <div
                        {...props}
                        role={undefined} // It complains unless I put this here ):
                        style={{
                            ...props.style,
                            display: "flex",
                            alignItems: "center",
                            left: "-24px"
                        }}
                    >
                        <h4
                            style={{
                                width: "30px",
                                paddingRight: "8px"
                            }}
                        >
                            {values}
                        </h4>
                        <div
                            style={{
                                height: '21px',
                                width: '48px',
                                borderRadius: '1px',
                                backgroundColor: '#FFF',
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                boxShadow: '0 0 12px #AAA'
                            }}
                        >
                        </div>
                    </div>
                )}
            />
            <div
                style={{
                    marginLeft: "5px",
                    display: "flex",
                    flexDirection: "column",
                    height: "100%",
                    justifyContent: "space-between"
                }}
            >
                {createMarkers()}
            </div>
        </div>
    );
};
