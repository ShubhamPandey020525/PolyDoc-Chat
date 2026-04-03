import { Copy, RefreshCw, User, Bot } from "lucide-react";
import ReactMarkdown from "react-markdown";
import type { ChatMessage as ChatMessageType } from "@/lib/types";
import { toast } from "sonner";

interface ChatMessageProps {
  message: ChatMessageType;
}

const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === 'user';

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    toast.success("Copied to clipboard");
  };

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <div className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
        isUser
          ? 'bg-gradient-to-br from-orange-500 to-pink-500'
          : 'bg-card border border-border shadow-sm'
      }`}>
        {isUser
          ? <User size={14} className="text-white" />
          : <Bot size={14} className="text-primary" />
        }
      </div>

      <div className={`group max-w-[80%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-gradient-to-r from-orange-500 via-pink-500 to-purple-500 text-white'
            : 'bg-card border border-border shadow-sm text-card-foreground'
        }`}>
          {isUser ? (
            <p className="text-sm leading-relaxed">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none text-card-foreground prose-headings:text-card-foreground prose-strong:text-card-foreground prose-code:rounded prose-code:bg-muted prose-code:px-1 prose-code:py-0.5 prose-code:text-foreground">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>

        {!isUser && (
          <div className="mt-1.5 flex gap-1 opacity-0 transition-opacity group-hover:opacity-100">
            <button onClick={handleCopy} className="rounded-lg p-1.5 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground">
              <Copy size={14} />
            </button>
            <button className="rounded-lg p-1.5 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground">
              <RefreshCw size={14} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
