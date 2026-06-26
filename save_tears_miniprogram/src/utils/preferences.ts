const SAVING_TARGET_REMINDERS_KEY = 'saving_target_reminders_enabled';
const DEVICE_ABNORMALITY_ALERTS_KEY = 'device_abnormality_alerts_enabled';

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
    savingTargetRemindersEnabled: readBoolean(SAVING_TARGET_REMINDERS_KEY, true),
    deviceAbnormalityAlertsEnabled: readBoolean(DEVICE_ABNORMALITY_ALERTS_KEY, true),
  };
}

export function saveResidentPreferences(input: {
  savingTargetRemindersEnabled: boolean;
  deviceAbnormalityAlertsEnabled: boolean;
}) {
  writeBoolean(SAVING_TARGET_REMINDERS_KEY, input.savingTargetRemindersEnabled);
  writeBoolean(DEVICE_ABNORMALITY_ALERTS_KEY, input.deviceAbnormalityAlertsEnabled);
}
