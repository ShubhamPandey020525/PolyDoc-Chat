import { useCallback, useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, FileUp, Loader2, X, FileText, CheckCircle2, ArrowRight } from "lucide-react";
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

  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center px-10 py-20 overflow-hidden">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-5xl"
      >
        <div className="mb-16">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="mb-4 inline-flex"
          >
            <span className="rounded-sm bg-emerald-500/10 px-3 py-1 text-[9px] font-black uppercase tracking-[0.4em] text-emerald-500 border border-emerald-500/20">
              Ingestion Mode
            </span>
          </motion.div>
          <h2 className="text-6xl font-[1000] tracking-[-0.04em] text-white sm:text-7xl">
            KNOWLEDGE <span className="bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent">INGESTION</span>
          </h2>
          <p className="mt-4 text-lg font-medium text-slate-500 max-w-2xl">
            Transmit technical assets to the neural core for deep context indexing. 
            Deterministic processing active.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
          {/* Dropzone */}
          <div className="lg:col-span-7">
            <motion.div
              onDrop={(e) => { e.preventDefault(); setIsDragging(false); handleFiles(e.dataTransfer.files); }}
              onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onClick={() => !isUploading && inputRef.current?.click()}
              whileHover={{ scale: isUploading ? 1 : 1.01 }}
              whileTap={{ scale: isUploading ? 1 : 0.99 }}
              className={`group relative cursor-pointer overflow-hidden rounded-none border-2 border-dashed p-16 transition-all duration-500 ${
                isDragging
                  ? 'border-emerald-500 bg-emerald-500/5'
                  : isUploading
                  ? 'border-white/5 bg-white/5 cursor-not-allowed'
                  : 'border-white/10 bg-[#050505] hover:border-emerald-500/50'
              }`}
            >
              <input
                ref={inputRef}
                type="file"
                multiple
                onChange={(e) => e.target.files && handleFiles(e.target.files)}
                className="hidden"
                accept={ACCEPTED_EXTENSIONS.join(',')}
              />
              
              <div className="flex flex-col items-center justify-center space-y-8 text-center">
                <div className={`transition-all duration-500 ${
                  isDragging || isUploading ? 'text-emerald-500 scale-110' : 'text-slate-700 group-hover:text-emerald-500'
                }`}>
                  {isUploading ? <Loader2 size={64} className="animate-spin" strokeWidth={1} /> : <Upload size={64} strokeWidth={1} />}
                </div>
                
                <div className="space-y-2">
                  <p className="text-xl font-black uppercase tracking-widest text-white">
                    {isUploading ? 'INDEXING...' : isDragging ? 'RELEASE' : 'SELECT SOURCES'}
                  </p>
                  <p className="text-[10px] font-bold text-slate-600 uppercase tracking-[0.3em]">
                    PDF • DOCX • PPTX • CSV • TXT • MD
                  </p>
                </div>

                {isUploading && (
                  <div className="w-64 space-y-3">
                    <div className="h-[2px] w-full overflow-hidden bg-white/5">
                      <motion.div 
                        className="h-full bg-emerald-500"
                        animate={{ x: ["-100%", "100%"] }}
                        transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                      />
                    </div>
                    <p className="text-[8px] font-black uppercase tracking-[0.4em] text-emerald-500 animate-pulse">Neural Mapping Active</p>
                  </div>
                )}
              </div>
            </motion.div>
          </div>

          {/* File List & Start Button */}
          <div className="lg:col-span-5 flex flex-col gap-8">
            <AnimatePresence>
              {uploadedFiles.length > 0 ? (
                <motion.div 
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="space-y-6"
                >
                  <div className="flex items-center justify-between border-b border-white/5 pb-4">
                    <h3 className="text-[10px] font-black uppercase tracking-[0.4em] text-emerald-500 flex items-center gap-3">
                      <CheckCircle2 size={14} />
                      VALIDATED NODES ({uploadedFiles.length})
                    </h3>
                  </div>

                  <div className="max-h-[300px] overflow-y-auto pr-4 space-y-3 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
                    {uploadedFiles.map((file, idx) => (
                      <motion.div 
                        key={file.name}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.05 }}
                        className="group flex items-center justify-between border border-white/5 bg-[#050505] p-4 transition-all hover:border-emerald-500/30"
                      >
                        <div className="flex items-center gap-4 min-w-0">
                          <FileText size={18} className="text-emerald-500/50 shrink-0" />
                          <div className="min-w-0">
                            <p className="truncate text-xs font-bold text-slate-200">{file.name}</p>
                            <p className="text-[9px] font-bold uppercase tracking-tighter text-slate-600">
                              {(file.size / 1024).toFixed(0)} KB
                            </p>
                          </div>
                        </div>
                        <button 
                          onClick={(e) => { e.stopPropagation(); onRemoveFile(file.name); }}
                          className="text-slate-700 hover:text-red-500 transition-colors"
                        >
                          <X size={14} />
                        </button>
                      </motion.div>
                    ))}
                  </div>

                  <motion.div 
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="pt-4"
                  >
                    <Button 
                      onClick={onStartChat} 
                      className="group relative h-20 w-full rounded-none border border-white/10 bg-white text-lg font-[1000] text-black transition-all hover:bg-emerald-500 hover:text-white"
                    >
                      <span className="relative z-10 flex items-center justify-center gap-4">
                        BEGIN SESSION
                        <ArrowRight size={24} className="transition-transform duration-500 group-hover:translate-x-2" />
                      </span>
                    </Button>
                  </motion.div>
                </motion.div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center border border-white/5 bg-white/[0.02] p-12 text-center">
                  <span className="text-[10px] font-black uppercase tracking-[0.4em] text-slate-700">
                    Awaiting Source Transmission
                  </span>
                </div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default UploadBox;
