export const AGENT_PRESETS = {
  A001: {
    label: "A001 research sample",
    mode: "a001",
    payload: {
      research_question: "What is demand for governed multi-agent sales automation?",
      target_market: "B2B services",
      geography: "India",
      evidence: [],
    },
  },
  A034: {
    label: "A034 lead discovery sample",
    mode: "execute",
    payload: {
      icp_definition: {
        industry: "B2B SaaS",
        size: "10-200",
        geography: "India",
      },
      lead_generation_strategy: {
        sources: ["public_web", "directories"],
        channels: ["email"],
      },
    },
  },
};

export const WORKFLOW_PRESETS = {
  "lead-outreach": {
    label: "Lead outreach dry-run sample",
    payload: {
      campaign_id: "ui-test-001",
      icp: { industry: "B2B services", geography: "India" },
      offer: { name: "AIOS setup", scope: "lead-to-outreach" },
    },
  },
  "inbound-email-triage": {
    label: "Inbound triage sample",
    payload: {
      inbound: {
        message_id: "msg-ui-1",
        mailbox: "hello@example.com",
        message: { subject: "Pricing question", body: "Can you share pricing?" },
      },
    },
  },
};
