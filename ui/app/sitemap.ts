import type { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  const base = 'https://impp.sh';
  const now = new Date().toISOString().split('T')[0];

  return [
    { url: base, lastModified: now, changeFrequency: 'weekly', priority: 1.0 },
    { url: `${base}/paper`, lastModified: now, changeFrequency: 'monthly', priority: 0.9 },
    { url: `${base}/docs`, lastModified: now, changeFrequency: 'weekly', priority: 0.8 },
    { url: `${base}/sdk`, lastModified: now, changeFrequency: 'monthly', priority: 0.8 },
    { url: `${base}/leaderboard`, lastModified: now, changeFrequency: 'daily', priority: 0.7 },
    { url: `${base}/sandbox`, lastModified: now, changeFrequency: 'weekly', priority: 0.7 },
    { url: `${base}/signup`, lastModified: now, changeFrequency: 'yearly', priority: 0.6 },
    { url: `${base}/waitlist`, lastModified: now, changeFrequency: 'yearly', priority: 0.6 },
    { url: `${base}/seller-apply`, lastModified: now, changeFrequency: 'yearly', priority: 0.6 },
    { url: `${base}/preview/market`, lastModified: now, changeFrequency: 'daily', priority: 0.7 },
    { url: `${base}/preview/incidents`, lastModified: now, changeFrequency: 'weekly', priority: 0.5 },
    { url: `${base}/preview/policies`, lastModified: now, changeFrequency: 'monthly', priority: 0.5 },
  ];
}
