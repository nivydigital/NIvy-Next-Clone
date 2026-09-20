# Remaining FOSS / Freemium Gaps — 2026-09-20

**Parent plan:** [04-UPDATED-PLAN-ARCHITECTURE](./04-UPDATED-PLAN-ARCHITECTURE-2026-09-20.md)  
**Policy:** OSS first; freemium only if FOSS fails evaluation.

Pehle wali list me ye major categories thin / weak thin — ab fill:

---

## 1. E-Signature / Contracts / Proposals

| Tool | Type | Role |
|------|------|------|
| **Documenso** | OSS (self-host) | DocuSign alternative — send, sign, audit |
| **Supersign** | OSS (AGPL) | PKI e-sign, audit trails, unlimited self-host |
| **OpenSign** / community forks | OSS | Lightweight signing |
| **Quote and Sign** | OSS + freemium | Proposals clients can accept/sign on phone |
| Templates in Odoo/ERPNext + PDF | OSS | Quote → PDF → sign workflow via n8n |

**Nivy default:** Documenso or Supersign self-host + n8n webhooks into CRM.

---

## 2. Status Page / Uptime / Incidents

| Tool | Type | Role |
|------|------|------|
| **OneUptime** | OSS (Apache) | Full stack: uptime, status page, on-call, incidents, APM |
| **Uptime Kuma** | OSS | Simple beautiful uptime monitors |
| **Cachet** / **Gatus** | OSS | Status page alternatives |
| **Grafana + Prometheus** | OSS | Already in stack for metrics |

**Nivy default:** Uptime Kuma (simple) or OneUptime (full).

---

## 3. Link Shortener / QR / Tracking links

| Tool | Type | Role |
|------|------|------|
| **Shlink** | OSS (MIT) | Self-host short URLs, QR, visit analytics, multi-domain |
| **YOURLS** | OSS | Classic PHP shortener |
| Postiz / Matomo UTM | OSS | Campaign links without separate shortener |

**Nivy default:** Shlink on own domain.

---

## 4. Low-code Internal Tools / Admin Panels

| Tool | Type | Role |
|------|------|------|
| **Appsmith** | OSS (Apache) | Internal admin panels, CRUD, dashboards |
| **ToolJet** | OSS | Dashboards + internal apps |
| **Budibase** | OSS | Low-code business apps |
| **NocoDB / Baserow** | OSS | Airtable alternative |

**Nivy default:** Appsmith or NocoDB when custom internal UI needed beyond Odoo.

---

## 5. 2FA / OTP / Secrets UX

| Tool | Type | Role |
|------|------|------|
| **Vaultwarden** | Already listed | Passwords + TOTP |
| **2FAuth** | OSS | Team 2FA code manager |
| **Authentik / Keycloak** | Already listed | SSO + MFA |

---

## 6. Screenshots / Visual QA / Page capture

| Tool | Type | Role |
|------|------|------|
| **Playwright / Puppeteer** | OSS | Automated screenshots in CI/n8n |
| **Shot-Scraper** | OSS | CLI screenshots |
| **Browserless** (self-host) | OSS-friendly | Headless Chrome as a service |
| Freemium | ScreenshotOne / similar free tiers | Only if self-host hard |

---

## 7. WhatsApp / Messaging business (India-heavy)

| Tool | Type | Role |
|------|------|------|
| **Chatwoot** | Already listed | WhatsApp channel via official API |
| **Evolution API** / open WA gateways | OSS (check ToS) | Self-host WA API bridge — **use only within Meta policy** |
| n8n WhatsApp Business nodes | OSS | Official Cloud API workflows |

**Rule:** Prefer official WhatsApp Business API; avoid banned unofficial scrapers.

---

## 8. DNS / Domain / SSL helpers

| Tool | Type | Role |
|------|------|------|
| **Nginx Proxy Manager** | OSS | Reverse proxy + SSL (Let's Encrypt) |
| **Caddy** | OSS | Auto-HTTPS reverse proxy |
| **Technitium DNS** / AdGuard Home | OSS | Internal DNS / filtering |

---

## 9. Password share / one-time secrets

| Tool | Type | Role |
|------|------|------|
| **PrivateBin** / **OneTimeSecret** self-host | OSS | One-time secret links |
| Vaultwarden send | OSS | Secure share from password manager |

---

## 10. Still thin / hybrid often needed (India)

| Need | Reality |
|------|--------|
| **Payroll / PF / ESI / TDS** | ERPNext/Odoo localization helps; pure India payroll often needs specialist or CA tool (freemium/paid) |
| **GST e-invoice / e-way** | ERPNext/Odoo India compliance modules — verify current year |
| **Payment gateway** | Razorpay/PayU etc. are commercial APIs (no full OSS replacement) — integrate via n8n |
| **SMS OTP** | Commercial SMS APIs (MSG91 etc.) — no pure OSS carrier |
| **Google/Meta ads** | Closed platforms — only APIs + n8n reporting |

In in cases: FOSS for workflow + commercial API with clear exit/data export.

---

## Updated “install if needed” add-ons

| Priority | Tool |
|----------|------|
| High | **Documenso** or Supersign (contracts) |
| High | **Shlink** (branded short links) |
| High | **Uptime Kuma** or OneUptime (status) |
| Medium | Appsmith / NocoDB (internal tools) |
| Medium | Nginx Proxy Manager / Caddy |
| As needed | 2FAuth, PrivateBin, Shot-Scraper |

---

## Gap status

| Area | Status |
|------|--------|
| Social scheduler (Postiz) | Covered |
| AI video / sound | Covered |
| Email warmup | Covered |
| CRM/ERP/HR/Wiki/Chat/Support | Covered |
| E-sign / proposals | **Now covered** |
| Status / uptime | **Now covered** |
| Link shortener / QR | **Now covered** |
| Low-code internal | **Now covered** |
| India payroll/GST/SMS/payments | Hybrid (FOSS + regulated APIs) |

**Bottom line:** Functional company stack almost complete on OSS. Remaining “must buy” usually regulated rails (payments, SMS, ads, some India tax filing) — not general software.
