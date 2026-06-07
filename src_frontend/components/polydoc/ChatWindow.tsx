import { useRef, useEffect, useState, useCallback } from "react";
import { ArrowLeft, Loader2, Sparkles, BookOpen, ChevronRight, Brain, File } from "lucide-react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import type { ChatMessage as ChatMessageType, UploadedFile } from "@/lib/types";
import { sendMessage } from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { motion, AnimatePresence } from "framer-motion";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

const SUGGESTIONS = [
  "Summarize these documents",
  "What are the key takeaways?",
  "Analyze the data trends",
  "Compare the documents",
];

interface ChatWindowProps {
  files: UploadedFile[];
  onBack: () => void;
}

const ChatWindow = ({ files, onBack }: ChatWindowProps) => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  }, [messages, isLoading]);

  const handleSend = useCallback(async (content: string) => {
    const userMsg: ChatMessageType = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const { answer, citations, sources } = await sendMessage(content, messages);
      
      const assistantMsg: ChatMessageType = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: answer,
        citations,
        sources,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (error: any) {
      console.error("Chat failed", error);
      const detail = error.response?.data?.detail || "Is the backend running?";
      toast.error(`AI response failed: ${detail}`);
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  return (
    <div className="relative flex h-screen flex-col overflow-hidden">
      {/* Cinematic Header */}
      <header className="relative z-20 flex items-center justify-between border-b border-white/5 bg-[#020202]/80 px-10 py-6 backdrop-blur-xl">
        <div className="flex items-center gap-10">
          <button 
            onClick={onBack} 
            className="group flex items-center gap-3 text-[10px] font-black uppercase tracking-[0.4em] text-slate-500 hover:text-emerald-500 transition-colors"
          >
            <ArrowLeft size={16} className="transition-transform group-hover:-translate-x-1" />
            Terminal
          </button>
          
          <div className="h-8 w-[1px] bg-white/5" />

          <div className="flex flex-col">
            <h1 className="text-2xl font-[1000] tracking-[-0.04em] text-white uppercase">
              Intelligence <span className="text-emerald-500">Session</span>
            </h1>
            <div className="flex items-center gap-2 mt-1">
              <div className="h-1 w-1 rounded-full bg-emerald-500 animate-pulse" />
              <p className="text-[9px] font-black uppercase tracking-[0.3em] text-slate-600">
                {files.length} ACTIVE NODES
              </p>
            </div>
          </div>
        </div>
        
        <div className="hidden sm:flex items-center gap-4 rounded-none border border-white/10 bg-white/5 px-6 py-3">
          <Brain size={18} className="text-emerald-500" strokeWidth={1.5} />
          <span className="text-[10px] font-black uppercase tracking-[0.4em] text-white">Neural Core v1.0.4</span>
        </div>
      </header>

      {/* Main Neural Field */}
      <main 
        ref={scrollRef} 
        className="relative z-10 flex-1 overflow-y-auto scroll-smooth [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]"
      >
        <div className={`mx-auto max-w-5xl px-10 h-full flex flex-col ${messages.length === 0 ? 'justify-center' : 'py-16'}`}>
          <AnimatePresence mode="popLayout">
            {messages.length === 0 && !isLoading && (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col items-center justify-center text-center w-full"
              >
                <div className="mb-6">
                  <div className="relative inline-flex h-20 w-20 items-center justify-center rounded-full border border-emerald-500/20 bg-emerald-500/5">
                    <Sparkles size={28} className="text-emerald-500" strokeWidth={1} />
                    <div className="absolute inset-0 animate-ping rounded-full border border-emerald-500/10" />
                  </div>
                </div>
                <h2 className="text-3xl font-black tracking-tight text-white uppercase sm:text-4xl">
                  Awaiting Input
                </h2>
                <p className="mt-2 max-w-xl text-sm font-medium text-slate-500">
                  Direct the neural core to analyze ingested assets. 
                  Deterministic verification enabled.
                </p>
                <div className="mt-8 grid w-full grid-cols-1 gap-3 sm:grid-cols-2 max-w-2xl">
                  {SUGGESTIONS.map((s, i) => (
                    <motion.button
                      key={s}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.1 }}
                      onClick={() => handleSend(s)}
                      className="group flex items-center justify-between border border-white/5 bg-[#050505] px-5 py-3 text-left transition-all hover:border-emerald-500/40 hover:bg-emerald-500/[0.02]"
                    >
                      <span className="text-[9px] font-black uppercase tracking-[0.2em] text-slate-400 group-hover:text-white transition-colors">{s}</span>
                      <ChevronRight size={14} className="text-slate-700 transition-transform group-hover:translate-x-1 group-hover:text-emerald-500" />
                    </motion.button>
                  ))}
                </div>
              </motion.div>
            )}

            {messages.map((msg, i) => (
              <motion.div 
                key={msg.id} 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-16"
              >
                <ChatMessage message={msg} />
                
                {msg.role === 'assistant' && msg.sources && msg.sources.length > 0 && (
                  <motion.div 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="ml-16 mt-6 flex flex-wrap items-center gap-6"
                  >
                    <Sheet>
                      <SheetTrigger asChild>
                        <button className="flex items-center gap-3 text-[9px] font-black uppercase tracking-[0.3em] text-emerald-500/60 hover:text-emerald-500 transition-colors">
                          <BookOpen size={14} strokeWidth={1.5} />
                          Context Sources
                        </button>
                      </SheetTrigger>
                      <SheetContent side="right" className="w-full border-l border-white/5 bg-[#020202] p-0 sm:max-w-2xl">
                        <div className="flex h-full flex-col">
                          <div className="border-b border-white/5 p-10">
                            <h3 className="text-3xl font-[1000] tracking-tight text-white uppercase">Neural <span className="text-emerald-500">Attribution</span></h3>
                            <p className="mt-2 text-sm font-medium text-slate-500 uppercase tracking-widest">Verification Protocol Active</p>
                          </div>
                          <div className="flex-1 overflow-y-auto p-10 space-y-8 scrollbar-hide">
                            {msg.sources.map((source, idx) => (
                              <motion.div 
                                key={idx}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: idx * 0.1 }}
                                className="border border-white/5 bg-white/[0.02] p-8"
                              >
                                <div className="mb-6 flex items-center justify-between border-b border-white/5 pb-4">
                                  <span className="text-[10px] font-black uppercase tracking-[0.4em] text-emerald-500">
                                    Segment {idx + 1}
                                  </span>
                                  <span className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">
                                    {source.metadata.source}
                                  </span>
                                </div>
                                <p className="text-sm leading-relaxed text-slate-300 italic font-medium">
                                  "{source.content}"
                                </p>
                                {source.metadata.page_number && (
                                  <div className="mt-6">
                                    <span className="rounded-sm bg-white/5 px-2 py-1 text-[9px] font-black uppercase tracking-[0.2em] text-slate-500 border border-white/5">
                                      PAGE {source.metadata.page_number}
                                    </span>
                                  </div>
                                )}
                              </motion.div>
                            ))}
                          </div>
                        </div>
                      </SheetContent>
                    </Sheet>

                    {msg.citations && msg.citations.trim() && (
                      <div className="flex items-center gap-3 border-l border-white/5 pl-6">
                        <div className="h-1 w-1 rounded-full bg-emerald-500" />
                        <span className="text-[9px] font-black uppercase tracking-[0.3em] text-slate-700">
                          {msg.citations.split('\n').filter(c => c.trim()).length} VERIFIED NODES
                        </span>
                      </div>
                    )}
                  </motion.div>
                )}
              </motion.div>
            ))}

            {isLoading && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-start gap-8 mb-16"
              >
                <div className="flex h-12 w-12 shrink-0 items-center justify-center border border-emerald-500/20 bg-emerald-500/5 text-emerald-500">
                  <Loader2 size={20} className="animate-spin" strokeWidth={1.5} />
                </div>
                <div className="flex flex-col gap-4">
                  <span className="text-[10px] font-black uppercase tracking-[0.5em] text-emerald-500/60 animate-pulse">
                    Neural Synthesis in Progress...
                  </span>
                  <div className="flex gap-2">
                    <motion.div animate={{ scale: [1, 1.5, 1], opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1 }} className="h-1 w-1 rounded-full bg-emerald-500" />
                    <motion.div animate={{ scale: [1, 1.5, 1], opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1, delay: 0.2 }} className="h-1 w-1 rounded-full bg-emerald-500" />
                    <motion.div animate={{ scale: [1, 1.5, 1], opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} className="h-1 w-1 rounded-full bg-emerald-500" />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      {/* Cinematic Input Field */}
      <footer className="relative z-20 border-t border-white/5 bg-[#020202]/80 px-10 pb-12 pt-8 backdrop-blur-xl">
        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </footer>
    </div>
  );
};

export default ChatWindow;
