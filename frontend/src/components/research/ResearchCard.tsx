import { useState } from "react";
import { Publication } from "@/types/chat";
import { ExternalLink, ChevronDown, ChevronUp, BookOpen } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface ResearchCardProps {
  pub: Publication;
}

const ResearchCard = ({ pub }: ResearchCardProps) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass glass-border rounded-xl p-3.5 hover:border-primary/20 transition-all duration-300 group"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2 mb-2">
          <BookOpen size={12} className="text-primary flex-shrink-0" />
          <span className="text-[9px] font-semibold text-primary bg-primary/10 px-2 py-0.5 rounded-full">
            {pub.source}
          </span>
          {pub.relevance_score && (
            <span className="text-[9px] text-muted-foreground">
              {Math.round(pub.relevance_score * 100)}% match
            </span>
          )}
        </div>
        <a
          href={pub.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-muted-foreground hover:text-primary flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <ExternalLink size={12} />
        </a>
      </div>

      <h4 className="text-xs font-semibold text-foreground leading-snug mb-2 line-clamp-2 group-hover:text-primary transition-colors">
        {pub.title}
      </h4>

      {pub.authors?.length > 0 && (
        <p className="text-[10px] text-muted-foreground mb-1">
          {pub.authors.slice(0, 2).join(", ")}
          {pub.authors.length > 2 ? ` +${pub.authors.length - 2} more` : ""}
        </p>
      )}

      {pub.journal && (
        <p className="text-[10px] text-muted-foreground/50 italic mb-2">
          {pub.journal} · {pub.pubdate}
        </p>
      )}

      {pub.abstract && (
        <>
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-[10px] text-secondary flex items-center gap-1 hover:opacity-80 transition-opacity font-medium"
          >
            {expanded ? <ChevronUp size={11} /> : <ChevronDown size={11} />}
            {expanded ? "Hide abstract" : "Show abstract"}
          </button>
          <AnimatePresence>
            {expanded && (
              <motion.p
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="text-[10px] text-muted-foreground mt-2 leading-relaxed overflow-hidden"
              >
                {pub.abstract.slice(0, 400)}...
              </motion.p>
            )}
          </AnimatePresence>
        </>
      )}
    </motion.div>
  );
};

export default ResearchCard;
