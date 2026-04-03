import axios from 'axios';
import type { ChatMessage } from '@/lib/types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function uploadFile(file: File): Promise<{ filename: string; message: string }> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
}

export async function sendMessage(
  query: string, 
  history: ChatMessage[] = []
): Promise<{ answer: string; citations: string; sources: any[] }> {
  // Convert frontend message format to backend history format
  const conversation_history = history.map(msg => ({
    role: msg.role,
    content: msg.content
  }));

  const response = await api.post('/chat', {
    query,
    conversation_history
  });

  return response.data;
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await api.get('/health');
    return response.data.status === 'healthy';
  } catch {
    return false;
  }
}
