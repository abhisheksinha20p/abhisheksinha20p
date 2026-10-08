import { motion } from "framer-motion";

const milestones = [
  {
    year: "2024",
    title: "Engineering Foundation",
    description: "ECE background and transition into software engineering.",
  },
  {
    year: "2025",
    title: "Full Stack Engineering",
    description: "React, Node.js, APIs, SaaS products and production workflows.",
  },
  {
    year: "2025 →",
    title: "Full Stack + Mobile",
    description: "React Native, microservices, Kafka, Redis and real-time systems.",
  },
  {
    year: "2026 →",
    title: "Frontline Deployment",
    description: "Production deployment, infrastructure, observability and automation.",
  },
];

export function CareerTimeline() {
  return (
    <section className="scene">
      <div className="scene-label">ENGINEERING EVOLUTION</div>

      <div className="timeline">
        {milestones.map((item, index) => (
          <motion.article
            className="timeline-item"
            key={item.year}
            initial={{ opacity: 0, x: index % 2 ? 30 : -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.4 }}
            transition={{ duration: 0.6, delay: index * 0.12 }}
          >
            <div className="timeline-year">{item.year}</div>
            <div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </div>
          </motion.article>
        ))}
      </div>
    </section>
  );
}
