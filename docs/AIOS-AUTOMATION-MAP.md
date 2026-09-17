# Nivy AIOS Automation Map

## 1. Lead generation to outreach
1. Scheduled/manual campaign trigger
2. Discover businesses from approved source
3. Normalize and deduplicate
4. Enrich website/contact information
5. Verify email through Reacher
6. Store lead and verification evidence in PostgreSQL
7. Generate personalized outreach
8. Human approval gate for external send
9. Send through configured email provider
10. Record message/campaign evidence
11. Wait according to campaign policy
12. Detect reply/opt-out before every follow-up
13. Generate and send approved follow-ups
14. Stop sequence on reply, unsubscribe, bounce, or campaign completion

## 2. Inbound email automation
Email received -> classify -> retrieve customer/lead context -> detect urgency/escalation -> draft -> approval or configured auto-reply -> send -> audit.

## 3. Social content automation
Brief/form/schedule -> research -> generate master content -> adapt to LinkedIn/Instagram/Facebook/X/TikTok/Threads/YouTube Shorts -> approval -> publish/export -> record evidence.

## 4. SEO automation
Target URL -> crawl/collect allowed signals -> analyze technical/content/keyword issues -> prioritize -> generate report -> optionally create content tasks.

## 5. Knowledge automation
Document upload -> extract text -> chunk -> embed -> store in Qdrant -> object stored in MinIO -> metadata in PostgreSQL -> retrieval available to agents.

## 6. Agent evaluation automation
Discover registry -> execute test cases -> validate output/schema/tool permissions -> capture evidence -> mark PASS/FAIL -> regression report.

## 7. Governance
All external side effects require a registered tool, validated input, audit event, and the configured approval policy. Secrets stay in environment/secret stores and never in Git.
