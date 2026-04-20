export interface ApiBaseResolutionOptions {
  customBaseUrl?: string | null;
  envBaseUrl?: string | null;
  browserProtocol?: string | null;
  browserHostname?: string | null;
}

export function normalizeApiBaseUrl(baseUrl?: string | null) {
  return String(baseUrl || '').trim().replace(/\/+$/, '');
}

export function resolveApiBaseUrl(options: ApiBaseResolutionOptions = {}) {
  const customBaseUrl = normalizeApiBaseUrl(options.customBaseUrl);
  if (customBaseUrl) {
    return customBaseUrl;
  }

  const envBaseUrl = normalizeApiBaseUrl(options.envBaseUrl);
  if (envBaseUrl) {
    return envBaseUrl;
  }

  const browserHostname = String(options.browserHostname || '').trim();
  const browserProtocol = String(options.browserProtocol || '').trim();
  if (browserHostname && /^https?:$/.test(browserProtocol)) {
    return `${browserProtocol}//${browserHostname}:8000`;
  }

  return 'http://127.0.0.1:8000';
}
