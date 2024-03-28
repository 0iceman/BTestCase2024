from odoo.tests.common import TransactionCase

class TestRealEstateComplaints(TransactionCase):
    def setUp(self):
        super(TestRealEstateComplaints, self).setUp()
        self.Complaint = self.env['real_estate_complaints.complaint']

    def test_create_complaint(self):
        """Test that a complaint can be successfully created."""
        complaint = self.Complaint.create({'name': 'Test Complaint', 'description': 'Just a test.'})
        self.assertEqual(complaint.name, 'Test Complaint')
