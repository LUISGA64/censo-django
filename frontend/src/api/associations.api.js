import axios from "axios";

const associationApi = axios.create({
    baseURL: "http://127.0.0.1:8000/api/v1.0/associations/",
});

export const getAllAssociations = () => associationApi.get("/");
export const getAssociation = (id) => associationApi.get(`/${id}/`);

export const createAssociation = (association) => associationApi.post("/", association);

export const deleteAssociation = (id) => associationApi.delete(`/${id}`);

export const updateAssociation = (id, association) => associationApi.put(`/${id}/`, association);