import axios from 'axios';

const sidewalkApi = axios.create({
    baseURL: "http://127.0.0.1:8000/api/v1.0/sidewalks/",
});

export const getAllSidewalks = () => sidewalkApi.get("/");
export const createSidewalk = (sidewalks) => sidewalkApi.post("/", sidewalks);
export const deleteSidewalk = (id) => sidewalkApi.delete(`/${id}`)