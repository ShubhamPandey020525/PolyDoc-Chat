export type AppState = 'landing' | 'upload' | 'chat';

export interface UploadedFile {
  name: string;
  size: number;
  type: string;
  file: File;
}

export interface DocumentSource {
  content: string;
  metadata: {
    source: string;
    page_number?: number;
    slide_number?: number;
    row_index?: number;
    file_type: string;
    [key: string]: any;
  };
  score?: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  citations?: string;
  sources?: DocumentSource[];
}
