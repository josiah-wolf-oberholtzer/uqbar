import collections
from uqbar.graphs.Color import Color
from uqbar.graphs.Point import Point


class Attributes(collections.Mapping):
    """
    Abstract base for Graphviz attributes classes.
    """

    ### CLASS VARIABLES ###

    _arrow_types = frozenset(['box', 'circle', 'crow', 'diamond', 'dot',
        'ediamond', 'empty', 'halfopen', 'inv', 'invdot', 'invempty',
        'invodot', 'none', 'normal', 'obox', 'odiamond', 'odot', 'open', 'tee',
        'vee'])

    _cluster_modes = frozenset(['global', 'local', 'none'])

    _dir_types = frozenset(['back', 'both', 'forward', 'none'])

    _output_modes = frozenset(['breadthfirst', 'nodesfirst', 'edgesfirst'])

    _pack_modes = frozenset(['node', 'clust', 'graph'])

    _page_dirs = frozenset(['BL', 'BR', 'LB', 'LT', 'RB', 'RT', 'TL', 'TR'])

    _quad_types = frozenset(['fast', 'none', 'normal'])

    _rank_types = frozenset(['max', 'min', 'same', 'sink', 'source'])

    _rank_dirs = frozenset(['BT', 'LR', 'RL', 'TB'])

    _shapes = frozenset(['Mcircle', 'Mdiamond', 'Msquare', 'assembly', 'box',
        'box3d', 'cds', 'circle', 'component', 'cylinder', 'diamond',
        'doublecircle', 'doubleoctagon', 'egg', 'ellipse', 'fivepoverhang',
        'folder', 'hexagon', 'house', 'insulator', 'invhouse', 'invtrapezium',
        'invtriangle', 'larrow', 'lpromoter', 'none', 'note', 'noverhang',
        'octagon', 'oval', 'parallelogram', 'pentagon', 'plain', 'plaintext',
        'point', 'polygon', 'primersite', 'promoter', 'proteasesite',
        'proteinstab', 'rarrow', 'rect', 'rectangle', 'restrictionsite',
        'ribosite', 'rnastab', 'rpromoter', 'septagon', 'signature', 'square',
        'star', 'tab', 'terminator', 'threepoverhang', 'trapezium', 'triangle',
        'tripleoctagon', 'underline', 'utr'])

    _smooth_types = frozenset(['avg_dist', 'graph_dist', 'none', 'power_dist',
        'rng', 'spring', 'triangle'])

    _styles = frozenset()

    ### GRAPH OBJECT SPECIFICS ###

    _cluster_attributes = frozenset(['K', 'URL', 'area', 'bgcolor', 'color',
        'colorscheme', 'fillcolor', 'fontcolor', 'fontname', 'fontsize',
        'gradientangle', 'href', 'id', 'label', 'labeljust', 'labelloc',
        'layer', 'lheight', 'lp', 'lwidth', 'margin', 'nojustify', 'pencolor',
        'penwidth', 'peripheries', 'sortv', 'style', 'target', 'tooltip'])

    _cluster_overrides = {}

    _cluster_styles = frozenset(['bold', 'dashed', 'dotted', 'filled',
        'rounded', 'solid', 'striped'])

    _edge_attributes = frozenset(['arrowhead', 'arrowsize', 'arrowtail',
        'color', 'colorscheme', 'comment', 'constraint', 'decorate', 'dir',
        'edgeURL', 'edgehref', 'edgetarget', 'edgetooltip', 'fillcolor',
        'fontcolor', 'fontname', 'fontsize', 'headURL', 'head_lp', 'headclip',
        'headhref', 'headlabel', 'headport', 'headtarget', 'headtooltip',
        'href', 'id', 'label', 'labelURL', 'labelangle', 'labeldistance',
        'labelfloat', 'labelfontcolor', 'labelfontname', 'labelfontsize',
        'labelhref', 'labeltarget', 'labeltooltip', 'layer', 'len', 'lhead',
        'lp', 'ltail', 'minlen', 'nojustify', 'penwidth', 'pos', 'samehead',
        'sametail', 'showboxes', 'style', 'tailURL', 'tail_lp', 'tailclip',
        'tailhref', 'taillabel', 'tailport', 'tailtarget', 'tailtooltip',
        'target', 'tooltip', 'weight'])

    _edge_styles = frozenset(['bold', 'dashed', 'dotted', 'solid'])

    _graph_attributes = frozenset(['Damping', 'K', 'URL', 'bb', 'bgcolor',
        'center', 'charset', 'clusterrank', 'colorscheme', 'comment',
        'compound', 'concentrate', 'defaultdist', 'dim', 'dimen',
        'diredgeconstraints', 'dpi', 'epsilon', 'esep', 'fontcolor',
        'fontname', 'fontnames', 'fontpath', 'fontsize', 'forcedlabels',
        'gradientangle', 'href', 'id', 'imagepath', 'inputscale', 'label',
        'label_scheme', 'labeljust', 'labelloc', 'landscape', 'layerlistsep',
        'layers', 'layerselect', 'layersep', 'layout', 'levels', 'levelsgap',
        'lheight', 'lp', 'lwidth', 'margin', 'maxiter', 'mclimit', 'mode',
        'model', 'mosek', 'newrank', 'nodesep', 'nojustify', 'normalize',
        'notranslate', 'nslimit', 'nslimit1', 'ordering', 'orientation',
        'outputorder', 'overlap', 'overlap_scaling', 'overlap_shrink', 'pack',
        'packmode', 'pad', 'page', 'pagedir', 'quadtree', 'quantum', 'rank',
        'rankdir', 'ranksep', 'remincross', 'repulsiveforce', 'resolution',
        'root', 'rotate', 'rotation', 'scale', 'searchsize', 'sep',
        'showboxes', 'size', 'smoothing', 'sortv', 'splines', 'start', 'style',
        'stylesheet', 'target', 'truecolor', 'viewport', 'voro_margin',
        'xdotversion', 'xlabel', 'xlp'])

    _graph_styles = frozenset()

    _node_attributes = frozenset(['URL', 'area', 'color', 'colorscheme',
        'comment', 'distortion', 'fillcolor', 'fixedsize', 'fontcolor',
        'fontname', 'fontsize', 'gradientangle', 'group', 'height', 'href',
        'id', 'image', 'imagepos', 'imagescale', 'label', 'labelloc', 'layer',
        'margin', 'nojustify', 'ordering', 'orientation', 'penwidth',
        'peripheries', 'pin', 'pos', 'rects', 'regular', 'root',
        'samplepoints', 'shape', 'shapefile', 'showboxes', 'sides', 'skew',
        'sortv', 'style', 'target', 'tooltip', 'vertixes', 'width', 'z'])

    _node_styles = frozenset(['solid', 'dashed', 'dotted', 'bold', 'rounded',
        'diagonals', 'filled', 'striped', 'wedged'])

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        self._attributes = kwargs.copy()

    ### SPECIAL METHODS ###

    def __getitem__(self, key):
        return self._attributes[key]

    def __iter__(self):
        return iter(self._attributes)

    def __len__(self):
        return len(self._attributes)

    ### VALIDATORS ###

    @classmethod
    def _validate_arrow_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._arrow_types
        return value

    @classmethod
    def _validate_cluster_mode(cls, value, **kwargs):
        value = str(value)
        assert value in cls._cluster_modes
        return value

    @classmethod
    def _validate_color(cls, value, **kwargs):
        if isinstance(value, Color):
            return value
        value = Color(value)
        return value

    @classmethod
    def _validate_colors(cls, value, **kwargs):
        if isinstance(value, (Color, str)):
            return cls._validate_color(value, **kwargs)
        assert len(value)
        value = tuple(cls._validate_color(_, **kwargs) for _ in value)
        if len(value) == 1:
            return value[0]
        return value

    @classmethod
    def _validate_dir_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._dir_types
        return value

    @classmethod
    def _validate_floats(cls, value, **kwargs):
        assert len(value)
        return tuple(float(_) for _ in value)

    @classmethod
    def _validate_output_mode(cls, value, **kwargs):
        value = str(value)
        assert value in cls._output_modes
        return value

    @classmethod
    def _validate_pack_mode(cls, value, **kwargs):
        value = str(value)
        assert value in cls._pack_modes
        return value

    @classmethod
    def _validate_page_dir(cls, value, **kwargs):
        value = str(value)
        assert value in cls._page_dirs
        return value

    @classmethod
    def _validate_point(cls, value, **kwargs):
        if isinstance(value, Point):
            return value
        value = Point(*value)
        return value

    @classmethod
    def _validate_points(cls, value_list, **kwargs):
        assert value_list
        return tuple(cls._validate_point(_, **kwargs) for _ in value_list)

    @classmethod
    def _validate_quad_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._quad_types
        return value

    @classmethod
    def _validate_rank_dir(cls, value, **kwargs):
        value = str(value)
        assert value in cls._rank_dirs
        return value

    @classmethod
    def _validate_rank_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._rank_types
        return value

    @classmethod
    def _validate_rect(cls, value, **kwargs):
        assert len(value) == 4
        value = tuple(float(_) for _ in value)
        return value

    @classmethod
    def _validate_shape(cls, value, **kwargs):
        value = str(value)
        assert value in cls._shapes
        return value

    @classmethod
    def _validate_smooth_type(cls, value, **kwargs):
        value = str(value)
        assert value in cls._smooth_types
        return value

    @classmethod
    def _validate_style(cls, value, valid_styles=None, **kwargs):
        value = str(value)
        assert value in valid_styles
        return value

    @classmethod
    def _validate_styles(cls, value, valid_styles=None, **kwargs):
        if isinstance(value, str):
            return cls._validate_style(
                value,
                valid_styles=valid_styles,
                **kwargs
                )
        assert value
        return tuple(cls._validate_style(
            _, valid_styles=valid_styles, **kwargs
            ) for _ in value)

    ### PRIVATE METHODS ###

    @classmethod
    def _validate_attributes(cls, mode, **kwargs):
        valid_attributes, valid_styles = dict(
            cluster=(cls._cluster_attributes, cls._cluster_styles),
            edge=(cls._edge_attributes, cls._edge_styles),
            graph=(cls._graph_attributes, cls._graph_styles),
            node=(cls._node_attributes, cls._node_styles),
            )[mode]
        attributes = {}
        for key, value in kwargs.items():
            if key not in valid_attributes:
                continue
            validators = cls._validators[key]
            if not isinstance(validators, tuple):
                validators = (validators,)
            for validator in validators:
                if isinstance(validator, str) and str(value) == validator:
                    value = str(value)
                    break
                elif isinstance(validator, type):
                    value = validator(value)
                else:
                    value = validator(value, valid_styles=valid_styles)
            attributes[key] = value
        return attributes

    ### PUBLIC METHODS ###

    @classmethod
    def from_cluster_attributes(cls, **kwargs):
        attributes = cls._validate_attributes('cluster', **kwargs)
        return cls(attributes)

    @classmethod
    def from_edge_attributes(cls, **kwargs):
        attributes = cls._validate_attributes('edge', **kwargs)
        return cls(attributes)

    @classmethod
    def from_graph_attributes(cls, **kwargs):
        attributes = cls._validate_attributes('graph', **kwargs)
        return cls(attributes)

    @classmethod
    def from_node_attributes(cls, **kwargs):
        attributes = cls._validate_attributes('node', **kwargs)
        return cls(attributes)


Attributes._validators = {
    'Damping': float,
    'K': float,
    'URL': str,
    '_background': str,
    'area': float,
    'arrowhead': Attributes._validate_arrow_type,
    'arrowsize': float,
    'arrowtail': Attributes._validate_arrow_type,
    'bb': Attributes._validate_rect,
    'bgcolor': Attributes._validate_colors,
    'center': bool,
    'charset': str,
    'clusterrank': Attributes._validate_cluster_mode,
    'color': Attributes._validate_colors,
    'colorscheme': str,
    'comment': str,
    'compound': bool,
    'concentrate': bool,
    'constraint': bool,
    'decorate': bool,
    'defaultdist': float,
    'dim': int,
    'dimen': int,
    'dir': Attributes._validate_dir_type,
    'diredgeconstraints': ('hier', bool),
    'distortion': float,
    'dpi': float,
    'edgeURL': str,
    'edgehref': str,
    'edgetarget': str,
    'edgetooltip': str,
    'epsilon': float,
    'esep': (float, Attributes._validate_point),
    'fillcolor': Attributes._validate_colors,
    'fixedsize': ('shape', bool),
    'fontcolor': Attributes._validate_color,
    'fontname': str,
    'fontnames': str,
    'fontpath': str,
    'fontsize': float,
    'forcelabels': bool,
    'gradientangle': int,
    'group': str,
    'headURL': str,
    'head_lp': Attributes._validate_point,
    'headclip': bool,
    'headhref': str,
    'headlabel': str,
    'headport': str,
    'headtarget': str,
    'headtooltip': str,
    'height': float,
    'href': str,
    'id': str,
    'image': str,
    'imagepath': str,
    'imagepos': str,
    'imagescale': ('width', 'height', 'both', bool),
    'inputscale': float,
    'label': str,
    'labelURL': str,
    'label_scheme': int,
    'labelangle': float,
    'labeldistance': float,
    'labelfloat': bool,
    'labelfontcolor': Attributes._validate_color,
    'labelfontname': str,
    'labelfontsize': float,
    'labelhref': str,
    'labeljust': str,
    'labelloc': str,
    'labeltarget': str,
    'labeltooltip': str,
    'landscape': bool,
    'layer': str,
    'layerlistsep': str,
    'layers': str,
    'layerselect': str,
    'layersep': str,
    'layout': str,
    'len': float,
    'levels': int,
    'levelsgap': float,
    'lhead': str,
    'lheight': float,
    'lp': Attributes._validate_point,
    'ltail': str,
    'lwidth': float,
    'margin': (float, Attributes._validate_point),
    'maxiter': int,
    'mclimit': float,
    'mindist': float,
    'minlen': int,
    'mode': str,
    'model': str,
    'mosek': bool,
    'newrank': bool,
    'nodesep': float,
    'nojustify': bool,
    'normalize': (float, bool),
    'notranslate': bool,
    'nslimit': float,
    'nslimit1': float,
    'ordering': str,
    'outputorder': Attributes._validate_output_mode,
    'overlap': ('scale', 'scalexy', 'compress', 'ipsep', 'prism', bool),
    'overlap_scaling': float,
    'overlap_shrink': bool,
    'pack': bool,
    'packmode': Attributes._validate_pack_mode,
    'pad': (float, Attributes._validate_point),
    'page': (float, Attributes._validate_point),
    'pagedir': Attributes._validate_page_dir,
    'pencolor': Attributes._validate_color,
    'penwidth': float,
    'peripheries': int,
    'pin': bool,
    'pos': Attributes._validate_point,
    'quadtree': (Attributes._validate_quad_type, bool),
    'quantum': float,
    'rank': Attributes._validate_rank_type,
    'rankdir': Attributes._validate_rank_dir,
    'ranksep': (float, Attributes._validate_floats),
    'ratio': ('fill', 'compress', 'expand', 'auto', float),
    'rects': Attributes._validate_rect,
    'regular': bool,
    'remincross': bool,
    'repulsiveforce': float,
    'resolution': float,
    'root': str,
    'rotate': int,
    'rotation': float,
    'samehead': str,
    'sametail': str,
    'samplepoints': int,
    'scale': (float, Attributes._validate_point),
    'searchsize': int,
    'sep': (float, Attributes._validate_point),
    'shape': Attributes._validate_shape,
    'shapefile': str,
    'showboxes': int,
    'sides': int,
    'size': (float, Attributes._validate_point),
    'skew': float,
    'smoothing': Attributes._validate_smooth_type,
    'sortv': int,
    'splines': ('none', 'line', 'polyline', 'curved', 'ortho', 'spline', bool),
    'start': str,
    'style': Attributes._validate_styles,
    'stylesheet': str,
    'tailURL': str,
    'tail_lp': Attributes._validate_point,
    'tailclip': bool,
    'tailhref': str,
    'taillabel': str,
    'tailport': str,
    'tailtarget': str,
    'tailtooltip': str,
    'target': str,
    'tooltip': str,
    'truecolor': bool,
    'vertices': Attributes._validate_points,
    'viewport': str,
    'voro_margin': float,
    'weight': int,
    'width': float,
    'xdotversion': str,
    'xlabel': str,
    'xlp': Attributes._validate_point,
    'z': float,
    }
