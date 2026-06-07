import { motion } from "framer-motion";
import { ArrowRight, Sparkles, Brain, Shield, Zap, FileSearch } from "lucide-react";
import { Button } from "../ui/button";

interface LandingHeroProps {
  onStart: () => void;
}

const LandingHero = ({ onStart }: LandingHeroProps) => {
  return (
    <div className="relative h-screen w-full overflow-hidden bg-[#020202] text-white selection:bg-emerald-500/30">
      {/* Intense Cinematic Background */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-[-10%] right-[-5%] h-[80%] w-[60%] rounded-full bg-emerald-600/10 blur-[140px]" />
        <div className="absolute bottom-[-10%] left-[-5%] h-[80%] w-[60%] rounded-full bg-blue-700/10 blur-[140px]" />
      </div>

      {/* High-Visibility Tech Grid */}
      <div className="absolute inset-0 z-0 opacity-[0.08] [background-image:linear-gradient(to_right,#ffffff_1px,transparent_1px),linear-gradient(to_bottom,#ffffff_1px,transparent_1px)] [background-size:80px_80px]" />
      <div className="absolute inset-0 z-0 opacity-[0.04] [background-image:linear-gradient(to_right,#ffffff_1px,transparent_1px),linear-gradient(to_bottom,#ffffff_1px,transparent_1px)] [background-size:20px_20px]" />

      {/* Layout Container */}
      <div className="container relative z-10 mx-auto flex h-full items-center px-10">
        <div className="grid w-full grid-cols-1 gap-20 lg:grid-cols-12 items-center">
          
          {/* Left Side: Branding & Features */}
          <div className="lg:col-span-8 flex flex-col justify-center">
            {/* Version Protocol */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="mb-6 inline-flex"
            >
              <span className="rounded-sm bg-emerald-500/10 px-3 py-1 text-[9px] font-black uppercase tracking-[0.4em] text-emerald-500 border border-emerald-500/20">
                Protocol v1.0.4
              </span>
            </motion.div>

            {/* Main Title */}
            <motion.h1
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
              className="text-6xl font-[1000] leading-none tracking-[-0.06em] text-white sm:text-8xl lg:text-[8rem] whitespace-nowrap"
            >
              POLY-DOC <span className="bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent">CHAT</span>
            </motion.h1>

            {/* Tagline & Description */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="mt-8 space-y-4"
            >
              <h2 className="text-2xl font-black tracking-tight text-white sm:text-3xl">
                Precision Insight <span className="text-emerald-500">/</span> Zero Hallucination
              </h2>
              <p className="max-w-xl text-lg font-medium leading-relaxed text-slate-500">
                A high-fidelity RAG ecosystem for multi-document neural analysis. 
                Engineered for deterministic knowledge retrieval.
              </p>
            </motion.div>

            {/* Integrated Features */}
            <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-3 border-t border-white/5 pt-10">
              <FeatureItem 
                index="01"
                icon={<Brain size={20} strokeWidth={1} />}
                title="NEURAL RAG"
                desc="Context-strictly bound generation via ChromaDB persistence."
              />
              <FeatureItem 
                index="02"
                icon={<Shield size={20} strokeWidth={1} />}
                title="DATA ISOLATION"
                desc="Local embedding generation ensuring complete privacy."
              />
              <FeatureItem 
                index="03"
                icon={<FileSearch size={20} strokeWidth={1} />}
                title="DETERMINISTIC"
                desc="Source attribution with exact page referencing."
              />
            </div>
          </div>

          {/* Right Side: Large Initialize Button */}
          <div className="lg:col-span-4 flex justify-center lg:justify-end">
            <motion.div
              initial={{ opacity: 0, scale: 0.8, x: 50 }}
              animate={{ opacity: 1, scale: 1, x: 0 }}
              transition={{ duration: 1, delay: 0.6, ease: "easeOut" }}
            >
              <Button 
                onClick={onStart} 
                className="group relative h-64 w-64 rounded-full border border-white/10 bg-white text-2xl font-black text-black transition-all hover:bg-emerald-500 hover:text-white hover:scale-105 shadow-[0_0_80px_rgba(255,255,255,0.1)] active:scale-95 flex flex-col items-center justify-center gap-4"
              >
                <span className="relative z-10">INITIALIZE</span>
                <ArrowRight size={32} className="relative z-10 transition-transform duration-500 group-hover:translate-x-3" />
                
                {/* Visual Status Indicator inside button */}
                <div className="absolute bottom-10 flex flex-col items-center opacity-40 group-hover:opacity-100 transition-opacity">
                  <span className="text-[8px] font-black uppercase tracking-[0.3em]">Authorized Node</span>
                  <div className="mt-1 h-1 w-1 rounded-full bg-emerald-500 animate-pulse" />
                </div>
              </Button>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Decorative Bottom Line */}
      <div className="absolute bottom-0 left-0 h-1 w-full bg-gradient-to-r from-transparent via-emerald-500/20 to-transparent" />
    </div>
  );
};

const FeatureItem = ({ index, icon, title, desc }: { index: string, icon: React.ReactNode, title: string, desc: string }) => (
  <motion.div 
    initial={{ opacity: 0, x: 20 }}
    animate={{ opacity: 1, x: 0 }}
    className="group relative"
  >
    <div className="mb-4 flex items-center gap-4">
      <span className="text-[10px] font-black text-emerald-500/40">{index}</span>
      <div className="text-emerald-500 transition-colors group-hover:text-white">
        {icon}
      </div>
    </div>
    <h3 className="text-xs font-black uppercase tracking-[0.3em] text-white">{title}</h3>
    <p className="mt-2 text-[11px] leading-relaxed text-slate-500">{desc}</p>
  </motion.div>
);

export default LandingHero;
