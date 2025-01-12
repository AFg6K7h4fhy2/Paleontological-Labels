"""
Classes for creating labels for use in
paleontological collections. Labels have
headers, bodies, and footers. Labels can
have QR codes and watermarks.
"""

import pathlib
from typing import Iterable

import attrs
from PIL import Image, ImageColor, ImageDraw

SUPPORTED_COLORS = list(
    ImageColor.colormap.keys()
)
SUPPORTED_STYLES = [
    "bold",
    "regular",
    "italics",
    "underlined",
    "small_caps",
]
SUPPORTED_FONTS = ["Iosevka", "TeX Gyra Schola"]
SUPPORTED_POSITIONS = [
    "best",
    "upper-left",
    "upper-center",
    "upper-right",
    "middle-left",
    "middle-center",
    "middle-right",
    "lower-left",
    "lower-center",
    "lower-right",
]
SUPPORTED_ALIGNMENTS = ["center", "left", "right"]
SUPPORTED_BORDERS = ["dotted", "solid", "dashed"]
SUPPORTED_IMAGE_FORMATS = [
    ".jpg",
    ".png",
    ".heic",
]


def validate_save_directory(
    instance: any,
    attribute: attrs.Attribute,
    value: str | pathlib.Path,
):
    """
    NOTE: Does not check if file already
    exists by the same name.
    """
    # convert str path to path
    if isinstance(value, str):
        value = pathlib.Path(value)
    # check if path exists, if not, err
    if not value.exists():
        raise ValueError(
            f"{attribute.name} must be a valid path; got '{value}', which does not exist."
        )


@attrs.define(kw_only=True)
class Label:
    """
    Class for a Label. Each Label consists
    of a header, body, and footer section.
    Selected dimensions influence the section
    size. Sections can consist of images.
    All sections have "titles" and "content"
    text (e.g., in "Genus: Examplicus",
    Genus is the title and Examplicus is the
    content).
    """

    # OPTIONS FOR SAVING

    save_path: str | pathlib.Path = attrs.field(
        validator=[
            attrs.validators.instance_of(
                (str, pathlib.Path)
            ),
            validate_save_directory,
        ]
    )
    save_as_image: bool = attrs.field(
        default=True,
        validator=attrs.validators.instance_of(
            bool
        ),
    )
    image_format: str = attrs.field(
        default=".jpg",
        validator=[
            attrs.validators.in_(
                SUPPORTED_IMAGE_FORMATS
            ),
            attrs.validators.instance_of(str),
        ],
    )
    save_as_text: bool = attrs.field(
        default=False,
        validator=attrs.validators.instance_of(
            bool
        ),
    )
    save_as_svg: bool = attrs.field(
        default=False,
        validator=attrs.validators.instance_of(
            bool
        ),
    )
    save_as_tex: bool = attrs.field(
        default=False,
        validator=attrs.validators.instance_of(
            bool
        ),
    )

    # OPTIONS FOR BODY FONT

    body_font_path: str = attrs.field(
        default="TeX Gyra Schola",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(SUPPORTED_FONTS),
        ],
    )
    group_title_font_size: int = attrs.field(
        default=9,
        validator=[
            attrs.validators.instance_of(int),
            attrs.validators.ge(4),
            attrs.validators.le(20),
        ],
    )
    group_content_font_size: int = attrs.field(
        default=9,
        validator=[
            attrs.validators.instance_of(int),
            attrs.validators.ge(4),
            attrs.validators.le(20),
        ],
    )

    # OPTIONS FOR WATERMARKS

    watermark: str = attrs.field(
        default="",
        validator=attrs.validators.instance_of(
            str
        ),
    )
    watermark_font_path: str = attrs.field(
        default="TeX Gyra Schola",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(SUPPORTED_FONTS),
        ],
    )
    watermark_font_style: str = attrs.field(
        default="regular",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_STYLES
            ),
        ],
    )
    watermark_font_size: int = attrs.field(
        default=9,
        validator=[
            attrs.validators.instance_of(int),
            attrs.validators.ge(4),
            attrs.validators.le(20),
        ],
    )
    watermark_color: str = attrs.field(
        default="black",
        validator=attrs.validators.instance_of(
            str
        ),
    )
    watermark_opacity: float = attrs.field(
        default=0.5,
        validator=[
            attrs.validators.ge(0.0),
            attrs.validators.le(1.0),
        ],
    )
    watermark_image: str | None = attrs.field(
        default=None,
        validator=attrs.validators.optional(
            attrs.validators.instance_of(str)
        ),
    )
    watermark_position: str = attrs.field(
        default="best",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_POSITIONS
            ),
        ],
    )

    # OPTIONS FOR COLORING OF COMPONENTS

    background_color: str = attrs.field(
        default="white",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_COLORS
            ),
        ],
    )
    group_title_color: str = attrs.field(
        default="black",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_COLORS
            ),
        ],
    )
    group_content_color: str = attrs.field(
        default="black",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_COLORS
            ),
        ],
    )

    # OPTIONS FOR TEXT COMPONENT STYLING

    group_title_styling: str = attrs.field(
        default="regular",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_STYLES
            ),
        ],
    )
    group_content_styling: str = attrs.field(
        default="regular",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_STYLES
            ),
        ],
    )
    group_titles_to_hide: list[str] | None = (
        attrs.field(
            default=None,
            validator=attrs.validators.optional(
                attrs.validators.deep_iterable(
                    member_validator=attrs.validators.instance_of(
                        str
                    ),
                    iterable_validator=attrs.validators.instance_of(
                        list
                    ),
                )
            ),
        )
    )
    spaces_between_group_lines: int = attrs.field(
        default=0,
        validator=[
            attrs.validators.ge(0),
            attrs.validators.le(2),
        ],
    )

    # OPTIONS FOR TEXT ALIGNMENT

    text_alignment: str = attrs.field(
        default="center",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_ALIGNMENTS
            ),
        ],
    )
    text_flush: bool = attrs.field(
        default=False,
        validator=attrs.validators.instance_of(
            bool
        ),
    )

    # OPTIONS FOR IMAGE DIMENSIONS

    image_dots_per_inch: int = attrs.field(
        default=150,
        validator=[
            attrs.validators.ge(50),
            attrs.validators.le(500),
        ],
    )
    dimensions: tuple[float, float] = attrs.field(
        default=(4.0, 4.0),
        validator=[
            attrs.validators.deep_iterable(
                member_validator=attrs.validators.and_(
                    attrs.validators.ge(0.5),
                    attrs.validators.le(20.0),
                ),
                iterable_validator=attrs.validators.instance_of(
                    tuple
                ),
            ),
        ],
    )
    dimensions_in_inches: bool = attrs.field(
        default=True,
        validator=attrs.validators.instance_of(
            bool
        ),
    )
    dimensions_in_centimeters: bool = attrs.field(
        default=False,
        validator=attrs.validators.instance_of(
            bool
        ),
    )
    dimensions_as_inches: tuple[float, float] = (
        attrs.field(init=False)
    )
    dimensions_as_centimeters: tuple[
        float, float
    ] = attrs.field(init=False)
    dimensions_as_pixels: tuple[float, float] = (
        attrs.field(init=False)
    )
    dimensions_unit: str = attrs.field(init=False)

    # OPTIONS FOR BORDER

    border_style: str | None = attrs.field(
        default=None,
        validator=attrs.validators.optional(
            attrs.validators.and_(
                attrs.validators.instance_of(str),
                attrs.validators.in_(
                    SUPPORTED_BORDERS
                ),
            )
        ),
    )
    border_color: str = attrs.field(
        default="black",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_COLORS
            ),
        ],
    )
    border_size: float = attrs.field(
        default=0.05,
        validator=[
            attrs.validators.ge(0.01),
            attrs.validators.le(0.50),
        ],  # TODO: raise error depending on border size
    )
    border_padding_from_edge: float = attrs.field(
        default=0.05,
        validator=[
            attrs.validators.ge(0.01),
            attrs.validators.le(0.50),
        ],
    )

    # OPTIONS FOR QR CODES

    qr_code: bool = attrs.field(
        default=False,
        validator=attrs.validators.instance_of(
            bool
        ),
    )
    qr_code_size_in_inches: float = attrs.field(
        default=0.75,
        validator=[
            attrs.validators.ge(0.25),
            attrs.validators.le(2.0),
        ],  # TODO: raise error depending on border size
    )
    qr_code_position: str = attrs.field(
        default="best",
        validator=[
            attrs.validators.instance_of(str),
            attrs.validators.in_(
                SUPPORTED_POSITIONS
            ),
        ],
    )
    qr_code_on_back: bool = attrs.field(
        default=False,
        validator=attrs.validators.instance_of(
            bool
        ),
    )

    def _convert_values_to_pixels(
        self, values: Iterable[float], unit: str
    ) -> float:
        """
        Internal method to convert unit
        values to pixels.
        """
        if unit == "inches":
            return [
                value * self.image_dots_per_inch
                for value in values
            ]
        elif unit == "centimeters":
            return [
                value
                * (
                    self.image_dots_per_inch
                    / 2.54
                )
                for value in values
            ]
        else:
            raise ValueError(
                "Unit must be either 'inches' or 'centimeters'"
            )

    def _convert_values_to_inches(
        self, values: Iterable[float], unit: str
    ) -> list[float]:
        """
        Internal method to convert unit
        values to inches.
        """
        if unit == "pixels":
            return [
                value / self.image_dots_per_inch
                for value in values
            ]
        elif unit == "centimeters":
            return [
                value / 2.54 for value in values
            ]
        else:
            raise ValueError(
                "Unit must be either 'pixels' or 'centimeters'"
            )

    def _convert_values_to_centimeters(
        self, values: Iterable[float], unit: str
    ) -> list[float]:
        """
        Internal method to convert unit
        values to centimeters.
        """
        if unit == "pixels":
            return [
                value
                / self.image_dots_per_inch
                * 2.54
                for value in values
            ]
        elif unit == "inches":
            return [
                value * 2.54 for value in values
            ]
        else:
            raise ValueError(
                "Unit must be either 'pixels' or 'inches'"
            )

    def __attrs_post_init__(self):
        # ensure only one dimension unit is specified (either inches or centimeters)
        if (
            self.dimensions_in_centimeters
            and self.dimensions_in_inches
        ):
            raise ValueError(
                "You cannot specify both dimensions_in_inches and dimensions_in_centimeters. Please provide only one."
            )
        # handle case when dimensions are specified in centimeters
        if self.dimensions_in_centimeters:
            # set dimensions in centimeters
            self.dimensions_unit = "centimeters"
            self.dimensions_as_centimeters = (
                self.dimensions
            )
            # convert to inches and pixels using the helper methods
            self.dimensions_as_inches = (
                self._convert_values_to_inches(
                    values=self.dimensions,
                    unit=self.dimensions_unit,
                )
            )
            self.dimensions_as_pixels = self._convert_values_to_pixels(
                values=self.dimensions_as_inches,
                unit="inches",
            )
        # handle the case when dimensions are specified in inches
        elif self.dimensions_in_inches:
            # set dimensions in inches
            self.dimensions_unit = "inches"
            self.dimensions_as_inches = (
                self.dimensions
            )
            # convert to centimeters and pixels using the helper methods
            self.dimensions_as_centimeters = self._convert_values_to_centimeters(
                values=self.dimensions,
                unit=self.dimensions_unit,
            )
            self.dimensions_as_pixels = (
                self._convert_values_to_pixels(
                    values=self.dimensions,
                    unit=self.dimensions_unit,
                )
            )
        # raise an error if neither dimensions_in_centimeters nor dimensions_in_inches is specified
        elif not (
            self.dimensions_in_centimeters
            or self.dimensions_in_inches
        ):
            raise ValueError(
                "You must specify either dimensions_in_centimeters or dimensions_in_inches."
            )

    @classmethod
    def from_dict(cls, data: dict):
        """
        Instantiates a Label object from a
        dictionary.
        """
        return cls(**data)

    def _create_label_body(self):
        """
        Create the body of the Label using
        PIL and the provided dimensions in
        pixels, including background color.
        """
        # get label width and height in pixels
        label_width, label_height = (
            self.dimensions_as_pixels
        )
        # create the base image with background color
        img = Image.new(
            mode="RGB",
            size=(
                int(label_width),
                int(label_height),
            ),
            color=self.background_color,
        )
        drawn_img = ImageDraw.Draw(img)
        # add the border if specified
        if self.border_style:
            self._add_border(
                label_as_img=drawn_img,
                label_width=label_width,
                label_height=label_height,
            )
        # return generated image
        return img

    def _add_border(
        self,
        label_as_img,
        label_width: float,
        label_height: float,
    ) -> float:
        """
        Add a border to the label using
        the specified border style, color,
        and size.
        """
        # convert border size and padding
        # to pixels from whatever unit was
        # used
        border_size = (
            self._convert_values_to_pixels(
                [self.border_size],
                unit=self.dimensions_unit,
            )[0]
        )
        border_padding = (
            self._convert_values_to_pixels(
                [self.border_padding_from_edge],
                unit=self.dimensions_unit,
            )[0]
        )
        # border coordinates
        border_left = border_padding
        border_top = border_padding
        border_right = (
            label_width - border_padding
        )
        border_bottom = (
            label_height - border_padding
        )
        if self.border_style == "solid":
            # draw a solid border using
            # rectangle
            label_as_img.rectangle(
                [
                    (border_left, border_top),
                    (border_right, border_bottom),
                ],
                outline=self.border_color,
                width=int(border_size),
            )
        elif self.border_style == "dashed":
            # draw a dashed border
            dash_length = 10  # TODO: adjust length of each dash
            for x in range(
                border_left,
                border_right,
                dash_length * 2,
            ):
                label_as_img.line(
                    [
                        (x, border_top),
                        (
                            x + dash_length,
                            border_top,
                        ),
                    ],
                    fill=self.border_color,
                    width=int(border_size),
                )
                label_as_img.line(
                    [
                        (x, border_bottom),
                        (
                            x + dash_length,
                            border_bottom,
                        ),
                    ],
                    fill=self.border_color,
                    width=int(border_size),
                )
            for y in range(
                border_top,
                border_bottom,
                dash_length * 2,
            ):
                label_as_img.line(
                    [
                        (border_left, y),
                        (
                            border_left,
                            y + dash_length,
                        ),
                    ],
                    fill=self.border_color,
                    width=int(border_size),
                )
                label_as_img.line(
                    [
                        (border_right, y),
                        (
                            border_right,
                            y + dash_length,
                        ),
                    ],
                    fill=self.border_color,
                    width=int(border_size),
                )
        elif self.border_style == "dotted":
            # draw a dotted border using
            # small circles
            dot_radius = (
                2  # TODO adjust size of the dot
            )
            for x in range(
                border_left,
                border_right,
                2 * dot_radius,
            ):
                label_as_img.ellipse(
                    [
                        x,
                        border_top,
                        x + dot_radius,
                        border_top + dot_radius,
                    ],
                    fill=self.border_color,
                )
                label_as_img.ellipse(
                    [
                        x,
                        border_bottom
                        - dot_radius,
                        x + dot_radius,
                        border_bottom,
                    ],
                    fill=self.border_color,
                )
            for y in range(
                border_top,
                border_bottom,
                2 * dot_radius,
            ):
                label_as_img.ellipse(
                    [
                        border_left,
                        y,
                        border_left + dot_radius,
                        y + dot_radius,
                    ],
                    fill=self.border_color,
                )
                label_as_img.ellipse(
                    [
                        border_right - dot_radius,
                        y,
                        border_right,
                        y + dot_radius,
                    ],
                    fill=self.border_color,
                )
        else:
            raise ValueError(
                f"Unsupported border style: {self.border_style}"
            )

    def add_systematics_text():
        pass

    def add_collections_text():
        pass

    def _add_qr_code():
        pass

    def _add_watermark():
        pass

    def _save_as_plain_text(self):
        """Saves label as plain text."""
        pass

    def _save_as_tex(self):
        """Saves label as LaTeX."""
        pass

    def _save_as_svg(self):
        """Saves label as SVG."""
        pass

    def _save_as_image(self):
        """Saves label as an image."""
        pass

    def save(self):
        """
        Method to the save based on the specified
        formats. Each label is expected to start
        out as a Python string.
        """
        if self.save_as_text:
            self._save_as_plain_text()
        if self.save_as_tex:
            self._save_as_tex()
        if self.save_as_svg:
            self._save_as_svg()
        if self.save_as_image == "image":
            self._save_as_image()

        # if self.save_as_image:
        #     self.label.save(self.save_path, self.image_format)

        # if self.save_as_text:
        #     with open(self.save_path, "w") as f:
        #         f.write(self.text)


@attrs.define(kw_only=True)
class CollectionsLabel(Label):
    """
    A label for collections specimens, i.e.
    labels involving more details than
    fossil systematics. The kwargs parameter
    used is the group title.
    """

    collection: str | None = attrs.field(
        default=None
    )
    id_number: str | None = attrs.field(
        default=None
    )
    collector: str | None = attrs.field(
        default=None
    )
    species: str | None = attrs.field(
        default=None
    )
    species_author: str | None = attrs.field(
        default=None
    )
    common_name: str | None = attrs.field(
        default=None
    )
    location: str | None = attrs.field(
        default=None
    )
    coordinates: tuple[float, float] | None = (
        attrs.field(default=None)
    )
    coordinates_separate: bool = attrs.field(
        default=False
    )
    date_found: str | None = attrs.field(
        default=None
    )
    date_cataloged: str | None = attrs.field(
        default=None
    )
    formation: str | None = attrs.field(
        default=None
    )
    formation_author: str | None = attrs.field(
        default=None
    )
    chrono_age: str | None = attrs.field(
        default=None
    )
    chrono_age_author: str | None = attrs.field(
        default=None
    )
    size: str | None = attrs.field(default=None)
    link: str | None = attrs.field(default=None)

    default_titles = {
        "collection": "Collection: ",
        "id_number": "ID Number: ",
        "collector": "Collector: ",
        "species": "Scientific Name: ",
        "species_author": "Species Author: ",
        "common_name": "Common Name: ",
        "location": "Location: ",
        "coordinates": "Coordinates: ",
        "date_found": "Date Found: ",
        "date_cataloged": "Date Cataloged: ",
        "formation": "Formation: ",
        "formation_author": "Formation Author: ",
        "chrono_age": "Age: ",
        "chrono_age_author": "Age Author: ",
        "size": "Size: ",
        "link": "Link: ",
    }

    title_overrides: dict[str, str] = attrs.field(
        factory=dict
    )  # empty by default

    _ordered_kwargs: dict = attrs.field(
        init=False
    )

    def __init__(self, **kwargs):
        self._ordered_kwargs = {
            key: kwargs[key] for key in kwargs
        }

    def __attrs_post_init__(self):
        # update title_overrides with any user-provided overrides
        if self.title_overrides:
            # merge user-provided titles, overriding defaults
            for (
                key,
                value,
            ) in self.title_overrides.items():
                if key in self.default_titles:
                    self.default_titles[key] = (
                        value
                    )

    def _get_collections_attrs(self):
        label_attrs = {
            attr.name
            for attr in Label.__attrs_attrs__
        }
        # collections_attrs = {
        #     attr.name: getattr(self, attr.name)
        #     for attr in self.__attrs_attrs__
        #     if attr.name not in label_attrs
        # }
        # print(self.__attrs_attrs__)
        collections_attrs = {
            key: value
            for key, value in self._ordered_kwargs.items()
            if key not in label_attrs
        }
        return collections_attrs

    def label(self):
        # empty list for parts of the final label
        parts = []
        # collections label exclusive attrs
        collections_attrs = (
            self._get_collections_attrs()
        )
        # iterative over collections attrs
        for (
            key,
            value,
        ) in collections_attrs.items():
            # for all non-None collections attrs, proceed
            if (
                value is not None
                and not isinstance(value, dict)
            ):
                # edit title with spaces and capitalized
                title = self.default_titles.get(
                    key,
                    f"{key.replace('_', ' ').capitalize()}: ",
                )
                # add the group
                parts.append(f"{title}{value}")
        # consolidate to multiline label
        return "\n".join(parts)
