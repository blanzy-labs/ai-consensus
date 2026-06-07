import type { HealthStatus } from "../types/consensus";

type StatusBannerProps = {
  health: HealthStatus | null;
  error: string;
  isChecking: boolean;
};

function StatusBanner({ health, error, isChecking }: StatusBannerProps) {
  if (isChecking) {
    return <div className="status-banner neutral">Backend status unknown. Checking...</div>;
  }

  if (error) {
    return <div className="status-banner error">Backend unavailable. {error}</div>;
  }

  if (health) {
    return (
      <div className="status-banner success">
        Backend online. {health.status} ({health.service})
      </div>
    );
  }

  return <div className="status-banner neutral">Backend status unknown.</div>;
}

export default StatusBanner;
