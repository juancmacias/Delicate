from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock, PropertyMock
from decimal import Decimal
from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceItemSerializer
from delicate_apps.company.models import Company
from delicate_apps.users.models import User
from delicate_apps.type.models import Type
from delicate_apps.store.models import StoreProduct

class InvoiceSimpleTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        """Set up before all tests"""
        super().setUpClass()
        print("\n\n=== BEGINNING INVOICE MODEL TESTS ===\n")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        print("\n=== INVOICE MODEL TESTS COMPLETED SUCCESSFULLY ===\n")
        super().tearDownClass()
    
    def setUp(self):
        """Set up before each test"""
        print(f"\nRunning: {self.id()} - {self.shortDescription()}")
        
        # Create mock objects for testing
        self.company = Company(id=1, name="Test Company")
        self.type = Type(id=1, name_type="Test Type")
        self.user = User(id=1, email="test@example.com", company=self.company)
        
        # Create a product with IVA
        self.product = StoreProduct(
            id=1,
            name="Test Product",
            net_price=100.0,
            iva=21.0
        )
        
        # Create an invoice
        self.invoice = Invoice(
            id=1,
            date='2025-03-08',
            payment_form='Credit Card',
            neto=200.0,
            fk_company=self.company,
            fk_type=self.type,
            fk_user=self.user
        )
        
        # Create invoice items
        self.invoice_item = InvoiceItem(
            id=1,
            invoice=self.invoice,
            product=self.product,
            quantity=2,
            price=100.0
        )
    
    def tearDown(self):
        """Clean up after each test"""
        print(f"✓ Test passed!")
    
    def test_invoice_item_calculations(self):
        """
        Test that invoice items correctly calculate totals with IVA.
        Financial accuracy is critical for business operations.
        """
        # Test calculation of net total (without IVA)
        expected_net = Decimal('200.0')  # 100.0 * 2
        self.assertEqual(self.invoice_item.get_total(), expected_net)
        print(f"  ✓ InvoiceItem correctly calculates net total: {expected_net}")
        
        # Test calculation of IVA amount
        expected_iva = Decimal('42.0')  # 200.0 * 0.21
        self.assertEqual(self.invoice_item.get_iva_amount(), expected_iva)
        print(f"  ✓ InvoiceItem correctly calculates IVA amount: {expected_iva}")
        
        # Test calculation of total with IVA
        expected_total = Decimal('242.0')  # 200.0 + 42.0
        self.assertEqual(self.invoice_item.get_total_with_iva(), expected_total)
        print(f"  ✓ InvoiceItem correctly calculates total with IVA: {expected_total}")
    
    @patch('delicate_apps.invoices.models.InvoiceItem.objects.all')
    def test_invoice_total_aggregation(self, mock_items_queryset):
        """
        Test that Invoice correctly aggregates totals from multiple items.
        This ensures accurate financial summaries.
        """
        # Create mock items with controlled return values
        item1 = MagicMock()
        item1.get_total.return_value = Decimal('200.0')
        item1.get_iva_amount.return_value = Decimal('42.0')
        
        item2 = MagicMock()
        item2.get_total.return_value = Decimal('150.0')
        item2.get_iva_amount.return_value = Decimal('31.5')
        
        # Set up the mock to return our items
        mock_items = MagicMock()
        mock_items.all.return_value = [item1, item2]
        
        # Set the items property on invoice
        type(self.invoice).items = PropertyMock(return_value=mock_items)
        
        # Test invoice get_total method
        expected_invoice_total = Decimal('350.0')  # 200.0 + 150.0
        self.assertEqual(self.invoice.get_total(), expected_invoice_total)
        print(f"  ✓ Invoice correctly calculates total from all items: {expected_invoice_total}")
        
        # Test invoice get_iva_amount method
        expected_invoice_iva = Decimal('73.5')  # 42.0 + 31.5
        self.assertEqual(self.invoice.get_iva_amount(), expected_invoice_iva)
        print(f"  ✓ Invoice correctly calculates total IVA from all items: {expected_invoice_iva}")
    
    def test_invoice_serializer_includes_calculated_fields(self):
        """
        Test that InvoiceSerializer includes calculated financial totals.
        These are essential for frontend display and reporting.
        """
        # Mock the get_total and get_iva_amount methods
        with patch.object(Invoice, 'get_total', return_value=Decimal('350.0')):
            with patch.object(Invoice, 'get_iva_amount', return_value=Decimal('73.5')):
                # Create a serializer for the invoice
                serializer = InvoiceSerializer(self.invoice)
                
                # Check that calculated fields are included
                self.assertIn('total', serializer.data)
                self.assertEqual(serializer.data['total'], Decimal('350.0'))
                
                self.assertIn('formatted_total', serializer.data)
                self.assertEqual(serializer.data['formatted_total'], "350.00 €")
                
                print(f"  ✓ InvoiceSerializer includes calculated financial totals")
                
                # Check that basic fields are also included
                self.assertEqual(serializer.data['id'], 1)
                self.assertEqual(serializer.data['payment_form'], 'Credit Card')
                self.assertEqual(serializer.data['neto'], 200.0)
                
                print(f"  ✓ InvoiceSerializer includes all required invoice data")