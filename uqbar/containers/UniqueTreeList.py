import copy

from uqbar.containers.UniqueTreeNode import UniqueTreeNode


class UniqueTreeList(UniqueTreeNode):
    """
    A list-like node in a "unique" tree.

    List nodes may contain zero or more other nodes.

    Unique tree nodes may have at most one parent and may appear only once in
    the tree.
    """

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        UniqueTreeNode.__init__(self, name=name)
        self._children = []
        self._named_children = {}
        if children is not None:
            self[:] = children

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        if isinstance(expr, str):
            return expr in self._named_children
        for x in self._children:
            if x is expr:
                return True
        return False

    def __delitem__(self, i):
        if isinstance(i, str):
            children = tuple(self._named_children[i])
            for child in children:
                parent = child.parent
                del parent[parent.index(child)]
            return
        if isinstance(i, int):
            if i < 0:
                i = len(self) + i
            i = slice(i, i + 1)
        self.__setitem__(i, [])
        self._mark_entire_tree_for_later_update()

    def __getitem__(self, expr):
        if isinstance(expr, (int, slice)):
            return self._children[expr]
        elif isinstance(expr, str):
            result = sorted(self._named_children[expr], key=lambda x: x.graph_order)
            if len(result) == 1:
                return result[0]
            return result
        raise ValueError(expr)

    def __iter__(self):
        for child in self._children:
            yield child

    def __len__(self):
        return len(self._children)

    def __setitem__(self, i, new_items):
        if isinstance(i, int):
            new_items = self._prepare_setitem_single(new_items)
            start_index, stop_index, _ = slice(i, i + 1).indices(len(self))
        else:
            new_items = self._prepare_setitem_multiple(new_items)
            start_index, stop_index, _ = i.indices(len(self))
        old_items = self[start_index:stop_index]
        self._validate_setitem_expr(new_items, old_items, start_index, stop_index)
        self._set_items(new_items, old_items, start_index, stop_index)
        self._mark_entire_tree_for_later_update()

    ### PRIVATE METHODS ###

    def _cache_named_children(self):
        name_dictionary = super()._cache_named_children()
        if hasattr(self, "_named_children"):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        return name_dictionary

    def _prepare_setitem_multiple(self, expr):
        return list(expr)

    def _prepare_setitem_single(self, expr):
        return [expr]

    def _set_items(self, new_items, old_items, start_index, stop_index):
        for old_item in old_items:
            old_item._set_parent(None)
        for new_item in new_items:
            new_item._set_parent(self)
        self._children.__setitem__(slice(start_index, start_index), new_items)

    def _validate_setitem_expr(self, new_items, old_items, start_index, stop_index):
        parentage = self.parentage
        for new_item in new_items:
            if not isinstance(new_item, self._node_class):
                raise ValueError(f"Expected {self._node_class}, got {type(new_item)}")
            elif new_item in parentage:
                raise ValueError("Cannot set parent node as child.")

    ### PRIVATE PROPERTIES ###

    @property
    def _node_class(self):
        return UniqueTreeNode

    ### PUBLIC METHODS ###

    def append(self, expr):
        self.__setitem__(slice(len(self), len(self)), [expr])

    def depth_first(self, top_down=True):
        """
        Iterate depth-first.

        ::

            >>> from uqbar.containers import UniqueTreeList, UniqueTreeNode
            >>> root_container = UniqueTreeList(name="root")
            >>> outer_container = UniqueTreeList(name="outer")
            >>> inner_container = UniqueTreeList(name="inner")
            >>> node_a = UniqueTreeNode(name="a")
            >>> node_b = UniqueTreeNode(name="b")
            >>> node_c = UniqueTreeNode(name="c")
            >>> node_d = UniqueTreeNode(name="d")
            >>> root_container.extend([node_a, outer_container])
            >>> outer_container.extend([inner_container, node_d])
            >>> inner_container.extend([node_b, node_c])

        ::

            >>> for node in root_container.depth_first():
            ...     print(node.name)
            ...
            a
            outer
            inner
            b
            c
            d

        ::

            >>> for node in root_container.depth_first(top_down=False):
            ...     print(node.name)
            ...
            a
            b
            c
            inner
            d
            outer

        """
        for child in tuple(self):
            if top_down:
                yield child
            if isinstance(child, UniqueTreeList):
                yield from child.depth_first(top_down=top_down)
            if not top_down:
                yield child

    def extend(self, expr):
        self.__setitem__(slice(len(self), len(self)), expr)

    def index(self, expr):
        for i, child in enumerate(self._children):
            if child is expr:
                return i
        else:
            message = "{!r} not in {!r}."
            message = message.format(expr, self)
            raise ValueError(message)

    def insert(self, i, expr):
        self.__setitem__(slice(i, i), [expr])

    def pop(self, i=-1):
        node = self[i]
        del self[i]
        return node

    def recurse(self):
        for child in self:
            yield child
            if isinstance(child, type(self)):
                for grandchild in child.recurse():
                    yield grandchild

    def remove(self, node):
        i = self.index(node)
        del self[i]

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)