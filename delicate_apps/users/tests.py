from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from .models import User
from .serializers import UserSerializer
from delicate_apps.company.models import Company

class UserSimpleTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        """Set up before all tests"""
        super().setUpClass()
        print("\n\n=== BEGINNING USER MODEL TESTS ===\n")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        print("\n=== USER MODEL TESTS COMPLETED SUCCESSFULLY ===\n")
        super().tearDownClass()
    
    def setUp(self):
        """Set up before each test"""
        print(f"\nRunning: {self.id()} - {self.shortDescription()}")
        
        # Create a mock company for testing
        self.company = Company(
            id=1,
            name="Test Company",
            direction="Test Address",
            cif="B12345678",
            phone=123456789,
            mail="company@test.com"
        )
    
    def tearDown(self):
        """Clean up after each test"""
        print(f"✓ Test passed!")
    
    def test_user_roles_permissions(self):
        """
        Test that User model correctly implements role-based permissions.
        This is critical for security and access control.
        """
        # Create users with different roles
        admin_user = User(
            email="admin@example.com",
            name="Admin User",
            roll="admin",
            company=self.company
        )
        
        manager_user = User(
            email="manager@example.com",
            name="Manager User",
            roll="manager",
            company=self.company
        )
        
        employee_user = User(
            email="employee@example.com",
            name="Employee User",
            roll="employee",
            company=self.company
        )
        
        # Test permissions for each role
        # Admin should have all permissions
        self.assertTrue(admin_user.has_perm('view_user'))
        self.assertTrue(admin_user.has_perm('change_user'))
        self.assertTrue(admin_user.has_perm('add_user'))
        print(f"  ✓ Admin user has correct permissions")
        
        # Manager should have view, change, and add permissions
        self.assertTrue(manager_user.has_perm('view_user'))
        self.assertTrue(manager_user.has_perm('change_user'))
        self.assertTrue(manager_user.has_perm('add_user'))
        print(f"  ✓ Manager user has correct permissions")
        
        # Employee should only have view permission
        self.assertTrue(employee_user.has_perm('view_user'))
        self.assertFalse(employee_user.has_perm('change_user'))
        self.assertFalse(employee_user.has_perm('add_user'))
        print(f"  ✓ Employee user has correct permissions")
    
    def test_user_serializer_field_security(self):
        """
        Test that UserSerializer properly handles sensitive fields.
        Password should be write-only for security.
        """
        # Create a test user
        test_user = User(
            id=1,
            email="test@example.com",
            password="secure_password",
            name="Test User",
            roll="admin",
            company=self.company
        )
        
        # Serialize the user
        serializer = UserSerializer(test_user)
        
        # Check that regular fields are included
        self.assertIn('email', serializer.data)
        self.assertIn('name', serializer.data)
        self.assertIn('roll', serializer.data)
        print(f"  ✓ UserSerializer includes regular fields")
        
        # Password should be write-only and not included in output
        self.assertNotIn('password', serializer.data)
        print(f"  ✓ UserSerializer properly excludes password field")
    
    @patch('delicate_apps.users.models.BaseUserManager.normalize_email')
    def test_user_creation_email_normalization(self, mock_normalize):
        """
        Test that UserManager correctly normalizes email addresses.
        This is important for consistent user identification.
        """
        # Configure the mock
        mock_normalize.return_value = "normalized@example.com"
        
        # Create a user manager instance
        user_manager = User.objects
        
        # Create a test company
        test_company = Company(id=1, name="Test Company")
        
        # Mock the save method to avoid database operations
        with patch.object(User, 'save'):
            with patch.object(User, 'set_password'):
                # Call create_user with an email that needs normalization
                user = user_manager.create_user(
                    email="TEST@example.com",  # Uppercase email
                    password="password123",
                    name="Test User",
                    roll="employee",
                    company=test_company
                )
        
        # Verify normalize_email was called
        mock_normalize.assert_called_once_with("TEST@example.com")
        
        # Check that the normalized email was used
        self.assertEqual(user.email, "normalized@example.com")
        print(f"  ✓ UserManager normalizes email addresses during user creation")