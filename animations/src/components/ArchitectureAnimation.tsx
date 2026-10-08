import { motion } from "framer-motion";
import { Activity, Database, Globe, Server, Zap } from "lucide-react";

const nodes = [
  { label: "CLIENT", icon: Globe },
  { label: "GATEWAY", icon: Zap },
  { label: "SERVICES", icon: Server },
  { label: "DATABASE", icon: Database },
  { label: "OBSERVE", icon: Activity },
];

export function ArchitectureAnimation() {
  return (
    <section className="scene">
      <div className="scene-label">PRODUCTION PIPELINE</div>

      <div className="architecture">
        {nodes.map((node, index) => {
          const Icon = node.icon;

          return (
            <div className="architecture-node" key={node.label}>
              <motion.div
                className="node-card"
                whileHover={{ y: -8, scale: 1.04 }}
                animate={{
                  boxShadow: [
                    "0 0 0 rgba(97,218,251,0)",
                    "0 0 28px rgba(97,218,251,.18)",
                    "0 0 0 rgba(97,218,251,0)",
                  ],
                }}
                transition={{
                  duration: 2.5,
                  repeat: Infinity,
                  delay: index * 0.3,
                }}
              >
                <Icon size={24} />
                <span>{node.label}</span>
              </motion.div>

              {index < nodes.length - 1 && (
                <motion.div
                  className="pipeline"
                  animate={{ opacity: [0.2, 1, 0.2] }}
                  transition={{
                    duration: 1.3,
                    repeat: Infinity,
                    delay: index * 0.25,
                  }}
                >
                  <span />
                </motion.div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
