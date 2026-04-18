import { ChatMessage } from "@/types/chat";
import ReactMarkdown from "react-markdown";
import { User, Zap } from "lucide-react";
import { motion } from "framer-motion";

interface ChatMessageBubbleProps {
  message: ChatMessage;
}

const ChatMessageBubble = ({ message }: ChatMessageBubbleProps) => {
  const isUser = message.role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
      className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"} mb-5`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center ${
          isUser ? "gradient-primary shadow-glow" : "gradient-accent"
        }`}
      >
        {isUser ? (
          <User size={14} className="text-primary-foreground" />
        ) : (
          <Zap size={14} className="text-accent-foreground" />
        )}
      </div>

      {/* Bubble */}
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? "gradient-primary text-primary-foreground rounded-tr-md"
            : "glass glass-border text-foreground rounded-tl-md"
        }`}
      >
        {isUser ? (
          <p>{message.content}</p>
        ) : (
          <ReactMarkdown
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              strong: ({ children }) => (
                <strong className="text-foreground font-semibold">{children}</strong>
              ),
              ul: ({ children }) => (
                <ul className="list-disc ml-4 mb-2 space-y-1">{children}</ul>
              ),
              li: ({ children }) => <li className="text-muted-foreground">{children}</li>,
              a: ({ children, href }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary underline underline-offset-2 hover:text-primary/80 transition-colors"
                >
                  {children}
                </a>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
        <span className="text-[10px] opacity-30 mt-2 block text-right font-medium">
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </div>
    </motion.div>
  );
};

export default ChatMessageBubble;
