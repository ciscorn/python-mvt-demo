import numpy as np
from HersheyFonts import HersheyFonts

_thefont = HersheyFonts()
_thefont.load_default_font("rowmans")
_thefont.normalize_rendering(0.04)
_thefont.render_options.scaley *= -1
_thefont.render_options.yofs = _thefont.render_options.scaley // 2


def get_strokes(text: str):
    for stroke in _thefont.strokes_for_text(text):
        st = np.asarray(stroke)
        yield st + np.random.normal(0, 0.001, st.shape)
