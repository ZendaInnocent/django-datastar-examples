"""
Django template tags for HowTo panels.
"""

from django import template

from ..howto_config import get_example

register = template.Library()


@register.simple_tag
def howto_config(slug: str):
    """Get HowTo configuration for an example."""
    return get_example(slug)


@register.simple_tag
def howto_title(slug: str, default: str = ''):
    """Get the title for an example's HowTo panel."""
    example = get_example(slug)
    return example.title if example else default


@register.simple_tag
def howto_description(slug: str, default: str = ''):
    """Get the description for an example's HowTo panel."""
    example = get_example(slug)
    return example.description if example else default


@register.inclusion_tag('examples/fragments/howto_content.html')
def howto_content(slug: str):
    """
    Render complete HowTo content for an example.

    Usage:
        {% howto_content "active-search" %}
    """
    example = get_example(slug)
    return {
        'example': example,
        'slug': slug,
    }


@register.inclusion_tag('examples/fragments/howto_code_block.html')
def howto_code_block(
    title: str,
    code: str,
    language: str = 'python',
    step_number: int = 1,
    description: str = '',
):
    """
    Render a code block for a HowTo step.

    Usage:
        {% howto_code_block "The View" code_var "python" 1 "Description here" %}
    """
    return {
        'title': title,
        'code': code,
        'language': language,
        'step_number': step_number,
        'description': description,
    }


@register.simple_tag
def howto_doc_links(slug: str):
    """Get documentation links for an example."""
    example = get_example(slug)
    return example.doc_links if example else []


@register.simple_tag
def howto_step_count(slug: str) -> int:
    """Get the number of steps for an example."""
    example = get_example(slug)
    return len(example.steps) if example and example.steps else 0
