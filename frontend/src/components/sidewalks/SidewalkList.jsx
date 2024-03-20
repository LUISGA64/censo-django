import {useEffect, useState} from 'react';
import {getAllSidewalks, deleteSidewalk} from '../../api/sidewalks.api.js'
import {useNavigate, useParams} from 'react-router-dom'
import Table from 'react-bootstrap/Table';
import Swal from 'sweetalert2';


export function SidewalkList() {

    const [sidewalks, setSidewalks] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        async function loadSidewalks() {
            await getAllSidewalks().then((response) => {
                setSidewalks(response.data);
            });
        }

        loadSidewalks();
    }, []);

    // Eliminar Regsitros Sidewalk
    const borrarSidewalk = (id) => {
        Swal.fire({
            title: '¿Estás seguro?',
            text: "No podrás revertir esto",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminar'
        }).then(async (result) => {
            if (result.isConfirmed) {
                const response = await deleteSidewalk(id);
                if (response.status === 204) {
                    Swal.fire(
                        'Eliminado',
                        'La vereda ha sido eliminada',
                        'success'
                    )
                    const newSidewalks = sidewalks.filter((sidewalk) => sidewalk.id !== id);
                    setSidewalks(newSidewalks);
                }
            }
        })
    }

    // Editar registros Sidewalk
    const editarSidewalk = (id) => {
        navigate(`/sidewalks/${id}`);
    }

    return (
        <Table striped>
            <thead>
            <tr>
                <th>#</th>
                <th>ID</th>
                <th>Vereda</th>
                <th>Resguardo</th>
                <th>Opciones</th>
            </tr>
            </thead>
            <tbody>
            {sidewalks.map((sidewalk, index) => {
                return (
                    <tr key={index}>
                        <td>{index + 1}</td>
                        <td>{sidewalk.id}</td>
                        <td>{sidewalk.sidewalk_name}</td>
                        <td>{sidewalk.organization_id}</td>
                        <td>
                            <button onClick={() => editarSidewalk(sidewalk.id)}>Editar</button>
                            <button onClick={() => borrarSidewalk(sidewalk.id)}>Eliminar</button>
                        </td>
                    </tr>
                );
            })}
            </tbody>
        </Table>
    )
}
