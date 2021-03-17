"""# HTML attributes dictionary

SQLAlchemy-Mutable is often used with web applications. The HTML attributes 
dict is a mutable JSON serialized dictionary for storing HTML attributes.
"""

from .mutable_dict import MutableDict

from sqlalchemy.types import JSON


class HTMLAttrsType(JSON):
    """
    Column type for HTML attributes dictionaries.
    """
    pass


class HTMLAttrs(MutableDict):
    """
    Maps HTML attribute names to values.

    Notes
    -----
    1. The `class` attribute can be stored as a list of HTML classes.
    2. The `style` attribute can be stored as a dict mapping style keys to 
    values.
    """
    def to_html(self):
        """
        Renders the dictionary as a string of HTML attributes.

        Returns
        -------
        html attributes : str
        """
        def format_item(key, val):
            if val is None or val is False or val == '':
                return ''
            return key if val is True else '{}="{}"'.format(key, val)

        attrs = self.copy()
        if 'class' in attrs and isinstance(attrs['class'], list):
            attrs['class'] = ' '.join(attrs['class'])
        if 'style' in attrs and isinstance(attrs['style'], dict):
            attrs['style'] = ' '.join(
                ['{}:{};'.format(*item) for item in attrs['style'].items()
            ])
        return ' '.join(format_item(*item) for item in attrs.items())


HTMLAttrs.associate_with(HTMLAttrsType)