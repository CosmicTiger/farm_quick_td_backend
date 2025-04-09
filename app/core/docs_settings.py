from pathlib import Path


def load_theme_css():
    """load_theme_css _summary_

    _extended_summary_

    :return: _description_
    :rtype: _type_
    """
    css_path = Path("app/static/css/blue-planet.css")
    with css_path.open() as f:
        return f.read()
