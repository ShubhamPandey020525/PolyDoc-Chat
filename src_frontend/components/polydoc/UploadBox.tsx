import { useCallback, useState, useRef } from "react";
import { Upload, FileUp, Loader2 } from "lucide-react";
import DocumentCard from "./DocumentCard";
import type { UploadedFile } from "@/lib/types";
import { uploadFile } from "@/lib/api";
import { toast } from "sonner";

const ACCEPTED_TYPES = [
  'application/pdf',
  'text/csv',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/plain',
];

const ACCEPTED_EXTENSIONS = ['.pdf', '.csv', '.xls', '.xlsx', '.docx', '.txt'];

interface UploadBoxProps {
  onFileUploaded: (file: UploadedFile) => void;
  uploadedFile: UploadedFile | null;
  onRemoveFile: () => void;
  onStartChat: () => void;
}

const UploadBox = ({ onFileUploaded, uploadedFile, onRemoveFile, onStartChat }: UploadBoxProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback(async (file: File) => {
    const isAccepted = ACCEPTED_TYPES.includes(file.type) ||
      ACCEPTED_EXTENSIONS.some(ext => file.name.toLowerCase().endsWith(ext));
    
    if (!isAccepted) {
      toast.error("Invalid file type. Please upload a supported document.");
      return;
    }

    setIsUploading(true);
    try {
      await uploadFile(file);
      onFileUploaded({ name: file.name, size: file.size, type: file.type, file });
      toast.success(`'${file.name}' indexed successfully!`);
    } catch (error) {
      console.error("Upload failed", error);
      toast.error("Failed to upload and index document. Is the backend running?");
    } finally {
      setIsUploading(false);
    }
  }, [onFileUploaded]);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback(() => setIsDragging(false), []);

  const onInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }, [handleFile]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4">
      <div className="w-full max-w-lg">
        <h2 className="mb-2 text-center text-2xl font-bold text-foreground">Upload Your Document</h2>
        <p className="mb-8 text-center text-muted-foreground">
          Upload a file to start chatting with it
        </p>

        {!uploadedFile ? (
          <div
            onDrop={onDrop}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onClick={() => inputRef.current?.click()}
            className={`group cursor-pointer rounded-2xl border-2 border-dashed p-12 text-center transition-all duration-300 ${
              isDragging
                ? 'border-primary bg-primary/5 scale-[1.02]'
                : isUploading
                ? 'border-muted bg-muted/20 cursor-not-allowed'
                : 'border-border bg-card hover:border-primary/50 hover:bg-card/80'
            } shadow-lg`}
          >
            <div className="mb-4 flex justify-center">
              <div className={`rounded-2xl p-4 transition-all duration-300 ${
                isDragging || isUploading
                  ? 'bg-gradient-to-br from-orange-500 to-pink-500 text-white'
                  : 'bg-muted text-muted-foreground group-hover:bg-gradient-to-br group-hover:from-orange-500 group-hover:to-pink-500 group-hover:text-white'
              }`}>
                {isUploading ? <Loader2 size={32} className="animate-spin" /> : isDragging ? <FileUp size={32} /> : <Upload size={32} />}
              </div>
            </div>
            <p className="mb-2 text-lg font-medium text-foreground">
              {isUploading ? 'Processing Document...' : isDragging ? 'Drop your file here' : 'Drag and drop your document here'}
            </p>
            <p className="mb-4 text-sm text-muted-foreground">
              {isUploading ? 'Our AI is indexing your content' : 'or click to upload'}
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {['PDF', 'CSV', 'Excel', 'DOCX', 'TXT'].map(t => (
                <span key={t} className="rounded-full bg-muted px-3 py-1 text-xs font-medium text-muted-foreground">
                  {t}
                </span>
              ))}
            </div>
            <input
              ref={inputRef}
              type="file"
              className="hidden"
              accept={ACCEPTED_EXTENSIONS.join(',')}
              onChange={onInputChange}
            />
          </div>
        ) : (
          <div className="space-y-4">
            <DocumentCard file={uploadedFile} onRemove={onRemoveFile} />
            <button
              onClick={onStartChat}
              className="w-full rounded-2xl bg-gradient-to-r from-orange-500 via-pink-500 to-purple-500 py-3.5 text-lg font-semibold text-white shadow-lg shadow-orange-500/20 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl hover:shadow-orange-500/30 active:scale-[0.98]"
            >
              Start Chatting
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadBox;
