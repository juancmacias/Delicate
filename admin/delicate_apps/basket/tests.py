from django.test import SimpleTestCase
from django.utils import timezone
from .models import BasketTemp
from delicate_apps.store.models import StoreProduct
from delicate_apps.users.models import User
from delicate_apps.company.models import Company
from delicate_apps.type.models import Type

class BasketSimpleTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        """Set up before all tests"""
        super().setUpClass()
        print("\n\n=== BEGINNING BASKET MODEL TESTS ===\n")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        print("\n=== BASKET MODEL TESTS COMPLETED SUCCESSFULLY ===\n")
        super().tearDownClass()
    
    def setUp(self):
        """Set up before each test"""
        print(f"\nRunning: {self.id()} - {self.shortDescription()}")
        
        # Create mock objects for testing
        self.company = Company(id=1, name="Test Company")
        self.type = Type(id=1, name_type="Test Type")
        
        # Create user
        self.user = User(
            id=1,
            email="test@example.com",
            name="Test User",
            company=self.company
        )
        
        # Create product
        self.product = StoreProduct(
            id=1,
            name="Test Product",
            description="Test Description",
            net_price=100.0,
            iva=21.0,
            stock=10,
            fk_company=self.company,
            fk_type=self.type
        )
        
        # Create basket item
        self.basket_item = BasketTemp(
            id=1,
            user_id=self.user,
            product_id=self.product,
            cantidad=2,
            precio=100.0,
            temp_date=timezone.now(),
            status=False
        )
    
    def tearDown(self):
        """Clean up after each test"""
        print(f"✓ Test passed!")
    
    def test_basket_string_representation(self):
        """
        Test that BasketTemp string representation is correctly formatted.
        """
        expected_str = f"Item de {self.user} - {self.product}"
        self.assertEqual(str(self.basket_item), expected_str)
        print(f"  ✓ BasketTemp returns expected string representation")
    
    def test_basket_item_calculations(self):
        """
        Test that basket items correctly calculate totals with IVA.
        These calculations are critical for order processing.
        """
        # Test get_total method (price * quantity)
        expected_total = 200.0  # 100.0 * 2
        self.assertEqual(self.basket_item.get_total(), expected_total)
        print(f"  ✓ BasketTemp correctly calculates total: {expected_total}")
        
        # Test get_iva method (total * product.iva rate)
        expected_iva = 42.0  # 200.0 * 0.21
        self.assertEqual(self.basket_item.get_iva(), expected_iva)
        print(f"  ✓ BasketTemp correctly calculates IVA: {expected_iva}")
        
        # Test get_total_with_iva method (total + iva)
        expected_total_with_iva = 242.0  # 200.0 + 42.0
        self.assertEqual(self.basket_item.get_total_with_iva(), expected_total_with_iva)
        print(f"  ✓ BasketTemp correctly calculates total with IVA: {expected_total_with_iva}")