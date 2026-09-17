import os
import tempfile
import unittest

from app.revenue import LeadStatus, RevenueEngine


class RevenueEngineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.engine = RevenueEngine(self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_qualify_and_approval_gate_is_audited(self):
        lead = self.engine.create_lead(name="A", email="a@example.com", company="Acme", source="web", request_id="r-1")
        self.assertEqual(lead.status, LeadStatus.NEW)
        qualified = self.engine.qualify(lead.id, score=80)
        self.assertEqual(qualified.status, LeadStatus.QUALIFIED)
        pending = self.engine.request_proposal_approval(lead.id)
        self.assertEqual(pending.next_action, "approval_required")
        self.assertFalse(self.engine.approval_exists(lead.id))
        approved = self.engine.approve_proposal(lead.id, actor="human:owner")
        self.assertEqual(approved.status, LeadStatus.PROPOSAL)
        self.assertTrue(self.engine.approval_exists(lead.id))
        self.assertEqual([e["event_type"] for e in self.engine.audit_events(lead.id)], ["lead_created", "lead_qualified", "proposal_approval_requested", "proposal_approved"])

    def test_idempotent_create_returns_same_lead(self):
        first = self.engine.create_lead(name="B", email="b@example.com", company=None, source="referral", request_id="same")
        second = self.engine.create_lead(name="B", email="b@example.com", company=None, source="referral", request_id="same")
        self.assertEqual(first.id, second.id)
        self.assertEqual(len(self.engine.list_leads()), 1)

    def test_persists_across_engine_instances(self):
        lead = self.engine.create_lead(name="C", email="c@example.com", company=None, source="unknown")
        reopened = RevenueEngine(self.tmp.name)
        self.assertEqual(reopened.get_lead(lead.id).email, "c@example.com")

    def test_low_score_stays_in_nurture(self):
        lead = self.engine.create_lead(name="D", email="d@example.com", company=None, source="referral")
        updated = self.engine.qualify(lead.id, score=20)
        self.assertEqual(updated.status, LeadStatus.NEW)
        self.assertEqual(updated.next_action, "nurture")

    def test_score_range_is_enforced(self):
        lead = self.engine.create_lead(name="E", email="e@example.com", company=None, source="unknown")
        with self.assertRaises(ValueError):
            self.engine.qualify(lead.id, score=101)


if __name__ == "__main__":
    unittest.main()
