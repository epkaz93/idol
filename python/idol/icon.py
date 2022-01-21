from __future__ import annotations

from functools import lru_cache
from PIL import Image, ImageDraw, ImageOps

from idol.colour import Colour

import typing


class Icon(object):

    def __init__(self, image: Image.Image):
        self._image = image

    @property
    def width(self):
        return self._image.width

    @property
    def height(self):
        return self._image.height

    @property
    def size(self):
        return self.width, self.height

    @property
    @lru_cache
    def qpixmap(self):
        return self._image.toqpixmap()

    @lru_cache
    def badge(self, image: Icon, colour: Colour) -> Icon:
        width, height = image.size
        factor = 0.4
        padding = 0.075
        outline = colour.multiply(0.3)
        outline_width = 0.05

        image = image.resize(
            (round(width * (factor - outline_width * 2) - 1), round(height * (factor - outline_width * 2) - 1)),
            resample=Image.ANTIALIAS
        )

        image_with_badge = self.draw_badge(colour, outline=outline, padding=padding, width=outline_width, factor=factor)

        bounding_box = self._badge_bounding_box(image_with_badge, padding, factor)
        x = bounding_box[0] + round(image_with_badge.width * outline_width + 1)
        y = bounding_box[1] + round(image_with_badge.height * outline_width + 1)

        new_image = Icon.new(image_with_badge.size)
        new_image = new_image.paste(image, box=(x, y))

        return image_with_badge.overlay(new_image)

    def paste(self, image, box=None, mask=None):
        new_image = self._image.copy()
        new_image.paste(image._image, box, mask)
        return self.from_pil_image(new_image)

    def resize(self, size, resample=None, box=None, reducing_gap=None) -> Icon:
        return self.from_pil_image(self._image.resize(size, resample, box, reducing_gap))

    def coloured_icon(self, colour: Colour, mode='fill'):
        r, g, b, alpha = self._image.split()

        if mode == 'colourise':
            greyscale = ImageOps.autocontrast(ImageOps.grayscale(self._image))
            coloured = ImageOps.colorize(greyscale, (0, 0, 0, 0), colour.rgb)
            coloured.putalpha(alpha)
            image = Image.new('RGBA', coloured.size)
            image.paste(coloured)

            return self.from_pil_image(image)

        elif mode == 'fill':
            image = Image.new('RGBA', self.size)
            image.paste(colour.rgb, (0, 0, image.width, image.height))
            image.putalpha(alpha)
            return self.from_pil_image(image)

    def _badge_bounding_box(self, image, padding, factor) -> typing.Tuple:
        sample_size = min(image.width, image.height)
        padding_size = sample_size * padding
        badge_width = sample_size * factor

        return (
            round(image.width - padding_size - badge_width),
            round(0 + padding_size),
            round(image.width - padding_size),
            round(0 + padding_size + badge_width)
        )

    @lru_cache
    def overlay(self, image: Icon):
        return self.from_pil_image(Image.alpha_composite(self._image, image._image))

    def copy(self) -> Icon:
        return self.from_pil_image(self._image.copy())

    def super_resolution(self, factor=4):
        return self._image.copy().resize((self.width * factor, self.height * factor))

    @lru_cache
    def draw_badge(self, colour, padding: float = 0.075, outline=None, width: float = 0.05, factor=0.4) -> Icon:
        image = self.super_resolution()
        sample_size = min(image.width, image.height)
        width_size = sample_size * width
        bounding_box = self._badge_bounding_box(image, padding, factor)

        draw = ImageDraw.Draw(image)
        draw.ellipse(bounding_box, fill=colour.rgb, outline=outline.rgb, width=round(width_size))

        return self.from_pil_image(image.resize(self.size, resample=Image.ANTIALIAS))

    def show(self):
        self._image.show()

    @classmethod
    def open(cls, fp, mode='r', formats=None) -> Icon:
        image = Image.open(fp, mode, formats)
        if image.mode != 'RGBA':
            new_image = Image.new('RGBA', image.size)
            new_image.paste(image)
            image = new_image

        return cls(image)

    @classmethod
    def new(cls, size, mode='RGBA') -> Icon:
        return cls(Image.new(mode, size))

    @classmethod
    def from_pil_image(cls, image: Image.Image) -> Icon:
        return cls(image)
