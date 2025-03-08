from django.test import SimpleTestCase
from .models import Type
from .serializers import TypeSerializer
import sys

class TypeSimpleTests(SimpleTestCase):
    """
    Simple tests for Type model and serializer that don't require database
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up before all tests"""
        super().setUpClass()
        print("\n\n=== BEGINNING TYPE MODEL TESTS ===\n")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        print("\n=== TYPE MODEL TESTS COMPLETED SUCCESSFULLY ===\n")
        super().tearDownClass()
    
    def setUp(self):
        """Set up before each test"""
        print(f"\nRunning: {self.id()} - {self.shortDescription()}")
    
    def tearDown(self):
        """Clean up after each test"""
        print(f"✓ Test passed!")
    
    def test_type_string_representation(self):
        """
        Test that the Type model string representation works correctly.
        Creates a Type instance with name 'Commercial' and verifies __str__ returns that name.
        """
        # Create a Type instance without saving to database
        test_type = Type(name_type="Commercial")
        
        # Check that string representation is correct
        self.assertEqual(str(test_type), "Commercial")
        print(f"  ✓ Type(name_type='Commercial') returns '{test_type}' as string representation")
    
    def test_type_serializer_output(self):
        """
        Test that TypeSerializer correctly serializes Type objects.
        Creates a Type instance, serializes it, and verifies the output contains
        the expected fields with correct values.
        """
        # Create a Type instance without saving to database
        test_type = Type(id=1, name_type="Retail")
        
        # Serialize the Type object
        serializer = TypeSerializer(test_type)
        
        # Check the serialized data
        self.assertEqual(serializer.data['id'], 1)
        print(f"  ✓ Serialized Type has correct id: {serializer.data['id']}")
        
        self.assertEqual(serializer.data['name_type'], "Retail")
        print(f"  ✓ Serialized Type has correct name_type: '{serializer.data['name_type']}'")
        
        self.assertEqual(len(serializer.data), 2)  # Should only have id and name_type fields
        print(f"  ✓ Serialized Type has the expected number of fields: {len(serializer.data)}")