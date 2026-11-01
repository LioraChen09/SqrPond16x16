from kbitfont import KbitGlyph, KbitProps
from pixel_font_builder import Glyph
from pixel_font_knife.bitmap.mono_bitmap import MonoBitmap


def create_glyph_from_kbit(name: str, kbit_glyph: KbitGlyph, kbit_props: KbitProps) -> Glyph:
    return Glyph(
        name=name,
        horizontal_offset=(kbit_glyph.x, kbit_glyph.y - kbit_glyph.height),
        advance_width=kbit_glyph.advance,
        vertical_offset=(kbit_glyph.width // 2, kbit_props.em_ascent - kbit_glyph.y),
        advance_height=kbit_props.em_height,
        bitmap=[[0 if color <= 127 else 1 for color in bitmap_row] for bitmap_row in kbit_glyph.bitmap],
    )


def create_bold_glyph_from_kbit(name: str, kbit_glyph: KbitGlyph, kbit_props: KbitProps) -> Glyph:
    bitmap = MonoBitmap([[0 if color <= 127 else 1 for color in bitmap_row] for bitmap_row in kbit_glyph.bitmap])
    solid_bitmap = bitmap.resize(left=1).union(bitmap)
    shadow_bitmap = solid_bitmap.difference(bitmap).resize(left=1)
    result_bitmap = solid_bitmap.difference(shadow_bitmap)

    return Glyph(
        name=name,
        horizontal_offset=(kbit_glyph.x, kbit_glyph.y - kbit_glyph.height),
        advance_width=kbit_glyph.advance + 1,
        vertical_offset=(kbit_glyph.width // 2, kbit_props.em_ascent - kbit_glyph.y),
        advance_height=kbit_props.em_height,
        bitmap=result_bitmap.data,
    )
