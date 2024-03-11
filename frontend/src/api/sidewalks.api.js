import axios from 'axios';
export function getAllSidewalks() {
    return axios.get('http://127.0.0.1:8000/api/v1.0/sidewalks/');
}