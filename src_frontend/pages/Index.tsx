import { useState } from "react";
import LandingHero from "@/components/polydoc/LandingHero";
import UploadBox from "@/components/polydoc/UploadBox";
import ChatWindow from "@/components/polydoc/ChatWindow";
import type { AppState, UploadedFile } from "@/lib/types";
import { clearKnowledgeBase } from "@/lib/api";
import { toast } from "sonner";
import { Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";

import { motion, AnimatePresence } from "framer-motion";

const Index = () => {
  const [appState, setAppState] = useState<AppState>('landing');
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);

  const handleReset = async () => {
    if (window.confirm("Are you sure? This will delete all uploaded documents and clear the chat.")) {
      try {
        await clearKnowledgeBase();
        setUploadedFiles([]);
        setAppState('upload');
        toast.success("Knowledge base cleared!");
      } catch (error) {
        toast.error("Failed to clear knowledge base.");
      }
    }
  };

  return (
    <div className="relative min-h-screen bg-[#020202] font-sans antialiased overflow-hidden text-white selection:bg-emerald-500/30">
      {/* Intense Cinematic Background (Shared across all states) */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] h-[80%] w-[60%] rounded-full bg-emerald-600/5 blur-[140px]" />
        <div className="absolute bottom-[-10%] left-[-5%] h-[80%] w-[60%] rounded-full bg-blue-700/5 blur-[140px]" />
      </div>

      {/* High-Visibility Tech Grid */}
      <div className="fixed inset-0 z-0 opacity-[0.06] [background-image:linear-gradient(to_right,#ffffff_1px,transparent_1px),linear-gradient(to_bottom,#ffffff_1px,transparent_1px)] [background-size:80px_80px] pointer-events-none" />

      <AnimatePresence mode="wait">
        {appState === 'landing' && (
          <motion.div
            key="landing"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, scale: 0.95, filter: "blur(20px)" }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="relative z-10 h-screen w-full"
          >
            <LandingHero onStart={() => setAppState('upload')} />
          </motion.div>
        )}

        {appState === 'upload' && (
          <motion.div
            key="upload"
            initial={{ opacity: 0, scale: 1.05, filter: "blur(20px)" }}
            animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
            exit={{ opacity: 0, scale: 0.95, filter: "blur(20px)" }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="relative z-10 h-screen w-full"
          >
            <UploadBox
              uploadedFiles={uploadedFiles}
              onFilesUploaded={(files) => setUploadedFiles([...uploadedFiles, ...files])}
              onRemoveFile={(name) => setUploadedFiles(uploadedFiles.filter(f => f.name !== name))}
              onStartChat={() => setAppState('chat')}
            />
          </motion.div>
        )}

        {appState === 'chat' && uploadedFiles.length > 0 && (
          <motion.div
            key="chat"
            initial={{ opacity: 0, x: 40, filter: "blur(20px)" }}
            animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
            exit={{ opacity: 0, x: -40, filter: "blur(20px)" }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="relative z-10 h-screen w-full"
          >
            <ChatWindow
              files={uploadedFiles}
              onBack={() => setAppState('upload')}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {uploadedFiles.length > 0 && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="fixed bottom-10 right-10 z-50"
        >
          <Button 
            onClick={handleReset}
            className="h-14 rounded-none border border-red-500/20 bg-red-500/5 px-8 text-red-500 shadow-2xl backdrop-blur-xl transition-all hover:bg-red-500 hover:text-white active:scale-95 font-black uppercase tracking-[0.3em] text-[10px]"
          >
            <Trash2 size={16} className="mr-3" />
            Purge Protocol
          </Button>
        </motion.div>
      )}
    </div>
  );
};

export default Index;
