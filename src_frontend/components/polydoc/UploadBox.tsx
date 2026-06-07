import { useCallback, useState, useRef } from "react";
import { Upload, FileUp, Loader2, X } from "lucide-react";
import type { UploadedFile } from "@/lib/types";
import { uploadFiles } from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";

const ACCEPTED_EXTENSIONS = ['.pdf', '.csv', '.xls', '.xlsx', '.docx', '.pptx', '.txt', '.md'];

interface UploadBoxProps {
  onFilesUploaded: (files: UploadedFile[]) => void;
  uploadedFiles: UploadedFile[];
  onRemoveFile: (name: string) => void;
  onStartChat: () => void;
}

const UploadBox = ({ onFilesUploaded, uploadedFiles, onRemoveFile, onStartChat }: UploadBoxProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFiles = useCallback(async (files: FileList | File[]) => {
    const fileList = Array.from(files);
    const validFiles = fileList.filter(file => 
      ACCEPTED_EXTENSIONS.some(ext => file.name.toLowerCase().endsWith(ext))
    );
    
    if (validFiles.length === 0) {
      toast.error("No supported files found. Please upload PDF, DOCX, PPTX, CSV, TXT, or MD.");
      return;
    }

    if (validFiles.length < fileList.length) {
      toast.warning(`${fileList.length - validFiles.length} unsupported files were skipped.`);
    }

    setIsUploading(true);
    try {
      const response = await uploadFiles(validFiles);
      
      const successfulFiles: UploadedFile[] = [];
      response.files.forEach((res, index) => {
        if (res.status === 'success') {
          const file = validFiles[index];
          successfulFiles.push({ name: file.name, size: file.size, type: file.type, file });
        } else {
          toast.error(`Failed to process ${res.filename}: ${res.message}`);
        }
      });

      if (successfulFiles.length > 0) {
        onFilesUploaded(successfulFiles);
        toast.success(`Successfully indexed ${successfulFiles.length} file(s)!`);
      }
    } catch (error: any) {
      console.error("Upload failed", error);
      const detail = error.response?.data?.detail || "Is the backend running?";
      toast.error(`Upload failed: ${detail}`);
    } finally {
      setIsUploading(false);
    }
  }, [onFilesUploaded]);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files) handleFiles(e.dataTransfer.files);
  }, [handleFiles]);

  const onDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const onDragLeave = useCallback(() => setIsDragging(false), []);

  const onInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) handleFiles(e.target.files);
  }, [handleFiles]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl">
        <h2 className="mb-2 text-center text-3xl font-bold text-foreground">Build Your Knowledge Base</h2>
        <p className="mb-8 text-center text-muted-foreground">
          Upload documents (PDF, DOCX, PPTX, CSV, TXT, MD) to start chatting
        </p>

        <div
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onClick={() => !isUploading && inputRef.current?.click()}
          className={`group cursor-pointer rounded-2xl border-2 border-dashed p-10 text-center transition-all duration-300 ${
            isDragging
              ? 'border-primary bg-primary/5 scale-[1.01]'
              : isUploading
              ? 'border-muted bg-muted/20 cursor-not-allowed'
              : 'border-border bg-card hover:border-primary/50 hover:bg-card/80'
          } shadow-xl mb-8`}
        >
          <input
            ref={inputRef}
            type="file"
            multiple
            onChange={onInputChange}
            className="hidden"
            accept={ACCEPTED_EXTENSIONS.join(',')}
          />
          <div className="mb-4 flex justify-center">
            <div className={`rounded-2xl p-4 transition-all duration-300 ${
              isDragging || isUploading
                ? 'bg-primary text-primary-foreground'
                : 'bg-muted text-muted-foreground group-hover:bg-primary group-hover:text-primary-foreground'
            }`}>
              {isUploading ? <Loader2 size={32} className="animate-spin" /> : isDragging ? <FileUp size={32} /> : <Upload size={32} />}
            </div>
          </div>
          <p className="mb-2 font-semibold">
            {isUploading ? 'Indexing documents...' : isDragging ? 'Drop to upload' : 'Click or drag documents here'}
          </p>
          <p className="text-sm text-muted-foreground">
            Support for multiple files up to 10MB each
          </p>
        </div>

        {uploadedFiles.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold px-1">Uploaded Documents ({uploadedFiles.length})</h3>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              {uploadedFiles.map((file) => (
                <div key={file.name} className="relative group rounded-xl border bg-card p-4 shadow-sm">
                  <button 
                    onClick={() => onRemoveFile(file.name)}
                    className="absolute -right-2 -top-2 rounded-full bg-destructive p-1 text-destructive-foreground opacity-0 transition-opacity group-hover:opacity-100 shadow-sm"
                  >
                    <X size={14} />
                  </button>
                  <div className="flex items-center gap-3">
                    <div className="rounded-lg bg-primary/10 p-2 text-primary">
                      <FileUp size={20} />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="truncate font-medium text-sm">{file.name}</p>
                      <p className="text-xs text-muted-foreground">{(file.size / 1024).toFixed(1)} KB</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="flex justify-center pt-4">
              <Button 
                onClick={onStartChat} 
                className="w-full sm:w-auto px-12 py-6 text-lg font-semibold rounded-xl"
              >
                Start Chatting
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadBox;
