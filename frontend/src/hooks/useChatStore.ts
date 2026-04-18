import { useState, useCallback } from "react";
import { ChatMessage, Publication, ClinicalTrial } from "@/types/chat";
import { sendMessage } from "@/services/api";

const getStoredSessionId = () => localStorage.getItem('curalink_session_id');
const storeSessionId = (id: string) => localStorage.setItem('curalink_session_id', id);

export const useChatStore = () => {
  const [sessionId, setSessionId] = useState<string | null>(getStoredSessionId());
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [publications, setPublications] = useState<Publication[]>([]);
  const [trials, setTrials] = useState<ClinicalTrial[]>([]);
  const [disease, setDisease] = useState("");
  const [location, setLocation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const addMessage = useCallback((role: "user" | "assistant", content: string) => {
    const msg: ChatMessage = {
      id: crypto.randomUUID(),
      role,
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, msg]);
  }, []);

  const handleSend = useCallback(
    async (userMessage: string) => {
      if (!userMessage.trim()) return;
      
      addMessage("user", userMessage);
      setLoading(true);
      setError(null);

      try {
        console.log("Sending message to backend:", userMessage);
        const data = await sendMessage(userMessage, sessionId);
        console.log("Backend response received:", data);
        
        // Update session ID if it's the first message
        if (data.session_id && data.session_id !== sessionId) {
          console.log("Updating session ID to:", data.session_id);
          setSessionId(data.session_id);
          storeSessionId(data.session_id);
        }

        // Update state with backend response
        setMessages((prev) => [...prev, {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: data.response,
          timestamp: new Date()
        }]);

        if (data.publications) setPublications(data.publications);
        if (data.trials) setTrials(data.trials);
        if (data.disease) setDisease(data.disease);
        if (data.location) setLocation(data.location);

      } catch (err: any) {
        console.error("Chat error:", err);
        const errMsg = err.response?.data?.detail || "Something went wrong. Please check if the backend is running.";
        setError(errMsg);
        
        addMessage("assistant", `**Error**: ${errMsg}`);
      } finally {
        setLoading(false);
      }
    },
    [addMessage, sessionId]
  );

  const clearSession = useCallback(() => {
    localStorage.removeItem('curalink_session_id');
    setSessionId(null);
    setMessages([]);
    setPublications([]);
    setTrials([]);
    setDisease("");
    setLocation("");
    setError(null);
  }, []);

  return {
    sessionId,
    messages,
    publications,
    trials,
    disease,
    location,
    loading,
    error,
    handleSend,
    clearSession,
  };
};
