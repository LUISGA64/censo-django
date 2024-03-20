import {Controller, useForm} from 'react-hook-form';
import {useEffect, useState} from 'react';
import {SelectOrganizations} from '../../components/organizations/SelectOrganizations.jsx';
import Row from 'react-bootstrap/Row';
import {Container} from 'react-bootstrap';
import {createSidewalk, deleteSidewalk, getSidewalk, updatedSidewalk} from '../../api/sidewalks.api.js'
import {getAllOrganizations, getOrganization} from '../../api/organizations.api';
import {useNavigate, useParams} from 'react-router-dom';
import Swal from 'sweetalert2';
import {toast} from 'react-hot-toast';

export function SidewalkFormPage() {
    // Hooks
    const {
        control, handleSubmit,
        formState: {errors},
        setValue,
        register
    } = useForm();
    const navigate = useNavigate();
    const params = useParams();

    const notify = () => toast('Here is your toast.');

    const onSubmit = handleSubmit(async (data) => {

        let sidewalk_name;
        let organization_id;
        let sidewalkData;

        sidewalkData = {
            sidewalk_name: data.sidewalk_name,
            organization_id: data.organization_id.value
        };

        if (params.id) {
            await updatedSidewalk(params.id, sidewalkData).then((response) => {
                Swal.fire({
                    title: 'Censo Web',
                    text: 'Vereda actualizada con éxito!',
                    icon: 'success',
                    timer: 1500
                })
                navigate('/sidewalks')
            }).catch((error) => {
                Swal.fire({
                    title: 'Censo Web',
                    text: 'Error al actualizar la vereda',
                    icon: 'error',
                    timer: 1500
                });
            });
        } else {

            try {
                const res = await createSidewalk(sidewalkData);
                toast.success('Vereda creada con éxito!', {
                    duration: 2000,
                    position: 'top-right',
                });
                Swal.fire({
                    title: 'Censo Web',
                    text: 'Vereda creada con éxito!',
                    icon: 'success',
                    timer: 1500
                })
                navigate('/sidewalks')
            } catch (error) {
                console.error('Error al enviar la solicitud: ', error);
            }
        }
    })

    useEffect(() => {
        async function loadSidewalk() {
            if (params.id) {
                try {
                    const response = await getSidewalk(params.id);
                    const organizations = await getAllOrganizations();

                    // recorrer el arreglo de organizaciones y buscar la que tenga el id que se trae de la vereda
                    const organization = organizations.data.find((organization) => organization.id === response.data.organization_id);
                    setValue('organization_id', {value: organization.id, label: organization.organization_name});
                    setValue('sidewalk_name', response.data.sidewalk_name);

                } catch (e) {
                    console.error('Error al cargar la vereda: ', e);
                }
            }
        }

        loadSidewalk();
    }, []);

    return (
        <Container>
            <Row className="justify-content-md-center">
                <form onSubmit={handleSubmit(onSubmit)}>
                    <div>
                        <label htmlFor="sidewalk_name">Vereda:</label>
                        <Controller
                            name="sidewalk_name"
                            control={control}
                            defaultValue=""
                            rules={{required: 'Este campo es obligatorio'}} // Mensaje de error personalizado
                            render={({field}) => <input {...field} />}
                        />
                        {errors.sidewalk_name && <span>{errors.sidewalk_name.message}</span>}
                    </div>
                    <div>
                        <label htmlFor="organization_id">Organización</label>
                        <Controller
                            name="organization_id"
                            control={control}
                            rules={{required: 'Selecciona una organización'}} // Mensaje de error personalizado
                            render={({field}) => <SelectOrganizations control={control}/>}
                        />
                        {errors.organization_id && <span>{errors.organization_id.message}</span>}
                    </div>
                    <div>
                        <button type="submit">Save</button>
                    </div>
                </form>
            </Row>
        </Container>
    );
}

export default SidewalkFormPage;
