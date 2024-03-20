import {Controller, useForm} from 'react-hook-form';
import {useEffect, useState} from 'react';
import {SelectOrganizations} from '../../components/organizations/SelectOrganizations.jsx';
import Row from 'react-bootstrap/Row';
import {Container} from 'react-bootstrap';
import {createSidewalk, deleteSidewalk, getSidewalk} from '../../api/sidewalks.api.js'
import {useNavigate, useParams} from 'react-router-dom';
import Swal from 'sweetalert2';
import toast, { Toaster } from 'react-hot-toast';

export function SidewalkFormPage() {
    // Hooks
    const {
        control, handleSubmit,
        formState: {errors},
        setValue
    } = useForm();
    const navigate = useNavigate();
    const params = useParams();

    console.log(params.id);
    const notify = () => toast('Here is your toast.');

    const onSubmit = handleSubmit(async (data) => {
        console.log(data)
        let sidewalk_name;
        let organization_id;
        let sidewalkData;

        sidewalkData = {
            sidewalk_name: data.sidewalk_name,
            organization_id: data.organization_id.value
        };
        try {
            const res = await createSidewalk(sidewalkData);

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
    })

    useEffect(() => {
        async function loadSidewalk() {
            if (params.id) {
                const response = await getSidewalk(params.id);
                console.log(response.data);
                setValue('sidewalk_name', response.data.sidewalk_name);
                setValue('organization_id', {value: response.data.organization_id});
            }
        }
        loadSidewalk();
    }, []);

    return (
        <Container>
            <Row className="justify-content-md-center">
                <form onSubmit={onSubmit}>
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
