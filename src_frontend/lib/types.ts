export type AppState = 'landing' | 'upload' | 'chat';

export interface UploadedFile {
  name: string;
  size: number;
  type: string;
  file: File;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}
