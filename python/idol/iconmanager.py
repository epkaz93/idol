from __future__ import annotations
from pathlib import Path

from idol.icon import Icon

import typing

if typing:
    from idol.transformrules import TransformRuleBase


class IconManager(object):

    def __init__(self, directory: typing.Union[Path, str], name=None, recursive: bool = False,
                 patterns: typing.List[str] = None, transforms: typing.List[TransformRuleBase] = None):

        self._directory = directory if isinstance(directory, Path) else Path(directory)
        self._name = name
        self._recursive = recursive
        self._patterns = patterns if patterns else []
        self._transforms = transforms if transforms else []
        self._icons = []
        self._sub_managers = []

        self.setup()

    def setup(self):
        for pattern in self.patterns:
            for file_ in self.directory.glob(pattern):
                icon = Icon.open(file_)
                name = file_.stem
                for transform in self.transforms:
                    icon = transform.execute(icon)
                self.__setattr__(name, icon)
                self._icons.append(icon)

        if self.recursive:
            for directory in [d for d in self.directory.iterdir() if d.is_dir()]:
                cls = self.__class__
                sub_manager = cls(directory, recursive=self.recursive,
                                  patterns=self.patterns, transforms=self.transforms)

                self.__setattr__(sub_manager.name, sub_manager)
                self._sub_managers.append(sub_manager)

    @property
    def directory(self) -> Path:
        return self._directory

    @directory.setter
    def directory(self, directory):
        self._directory = directory

    @property
    def patterns(self):
        return self._patterns

    @property
    def transforms(self):
        return self._transforms

    @property
    def name(self):
        return self._name or self.directory.name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def recursive(self):
        return self._recursive

    def icon_from_name(self, name):
        if '.' in name:
            parts = name.split('.')
            sub_manager = self.__getattribute__(parts[0])
            return sub_manager.icon_from_name('.'.join(parts[1:]))
        else:
            return self.__getattribute__(name)

    def __getattribute__(self, item) -> typing.Union[Icon, IconManager]:
        return super().__getattribute__(item)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name} {len(self._sub_managers)} {len(self._icons)}>'


class PngBasedManager(IconManager):

    def __init__(self, directory, name=None, recursive=True, patterns=None, transforms=None):

        patterns_ = ['*.png']
        if patterns:
            for pattern in patterns:
                if pattern not in patterns_:
                    patterns_.extend(pattern)

        super().__init__(directory, name, recursive=recursive, patterns=patterns_, transforms=transforms)
