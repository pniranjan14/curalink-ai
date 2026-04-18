export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Publication {
  source: string;
  id: string;
  title: string;
  authors: string[];
  journal: string;
  pubdate: string;
  abstract: string;
  url: string;
  relevance_score?: number;
}

export interface ClinicalTrial {
  source: string;
  nct_id: string;
  title: string;
  status: string;
  phase: string;
  start_date: string;
  completion_date: string;
  summary: string;
  url: string;
  relevance_score?: number;
}

export interface ChatSession {
  sessionId: string | null;
  messages: ChatMessage[];
  publications: Publication[];
  trials: ClinicalTrial[];
  disease: string;
  location: string;
  loading: boolean;
}
