"""
Tests for models in examples app.

Tests the Contact, Todo, Notification, and Item models including:
- Model creation and string representation
- Model ordering
- Field validation
- CRUD operations
"""

import pytest

from examples.models import Contact, Item, Notification, Todo


@pytest.mark.django_db
class TestContactModel:
    """Tests for Contact model."""

    def test_create_contact(self):
        """Contact can be created with required fields."""
        contact = Contact.objects.create(
            first_name='John', last_name='Doe', email='john@example.com'
        )
        assert contact.pk is not None
        assert contact.first_name == 'John'
        assert contact.last_name == 'Doe'
        assert contact.email == 'john@example.com'

    def test_contact_str(self):
        """Contact string representation returns full name."""
        contact = Contact.objects.create(
            first_name='John', last_name='Doe', email='john@example.com'
        )
        assert str(contact) == 'John Doe'

    def test_contact_default_is_active(self):
        """Contact is active by default."""
        contact = Contact.objects.create(
            first_name='Jane', last_name='Doe', email='jane@example.com'
        )
        assert contact.is_active is True

    def test_contact_ordering(self):
        """Contacts are ordered by last_name, then first_name."""
        Contact.objects.create(
            first_name='Bob', last_name='Smith', email='bob@example.com'
        )
        Contact.objects.create(
            first_name='Alice', last_name='Smith', email='alice@example.com'
        )
        Contact.objects.create(
            first_name='Charlie', last_name='Brown', email='charlie@example.com'
        )

        contacts = list(Contact.objects.all())
        assert contacts[0].first_name == 'Charlie'  # Brown comes first
        assert contacts[1].first_name == 'Alice'  # Smith, Alice
        assert contacts[2].first_name == 'Bob'  # Smith, Bob

    def test_contact_email_unique(self):
        """Contact email must be unique."""
        Contact.objects.create(
            first_name='John', last_name='Doe', email='john@example.com'
        )
        with pytest.raises(Exception):  # IntegrityError
            Contact.objects.create(
                first_name='Jane', last_name='Doe', email='john@example.com'
            )

    def test_contact_phone_optional(self):
        """Contact phone field is optional."""
        contact = Contact.objects.create(
            first_name='John', last_name='Doe', email='john2@example.com'
        )
        assert contact.phone == ''

    def test_contact_with_phone(self):
        """Contact can have a phone number."""
        contact = Contact.objects.create(
            first_name='John',
            last_name='Doe',
            email='john3@example.com',
            phone='555-1234',
        )
        assert contact.phone == '555-1234'


@pytest.mark.django_db
class TestTodoModel:
    """Tests for Todo model."""

    def test_create_todo(self):
        """Todo can be created with required fields."""
        todo = Todo.objects.create(title='Buy milk')
        assert todo.pk is not None
        assert todo.title == 'Buy milk'
        assert todo.is_completed is False

    def test_todo_str(self):
        """Todo string representation returns title."""
        todo = Todo.objects.create(title='Buy milk')
        assert str(todo) == 'Buy milk'

    def test_todo_default_completed(self):
        """Todo is not completed by default."""
        todo = Todo.objects.create(title='Test')
        assert todo.is_completed is False

    def test_todo_ordering(self):
        """Todos are ordered by -order (descending), then created_at."""
        Todo.objects.create(title='First', order=1)
        Todo.objects.create(title='Second', order=0)
        Todo.objects.create(title='Third', order=2)

        todos = list(Todo.objects.all())
        assert todos[0].title == 'Third'  # order=2 (highest, descending)
        assert todos[1].title == 'First'  # order=1
        assert todos[2].title == 'Second'  # order=0

    def test_todo_mark_completed(self):
        """Todo can be marked as completed."""
        todo = Todo.objects.create(title='Test')
        todo.is_completed = True
        todo.save()

        todo.refresh_from_db()
        assert todo.is_completed is True


@pytest.mark.django_db
class TestNotificationModel:
    """Tests for Notification model."""

    def test_create_notification(self):
        """Notification can be created."""
        notification = Notification.objects.create(message='Test message')
        assert notification.pk is not None
        assert notification.message == 'Test message'
        assert notification.read is False

    def test_notification_str(self):
        """Notification string representation returns message."""
        notification = Notification.objects.create(message='Test message')
        assert str(notification) == 'Test message'

    def test_notification_default_read(self):
        """Notification is unread by default."""
        notification = Notification.objects.create(message='Test')
        assert notification.read is False

    def test_notification_ordering(self):
        """Notifications are ordered by created_at."""
        Notification.objects.create(message='First')
        Notification.objects.create(message='Second')

        notifications = list(Notification.objects.all())
        assert notifications[0].message == 'First'
        assert notifications[1].message == 'Second'

    def test_notification_mark_read(self):
        """Notification can be marked as read."""
        notification = Notification.objects.create(message='Test')
        notification.read = True
        notification.save()

        notification.refresh_from_db()
        assert notification.read is True


@pytest.mark.django_db
class TestItemModel:
    """Tests for Item model."""

    def test_create_item(self):
        """Item can be created."""
        item = Item.objects.create(name='Test Item')
        assert item.pk is not None
        assert item.name == 'Test Item'

    def test_item_str(self):
        """Item string representation returns name."""
        item = Item.objects.create(name='Test Item')
        assert str(item) == 'Test Item'

    def test_item_description_optional(self):
        """Item description field is optional."""
        item = Item.objects.create(name='Test')
        assert item.description == ''

    def test_item_with_description(self):
        """Item can have a description."""
        item = Item.objects.create(name='Test', description='A test item description')
        assert item.description == 'A test item description'

    def test_item_ordering(self):
        """Items are ordered by order field (ascending)."""
        Item.objects.create(name='First', order=2)
        Item.objects.create(name='Second', order=0)
        Item.objects.create(name='Third', order=1)

        items = list(Item.objects.all())
        # Ordered by 'order' ascending: 0, 1, 2
        assert items[0].name == 'Second'  # order=0
        assert items[1].name == 'Third'  # order=1
        assert items[2].name == 'First'  # order=2


class TestModelMeta:
    """Tests for model Meta options."""

    def test_contact_meta_ordering(self):
        """Contact model has correct ordering."""
        assert Contact._meta.ordering == ['last_name', 'first_name']

    def test_todo_meta_ordering(self):
        """Todo model has correct ordering."""
        assert Todo._meta.ordering == ['-order', 'created_at']

    def test_notification_meta_ordering(self):
        """Notification model has correct ordering."""
        assert Notification._meta.ordering == ['created_at']

    def test_item_meta_ordering(self):
        """Item model has correct ordering."""
        assert Item._meta.ordering == ['order']
