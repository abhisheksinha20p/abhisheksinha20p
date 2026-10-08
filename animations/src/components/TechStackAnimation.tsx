import { motion } from "framer-motion";

const technologies = [
  "React",
  "React Native",
  "TypeScript",
  "Node.js",
  "Kafka",
  "Redis",
  "MongoDB",
  "Docker",
  "AWS",
  "NGINX",
];

export function TechStackAnimation() {
  return (
    <section className="scene">
      <div className="scene-label">TECHNOLOGY ORBIT</div>

      <div className="orbit">
        <motion.div
          className="orbit-core"
          animate={{ rotate: 360 }}
          transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
        >
          <span>BUILD</span>
          <span>SHIP</span>
          <span>OBSERVE</span>
          <span>IMPROVE</span>
        </motion.div>

        {technologies.map((tech, index) => {
          const angle = (360 / technologies.length) * index;

          return (
            <motion.div
              key={tech}
              className="tech-node"
              style={{
                transform: `rotate(${angle}deg) translateX(190px) rotate(-${angle}deg)`,
              }}
              whileHover={{ scale: 1.18 }}
            >
              {tech}
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}
