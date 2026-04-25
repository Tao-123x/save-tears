export interface WaterFlowRecord {
  id?: number;
  flow_rate: number;
  timestamp: string;
}

export interface WaterBillRecord {
  id?: number;
  amount: number;
  month: string;
}

export interface WaterQualityRecord {
  id?: number;
  turbidity_value: number;
  timestamp: string;
}

export interface InsightPoint {
  label: string;
  value: number;
}

export interface TrendGeometryNode extends InsightPoint {
  x: number;
  y: number;
  isCurrent: boolean;
}

export interface TrendGeometrySegment {
  left: number;
  top: number;
  width: number;
  angle: number;
}

export interface MetricHighlight {
  label: string;
  value: string;
  helper: string;
  tone: 'mist' | 'deep' | 'warning';
}

function sortByDate<T>(records: T[], getValue: (record: T) => string) {
  return [...records].sort((left, right) => {
    return new Date(getValue(left)).getTime() - new Date(getValue(right)).getTime();
  });
}

function formatDayLabel(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return `${String(date.getMonth() + 1).padStart(2, '0')}/${String(date.getDate()).padStart(2, '0')}`;
}

function formatMonthLabel(value: string) {
  return value.replace(/^(\d{4})-(\d{2}).*$/, '$2月');
}

function roundNumber(value: number) {
  return Math.round(value * 10) / 10;
}

export function buildTrendGeometry(
  points: InsightPoint[],
  options?: {
    maxPoints?: number;
    width?: number;
    height?: number;
    topPadding?: number;
    bottomPadding?: number;
  },
) {
  const {
    maxPoints = 6,
    width = 300,
    height = 120,
    topPadding = 12,
    bottomPadding = 18,
  } = options || {};

  const safePoints = points.slice(-maxPoints);
  const baseline = Math.max(height - bottomPadding, topPadding);

  if (!safePoints.length) {
    return {
      baseline,
      maxValue: 0,
      nodes: [] as TrendGeometryNode[],
      segments: [] as TrendGeometrySegment[],
    };
  }

  const maxValue = Math.max(...safePoints.map((point) => Number(point.value || 0)), 1);
  const plotHeight = Math.max(height - topPadding - bottomPadding, 1);
  const xStep = safePoints.length > 1 ? width / (safePoints.length - 1) : 0;

  const nodes = safePoints.map((point, index) => {
    const value = Number(point.value || 0);
    return {
      ...point,
      x: safePoints.length > 1 ? roundNumber(index * xStep) : roundNumber(width / 2),
      y: roundNumber(baseline - (value / maxValue) * plotHeight),
      isCurrent: index === safePoints.length - 1,
    } satisfies TrendGeometryNode;
  });

  const segments = nodes.slice(0, -1).map((node, index) => {
    const next = nodes[index + 1];
    const dx = next.x - node.x;
    const dy = next.y - node.y;
    return {
      left: node.x,
      top: node.y,
      width: roundNumber(Math.sqrt(dx * dx + dy * dy)),
      angle: roundNumber((Math.atan2(dy, dx) * 180) / Math.PI),
    } satisfies TrendGeometrySegment;
  });

  return {
    baseline,
    maxValue,
    nodes,
    segments,
  };
}

export function buildWaterFlowInsights(records: WaterFlowRecord[]) {
  const ordered = sortByDate(records, (record) => record.timestamp);
  const values = ordered.map((record) => Number(record.flow_rate || 0));
  const total = values.reduce((sum, value) => sum + value, 0);
  const peak = values.length ? Math.max(...values) : 0;
  const latest = values.length ? values[values.length - 1] : 0;
  const average = values.length ? roundNumber(total / values.length) : 0;
  const anomalyThreshold = average * 1.25;

  return {
    total,
    peak,
    latest,
    average,
    anomalyCount: values.filter((value) => value > anomalyThreshold && value > average).length,
    points: ordered.map((record) => ({
      label: formatDayLabel(record.timestamp),
      value: Number(record.flow_rate || 0),
    })),
    summary:
      values.length === 0
        ? '暂无用水记录。'
        : `最近 ${values.length} 条记录里，峰值为 ${peak}L，平均每次 ${average}L。`,
  };
}

export function buildWaterBillInsights(records: WaterBillRecord[]) {
  const ordered = [...records].sort((left, right) => left.month.localeCompare(right.month));
  const values = ordered.map((record) => Number(record.amount || 0));
  const latest = values.length ? values[values.length - 1] : 0;
  const previous = values.length > 1 ? values[values.length - 2] : latest;
  const total = values.reduce((sum, value) => sum + value, 0);

  return {
    total,
    latest,
    average: values.length ? roundNumber(total / values.length) : 0,
    highest: values.length ? Math.max(...values) : 0,
    deltaFromPrevious: latest - previous,
    points: ordered.map((record) => ({
      label: formatMonthLabel(record.month),
      value: Number(record.amount || 0),
    })),
    summary:
      values.length === 0
        ? '暂无账单记录。'
        : latest <= previous
          ? '最近一期账单低于或持平上期。'
          : '最近一期账单高于上期，需要留意用水变化。',
  };
}

export function buildWaterQualityInsights(records: WaterQualityRecord[]) {
  const ordered = sortByDate(records, (record) => record.timestamp);
  const values = ordered.map((record) => Number(record.turbidity_value || 0));
  const latest = values.length ? values[values.length - 1] : 0;
  const peak = values.length ? Math.max(...values) : 0;
  const average = values.length ? roundNumber(values.reduce((sum, value) => sum + value, 0) / values.length) : 0;

  let statusTone: 'excellent' | 'steady' | 'watch';
  if (latest <= 10) {
    statusTone = 'excellent';
  } else if (latest <= 20) {
    statusTone = 'steady';
  } else {
    statusTone = 'watch';
  }

  return {
    latest,
    peak,
    average,
    statusTone,
    anomalyCount: values.filter((value) => value > Math.max(average * 1.3, 20)).length,
    points: ordered.map((record) => ({
      label: formatDayLabel(record.timestamp),
      value: Number(record.turbidity_value || 0),
    })),
    summary:
      values.length === 0
        ? '暂未检测到水质数据。'
        : statusTone === 'excellent'
          ? '近期浊度保持在理想区间。'
          : statusTone === 'steady'
            ? '近期浊度平稳，但仍建议持续关注。'
            : '近期浊度偏高，建议尽快复核设备。',
  };
}

export function buildHomeDigest(input: {
  username?: string;
  flowRecords: WaterFlowRecord[];
  billRecords: WaterBillRecord[];
  qualityRecords: WaterQualityRecord[];
}) {
  const flow = buildWaterFlowInsights(input.flowRecords);
  const bill = buildWaterBillInsights(input.billRecords);
  const quality = buildWaterQualityInsights(input.qualityRecords);
  const alerts: string[] = [];

  if (flow.anomalyCount > 0) {
    alerts.push(`检测到 ${flow.anomalyCount} 次用水峰值偏高。`);
  }

  if (quality.statusTone === 'watch') {
    alerts.push('污水浊度偏高，建议关注设备状态。');
  }

  return {
    heroMetric: {
      label: '月度累计用水',
      value: `${flow.total}L`,
      helper: flow.summary,
      tone: 'deep',
    } satisfies MetricHighlight,
    billMetric: {
      label: '最近账单',
      value: bill.latest ? `¥${bill.latest}` : '待更新',
      helper: bill.summary,
      tone: bill.deltaFromPrevious > 0 ? 'warning' : 'mist',
    } satisfies MetricHighlight,
    qualityMetric: {
      label: '最近浊度',
      value: quality.latest ? `${quality.latest} NTU` : '待更新',
      helper: quality.summary,
      tone: quality.statusTone === 'watch' ? 'warning' : 'mist',
    } satisfies MetricHighlight,
    editorNote: `${input.username || '住户'}，这是你的用水、账单与水质概览。`,
    alerts,
    flow,
    bill,
    quality,
  };
}

export interface AdminUserRecord {
  username: string;
  room_number?: string;
  role?: string | null;
}

export function buildAdminOverview(users: AdminUserRecord[]) {
  const totalUsers = users.length;
  const adminCount = users.filter((user) => String(user.role || '').toLowerCase() === 'admin').length;
  const roomsConfigured = users.filter((user) => String(user.room_number || '').trim()).length;

  return {
    totalUsers,
    adminCount,
    residentCount: totalUsers - adminCount,
    roomsConfigured,
    roomsMissing: users
      .filter((user) => !String(user.room_number || '').trim())
      .map((user) => user.username),
  };
}
