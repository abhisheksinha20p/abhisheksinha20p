import { motion } from "framer-motion";
import { ContributionShooter } from "./components/ContributionShooter";
import { ArchitectureAnimation } from "./components/ArchitectureAnimation";
import { TechStackAnimation } from "./components/TechStackAnimation";
import { CareerTimeline } from "./components/CareerTimeline";

export default function App() {
  return (
    <main className="app-shell">
      <motion.header
        className="hero"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="eyebrow">FRONTLINE DEPLOYMENT ENGINEER</div>
        <h1>ABHISHEK SINHA</h1>
        <p>Build · Deploy · Observe · Automate</p>
      </motion.header>

      <ContributionShooter />
      <ArchitectureAnimation />
      <TechStackAnimation />
      <CareerTimeline />
    </main>
  );
}
