import { useEffect, useRef } from "react";
import { ChatMessage } from "@/types/chat";
import ChatMessageBubble from "./ChatMessageBubble";
import TypingIndicator from "./TypingIndicator";
import { Sparkles, Zap } from "lucide-react";
import { motion } from "framer-motion";

interface ChatWindowProps {
  messages: ChatMessage[];
  loading: boolean;
  onExampleClick: (query: string) => void;
}

const exampleQueries = [
  { text: "I have lung cancer and I'm in Mumbai", icon: "🫁" },
  { text: "I'm diagnosed with type 2 diabetes in London", icon: "💉" },
  { text: "Parkinson's disease, located in New York", icon: "🧠" },
];

const ChatWindow = ({ messages, loading, onExampleClick }: ChatWindowProps) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-8">
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center max-w-lg mx-auto">
          <motion.div
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.6, type: "spring", bounce: 0.4 }}
            className="relative mb-8"
          >
            <div className="w-20 h-20 rounded-2xl gradient-primary flex items-center justify-center shadow-glow pulse-ring">
              <Zap size={32} className="text-primary-foreground" />
            </div>
            <div className="absolute -top-1 -right-1 w-5 h-5 rounded-full gradient-accent flex items-center justify-center">
              <Sparkles size={10} className="text-accent-foreground" />
            </div>
          </motion.div>

          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <h2 className="text-3xl font-extrabold text-foreground mb-2 tracking-tight">
              Hey, I'm <span className="text-gradient-primary">CuraLink</span>
            </h2>
            <p className="text-muted-foreground text-sm leading-relaxed mb-1">
              Your AI-powered medical research companion
            </p>
            <p className="text-muted-foreground/50 text-xs max-w-sm mx-auto">
              Tell me your condition and location — I'll find relevant research publications and clinical trials for you.
            </p>
          </motion.div>

          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="mt-10 w-full max-w-sm space-y-2"
          >
            <p className="text-[11px] text-muted-foreground font-semibold uppercase tracking-widest mb-3">
              Try asking
            </p>
            {exampleQueries.map((example) => (
              <button
                key={example.text}
                onClick={() => onExampleClick(example.text)}
                className="w-full text-left text-sm text-muted-foreground glass glass-border rounded-2xl px-4 py-3.5
                           hover:border-primary/30 hover:text-foreground hover:shadow-glow/10
                           transition-all duration-300 group flex items-center gap-3"
              >
                <span className="text-base">{example.icon}</span>
                <span className="opacity-70 group-hover:opacity-100 transition-opacity">
                  {example.text}
                </span>
              </button>
            ))}
          </motion.div>
        </div>
      )}

      <div className="max-w-3xl mx-auto">
        {messages.map((msg) => (
          <ChatMessageBubble key={msg.id} message={msg} />
        ))}

        {loading && <TypingIndicator />}
      </div>

      <div ref={bottomRef} />
    </div>
  );
};

export default ChatWindow;
