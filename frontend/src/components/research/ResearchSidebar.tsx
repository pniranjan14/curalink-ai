import { Publication, ClinicalTrial } from "@/types/chat";
import ResearchCard from "./ResearchCard";
import ClinicalTrialCard from "./ClinicalTrialCard";
import { BookOpen, FlaskConical, MapPin, Stethoscope, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface ResearchSidebarProps {
  publications: Publication[];
  trials: ClinicalTrial[];
  disease: string;
  location: string;
  isOpen: boolean;
  onToggle: () => void;
}

const ResearchSidebar = ({
  publications,
  trials,
  disease,
  location,
  isOpen,
  onToggle,
}: ResearchSidebarProps) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ width: 0, opacity: 0 }}
          animate={{ width: 380, opacity: 1 }}
          exit={{ width: 0, opacity: 0 }}
          transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          className="flex-shrink-0 border-l border-border/50 bg-card/50 backdrop-blur-sm overflow-hidden flex flex-col"
        >
          <div className="w-[380px] flex flex-col h-full">
            {/* Header */}
            <div className="p-4 border-b border-border/50 flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-foreground flex items-center gap-2">
                  <BookOpen size={15} className="text-primary" />
                  Research Panel
                </h2>
                {disease && (
                  <div className="flex gap-2 mt-2 flex-wrap">
                    <span className="text-[10px] flex items-center gap-1 text-primary bg-primary/10 px-2 py-0.5 rounded-full font-medium">
                      <Stethoscope size={10} /> {disease}
                    </span>
                    {location && (
                      <span className="text-[10px] flex items-center gap-1 text-secondary bg-secondary/10 px-2 py-0.5 rounded-full font-medium">
                        <MapPin size={10} /> {location}
                      </span>
                    )}
                  </div>
                )}
              </div>
              <button
                onClick={onToggle}
                className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-all"
              >
                <X size={16} />
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
              {publications.length > 0 && (
                <div>
                  <h3 className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-3 flex items-center gap-2">
                    <BookOpen size={10} />
                    Publications ({publications.length})
                  </h3>
                  <div className="space-y-2.5">
                    {publications.map((pub, i) => (
                      <ResearchCard key={pub.id || i} pub={pub} />
                    ))}
                  </div>
                </div>
              )}

              {trials.length > 0 && (
                <div>
                  <h3 className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-3 flex items-center gap-2">
                    <FlaskConical size={10} />
                    Clinical Trials ({trials.length})
                  </h3>
                  <div className="space-y-2.5">
                    {trials.map((trial, i) => (
                      <ClinicalTrialCard key={trial.nct_id || i} trial={trial} />
                    ))}
                  </div>
                </div>
              )}

              {publications.length === 0 && trials.length === 0 && (
                <div className="text-center py-20">
                  <div className="w-12 h-12 rounded-2xl glass glass-border flex items-center justify-center mx-auto mb-4">
                    <BookOpen size={20} className="text-muted-foreground/30" />
                  </div>
                  <p className="text-xs text-muted-foreground/40 font-medium">
                    Research results will appear here
                  </p>
                  <p className="text-[10px] text-muted-foreground/25 mt-1">
                    Start a conversation to see publications & trials
                  </p>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default ResearchSidebar;
