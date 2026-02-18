"""
Management command to rebuild the search index.

This command rebuilds the search index from examples and documentation.
Run this command whenever new examples or documentation are added.
"""

from django.core.management.base import BaseCommand, CommandError

from examples.search import rebuild_search_index


class Command(BaseCommand):
    """Rebuild the search index for examples and documentation."""

    help = 'Rebuild the search index from examples and documentation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed information about indexed content',
        )

    def handle(self, *args, **options):
        """Execute the command."""
        verbose = options.get('verbose', False)

        self.stdout.write('Rebuilding search index...')

        try:
            index = rebuild_search_index()

            # Get statistics
            examples = [e for e in index.entries if e.type == 'example']
            docs = [e for e in index.entries if e.type == 'doc']

            self.stdout.write(
                self.style.SUCCESS(
                    f'Search index rebuilt successfully!\n'
                    f'  - Total entries: {len(index.entries)}\n'
                    f'  - Examples: {len(examples)}\n'
                    f'  - Documentation: {len(docs)}'
                )
            )

            if verbose:
                self.stdout.write('\nIndexed Examples:')
                for entry in examples:
                    self.stdout.write(f'  - {entry.title} ({entry.category})')

                self.stdout.write('\nIndexed Documentation:')
                for entry in docs:
                    self.stdout.write(f'  - {entry.title}')

        except Exception as e:
            raise CommandError(f'Failed to rebuild search index: {e}')
