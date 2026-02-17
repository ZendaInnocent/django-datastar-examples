from django.core.management.base import BaseCommand

from examples.models import Contact, Item, Notification, Todo


class Command(BaseCommand):
    help = 'Seed the database with demo data for examples'

    def handle(self, *args, **options):
        # Clear existing data
        Contact.objects.all().delete()
        Todo.objects.all().delete()
        Item.objects.all().delete()
        Notification.objects.all().delete()

        # Create Contacts
        contacts_data = [
            ('John', 'Doe', 'john.doe@example.com', '555-0101'),
            ('Jane', 'Smith', 'jane.smith@example.com', '555-0102'),
            ('Bob', 'Johnson', 'bob.johnson@example.com', '555-0103'),
            ('Alice', 'Williams', 'alice.williams@example.com', '555-0104'),
            ('Charlie', 'Brown', 'charlie.brown@example.com', '555-0105'),
            ('Diana', 'Miller', 'diana.miller@example.com', '555-0106'),
            ('Edward', 'Davis', 'edward.davis@example.com', '555-0107'),
            ('Fiona', 'Garcia', 'fiona.garcia@example.com', '555-0108'),
            ('George', 'Martinez', 'george.martinez@example.com', '555-0109'),
            ('Hannah', 'Anderson', 'hannah.anderson@example.com', '555-0110'),
            ('Ivan', 'Taylor', 'ivan.taylor@example.com', '555-0111'),
            ('Julia', 'Thomas', 'julia.thomas@example.com', '555-0112'),
        ]

        for first_name, last_name, email, phone in contacts_data:
            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(contacts_data)} contacts'))

        # Create Todos
        todos_data = [
            'Learn Datastar fundamentals',
            'Build an active search component',
            'Implement inline editing',
            'Add form validation',
            'Create a todo app',
            'Build notifications system',
            'Implement drag and drop',
        ]

        for i, title in enumerate(todos_data):
            Todo.objects.create(title=title, completed=(i % 3 == 0), order=i)

        self.stdout.write(self.style.SUCCESS(f'Created {len(todos_data)} todos'))

        # Create Items (for sortable)
        items_data = [
            ('First Item', 'Description for first item'),
            ('Second Item', 'Description for second item'),
            ('Third Item', 'Description for third item'),
            ('Fourth Item', 'Description for fourth item'),
            ('Fifth Item', 'Description for fifth item'),
        ]

        for i, (name, description) in enumerate(items_data):
            Item.objects.create(name=name, description=description, order=i)

        self.stdout.write(self.style.SUCCESS(f'Created {len(items_data)} items'))

        # Create Notifications
        notifications_data = [
            'Welcome to Django Datastar Examples!',
            'New feature: Active Search is now available',
            'Check out the Click to Load pattern',
            'Inline validation now works in real-time',
            'Try the new TodoMVC example',
            'Notifications system has been updated',
            'Bulk update feature added',
            'Sortable lists are now supported',
        ]

        for i, message in enumerate(notifications_data):
            Notification.objects.create(message=message, read=(i > 2))

        self.stdout.write(
            self.style.SUCCESS(f'Created {len(notifications_data)} notifications')
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
