// lib/api.js
"use client";
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: false,
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const t = localStorage.getItem("sbtoken");
    if (t) config.headers = { ...config.headers, Authorization: `Bearer ${t}` };
  }
  return config;
});

export default api;
