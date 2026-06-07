import { Copy, User, Bot, Check } from "lucide-react";
import Markdown from "react-markdown";
import type { ChatMessage as ChatMessageType } from "@/lib/types";
import { toast } from "sonner";
import { useState } from "react";

interface ChatMessageProps {
  message: ChatMessageType;
}

const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    toast.success("Copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
      <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl border shadow-sm transition-all ${
        isUser
          ? 'bg-primary text-primary-foreground border-primary/20'
          : 'bg-card border-border text-primary'
      }`}>
        {isUser
          ? <User size={18} />
          : <Bot size={18} />
        }
      </div>

      <div className={`group flex flex-col max-w-[85%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`rounded-2xl px-5 py-3.5 shadow-sm ${
          isUser
            ? 'bg-primary text-primary-foreground'
            : 'bg-card border border-border text-card-foreground'
        }`}>
          {isUser ? (
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none dark:prose-invert prose-p:leading-relaxed prose-pre:bg-muted/50 prose-pre:border prose-pre:border-border prose-headings:font-bold prose-headings:text-foreground">
              <Markdown>{message.content}</Markdown>
            </div>
          )}
        </div>

        {!isUser && (
          <div className="mt-2 flex gap-1 opacity-0 transition-opacity group-hover:opacity-100 px-1">
            <button 
              onClick={handleCopy} 
              className="rounded-lg p-2 text-muted-foreground transition-all hover:bg-muted hover:text-foreground border border-transparent hover:border-border"
              title="Copy response"
            >
              {copied ? <Check size={14} className="text-green-500" /> : <Copy size={14} />}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
