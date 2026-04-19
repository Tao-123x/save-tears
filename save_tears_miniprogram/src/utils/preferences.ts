const DAILY_DIGEST_KEY = 'daily_digest_enabled';
const ANOMALY_ALERTS_KEY = 'anomaly_alerts_enabled';

function readBoolean(key: string, fallback = true) {
  if (typeof uni === 'undefined') {
    return fallback;
  }

  const value = uni.getStorageSync(key);
  if (value === '' || value === undefined || value === null) {
    return fallback;
  }

  return value === true || value === 'true' || value === 1;
}

function writeBoolean(key: string, value: boolean) {
  if (typeof uni === 'undefined') {
    return;
  }

  uni.setStorageSync(key, value);
}

export function getResidentPreferences() {
  return {
    dailyDigestEnabled: readBoolean(DAILY_DIGEST_KEY, true),
    anomalyAlertsEnabled: readBoolean(ANOMALY_ALERTS_KEY, true),
  };
}

export function saveResidentPreferences(input: {
  dailyDigestEnabled: boolean;
  anomalyAlertsEnabled: boolean;
}) {
  writeBoolean(DAILY_DIGEST_KEY, input.dailyDigestEnabled);
  writeBoolean(ANOMALY_ALERTS_KEY, input.anomalyAlertsEnabled);
}
