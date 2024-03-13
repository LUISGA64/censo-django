import {useEffect, useState} from "react";
import {getAllOrganizations} from '../../api/organizations.api';
import Select from "react-select";
import {Controller} from "react-hook-form";

export function SelectOrganizations({control, name}) {

    const [organizations, setOrganizations] = useState([]);

    useEffect(() => {
        async function loadOrganizations() {
            await getAllOrganizations().then((response) => {
                const datos = response.data;
                setOrganizations(datos);
            });
        }
        loadOrganizations();
    }, []);

    // Obtener las opciones del Select
    const data = organizations.map((item) => ({
        value: item.id,
        label: item.organization_name,
    }));

    return (
        <Controller
            name={"organization_id"} // nombre del campo en el formulario
            control={control}
            render={({field}) => (
                <Select
                    {...field}
                    options={data}
                    onChange={(selectedOption) => field.onChange(selectedOption)}
                />
            )}
        />
    );
}