import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 120000, // 120s
});

export const sendMessage = async (message: string, sessionId: string | null = null) => {
  const payload: { message: string; session_id?: string } = { message };
  if (sessionId) payload.session_id = sessionId;

  const { data } = await apiClient.post('/chat/', payload);
  return data;
};

export const getConversationHistory = async (sessionId: string) => {
  const { data } = await apiClient.get(`/conversation/${sessionId}/`);
  return data;
};
