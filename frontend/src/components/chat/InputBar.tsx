import { useState, useRef, KeyboardEvent } from "react";
import { Send, Loader2 } from "lucide-react";

interface InputBarProps {
  onSend: (message: string) => void;
  loading: boolean;
}

const InputBar = ({ onSend, loading }: InputBarProps) => {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (!value.trim() || loading) return;
    onSend(value.trim());
    setValue("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="relative z-10 px-4 pb-4 pt-2 sm:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="flex gap-3 items-end glass glass-border rounded-2xl p-2">
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your condition and location..."
            rows={1}
            className="flex-1 resize-none bg-transparent px-3 py-2.5
                       text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none
                       transition-all duration-200"
            disabled={loading}
          />
          <button
            onClick={handleSubmit}
            disabled={loading || !value.trim()}
            className="flex-shrink-0 w-10 h-10 rounded-xl gradient-primary shadow-glow
                       disabled:opacity-30 disabled:cursor-not-allowed disabled:shadow-none
                       flex items-center justify-center transition-all duration-200
                       hover:scale-105 active:scale-95"
          >
            {loading ? (
              <Loader2 size={16} className="animate-spin text-primary-foreground" />
            ) : (
              <Send size={16} className="text-primary-foreground" />
            )}
          </button>
        </div>
        <p className="text-[10px] text-muted-foreground/30 text-center mt-2 font-medium">
          Enter to send · Shift+Enter for new line · For research purposes only
        </p>
      </div>
    </div>
  );
};

export default InputBar;
