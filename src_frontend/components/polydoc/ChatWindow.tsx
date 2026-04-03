import { useRef, useEffect, useState, useCallback } from "react";
import { ArrowLeft, Loader2, Sparkles } from "lucide-react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import type { ChatMessage as ChatMessageType, UploadedFile } from "@/lib/types";
import { sendMessage } from "@/lib/api";
import { toast } from "sonner";

const SUGGESTIONS = [
  "Summarize this document",
  "Extract key insights",
  "Explain the data",
  "Find important numbers",
];

interface ChatWindowProps {
  file: UploadedFile;
  onBack: () => void;
}

const ChatWindow = ({ file, onBack }: ChatWindowProps) => {
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
    
    // Optimistically add user message
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      // Send message to actual backend with history
      const { answer, citations } = await sendMessage(content, messages);
      
      const assistantMsg: ChatMessageType = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: answer + (citations ? `\n\n**Sources:**\n${citations}` : ""),
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
    <div className="flex h-screen flex-col">
      {/* Header */}
      <div className="flex items-center gap-3 border-b border-border bg-card/80 px-4 py-3 backdrop-blur-sm">
        <button onClick={onBack} className="rounded-lg p-1.5 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground">
          <ArrowLeft size={20} />
        </button>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-foreground">PolyDoc Chat</p>
          <p className="truncate text-xs text-muted-foreground">{file.name}</p>
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-6">
        <div className="mx-auto max-w-3xl space-y-6">
          {messages.length === 0 && !isLoading && (
            <div className="flex flex-col items-center py-12">
              <div className="mb-4 rounded-2xl bg-gradient-to-br from-orange-100 to-pink-100 p-4">
                <Sparkles size={28} className="text-orange-500" />
              </div>
              <h3 className="mb-2 text-lg font-semibold text-foreground">Start a conversation</h3>
              <p className="mb-8 text-center text-sm text-muted-foreground">
                Ask anything about your document
              </p>
              <div className="flex flex-wrap justify-center gap-2">
                {SUGGESTIONS.map(s => (
                  <button
                    key={s}
                    onClick={() => handleSend(s)}
                    className="rounded-full border border-border bg-card px-4 py-2 text-sm text-foreground shadow-sm transition-all hover:border-primary/30 hover:bg-muted hover:shadow-md"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map(msg => (
            <ChatMessage key={msg.id} message={msg} />
          ))}

          {isLoading && (
            <div className="flex gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-full border border-border bg-card shadow-sm">
                <Loader2 size={14} className="animate-spin text-primary" />
              </div>
              <div className="rounded-2xl border border-border bg-card px-4 py-3 shadow-sm">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <span>AI is thinking</span>
                  <span className="flex gap-0.5">
                    <span className="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-primary/60" style={{ animationDelay: '0ms' }} />
                    <span className="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-primary/60" style={{ animationDelay: '150ms' }} />
                    <span className="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-primary/60" style={{ animationDelay: '300ms' }} />
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} isLoading={isLoading} />
    </div>
  );
};

export default ChatWindow;
