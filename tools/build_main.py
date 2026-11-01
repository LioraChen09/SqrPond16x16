import math

from kbitfont import KbitFont
from loguru import logger
from pixel_font_builder import FontBuilder, WeightName, SerifStyle, SlantStyle, WidthStyle

from tools.config import path_define, options
from tools.utils.font_util import create_glyph_from_kbit


def main() -> None:
    kbit_font = KbitFont.load_kbitx(path_define.SOURCES_DIR.joinpath('main.kbitx'))

    builder = FontBuilder()
    builder.font_metric.font_size = kbit_font.props.em_height
    builder.font_metric.horizontal_layout.ascent = kbit_font.props.line_ascent
    builder.font_metric.horizontal_layout.descent = -kbit_font.props.line_descent
    builder.font_metric.horizontal_layout.line_gap = kbit_font.props.line_gap
    builder.font_metric.vertical_layout.ascent = math.ceil(kbit_font.props.line_height / 2)
    builder.font_metric.vertical_layout.descent = -math.floor(kbit_font.props.line_height / 2)
    builder.font_metric.vertical_layout.line_gap = kbit_font.props.line_gap
    builder.font_metric.x_height = kbit_font.props.x_height
    builder.font_metric.cap_height = kbit_font.props.cap_height

    builder.meta_info.version = kbit_font.names.version
    builder.meta_info.family_name = kbit_font.names.family
    builder.meta_info.weight_name = WeightName.REGULAR
    builder.meta_info.serif_style = SerifStyle.SANS_SERIF
    builder.meta_info.slant_style = SlantStyle.NORMAL
    builder.meta_info.width_style = WidthStyle.MONOSPACED
    builder.meta_info.manufacturer = kbit_font.names.manufacturer
    builder.meta_info.designer = kbit_font.names.designer
    builder.meta_info.description = kbit_font.names.description
    builder.meta_info.copyright_info = kbit_font.names.copyright
    builder.meta_info.license_info = kbit_font.names.license_description
    builder.meta_info.vendor_url = kbit_font.names.vendor_url
    builder.meta_info.designer_url = kbit_font.names.designer_url
    builder.meta_info.license_url = kbit_font.names.license_url

    for code_point, kbit_glyph in sorted(kbit_font.characters.items()):
        glyph_name = f'u{code_point:04X}'
        builder.character_mapping[code_point] = glyph_name
        builder.glyphs.append(create_glyph_from_kbit(glyph_name, kbit_glyph, kbit_font.props))

    for glyph_name, kbit_glyph in kbit_font.named_glyphs.items():
        builder.glyphs.append(create_glyph_from_kbit(glyph_name, kbit_glyph, kbit_font.props))

    path_define.BUILD_DIR.mkdir(parents=True, exist_ok=True)
    for font_format in options.FONT_FORMATS:
        font_file_path = path_define.BUILD_DIR.joinpath(f'main.{font_format}')
        getattr(builder, f'save_{font_format.replace('.', '_')}')(font_file_path)
        logger.info('Make font: {!r}', str(font_file_path))


if __name__ == '__main__':
    main()
