import { motion } from "framer-motion";
import { Crosshair, Rocket, Target } from "lucide-react";

const stars = Array.from({ length: 70 }, (_, i) => ({
  id: i,
  left: `${(i * 37) % 100}%`,
  top: `${(i * 61) % 100}%`,
  delay: (i % 9) * 0.25,
}));

const targets = [
  { left: "18%", top: "30%", delay: 0 },
  { left: "42%", top: "58%", delay: 1.2 },
  { left: "68%", top: "24%", delay: 2.1 },
  { left: "83%", top: "64%", delay: 0.7 },
];

export function ContributionShooter() {
  return (
    <section className="scene shooter-scene">
      <div className="scene-label">
        <Rocket size={16} />
        CONTRIBUTION MISSION
      </div>

      <div className="space-field">
        {stars.map((star) => (
          <motion.i
            key={star.id}
            className="star"
            style={{ left: star.left, top: star.top }}
            animate={{ opacity: [0.15, 0.9, 0.15] }}
            transition={{
              duration: 2 + (star.id % 4),
              repeat: Infinity,
              delay: star.delay,
            }}
          />
        ))}

        {targets.map((target, index) => (
          <motion.div
            key={index}
            className="target"
            style={{ left: target.left, top: target.top }}
            initial={{ scale: 0.4, opacity: 0 }}
            animate={{
              scale: [0.8, 1.15, 0.8],
              opacity: [0.4, 1, 0.4],
              rotate: [0, 90, 180],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              delay: target.delay,
            }}
          >
            <Target size={28} />
          </motion.div>
        ))}

        <motion.div
          className="crosshair"
          animate={{
            x: ["-20%", "20%", "10%", "-25%", "-20%"],
            y: ["10%", "-15%", "25%", "5%", "10%"],
          }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        >
          <Crosshair size={40} />
        </motion.div>

        <motion.div
          className="player-ship"
          animate={{
            y: [-8, 8, -8],
            rotate: [-2, 2, -2],
          }}
          transition={{ duration: 2.4, repeat: Infinity, ease: "easeInOut" }}
        >
          <Rocket size={52} />
        </motion.div>

        <motion.div
          className="laser laser-one"
          animate={{ scaleY: [0, 1, 1, 0], opacity: [0, 1, 1, 0] }}
          transition={{ duration: 1.4, repeat: Infinity, delay: 0.2 }}
        />

        <motion.div
          className="laser laser-two"
          animate={{ scaleY: [0, 1, 1, 0], opacity: [0, 1, 1, 0] }}
          transition={{ duration: 1.4, repeat: Infinity, delay: 0.9 }}
        />

        <div className="hud">
          <span>MISSION: CONTRIBUTIONS</span>
          <span>STATUS: ONLINE</span>
          <span>CODE SHIPPED: ∞</span>
        </div>
      </div>
    </section>
  );
}
