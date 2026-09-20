# Supporting Software & Platforms — Full List

**Parent:** [04 Architecture](./04-UPDATED-PLAN-ARCHITECTURE-2026-09-20.md) · [05 Gaps](./05-REMAINING-GAPS-FOSS-2026-09-20.md)  
**Updated:** 2026-09-20  
**Note:** Core FOSS stack alag docs me hai. Yahan **supporting** = ads platforms, Docker/DevOps, SEO tools, paid APIs, browser tools — jo fully functional hone ke liye chahiye.

---

## 1. Ads & Paid Acquisition Platforms (closed — API integrate)

| Platform | Use | How we connect |
|----------|-----|----------------|
| **Meta Ads** (Facebook / Instagram) | Social ads, lead forms, retargeting | Meta Marketing API + n8n / official SDK |
| **Google Ads** | Search, Display, YouTube, Performance Max | Google Ads API + n8n |
| **Google Analytics 4** | Optional (prefer Matomo) | GA4 API if client forces |
| **YouTube Ads** | Video campaigns | Via Google Ads |
| **LinkedIn Ads** | B2B | LinkedIn Marketing API |
| **X (Twitter) Ads** | Brand / engagement | X Ads API |
| **TikTok Ads** | Short video | TikTok Marketing API |
| **Pinterest Ads** | Visual commerce | Pinterest API |
| **Microsoft Ads (Bing)** | Search alternate | Microsoft Advertising API |
| **Amazon Ads** | If ecom | Amazon Advertising API |

**Rule:** Spend + creative on platform UI/API; reporting + lead sync into CRM via **n8n**. No OSS replacement for ad auctions.

---

## 2. Organic / Social Platforms (publish via Postiz)

| Platform | Via Postiz / API |
|----------|------------------|
| X (Twitter) | Yes |
| LinkedIn | Yes |
| Instagram | Yes |
| Facebook Pages | Yes |
| TikTok | Yes |
| YouTube | Yes |
| Threads | Yes |
| Bluesky | Yes |
| Mastodon | Yes |
| Reddit | Yes |
| Pinterest | Yes |
| Discord / Telegram | Postiz / bots |
| WhatsApp Business | Chatwoot + official Cloud API |
| Google Business Profile | API / n8n |

---

## 3. SEO Supporting Tools

| Tool | Type | Role |
|------|------|------|
| **OpenSEO** | OSS self-host | Keyword research, ranks, backlinks (BYOK DataForSEO) |
| **SerpBear** | OSS self-host | Rank tracking |
| **SEONaut** | OSS | Technical SEO site audit |
| **LibreCrawl** | OSS | Crawl / audit (Screaming Frog style) |
| **Matomo** / Plausible | OSS | On-site analytics + goals |
| **Google Search Console** | Free (Google) | Indexing, queries — mandatory for SEO |
| **Bing Webmaster Tools** | Free | Alternate search |
| Screaming Frog (free tier) | Freemium | Desktop crawl |
| DataForSEO / SerpAPI | Paid data API | SERP data for OpenSEO/SerpBear |
| Ahrefs / Semrush | Paid SaaS | Only if client demands deep backlink DB |
| Schema / sitemap | Code + Docusaurus/Ghost | Structured data |
| astDeniss SEO skills + Anthropic marketing | OSS skills | Content/SEO playbooks for agents |

**Nivy SEO stack:** Matomo + Search Console + SerpBear/OpenSEO + LibreCrawl/SEONaut + agent skills.

---

## 4. Docker / Containers / Local DevOps

| Tool | Type | Role |
|------|------|------|
| **Docker Engine** + Compose | OSS | Production containers on Linux |
| **Podman** + **Podman Desktop** | OSS | Docker Desktop alternative (rootless) |
| **Rancher Desktop** | OSS | Containers + local Kubernetes |
| **Colima / Lima** | OSS | Mac/Linux lightweight VMs for containers |
| **Portainer** | OSS | Web UI for Docker/K8s |
| **Coolify / CapRover / Dokploy** | OSS | Self-host PaaS (Heroku-like) |
| **Kubernetes** (k3s / k0s) | OSS | Scale when needed |
| **Nginx Proxy Manager / Caddy / Traefik** | OSS | Reverse proxy + SSL |
| Docker Desktop | Proprietary (free personal) | OK for local Windows/Mac if team already uses |

**Nivy default:** Linux servers = Docker Compose; desktops = Podman Desktop or Rancher Desktop; deploy UI = Coolify or Portainer.

---

## 5. Payment / SMS / Communication APIs (India + global)

| Service | Type | Role |
|---------|------|------|
| **Razorpay** | Commercial API | India payments, UPI, subscriptions |
| **Stripe** | Commercial API | Global cards |
| **PayU / Cashfree / PhonePe** | Commercial | India alternates |
| **MSG91 / Twilio / Textlocal** | Commercial | SMS OTP, transactional SMS |
| **WhatsApp Cloud API** (Meta) | Commercial | Official WA business messaging |
| **Resend / Postmark / Amazon SES** | Commercial / freemium | Transactional email deliverability |
| **Plunk** | OSS option | Self-host transactional + marketing email |

Integrate via **n8n** + approval for money moves.

---

## 6. Maps / Places / Enrichment (supporting data)

| Service | Type | Role |
|---------|------|------|
| **OpenStreetMap** + Nominatim | OSS | Maps, geocode |
| **Photon / Pelias** | OSS | Geocoding |
| Google Places / Maps | Commercial API | If client requires Google data |
| Clearbit / Apollo style | Commercial | Enrichment — prefer scrape+OSS first |
| Hunter / Snov freemium | Freemium | Email find (policy-compliant only) |

---

## 7. Browser / Desktop / Agent Helpers

| Tool | Type | Role |
|------|------|------|
| **Playwright / Puppeteer** | OSS | Browser automation, screenshots |
| **Browser Use / Skyvern** | OSS | LLM-driven browser |
| Chrome / Firefox + profiles | Free | Manual QA, warm accounts carefully |
| uBlock Origin etc. | OSS extensions | Privacy on research machines |

---

## 8. Office / Files (already core, supporting formats)

| Tool | Role |
|------|------|
| Collabora / OnlyOffice | Edit docx/xlsx in browser |
| LibreOffice | Desktop office |
| FFmpeg | All media convert |
| ImageMagick | Image batch |

---

## 9. Monitoring / Logs / Errors (supporting ops)

| Tool | Role |
|------|------|
| Uptime Kuma / OneUptime | Uptime + status page |
| Grafana + Prometheus + Loki | Metrics + logs |
| Sentry (self-host GlitchTip) | Error tracking OSS alternative |
| Healthchecks.io self-host | Cron job monitoring |

---

## 10. Identity / Domain / Email infra support

| Tool | Role |
|------|------|
| Cloudflare (free tier) | DNS, CDN, WAF — freemium |
| Let's Encrypt | Free SSL |
| Mailcow / docker-mailserver | Own mail |
| SPF / DKIM / DMARC checkers | Free online + DNS |
| Namecheap / Cloudflare Registrar | Domains (commercial) |

---

## 11. Function → Supporting software quick map

| Function | Supporting (beyond core FOSS) |
|----------|-------------------------------|
| **SEO** | Search Console, SerpBear/OpenSEO, LibreCrawl, DataForSEO key |
| **Paid ads** | Meta Ads, Google Ads, LinkedIn Ads + n8n reporting |
| **Social organic** | Postiz → all major networks |
| **Email deliverability** | SES/Postmark + Kindling warmup + DNS auth |
| **Payments** | Razorpay / Stripe |
| **SMS / OTP** | MSG91 / Twilio |
| **WhatsApp** | Meta Cloud API + Chatwoot |
| **Dev / deploy** | Docker/Podman, Coolify, Portainer, Caddy |
| **SEO content** | Agent skills + Ghost/Strapi |
| **Video ads** | ComfyUI output → Meta/Google/TikTok upload |
| **Analytics** | Matomo primary; GA4 only if required |
| **Contracts** | Documenso + PDF |
| **Short links** | Shlink on own domain |

---

## 12. Minimal “supporting” install checklist

1. **Docker/Podman** on all servers + Portainer or Coolify  
2. **Cloudflare** (or equivalent) for DNS/SSL  
3. **Google Search Console** + **Matomo**  
4. **SerpBear** or OpenSEO (SEO ranks)  
5. **Meta + Google Ads** accounts (when budget) + n8n sync  
6. **Razorpay** (India) or Stripe  
7. **MSG91** or similar for SMS  
8. **WhatsApp Cloud API** if WA is a channel  
9. **Amazon SES** or Resend for transactional mail  
10. **Shlink** for campaign links  

---

**Bottom line:**  
Core company = FOSS.  
Supporting = **ads platforms (Meta/Google/…)**, **Docker/Podman/Coolify**, **SEO (SerpBear/OpenSEO + Search Console)**, **payments/SMS/WA APIs**, **CDN/DNS**.  
In sab ke bina bhi internal ops chal sakte hain; **market me fully functional** hone ke liye ye supporting layer zaroori hai.
