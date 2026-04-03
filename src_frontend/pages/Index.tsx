import { useState } from "react";
import LandingHero from "@/components/polydoc/LandingHero";
import UploadBox from "@/components/polydoc/UploadBox";
import ChatWindow from "@/components/polydoc/ChatWindow";
import type { AppState, UploadedFile } from "@/lib/types";

const Index = () => {
  const [appState, setAppState] = useState<AppState>('landing');
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);

  if (appState === 'landing') {
    return <LandingHero onStart={() => setAppState('upload')} />;
  }

  if (appState === 'upload') {
    return (
      <UploadBox
        uploadedFile={uploadedFile}
        onFileUploaded={(file) => setUploadedFile(file)}
        onRemoveFile={() => setUploadedFile(null)}
        onStartChat={() => setAppState('chat')}
      />
    );
  }

  if (appState === 'chat' && uploadedFile) {
    return (
      <ChatWindow
        file={uploadedFile}
        onBack={() => setAppState('upload')}
      />
    );
  }

  return null;
};

export default Index;
