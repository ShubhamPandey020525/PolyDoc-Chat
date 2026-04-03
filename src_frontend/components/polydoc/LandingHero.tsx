import { FileText, Sparkles, MessageSquare, Upload } from "lucide-react";

interface LandingHeroProps {
  onStart: () => void;
}

const LandingHero = ({ onStart }: LandingHeroProps) => {
  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-4">
      {/* Decorative background shapes */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-20 -top-20 h-72 w-72 rounded-full bg-gradient-to-br from-orange-200/40 to-pink-200/40 blur-3xl" />
        <div className="absolute -bottom-32 -right-20 h-96 w-96 rounded-full bg-gradient-to-br from-pink-200/30 to-purple-200/30 blur-3xl" />
        <div className="absolute left-1/2 top-1/4 h-48 w-48 -translate-x-1/2 rounded-full bg-gradient-to-br from-orange-100/30 to-yellow-100/30 blur-2xl" />
      </div>

      {/* Floating icons */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-[15%] top-[20%] animate-bounce text-orange-300/40" style={{ animationDuration: '3s' }}>
          <FileText size={32} />
        </div>
        <div className="absolute right-[18%] top-[25%] animate-bounce text-pink-300/40" style={{ animationDuration: '4s', animationDelay: '1s' }}>
          <MessageSquare size={28} />
        </div>
        <div className="absolute bottom-[30%] left-[20%] animate-bounce text-purple-300/40" style={{ animationDuration: '3.5s', animationDelay: '0.5s' }}>
          <Sparkles size={24} />
        </div>
        <div className="absolute bottom-[25%] right-[15%] animate-bounce text-orange-300/40" style={{ animationDuration: '4.5s', animationDelay: '1.5s' }}>
          <Upload size={26} />
        </div>
      </div>

      {/* Content */}
      <div className="relative z-10 flex max-w-2xl flex-col items-center text-center">
        <div className="mb-6 flex items-center gap-2 rounded-full border border-orange-200/50 bg-white/60 px-4 py-2 shadow-sm backdrop-blur-sm">
          <Sparkles size={16} className="text-orange-500" />
          <span className="text-sm font-medium text-orange-700">AI-Powered Document Chat</span>
        </div>

        <h1 className="mb-4 bg-gradient-to-r from-orange-600 via-pink-500 to-purple-500 bg-clip-text text-5xl font-bold tracking-tight text-transparent sm:text-6xl md:text-7xl">
          PolyDoc Chat
        </h1>

        <p className="mb-3 text-xl font-medium text-foreground/80 sm:text-2xl">
          Chat with your documents instantly using AI.
        </p>

        <p className="mb-10 max-w-md text-muted-foreground">
          Upload a document and ask questions about it. Get instant, intelligent answers powered by AI.
        </p>

        <button
          onClick={onStart}
          className="group relative rounded-2xl bg-gradient-to-r from-orange-500 via-pink-500 to-purple-500 px-10 py-4 text-lg font-semibold text-white shadow-lg shadow-orange-500/25 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-orange-500/30 active:scale-[0.98]"
        >
          <span className="relative z-10">Let's Get Started</span>
          <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-orange-400 via-pink-400 to-purple-400 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
          <span className="relative z-10" />
        </button>
      </div>
    </div>
  );
};

export default LandingHero;
