import {useEffect, useState} from "react";
import {getAllOrganizations} from '../../api/organizations.api';
import AsyncSelect from 'react-select/async'
import Select from "react-select";

export function SelectOrganizations() {

    const [organizations, setOrganizations] = useState([])


    useEffect(() => {
        async function loadOrganizations() {
            await getAllOrganizations().then((response) => {
                const datos = response.data
                setOrganizations(datos)
            })
        }

        loadOrganizations()
    }, []);

    // Obtener las opciones del Select
    const data = organizations.map((item) => ({
        value: item.id,
        label: item.organization_name
    }))

    const


    return (
        <Select options={data}/>
    )
}