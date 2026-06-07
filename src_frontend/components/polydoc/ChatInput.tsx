import { useState, useRef, useEffect } from "react";
import { Send, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

const ChatInput = ({ onSend, isLoading }: ChatInputProps) => {
  const [value, setValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px';
    }
  }, [value]);

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed || isLoading) return;
    onSend(trimmed);
    setValue('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative mx-auto w-full max-w-5xl"
    >
      <div className="relative flex items-end gap-3 rounded-[2.5rem] border border-slate-800/50 bg-slate-900/40 p-4 shadow-[0_0_50px_rgba(0,0,0,0.5)] backdrop-blur-3xl focus-within:border-indigo-500/40 transition-all duration-500">
        <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
          <Sparkles size={24} />
        </div>
        <textarea
          ref={textareaRef}
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Inquire about ingested documentation..."
          rows={1}
          className="flex-1 resize-none bg-transparent px-3 py-4 text-base text-slate-200 placeholder:text-slate-600 focus:outline-none font-medium"
        />
        <motion.button
          onClick={handleSend}
          disabled={!value.trim() || isLoading}
          whileHover={{ scale: 1.05, boxShadow: "0 0 20px rgba(79,70,229,0.4)" }}
          whileTap={{ scale: 0.95 }}
          className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-indigo-600 text-white shadow-2xl shadow-indigo-600/20 transition-all duration-300 disabled:opacity-20 disabled:grayscale"
        >
          <Send size={22} />
        </motion.button>
      </div>
      <p className="mt-4 text-center text-[9px] font-black uppercase tracking-[0.4em] text-slate-700">
        Neural Core Llama 3.3 • Deterministic Context Retrieval
      </p>
    </motion.div>
  );
};

export default ChatInput;
