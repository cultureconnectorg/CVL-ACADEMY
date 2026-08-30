import { useEffect, useRef, useState } from "react";
import { SparksSolid, SendDiagonal, Xmark } from "iconoir-react";
import { api } from "@/lib/api";
import { useI18n } from "@/lib/i18n.jsx";
import { toast } from "sonner";

export default function MentorPanel() {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  const [msg, setMsg] = useState("");
  const [messages, setMessages] = useState([
    { role: "assistant", content: t("mentor_intro") },
  ]);
  const [sending, setSending] = useState(false);
  const [sessionId] = useState(() => `mentor-${Date.now()}`);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  const send = async () => {
    const text = msg.trim();
    if (!text || sending) return;
    setSending(true);
    setMessages((m) => [...m, { role: "user", content: text }]);
    setMsg("");
    try {
      const { data } = await api.post("/mentor/chat", { message: text, session_id: sessionId });
      setMessages((m) => [...m, { role: "assistant", content: data.reply }]);
    } catch {
      toast.error("Mentor CVLN indisponible pour l'instant.");
    } finally {
      setSending(false);
    }
  };

  return (
    <>
      {/* FAB */}
      <button
        data-testid="mentor-fab"
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-40 rounded-full w-14 h-14 bg-[--cvln-orange] text-white flex items-center justify-center shadow-lg hover:scale-110 hover:-translate-y-1 transition"
        aria-label="Ouvrir le Mentor CVLN"
      >
        <SparksSolid width={22} height={22} />
      </button>

      {/* Panel */}
      {open && (
        <div className="fixed inset-0 z-50 flex justify-end" data-testid="mentor-panel">
          <button
            type="button"
            aria-label="Fermer le Mentor CVLN"
            className="absolute inset-0 bg-black/20 cursor-default"
            onClick={() => setOpen(false)}
          />
          <div className="relative h-full w-full max-w-md glass flex flex-col fade-in">
            {/* header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-black/5">
              <div>
                <div className="font-display font-bold text-lg tracking-tight">Mentor CVLN</div>
                <div className="text-xs text-[--cvln-ink-2]">Premier agent · CVLN Agent Factory</div>
              </div>
              <button
                data-testid="mentor-close"
                onClick={() => setOpen(false)}
                className="w-9 h-9 rounded-full hover:bg-black/5 flex items-center justify-center"
              >
                <Xmark width={18} height={18} />
              </button>
            </div>
            {/* messages */}
            <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[85%] px-4 py-3 rounded-2xl text-sm leading-relaxed
                      ${m.role === "user"
                        ? "bg-white border border-black/10 text-[--cvln-ink]"
                        : "bg-gradient-to-br from-[#FFE9DE] to-[#FBD3B8] text-[--cvln-ink]"}`}
                  >
                    {m.content}
                  </div>
                </div>
              ))}
              {sending && (
                <div className="flex justify-start">
                  <div className="bg-gradient-to-br from-[#FFE9DE] to-[#FBD3B8] px-4 py-3 rounded-2xl text-sm text-[--cvln-ink-2]">
                    …
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
            {/* input */}
            <div className="p-4 border-t border-black/5 bg-white/60">
              <div className="flex items-center gap-2">
                <input
                  data-testid="mentor-input"
                  value={msg}
                  onChange={(e) => setMsg(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && send()}
                  placeholder={t("mentor_placeholder")}
                  disabled={sending}
                  className="flex-1 bg-white border border-black/10 rounded-full px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[--cvln-orange]"
                />
                <button
                  data-testid="mentor-send"
                  onClick={send}
                  disabled={sending}
                  className="w-11 h-11 rounded-full bg-[--cvln-orange] text-white flex items-center justify-center hover:bg-[--cvln-orange-2] disabled:opacity-50 transition"
                >
                  <SendDiagonal width={18} height={18} />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
