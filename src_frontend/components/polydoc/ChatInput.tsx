import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";

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
    <div className="border-t border-border bg-card/80 p-4 backdrop-blur-sm">
      <div className="mx-auto flex max-w-3xl items-end gap-3 rounded-2xl border border-border bg-card p-2 shadow-sm">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your document..."
          rows={1}
          className="flex-1 resize-none bg-transparent px-2 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none"
        />
        <button
          onClick={handleSend}
          disabled={!value.trim() || isLoading}
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-r from-orange-500 to-pink-500 text-white shadow-sm transition-all duration-200 hover:scale-105 hover:shadow-md disabled:opacity-40 disabled:hover:scale-100"
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
