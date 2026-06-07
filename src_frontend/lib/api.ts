import axios from 'axios';
import type { ChatMessage, DocumentSource } from '@/lib/types';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function uploadFiles(files: File[]): Promise<{ files: { filename: string; message: string; status: string }[] }> {
  const formData = new FormData();
  files.forEach(file => {
    formData.append('files', file);
  });

  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
}

export async function clearKnowledgeBase(): Promise<void> {
  await api.delete('/clear');
}

export async function sendMessage(
  query: string, 
  history: ChatMessage[] = []
): Promise<{ answer: string; citations: string; sources: DocumentSource[] }> {
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

/**
 * Professional Parallel Data Fetching
 * Example: Fetching health and other initial data in parallel
 */
export async function initializeApp(): Promise<{ health: boolean }> {
  const [health] = await Promise.all([
    checkHealth(),
    // Add other parallel initialization calls here
  ]);
  return { health };
}
