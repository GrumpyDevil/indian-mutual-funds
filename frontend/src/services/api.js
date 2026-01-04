import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const portfolioService = {
    getSummary: () => api.get('/portfolio/summary'),
    getHoldings: () => api.get('/portfolio/holdings'),
    getBenchmarkCompare: () => api.get('/benchmark/compare'),
    getSipPerformance: () => api.get('/portfolio/sip-performance'),
    parseCas: (formData) => api.post('/cas/parse', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    }),
};
