import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface CaseData {
  id: string;
  case_number: string;
  title: string;
  description?: string;
  category: string;
  status: string;
  priority: string;
  officer_name: string;
  ncrp_complaint_number?: string;
  created_at: string;
}

export interface AnalysisResultData {
  module_type: string;
  ai_generation_score?: number;
  manipulation_score?: number;
  provenance_score?: number;
  confidence?: number;
  c2pa_status?: string;
  watermark_status?: string;
  explanation?: string;
  heatmap_path?: string;
  details?: any;
}

export interface FullAnalysisData {
  media_item_id: string;
  original_filename: string;
  sha256_hash: string;
  media_type: string;
  analysis_status: string;
  results: AnalysisResultData[];
  fusion_summary?: any;
}

export const fetchCases = async (): Promise<CaseData[]> => {
  const res = await api.get("/api/v1/cases/");
  return res.data.cases || [];
};

export const fetchCaseById = async (caseId: string): Promise<CaseData> => {
  const res = await api.get(`/api/v1/cases/${caseId}`);
  return res.data;
};

export const createCase = async (payload: any): Promise<CaseData> => {
  const res = await api.post("/api/v1/cases/", payload);
  return res.data;
};

export const uploadMediaForAnalysis = async (caseId: string, file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await api.post(`/api/v1/analysis/upload/${caseId}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};

export const fetchAnalysisResults = async (mediaItemId: string): Promise<FullAnalysisData> => {
  const res = await api.get(`/api/v1/analysis/results/${mediaItemId}`);
  return res.data;
};

export const fetchMediaItemsForCase = async (caseId: string) => {
  const res = await api.get(`/api/v1/analysis/case/${caseId}/media`);
  return res.data;
};

export const downloadBsaCertificate = async (mediaItemId: string, officerName: string) => {
  const res = await api.post("/api/v1/reports/generate", {
    media_item_id: mediaItemId,
    report_type: "bsa_certificate",
    officer_name: officerName,
  }, { responseType: "blob" });
  return res.data;
};
