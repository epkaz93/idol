from pathlib import Path

import pytest
from PIL import ImageChops

from idol import Icon, Colours

BASE_REFERENCE_DIR = Path(Path(__file__).parent / 'reference')
BASE_ICON_DIR = ROOT_DIRECTORY = Path(__file__).parent.parent.parent.parent / 'example' / 'actions'

@pytest.fixture(params=[('delete', 'white'), ('favourite', 'white')])
def colourise_input(request):
    name, colour = request.param
    return (
        Icon.open(BASE_ICON_DIR / f'{name}.png'),
        getattr(Colours, colour.title()),
        Icon.open(BASE_REFERENCE_DIR / f'colourise/{colour}_{name}.png')
    )

def test_colourise(colourise_input):
    icon, colour, expected = colourise_input
    diff = ImageChops.difference(icon.coloured_icon(colour)._image, expected._image)
    assert diff.getbbox() is None
