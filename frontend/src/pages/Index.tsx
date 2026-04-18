import { useState } from "react";
import ChatWindow from "@/components/chat/ChatWindow";
import InputBar from "@/components/chat/InputBar";
import ResearchSidebar from "@/components/research/ResearchSidebar";
import { useChatStore } from "@/hooks/useChatStore";
import { RefreshCw, Activity, PanelRight } from "lucide-react";

const Index = () => {
  const store = useChatStore();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex flex-col h-screen bg-background relative overflow-hidden">
      {/* Ambient background orbs */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="ambient-orb absolute -top-32 -left-32 w-96 h-96 rounded-full bg-primary/[0.04] blur-3xl" />
        <div className="ambient-orb-delay absolute -bottom-48 -right-48 w-[500px] h-[500px] rounded-full bg-secondary/[0.03] blur-3xl" />
      </div>

      {/* Header */}
      <header className="relative z-20 flex items-center justify-between px-5 py-3 glass glass-border">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl gradient-primary flex items-center justify-center shadow-glow">
            <Activity size={17} className="text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-sm font-extrabold text-foreground tracking-tight">
              CuraLink
            </h1>
            <p className="text-[10px] text-muted-foreground font-medium">
              AI Medical Research Assistant
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {store.disease && (
            <div className="hidden sm:flex items-center gap-2 mr-3">
              <span className="text-[10px] text-primary bg-primary/10 px-3 py-1 rounded-full font-semibold glass-border">
                {store.disease}
              </span>
              {store.location && (
                <span className="text-[10px] text-secondary bg-secondary/10 px-3 py-1 rounded-full font-semibold glass-border">
                  {store.location}
                </span>
              )}
            </div>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-xl text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-all duration-200"
            title="Toggle research panel"
          >
            <PanelRight size={16} />
          </button>
          <button
            onClick={store.clearSession}
            className="p-2 rounded-xl text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-all duration-200"
            title="New conversation"
          >
            <RefreshCw size={15} />
          </button>
        </div>
      </header>

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden relative z-10">
        {/* Chat area */}
        <div className="flex-1 flex flex-col min-w-0">
          <ChatWindow
            messages={store.messages}
            loading={store.loading}
            onExampleClick={store.handleSend}
          />
          <InputBar onSend={store.handleSend} loading={store.loading} />
        </div>

        {/* Research sidebar */}
        <ResearchSidebar
          publications={store.publications}
          trials={store.trials}
          disease={store.disease}
          location={store.location}
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen(!sidebarOpen)}
        />
      </div>
    </div>
  );
};

export default Index;
