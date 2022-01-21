from __future__ import annotations

import six
import abc

from idol.colour import Colour

import typing

if typing.TYPE_CHECKING:
    from idol import Icon


@six.add_metaclass(abc.ABCMeta)
class TransformRuleBase(object):

    @abc.abstractmethod
    def execute(self, icon: Icon) -> Icon:
        raise NotImplementedError()


class ColouriseTransformRule(TransformRuleBase):

    def __init__(self, colour: Colour):
        self._colour = colour

    def execute(self, icon: Icon) -> Icon:
        return icon.coloured_icon(self._colour)
