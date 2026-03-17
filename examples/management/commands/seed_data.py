from django.core.management.base import BaseCommand

from examples.models import Answer, Contact, Item, Notification, Question, Todo


class Command(BaseCommand):
    help = 'Seed the database with demo data for examples'

    def handle(self, *args, **options):
        # Clear existing data
        Contact.objects.all().delete()
        Todo.objects.all().delete()
        Item.objects.all().delete()
        Notification.objects.all().delete()
        Question.objects.all().delete()

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

        Contact.objects.bulk_create(
            [
                Contact(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                )
                for first_name, last_name, email, phone in contacts_data
            ]
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

        Todo.objects.bulk_create(
            [
                Todo(title=title, is_completed=(i % 3 == 0), order=i)
                for i, title in enumerate(todos_data)
            ]
        )
        self.stdout.write(self.style.SUCCESS(f'Created {len(todos_data)} todos'))

        # Create Items (for sortable)
        items_data = [
            ('First Item', 'Description for first item'),
            ('Second Item', 'Description for second item'),
            ('Third Item', 'Description for third item'),
            ('Fourth Item', 'Description for fourth item'),
            ('Fifth Item', 'Description for fifth item'),
        ]

        Item.objects.bulk_create(
            [
                Item(name=name, description=description, order=i)
                for i, (name, description) in enumerate(items_data)
            ]
        )
        self.stdout.write(self.style.SUCCESS(f'Created {len(items_data)} items'))

        # Create Notifications (one for each example)
        notifications_data = [
            'Active Search: Search contacts with debounced input',
            'Click to Load: Pagination with Load More button',
            'Edit Row: Inline editing for table rows',
            'Delete Row: Remove rows with animation',
            'TodoMVC: Classic todo app implementation',
            'Inline Validation: Real-time form validation',
            'Infinite Scroll: Auto-load more on scroll',
            'Lazy Tabs: Load tab content on demand',
            'File Upload: Upload with progress indicator',
            'Sortable: Drag-and-drop reordering',
            'Notifications: Real-time notification counter',
            'Bulk Update: Select and update multiple items',
        ]

        Notification.objects.bulk_create(
            [
                Notification(message=message, read=(i > 2))
                for i, message in enumerate(notifications_data)
            ]
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Created {len(notifications_data)} notifications (one per example)'
            )
        )

        # Create Quiz Questions (Django & Datastar themed)
        questions_data = [
            {
                'text': 'What is Datastar?',
                'answers': [
                    ('A hypermedia-driven UI library', True),
                    ('A JavaScript framework like React', False),
                    ('A CSS framework', False),
                    ('A database ORM', False),
                ],
            },
            {
                'text': 'What does SSE stand for in web development?',
                'answers': [
                    ('Server-Sent Events', True),
                    ('Single Socket Exchange', False),
                    ('Secure Session Encryption', False),
                    ('Simple State Engine', False),
                ],
            },
            {
                'text': 'Which Datastar attribute is used to bind input values to signals?',
                'answers': [
                    ('data-bind', True),
                    ('data-model', False),
                    ('data-value', False),
                    ('data-input', False),
                ],
            },
            {
                'text': 'What decorator does Datastar provide for Django views?',
                'answers': [
                    ('@datastar_response', True),
                    ('@sse_response', False),
                    ('@datastar_view', False),
                    ('@stream_response', False),
                ],
            },
            {
                'text': 'Which attribute triggers a GET request in Datastar?',
                'answers': [
                    ('data-on:click="@get()"', True),
                    ('data-fetch', False),
                    ('data-request', False),
                    ('data-http-get', False),
                ],
            },
            {
                'text': 'What is the purpose of data-signals in Datastar?',
                'answers': [
                    ('To define reactive state variables', True),
                    ('To create CSS animations', False),
                    ('To validate form inputs', False),
                    ('To configure routing', False),
                ],
            },
            {
                'text': 'How does Datastar merge HTML fragments into the DOM?',
                'answers': [
                    ('Using idiomorph for intelligent merging', True),
                    ('By replacing the entire page', False),
                    ('Using innerHTML only', False),
                    ('By creating new iframes', False),
                ],
            },
            {
                'text': 'What HTTP header identifies a Datastar request?',
                'answers': [
                    ('Datastar-Request', True),
                    ('X-Datastar', False),
                    ('Datastar-Version', False),
                    ('X-SSE-Request', False),
                ],
            },
            {
                'text': 'Which Django class is used for SSE responses in datastar-py?',
                'answers': [
                    ('ServerSentEventGenerator', True),
                    ('SSEStream', False),
                    ('EventStream', False),
                    ('DatastarStream', False),
                ],
            },
            {
                'text': 'What method merges new content into existing elements in Datastar?',
                'answers': [
                    ('patch_elements', True),
                    ('merge_html', False),
                    ('update_dom', False),
                    ('replace_content', False),
                ],
            },
            {
                'text': 'How do you add a debounce delay to an input event in Datastar?',
                'answers': [
                    ('data-on:input__debounce.200ms', True),
                    ('data-debounce:input:200', False),
                    ('data-input:debounce(200)', False),
                    ('data-on:input:delay(200)', False),
                ],
            },
            {
                'text': 'What is the purpose of data-indicator in Datastar?',
                'answers': [
                    ('Show loading state during requests', True),
                    ('Display tooltips', False),
                    ('Validate form fields', False),
                    ('Highlight active elements', False),
                ],
            },
            {
                'text': 'Which Django template function renders partial templates?',
                'answers': [
                    ('render_to_string', True),
                    ('render_partial', False),
                    ('fragment', False),
                    ('render_fragment', False),
                ],
            },
            {
                'text': 'What does data-on:submit.prevent do in Datastar?',
                'answers': [
                    ('Prevents the default form submission', True),
                    ('Adds a submit button', False),
                    ('Validates the form', False),
                    ('Creates a loading indicator', False),
                ],
            },
            {
                'text': 'What is the correct way to update signals in Datastar from Django?',
                'answers': [
                    ('SSE.patch_signals({"key": value})', True),
                    ('SSE.update_signals({"key": value})', False),
                    ('SSE.set_signal("key", value)', False),
                    ('SSE.send_signal({"key": value})', False),
                ],
            },
            {
                'text': 'How does data-on:click__throttle.500ms differ from __debounce?',
                'answers': [
                    ('Throttle fires at most once per 500ms', True),
                    ('They do the same thing', False),
                    ('Debounce fires more frequently', False),
                    ('Throttle only works on scroll events', False),
                ],
            },
            {
                'text': 'What Python package provides Django-Datastar integration?',
                'answers': [
                    ('datastar-py', True),
                    ('django-datastar', False),
                    ('datastar-django', False),
                    ('sse-django', False),
                ],
            },
            {
                'text': 'Which attribute modifier prevents default browser behavior?',
                'answers': [
                    ('__prevent', True),
                    ('__stop', False),
                    ('__block', False),
                    ('__cancel', False),
                ],
            },
            {
                'text': 'What is the recommended way to structure Datastar responses?',
                'answers': [
                    ('Return HTML fragments with SSE', True),
                    ('Return JSON objects', False),
                    ('Return full HTML pages', False),
                    ('Return XML responses', False),
                ],
            },
            {
                'text': 'How do you select a specific element to patch in Datastar?',
                'answers': [
                    ('SSE.patch_elements(html, selector="#id")', True),
                    ('SSE.patch_elements(html, target="#id")', False),
                    ('SSE.patch_to(html, "#id")', False),
                    ('SSE.update_element("#id", html)', False),
                ],
            },
        ]

        # Bulk create questions
        question_objects = [Question(text=q_data['text']) for q_data in questions_data]
        Question.objects.bulk_create(question_objects)

        # Bulk create answers (need to associate with created questions)
        answer_objects = []
        for question, q_data in zip(question_objects, questions_data):
            for answer_text, is_correct in q_data['answers']:
                answer_objects.append(
                    Answer(question=question, text=answer_text, is_correct=is_correct)
                )
        Answer.objects.bulk_create(answer_objects)

        self.stdout.write(
            self.style.SUCCESS(
                f'Created {len(question_objects)} quiz questions with {len(answer_objects)} answers'
            )
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
