from pathlib import Path

import pytest

from idol.iconmanager import PngBasedManager

ROOT_DIRECTORY = Path(__file__).parent.parent.parent.parent / 'example'

DIRECTORIES = [
    ROOT_DIRECTORY,
    ROOT_DIRECTORY / 'actions',
    ROOT_DIRECTORY / 'media'
]


@pytest.fixture(params=DIRECTORIES)
def manager(request) -> PngBasedManager:
    return PngBasedManager(request.param)


def test_submanager_discovery(manager):
    directories = [d for d in manager.directory.iterdir() if d.is_dir()]
    assert len(manager._sub_managers) == len(directories)
    sub_manager_names = [sm.name for sm in manager._sub_managers]
    for sub_dir in [d for d in manager.directory.iterdir() if d.is_dir()]:
        assert sub_dir.name in sub_manager_names


def test_icon_discovery(manager):
    pngs = list(manager.directory.glob('*.png'))
    assert len(pngs) == len(manager._icons)
