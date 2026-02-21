from itertools import cycle

from model_bakery.recipe import Recipe, baker

from .models import Contact, Item, Notification, Todo

# Contact Recipes
contact = Recipe(
    Contact,
    first_name=baker.seq('Contact'),
    last_name=baker.seq('User'),
    email=baker.seq('user', suffix='@example.com'),
    phone='',
)

contact_with_phone = Recipe(
    Contact,
    first_name=baker.seq('Contact'),
    last_name=baker.seq('User'),
    email=baker.seq('user', suffix='@example.com'),
    phone=baker.seq('555-000-', start=1000),
)


# Todo Recipes
todo = Recipe(
    Todo,
    title=baker.seq('Task'),
    is_completed=False,
    order=baker.seq(1),
)

todo_completed = Recipe(
    Todo,
    title=baker.seq('Completed Task'),
    is_completed=True,
    order=baker.seq(1),
)


# Notification Recipes
notification = Recipe(
    Notification,
    message=baker.seq('Notification message'),
    read=False,
)

notification_read = Recipe(
    Notification,
    message=baker.seq('Read notification'),
    read=True,
)

# Cycle through common notification messages
notification_messages = [
    'New message received',
    'Your order has shipped',
    'Password changed successfully',
    'New comment on your post',
    'Meeting reminder',
]
notification_cycled = Recipe(
    Notification,
    message=cycle(notification_messages),
    read=False,
)


# Item Recipes
item = Recipe(
    Item,
    name=baker.seq('Item'),
    description='',
    order=baker.seq(1),
)

item_with_description = Recipe(
    Item,
    name=baker.seq('Item'),
    description=baker.seq('Description for item'),
    order=baker.seq(1),
)
