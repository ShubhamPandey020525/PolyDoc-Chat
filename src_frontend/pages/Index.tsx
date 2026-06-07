import { useState } from "react";
import LandingHero from "@/components/polydoc/LandingHero";
import UploadBox from "@/components/polydoc/UploadBox";
import ChatWindow from "@/components/polydoc/ChatWindow";
import type { AppState, UploadedFile } from "@/lib/types";
import { clearKnowledgeBase } from "@/lib/api";
import { toast } from "sonner";
import { Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";

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

  if (appState === 'landing') {
    return <LandingHero onStart={() => setAppState('upload')} />;
  }

  return (
    <div className="relative min-h-screen bg-background">
      {uploadedFiles.length > 0 && (
        <div className="fixed bottom-4 right-4 z-50">
          <Button 
            variant="destructive" 
            size="sm" 
            onClick={handleReset}
            className="rounded-full shadow-lg gap-2"
          >
            <Trash2 size={16} />
            Reset All
          </Button>
        </div>
      )}

      {appState === 'upload' && (
        <UploadBox
          uploadedFiles={uploadedFiles}
          onFilesUploaded={(files) => setUploadedFiles([...uploadedFiles, ...files])}
          onRemoveFile={(name) => setUploadedFiles(uploadedFiles.filter(f => f.name !== name))}
          onStartChat={() => setAppState('chat')}
        />
      )}

      {appState === 'chat' && uploadedFiles.length > 0 && (
        <ChatWindow
          files={uploadedFiles}
          onBack={() => setAppState('upload')}
        />
      )}
    </div>
  );
};

export default Index;
