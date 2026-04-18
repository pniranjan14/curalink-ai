import { ClinicalTrial } from "@/types/chat";
import { ExternalLink, Activity } from "lucide-react";
import { motion } from "framer-motion";

interface ClinicalTrialCardProps {
  trial: ClinicalTrial;
}

const statusStyles: Record<string, string> = {
  RECRUITING: "text-primary bg-primary/10",
  COMPLETED: "text-secondary bg-secondary/10",
  "ACTIVE, NOT RECRUITING": "text-yellow-400 bg-yellow-400/10",
  TERMINATED: "text-destructive bg-destructive/10",
};

const ClinicalTrialCard = ({ trial }: ClinicalTrialCardProps) => {
  const colorClass = statusStyles[trial.status] || "text-muted-foreground bg-muted";

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass glass-border rounded-xl p-3.5 hover:border-secondary/20 transition-all duration-300 group"
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex items-center gap-2">
          <Activity size={12} className="text-secondary flex-shrink-0" />
          <span className={`text-[9px] font-semibold px-2 py-0.5 rounded-full ${colorClass}`}>
            {trial.status}
          </span>
        </div>
        <a
          href={trial.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-muted-foreground hover:text-secondary flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <ExternalLink size={12} />
        </a>
      </div>

      <h4 className="text-xs font-semibold text-foreground leading-snug mb-2 group-hover:text-secondary transition-colors">
        {trial.title}
      </h4>

      <div className="flex gap-3 text-[10px] text-muted-foreground mb-2">
        {trial.phase && <span>Phase: {trial.phase}</span>}
        {trial.start_date && <span>Start: {trial.start_date}</span>}
      </div>

      {trial.summary && (
        <p className="text-[10px] text-muted-foreground/50 leading-relaxed line-clamp-3">
          {trial.summary}
        </p>
      )}

      <p className="text-[9px] text-muted-foreground/30 mt-2 font-mono">{trial.nct_id}</p>
    </motion.div>
  );
};

export default ClinicalTrialCard;
