import { Copy, User, Sparkles, Check } from "lucide-react";
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
    <div className={`flex gap-8 ${isUser ? 'flex-row-reverse' : 'flex-row'} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
      <div className={`flex h-12 w-12 shrink-0 items-center justify-center border transition-all ${
        isUser
          ? 'bg-white/5 border-white/10 text-white'
          : 'bg-emerald-500/5 border-emerald-500/20 text-emerald-500'
      }`}>
        {isUser
          ? <User size={20} strokeWidth={1.5} />
          : <Sparkles size={20} strokeWidth={1.5} />
        }
      </div>

      <div className={`flex max-w-[80%] flex-col max-w-[80%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`px-8 py-5 shadow-2xl ${
          isUser
            ? 'bg-white text-black font-black'
            : 'bg-[#0a0a0a] border border-white/10 text-white font-medium'
        }`}>
          {isUser ? (
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none dark:prose-invert prose-p:leading-relaxed prose-p:text-white prose-p:opacity-100 prose-pre:bg-[#050505] prose-pre:border prose-pre:border-white/5 prose-headings:font-black prose-headings:text-white prose-headings:uppercase prose-headings:tracking-widest prose-li:text-white prose-li:opacity-100 prose-strong:text-emerald-400 prose-strong:font-black prose-strong:opacity-100">
              <Markdown>{message.content}</Markdown>
            </div>
          )}
        </div>

        <div className="mt-3 flex items-center gap-4 px-1">
          <span className="text-[9px] font-black uppercase tracking-[0.3em] text-slate-700">
            {isUser ? "Client Request" : "Neural Output"}
          </span>
          {!isUser && (
            <button 
              onClick={handleCopy} 
              className="opacity-0 transition-opacity group-hover:opacity-100 text-slate-600 hover:text-emerald-500"
              title="Copy response"
            >
              {copied ? <Check size={12} className="text-emerald-500" /> : <Copy size={12} />}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
