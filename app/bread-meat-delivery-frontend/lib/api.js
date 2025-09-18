// app/bread-meat-delivery-frontend/lib/api.js
"use client";
import axios from "axios";
const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || "/api";
const api = axios.create({ baseURL, withCredentials: false });
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const t = localStorage.getItem("sbtoken");
    if (t) config.headers = { ...config.headers, Authorization: `Bearer ${t}` };
  }
  return config;
});
export default api;
