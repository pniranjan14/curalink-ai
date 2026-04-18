import { Zap } from "lucide-react";

const TypingIndicator = () => (
  <div className="flex gap-3 mb-5">
    <div className="flex-shrink-0 w-8 h-8 rounded-xl gradient-accent flex items-center justify-center">
      <Zap size={14} className="text-accent-foreground" />
    </div>
    <div className="glass glass-border rounded-2xl rounded-tl-md px-5 py-4 flex items-center gap-1.5">
      <span className="w-2 h-2 rounded-full bg-primary/60 typing-dot" />
      <span className="w-2 h-2 rounded-full bg-primary/60 typing-dot" />
      <span className="w-2 h-2 rounded-full bg-primary/60 typing-dot" />
    </div>
  </div>
);

export default TypingIndicator;
