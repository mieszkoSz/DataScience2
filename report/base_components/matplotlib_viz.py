from .base_component import BaseComponent

import base64
import io
import matplotlib
import matplotlib.pyplot as plt
from fasthtml.common import Img

# This is necessary to prevent matplotlib from causing memory leaks
# https://stackoverflow.com/questions/31156578/matplotlib-doesnt-release-memory-after-savefig-and-close
matplotlib.use('Agg')

matplotlib.rcParams['savefig.transparent'] = True
matplotlib.rcParams['savefig.format'] = 'png'


def matplotlib2fasthtml(func):
    '''
    Copy of https://github.com/koaning/fh-matplotlib, which is currently hardcoding the 
    image format as jpg. png or svg is needed here.
    '''
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs)
        if fig is None:
            fig = plt.gcf()

        image = io.BytesIO()
        fig.savefig(image, format='png', bbox_inches='tight')
        encoded_image = base64.b64encode(image.getvalue()).decode('ascii')
        plt.close(fig)
        return Img(src=f'data:image/png;base64,{encoded_image}')
    return wrapper


class MatplotlibViz(BaseComponent):

    @matplotlib2fasthtml
    def build_component(self, entity_id, model):
        return self.visualization(entity_id, model)
    
    
    def visualization(self, entity_id, model):
        raise NotImplementedError

    def set_axis_styling(self, ax, bordercolor='white', fontcolor='white'):
        
        ax.title.set_color(fontcolor)
        ax.xaxis.label.set_color(fontcolor)
        ax.yaxis.label.set_color(fontcolor)

        ax.tick_params(color=bordercolor, labelcolor=fontcolor)
        for spine in ax.spines.values():
            spine.set_edgecolor(bordercolor)

        for line in ax.get_lines():
            line.set_linewidth(4)
            line.set_linestyle('dashdot')
