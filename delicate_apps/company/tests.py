from django.test import SimpleTestCase
from .models import Company
from .serializers import CompanySerializer

class CompanySimpleTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        """Set up before all tests"""
        super().setUpClass()
        print("\n\n=== BEGINNING COMPANY MODEL TESTS ===\n")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        print("\n=== COMPANY MODEL TESTS COMPLETED SUCCESSFULLY ===\n")
        super().tearDownClass()
    
    def setUp(self):
        """Set up before each test"""
        print(f"\nRunning: {self.id()} - {self.shortDescription()}")
    
    def tearDown(self):
        """Clean up after each test"""
        print(f"✓ Test passed!")
    
    def test_company_string_representation(self):
        """
        Test that the Company model string representation works correctly.
        Creates a Company instance and verifies __str__ returns the company name.
        """
        # Create a Company instance without saving to database
        test_company = Company(
            name="Test Company",
            direction="Test Address",
            cif="B12345678",
            phone=123456789,
            mail="test@company.com"
        )
        
        # Check that string representation is correct
        self.assertEqual(str(test_company), "Test Company")
        print(f"  ✓ Company returns '{test_company}' as string representation")
    
    def test_company_serializer_output(self):
        """
        Test that CompanySerializer correctly serializes Company objects.
        Creates a Company instance, serializes it, and verifies the output contains
        the expected fields with correct values.
        """
        # Create a Company instance without saving to database
        test_company = Company(
            id=1,
            name="Test Company",
            direction="Test Address",
            cif="B12345678",
            phone=123456789,
            mail="test@company.com"
        )
        
        # Serialize the Company object
        serializer = CompanySerializer(test_company)
        
        # Check the serialized data
        self.assertEqual(serializer.data['id'], 1)
        print(f"  ✓ Serialized Company has correct id: {serializer.data['id']}")
        
        self.assertEqual(serializer.data['name'], "Test Company")
        print(f"  ✓ Serialized Company has correct name: '{serializer.data['name']}'")
        
        self.assertEqual(serializer.data['cif'], "B12345678")
        print(f"  ✓ Serialized Company has correct CIF: '{serializer.data['cif']}'")
        
        self.assertEqual(serializer.data['phone'], '123456789')
        print(f"  ✓ Serialized Company has correct phone: {serializer.data['phone']}")
        
        self.assertEqual(serializer.data['mail'], "test@company.com")
        print(f"  ✓ Serialized Company has correct mail: '{serializer.data['mail']}'")
        
        self.assertEqual(serializer.data['direction'], "Test Address")
        print(f"  ✓ Serialized Company has correct direction: '{serializer.data['direction']}'")
        
        # All fields should be present (id, name, direction, cif, phone, mail)
        self.assertEqual(len(serializer.data), 6)
        print(f"  ✓ Serialized Company has the expected number of fields: {len(serializer.data)}")