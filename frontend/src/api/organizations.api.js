import axios from "axios";


const organizationApi = axios.create({
    baseURL: "http://127.0.0.1:8000/api/v1.0/organizations/",
});

export const getAllOrganizations = () => organizationApi.get("/");
export const getOrganization = (id) => organizationApi.get(`/${id}/`);