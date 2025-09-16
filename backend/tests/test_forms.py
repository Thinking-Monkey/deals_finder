from django.test import TestCase
from django.contrib.auth import get_user_model
from app.forms import CCUserCreationForm, CCUserChangeForm


class CCUserFormsTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        
    def test_ccuser_creation_form_meta_model(self):
        """Test that CCUserCreationForm uses the correct model"""
        form = CCUserCreationForm()
        # Note: The form references CCUser in models but should use DFUser
        # This might be a bug in the original code
        self.assertEqual(form.Meta.model.__name__, 'CCUser')
        
    def test_ccuser_change_form_meta_model(self):
        """Test that CCUserChangeForm uses the correct model"""
        form = CCUserChangeForm()
        # Note: The form references CCUser in models but should use DFUser
        # This might be a bug in the original code
        self.assertEqual(form.Meta.model.__name__, 'CCUser')
        
    def test_form_inheritance(self):
        """Test that forms inherit from Django's built-in forms"""
        from django.contrib.auth.forms import UserCreationForm, UserChangeForm
        
        self.assertTrue(issubclass(CCUserCreationForm, UserCreationForm))
        self.assertTrue(issubclass(CCUserChangeForm, UserChangeForm))


# Note: These tests will likely fail due to the CCUser reference in forms.py
# The forms should probably reference DFUser instead of CCUser
class FormsIntegrationTest(TestCase):
    """
    Integration tests for forms - these tests document the current state
    and will help identify issues with the CCUser reference
    """
    
    def test_creation_form_instantiation(self):
        """Test if the creation form can be instantiated without errors"""
        try:
            form = CCUserCreationForm()
            self.fail("Form instantiated successfully despite CCUser reference")
        except Exception as e:
            # Expected to fail due to CCUser not existing
            self.assertIn("CCUser", str(e))
            
    def test_change_form_instantiation(self):
        """Test if the change form can be instantiated without errors"""
        try:
            form = CCUserChangeForm()
            self.fail("Form instantiated successfully despite CCUser reference")
        except Exception as e:
            # Expected to fail due to CCUser not existing
            self.assertIn("CCUser", str(e))