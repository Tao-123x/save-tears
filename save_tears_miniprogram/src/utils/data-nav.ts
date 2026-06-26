const DATA_TAB_KEY = 'resident_saving_data_initial_tab';

export type ResidentDataTab = 'tap' | 'greywater' | 'trends' | 'plan';

export function queueResidentDataTab(tab: ResidentDataTab) {
  if (typeof uni === 'undefined') {
    return;
  }

  uni.setStorageSync(DATA_TAB_KEY, tab);
}

export function consumeResidentDataTab() {
  if (typeof uni === 'undefined') {
    return '';
  }

  const value = uni.getStorageSync(DATA_TAB_KEY);
  uni.removeStorageSync(DATA_TAB_KEY);
  return value as ResidentDataTab | '';
}
