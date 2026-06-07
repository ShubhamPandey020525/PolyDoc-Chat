import { useRef, useEffect, useState, useCallback } from "react";
import { ArrowLeft, Loader2, Sparkles, BookOpen, ChevronRight } from "lucide-react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import type { ChatMessage as ChatMessageType, UploadedFile } from "@/lib/types";
import { sendMessage } from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
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
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
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
    } catch (error) {
      console.error("Chat failed", error);
      toast.error("AI response failed. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  return (
    <div className="flex h-screen flex-col bg-background">
      {/* Header */}
      <div className="flex items-center gap-3 border-b border-border bg-card/50 px-4 py-3 backdrop-blur-md sticky top-0 z-10">
        <Button variant="ghost" size="icon" onClick={onBack} className="rounded-full">
          <ArrowLeft size={20} />
        </Button>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-bold text-foreground">PolyDoc Knowledge Base</p>
          <p className="truncate text-xs text-muted-foreground">
            {files.length} document(s) active
          </p>
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-6 scroll-smooth">
        <div className="mx-auto max-w-3xl space-y-8">
          {messages.length === 0 && !isLoading && (
            <div className="flex flex-col items-center py-20 text-center">
              <div className="mb-6 rounded-3xl bg-primary/10 p-6 animate-in zoom-in duration-500">
                <Sparkles size={40} className="text-primary" />
              </div>
              <h3 className="mb-2 text-2xl font-bold text-foreground">Your AI Assistant is ready</h3>
              <p className="mb-10 max-w-md text-muted-foreground">
                Ask specific questions about the uploaded content. I will only use the provided documents to answer.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-lg">
                {SUGGESTIONS.map(s => (
                  <Button
                    variant="outline"
                    key={s}
                    onClick={() => handleSend(s)}
                    className="h-auto py-3 px-4 justify-start text-left font-normal rounded-xl hover:bg-primary/5 hover:border-primary/30"
                  >
                    <ChevronRight size={16} className="mr-2 text-primary" />
                    {s}
                  </Button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <div key={msg.id} className="space-y-4">
              <ChatMessage message={msg} />
              {msg.role === 'assistant' && msg.sources && msg.sources.length > 0 && (
                <div className="ml-12 flex items-center gap-2">
                  <Sheet>
                    <SheetTrigger asChild>
                      <Button variant="ghost" size="sm" className="h-8 text-xs gap-2 rounded-full border bg-muted/30">
                        <BookOpen size={14} />
                        View Context Sources
                      </Button>
                    </SheetTrigger>
                    <SheetContent side="right" className="w-[400px] sm:w-[540px] overflow-y-auto">
                      <SheetHeader className="mb-6">
                        <SheetTitle>Retrieved Context</SheetTitle>
                        <SheetDescription>
                          These are the document chunks the AI used to generate its response.
                        </SheetDescription>
                      </SheetHeader>
                      <div className="space-y-6">
                        {msg.sources.map((source, i) => (
                          <div key={i} className="rounded-xl border bg-muted/20 p-4 space-y-2">
                            <div className="flex items-center justify-between text-xs font-semibold text-primary">
                              <span>Source {i + 1}: {source.metadata.source}</span>
                              {source.score && <span>Relevance: {(1 - source.score).toFixed(2)}</span>}
                            </div>
                            <p className="text-sm leading-relaxed text-muted-foreground">
                              "{source.content}"
                            </p>
                          </div>
                        ))}
                      </div>
                    </SheetContent>
                  </Sheet>
                  {msg.citations && msg.citations.trim() && (
                    <span className="text-[10px] text-muted-foreground bg-muted px-2 py-0.5 rounded-full border">
                      Citations: {msg.citations.split('\n').filter(c => c.trim()).length}
                    </span>
                  )}
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl border bg-card shadow-sm">
                <Loader2 size={18} className="animate-spin text-primary" />
              </div>
              <div className="rounded-2xl border bg-card px-5 py-4 shadow-sm max-w-[80%]">
                <div className="flex items-center gap-3 text-sm text-muted-foreground">
                  <span className="font-medium">AI is analyzing context...</span>
                  <span className="flex gap-1">
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary/40" style={{ animationDelay: '0ms' }} />
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary/40" style={{ animationDelay: '150ms' }} />
                    <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary/40" style={{ animationDelay: '300ms' }} />
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-border bg-card/30 p-4 backdrop-blur-md">
        <div className="mx-auto max-w-3xl">
          <ChatInput onSend={handleSend} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
