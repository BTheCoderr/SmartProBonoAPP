import unittest
from ai.document_analyzer import DocumentAnalyzer

class TestDocumentAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = DocumentAnalyzer()
        
        # Sample documents for testing
        self.sample_contract = """
        AGREEMENT
        
        This Agreement is made on April 15, 2023, between ABC Corporation ("Company") 
        and John Smith ("Consultant").
        
        1. SERVICES
        Consultant shall provide marketing consulting services.
        
        2. TERM
        This Agreement shall commence on May 1, 2023 and continue until terminated.
        
        3. COMPENSATION
        Company shall pay Consultant $5,000 per month.
        """
        
        self.sample_legal_brief = """
        IN THE UNITED STATES DISTRICT COURT
        FOR THE NORTHERN DISTRICT OF CALIFORNIA
        
        Case No. CV-2023-12345
        
        PLAINTIFF'S MOTION FOR SUMMARY JUDGMENT
        
        Plaintiff respectfully moves this Court for summary judgment pursuant to 
        Rule 56 of the Federal Rules of Civil Procedure.
        """
        
        self.sample_immigration_form = """
        FORM I-589
        APPLICATION FOR ASYLUM
        
        Full Name: Maria Garcia
        Date of Birth: 05/12/1985
        Country of Origin: Mexico
        """
    
    def test_document_type_detection(self):
        """Test automatic document type detection"""
        contract_type = self.analyzer._detect_document_type(self.sample_contract)
        self.assertEqual(contract_type, "contract")
        
        brief_type = self.analyzer._detect_document_type(self.sample_legal_brief)
        self.assertEqual(brief_type, "legal_brief")
        
        immigration_type = self.analyzer._detect_document_type(self.sample_immigration_form)
        self.assertEqual(immigration_type, "immigration_form")
    
    def test_contract_analysis(self):
        """Test contract document analysis"""
        result = self.analyzer.analyze_document(self.sample_contract, "contract")
        
        # Check basic structure
        self.assertIn("document_type", result)
        self.assertIn("analysis_timestamp", result)
        self.assertIn("basic_analysis", result)
        self.assertIn("contract_analysis", result)
        
        # Check contract-specific analysis
        contract_analysis = result["contract_analysis"]
        self.assertIn("parties", contract_analysis)
        self.assertIn("dates", contract_analysis)
        self.assertIn("key_clauses", contract_analysis)
        
        # Verify extracted information
        parties = contract_analysis["parties"]
        self.assertTrue(any("ABC Corporation" in party for party in parties))
        self.assertTrue(any("John Smith" in party for party in parties))
    
    def test_empty_document(self):
        """Test handling of empty documents"""
        with self.assertRaises(ValueError):
            self.analyzer.analyze_document("")
        
        with self.assertRaises(ValueError):
            self.analyzer.analyze_document(None)
    
    def test_entity_extraction(self):
        """Test named entity extraction"""
        result = self.analyzer.analyze_document(self.sample_contract)
        entities = result["basic_analysis"]["named_entities"]
        
        self.assertIn("organizations", entities)
        self.assertIn("people", entities)
        self.assertIn("dates", entities)
        self.assertIn("monetary_values", entities)
        
        # Verify extracted entities
        self.assertTrue(any("ABC Corporation" in org for org in entities["organizations"]))
        self.assertTrue(any("John Smith" in person for person in entities["people"]))
        self.assertTrue(any("$5,000" in value for value in entities["monetary_values"]))

if __name__ == '__main__':
    unittest.main() 