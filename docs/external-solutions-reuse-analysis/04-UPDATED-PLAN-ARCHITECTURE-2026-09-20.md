# Updated Plan & Architecture — Full Company FOSS + Freemium Stack

**Source library:** https://github.com/nivyindia/Raw-Repository/tree/main/external-solutions/business-structure-planning-ai-library  
**Updated:** 2026-09-20  
**Core rule:** `DISCOVER → DECOMPOSE → REUSE → ADAPT → INTEGRATE → BUILD ONLY WHAT IS MISSING`  
**Software policy:** **Open-source first.** Freemium only if FOSS insufficient after evaluation.

---

## Target Architecture

```
ONE NIVY WORKSPACE (role-aware UI)
        ↓
CONTROL PLANE (Identity · Policy · Router · Approval · Audit · Kill Switch)
        ↓
Agents + Postiz/n8n + Media pipeline (video/audio)
        ↓
Systems of Record + Knowledge + Storage + Warmup mail
```

---

## NEW / EXPANDED AREAS (requested)

### A. Social Media Scheduling (Postiz & alternatives)

| Tool | Type | Notes |
|------|------|-------|
| **Postiz** (gitroomhq/postiz-app) | **OSS (AGPL)** self-host | **Primary pick.** 30+ networks (X, LinkedIn, IG, TikTok, YouTube, Reddit, Bluesky, Mastodon, Discord…). AI copilot, design editor, API + **MCP** for agents, n8n-friendly. Cloud freemium from ~$29/mo if not self-hosting. |
| **Mixpost** | OSS Lite + paid Pro | Polished self-host UI; Lite free (few networks); Pro one-time license. |
| SocioBoard / PostyBirb | OSS | Lighter alternatives |
| n8n + platform APIs | OSS | Custom schedules if Postiz not used |

**Nivy default:** Self-host **Postiz** + wire agents via MCP/API + approval gate before publish.

---

### B. AI Video for Marketing

| Tool | Type | Role |
|------|------|------|
| **ComfyUI** | OSS | Node-based local video/image workflows (hub for models) |
| **Wan 2.2 / Wan family** (Alibaba) | OSS (Apache-2.0) | Strong open text-to-video / image-to-video |
| **LTX-Video / LTX-2.x** (Lightricks) | OSS weights | Fast / native audio+video options |
| **HunyuanVideo** | OSS | Cinematic motion |
| **CogVideoX / Mochi 1 / Open-Sora / SVD** | OSS | Additional T2V / I2V |
| **MoviePy + FFmpeg** | OSS | Edit, concat, captions, render |
| **Remotion / Motion Canvas / html-video** | OSS / source-available | Programmatic / agent-authored video |
| **Wav2Lip / SadTalker / LivePortrait** | OSS | Lip-sync / talking head |
| Freemium SaaS (only if local GPU weak) | Freemium | CapCut, InVideo free tiers, Kling/Haiper free credits — exit plan required |

**Nivy default:** ComfyUI + Wan/LTX models locally → FFmpeg/MoviePy polish → Postiz publish.

---

### C. AI Sound / Music / Voice

| Tool | Type | Role |
|------|------|------|
| **Whisper** | OSS | Speech-to-text |
| **Coqui TTS / OpenVoice / Fish Speech / CosyVoice / MOSS-TTS** | OSS | TTS + voice clone |
| **Amphion** | OSS | Audio/music/speech generation toolkit |
| **AudioCraft** (Meta) | OSS | Audio generation research |
| **YuE / ACE-Step / DiffRhythm** etc. | OSS | Music generation (quality varies; check license) |
| **FFmpeg** | OSS | Mix, normalize, export |
| Freemium | Freemium | ElevenLabs free tier, Suno free credits — only if OSS quality fails |

**Nivy default:** Whisper + Coqui/OpenVoice/Fish Speech locally; music from OSS models when license OK.

---

### D. Email Warmup / Deliverability / Account Warmup

| Tool | Type | Role |
|------|------|------|
| **Warmbly** | OSS (self-host) | Open-source B2B cold outreach + warmup platform |
| **Kindling** | OSS | Email warmer for Gmail + IMAP (owned mailboxes mesh) |
| Custom n8n + owned inboxes | OSS | Gradual send volume between own accounts |
| Mailcow / docker-mailserver + proper DNS (SPF/DKIM/DMARC) | OSS | Foundation for reputation |
| **TrulyInbox** | Freemium | Free-forever low-volume warmup (fallback) |
| Instantly / Smartlead / MailReach / Warmup Inbox | Freemium/paid | Bundled or dedicated warmup if OSS mesh not enough |

**Rules:** Warm only **owned** mailboxes. Never buy spam networks. Human approval on cold campaigns. Track bounce/complaint.

**Nivy default:** Kindling or Warmbly self-host + SPF/DKIM/DMARC + gradual volume via n8n; freemium only if deliverability still fails.

---

### E. Related fully-functional needs (also mapped)

| Need | FOSS / Freemium |
|------|----------------|
| Cold email sequences | n8n + Listmonk/Mautic + Warmbly + approval |
| Link-in-bio / landing | Ghost, Odoo Website, or simple static |
| UGC / ad variants | ComfyUI + Wan + Penpot |
| Podcast / long audio | Whisper + TTS + FFmpeg |
| Short-form clips from long video | FFmpeg + MoviePy + agents |
| Hashtag / caption AI | Postiz AI + Ollama skills |
| Multi-account social safely | Postiz workspaces + policy limits |
| Domain / inbox health | DNS tools + blacklist checks (open) + warmup |

---

## FULL MAP (previous sections kept, social/media updated)

### Social & content pipeline (recommended flow)
```
Idea → Agent draft (Ollama/skills)
     → Image/Video (ComfyUI + Wan/LTX)
     → Audio bed / VO (TTS + FFmpeg)
     → Schedule (Postiz)
     → Approval gate
     → Publish + analytics (Postiz / Matomo)
```

### Email outbound pipeline
```
Lead list → Enrich → Warm mailbox (Kindling/Warmbly)
         → Sequence (n8n + Listmonk)
         → Approval → Send → Reply capture → CRM
```

### Core stack reminder
| Layer | Pick |
|-------|------|
| Social scheduler | **Postiz** (self-host) |
| AI video | **ComfyUI + Wan / LTX** |
| AI voice/music | Whisper + Coqui/OpenVoice/Fish Speech |
| Email warmup | **Kindling** or **Warmbly** |
| Automation | **n8n** |
| CRM/ERP | Odoo Community or ERPNext |
| Files/wiki | Nextcloud + BookStack |
| Marketing email | Listmonk + Mautic |
| AI runtime | Ollama + LiteLLM |

---

## Decision Rules

1. OSS first (Postiz, ComfyUI, Kindling/Warmbly, n8n…).
2. Freemium only after FOSS test fails (document why).
3. External publish + cold email = human approval.
4. Warmup = owned accounts only.
5. Register every tool in Asset Registry.

---

## Immediate add-ons for functional marketing/sales

1. Deploy **Postiz** (Docker).  
2. Deploy **ComfyUI** + one video model (Wan or LTX).  
3. Deploy **Kindling** or **Warmbly** for mailbox warmup.  
4. Connect Postiz + n8n + approval workflow.  
5. Only then scale channels / cold volume.

**Bottom line:** Postiz (social), ComfyUI+Wan/LTX (AI video), Whisper/TTS (sound), Kindling/Warmbly (email warmup) — sab OSS path se cover. Freemium fallback documented jahan FOSS abhi kam padta hai.
