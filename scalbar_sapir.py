import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sympy import Line2D


class AnchoredHScaleBar(matplotlib.offsetbox.AnchoredOffsetbox):
    """Examples:
    x axis ms scale: ax.add_artist(AnchoredHScaleBar(size_x=2, extent=1, frameon=True, linekw=dict(color="crimson"),))
    y axis mV scale: ax.add_artist(AnchoredHScaleBar(size_y=1.5, extent=1, frameon=True, linekw=dict(color="crimson"),))
    x-y axes scales: ax.add_artist(AnchoredHScaleBar(size_x=2, size_y=1.5, frameon=True, linekw=dict(color="crimson"),))
     """
    def __init__(self, size_x=None, size_y=None, extent=0.03, loc=4, ax=None, x_to_ms=lambda x: x, y_to_mv=lambda y: y,
                 pad=0.2, borderpad=0, ppad=0, sep=1, prop=None, x_units="ms", y_units="mV",
                 frameon=False, linekw={}, txtkw={}, **kwargs):
        if size_x is None and size_y is None:
            raise Exception("One size must be valid (at least): x/y")
        if not ax:
            ax = plt.gca()

        is_2d = False
        size = size_x if size_x is not None else size_y
        f = x_to_ms if size_x is not None else y_to_mv
        sub_x_left, sub_y_left = [0, 0], [-extent / 2., extent / 2.]
        sub_x_right, sub_y_right = [f(size), f(size)], [-extent / 2., extent / 2.]
        if size_y is None:
            packer = matplotlib.offsetbox.VPacker
            txt = matplotlib.offsetbox.TextArea("{0} {1}".format(size, x_units), textprops=txtkw)
        elif size_x is None:
            sub_y_left, sub_x_left = sub_x_left, sub_y_left
            sub_y_right, sub_x_right = sub_x_right, sub_y_right
            packer = matplotlib.offsetbox.HPacker
            txt = matplotlib.offsetbox.TextArea("{0} {1}".format(size, y_units), textprops=txtkw)
        else:
            is_2d = True

        size_bar = matplotlib.offsetbox.AuxTransformBox(ax.transData)
        if size_x:
            size_bar.add_artist(Rectangle((0, 0), x_to_ms(size_x), 0, **linekw))
        if size_y:
            size_bar.add_artist(Rectangle((0, 0), 0, y_to_mv(size_y), **linekw))

        if not is_2d:  # x or y lines (with small shift)
            size_bar.add_artist(Line2D(sub_x_left, sub_y_left, **linekw))
            size_bar.add_artist(Line2D(sub_x_right, sub_y_right, **linekw))
            children = [size_bar, txt]
        else:  # todo flip direction as well?
            print(dir(matplotlib.offsetbox.TextArea))
            txt_x = matplotlib.offsetbox.TextArea("{0} {1}".format(size_x, x_units), textprops=txtkw)
            txt_y = matplotlib.offsetbox.TextArea("{0} {1}".format(size_y, y_units),textprops=txtkw)
            children = [txt_y, matplotlib.offsetbox.VPacker(children=[size_bar, txt_x], align="center", pad=ppad, sep=sep)]
            packer = matplotlib.offsetbox.HPacker
        self.vpac = packer(children=children, align="center", pad=ppad, sep=sep)
        matplotlib.offsetbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, borderpad=borderpad, child=self.vpac,
                                                        prop=prop, frameon=frameon, **kwargs)
