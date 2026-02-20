"""
Tests for forms in examples app.

Tests ContactForm including:
- Field validation
- Required fields
- Email validation
- Model form behavior
"""

import pytest

from examples.forms import ContactForm
from examples.models import Contact


@pytest.mark.django_db
class TestContactForm:
    """Tests for ContactForm."""

    def test_valid_form_with_all_fields(self):
        """Form is valid with all required fields."""
        form = ContactForm(
            data={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'phone': '555-1234',
            }
        )
        assert form.is_valid(), form.errors

    def test_valid_form_minimal_fields(self):
        """Form is valid with only required fields."""
        form = ContactForm(
            data={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
            }
        )
        assert form.is_valid(), form.errors

    def test_form_missing_first_name(self):
        """Form is invalid without first_name."""
        form = ContactForm(
            data={
                'last_name': 'Doe',
                'email': 'john@example.com',
            }
        )
        assert not form.is_valid()
        assert 'first_name' in form.errors

    def test_form_missing_last_name(self):
        """Form is invalid without last_name."""
        form = ContactForm(
            data={
                'first_name': 'John',
                'email': 'john@example.com',
            }
        )
        assert not form.is_valid()
        assert 'last_name' in form.errors

    def test_form_missing_email(self):
        """Form is invalid without email."""
        form = ContactForm(
            data={
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_form_invalid_email_format(self):
        """Form is invalid with invalid email format."""
        form = ContactForm(
            data={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'not-an-email',
            }
        )
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_form_valid_email_variations(self):
        """Form accepts various valid email formats."""
        valid_emails = [
            'test@example.com',
            'user.name@domain.org',
            'user+tag@example.co.uk',
        ]
        for email in valid_emails:
            form = ContactForm(
                data={
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': email,
                }
            )
            assert form.is_valid(), f'Failed for email: {email}'

    def test_form_phone_optional(self):
        """Phone field is optional."""
        form = ContactForm(
            data={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'phone': '',
            }
        )
        assert form.is_valid(), form.errors

    def test_form_saves_to_database(self):
        """Form can save to database."""
        form = ContactForm(
            data={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'phone': '555-1234',
            }
        )
        assert form.is_valid()
        contact = form.save()
        assert contact.pk is not None
        assert contact.first_name == 'John'
        assert contact.email == 'john@example.com'

    def test_form_updates_existing_contact(self):
        """Form can update existing contact."""
        contact = Contact.objects.create(
            first_name='Original',
            last_name='Name',
            email='original@example.com',
        )

        form = ContactForm(
            data={
                'first_name': 'Updated',
                'last_name': 'Name',
                'email': 'updated@example.com',
            },
            instance=contact,
        )
        assert form.is_valid()
        contact = form.save()
        assert contact.first_name == 'Updated'
        assert contact.email == 'updated@example.com'

    def test_form_fields_match_model(self):
        """Form fields match Contact model."""
        form = ContactForm()
        expected_fields = ['first_name', 'last_name', 'email', 'phone']
        assert list(form.fields.keys()) == expected_fields

    def test_form_email_field_is_emailfield(self):
        """Email field is properly typed as EmailField."""
        form = ContactForm()
        email_field = form.fields['email']
        assert email_field.__class__.__name__ == 'EmailField'

    def test_form_first_name_max_length(self):
        """First name has correct max length from model."""
        form = ContactForm(
            data={
                'first_name': 'A' * 101,  # 超过100字符
                'last_name': 'Doe',
                'email': 'john@example.com',
            }
        )
        assert not form.is_valid()
        assert 'first_name' in form.errors
