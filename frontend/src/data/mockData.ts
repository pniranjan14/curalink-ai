import { Publication, ClinicalTrial, ChatMessage } from "@/types/chat";

export const mockPublications: Publication[] = [
  {
    source: "PubMed",
    id: "38291034",
    title: "Advances in Immunotherapy for Non-Small Cell Lung Cancer: A Comprehensive Review",
    authors: ["Chen Y", "Kumar S", "Patel R", "Zhang W"],
    journal: "Journal of Clinical Oncology",
    pubdate: "2024 Jan",
    abstract: "This comprehensive review examines recent advances in immunotherapy treatments for non-small cell lung cancer (NSCLC), including checkpoint inhibitors, CAR-T cell therapy, and combination approaches. We analyzed data from 47 clinical trials involving over 12,000 patients...",
    url: "https://pubmed.ncbi.nlm.nih.gov/38291034/",
    relevance_score: 0.9542,
  },
  {
    source: "OpenAlex",
    id: "W4391234567",
    title: "Machine Learning Approaches in Early Detection of Pulmonary Malignancies",
    authors: ["Sharma A", "Liu X", "Thompson J"],
    journal: "Nature Medicine",
    pubdate: "2024",
    abstract: "We present a novel deep learning framework for early detection of lung cancer using low-dose CT scans. Our model achieved 94.3% sensitivity and 91.7% specificity across a multi-center validation cohort...",
    url: "https://doi.org/10.1038/s41591-024-0001",
    relevance_score: 0.8891,
  },
  {
    source: "PubMed",
    id: "38105672",
    title: "Targeted Therapy in EGFR-Mutated Lung Adenocarcinoma: Current Landscape and Future Directions",
    authors: ["Nakamura T", "Lee H", "Garcia M"],
    journal: "The Lancet Oncology",
    pubdate: "2023 Dec",
    abstract: "EGFR-mutated lung adenocarcinoma represents approximately 15-20% of all NSCLC cases. Third-generation TKIs have revolutionized treatment outcomes with improved progression-free survival...",
    url: "https://pubmed.ncbi.nlm.nih.gov/38105672/",
    relevance_score: 0.8234,
  },
];

export const mockTrials: ClinicalTrial[] = [
  {
    source: "ClinicalTrials",
    nct_id: "NCT05847291",
    title: "Phase III Study of Pembrolizumab Plus Chemotherapy vs Chemotherapy Alone in Advanced NSCLC",
    status: "RECRUITING",
    phase: "Phase 3",
    start_date: "2024-01",
    completion_date: "2026-06",
    summary: "A randomized, double-blind study evaluating the efficacy and safety of pembrolizumab in combination with platinum-based chemotherapy compared to chemotherapy alone in participants with previously untreated advanced NSCLC.",
    url: "https://clinicaltrials.gov/study/NCT05847291",
    relevance_score: 0.9123,
  },
  {
    source: "ClinicalTrials",
    nct_id: "NCT05923456",
    title: "Evaluating Novel CAR-T Cell Therapy for EGFR-Positive Lung Cancer",
    status: "ACTIVE, NOT RECRUITING",
    phase: "Phase 2",
    start_date: "2023-06",
    completion_date: "2025-12",
    summary: "This study evaluates a novel chimeric antigen receptor T-cell therapy targeting EGFR in patients with advanced, treatment-resistant non-small cell lung cancer.",
    url: "https://clinicaltrials.gov/study/NCT05923456",
    relevance_score: 0.8567,
  },
];

export const mockWelcomeMessages: ChatMessage[] = [];

export const exampleQueries = [
  "I have lung cancer and I'm in Mumbai",
  "I'm diagnosed with type 2 diabetes in London",
  "Parkinson's disease, located in New York",
  "What are the latest treatments for breast cancer?",
];
