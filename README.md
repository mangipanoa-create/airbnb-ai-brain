* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Inter, Arial, sans-serif;
  background: #0f172a;
  color: #e2e8f0;
}

.shell {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  background: #111827;
  border-right: 1px solid rgba(148, 163, 184, 0.2);
  padding: 24px 18px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 10px 18px;
  margin-bottom: 28px;
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  font-weight: 700;
  background: linear-gradient(135deg, #22c55e, #0ea5e9);
  color: white;
}

.brand strong {
  display: block;
  font-size: 1rem;
}

.brand small {
  color: #94a3b8;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

nav a {
  color: #cbd5e1;
  text-decoration: none;
  padding: 10px 12px;
  border-radius: 10px;
  transition: 0.2s ease;
}

nav a.active,
nav a:hover {
  background: rgba(59, 130, 246, 0.12);
  color: #fff;
}

.content {
  flex: 1;
  padding: 30px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.eyebrow {
  margin: 0 0 4px;
  color: #38bdf8;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.72rem;
}

h1 {
  margin: 0;
  font-size: 2rem;
}

.primary-btn {
  border: none;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  padding: 12px 18px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.stats-grid,
.panel-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 22px;
}

.stat-card,
.panel {
  background: rgba(15, 23, 42, 0.82);
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 16px;
  padding: 18px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-card span {
  color: #94a3b8;
}

.stat-card strong {
  font-size: 2rem;
}

.warning { border-top: 3px solid #fbbf24; }
.danger { border-top: 3px solid #ef4444; }
.success { border-top: 3px solid #22c55e; }

.panel {
  min-height: 220px;
}

.panel-header {
  margin-bottom: 12px;
}

.panel-header h2 {
  margin: 0;
  font-size: 1.15rem;
}

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.list li {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(30, 41, 59, 0.5);
}

.list p,
.list small {
  margin: 4px 0 0;
  color: #94a3b8;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 72px;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: capitalize;
}

.badge.high,
.badge.danger,
.badge.urgent { background: rgba(239, 68, 68, 0.15); color: #fca5a5; }
.badge.medium,
.badge.warning { background: rgba(251, 191, 36, 0.14); color: #fbbf24; }
.badge.low,
.badge.available,
.badge.confirmed,
.badge.success { background: rgba(34, 197, 94, 0.14); color: #86efac; }

@media (max-width: 900px) {
  .shell {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }

  nav {
    flex-direction: row;
    flex-wrap: wrap;
  }
}
