import {useEffect, useState} from 'react';
import {getAllSidewalks} from '../api/sidewalks.api.js'
import {SidewalkTable} from "../components/sidewalks/SidewalkTable";

export function SidewalkList() {

    const [sidewalks, setSidewalks] = useState([]);

    useEffect(() => {
        async function loadSidewalks() {
            await getAllSidewalks().then((response) => {
                setSidewalks(response.data);
            });
        }

        loadSidewalks();
    }, []);
    return (
        <div>
            <h1>Sidewalks</h1>
            <ul>
                {sidewalks.map((sidewalk) => (
                    <SidewalkTable key={sidewalk.id} sidewalk={sidewalk} />
                ))}
            </ul>
        </div>
    )
}
