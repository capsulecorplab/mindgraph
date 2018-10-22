# -*- coding: utf-8 -*-
from typing import Iterator, List
from yaml import dump, load


class Node(object):
    """node class"""

    def __init__(self, name: str = '', weight: int = 1) -> None:
        self._dependencies = list()  # type: List[Node]
        self._threads = list()  # type: List[Node]
        self._name = ''  # type: str
        self._weight = weight  # type: int
        if type(name) is str:
            self._name = name
        else:
            raise TypeError

    def append(self, newnode) -> "Node":
        """ Creates a new Node and appends it to threads """
        if type(newnode) is str:
            newnode = Node(newnode)
        elif type(newnode) is not Node:
            raise TypeError
        self._threads.append(newnode)
        return newnode

    def pop(self, index: int) -> "Node":
        """ Pops the Node from threads[index] """
        return self._threads.pop(index)

    def blockedby(self, node: "Node") -> None:
        """ Adds a Node to the dependenceis list """
        if type(node) is Node:
            self._dependencies.append(node)
            return None
        else:
            raise TypeError

    def blocking(self, node: "Node") -> None:
        """ Adds this Node to another node's dependencies list """
        if type(node) is Node:
            node._dependencies.append(self)
            return None
        else:
            raise TypeError

    def __getitem__(self, key: int) -> "Node":
        return self._threads[key]

    def __repr__(self) -> str:
        return '\n'.join(self.format_tree())

    def format_tree(self: "Node", depth: int = 0) -> Iterator[str]:
        """Format node and dependents in tree format, emitting lines

        Assumes no cycles in graph
        """
        indent = '    ' * depth
        bullet = '- ' if depth != 0 else ''
        suffix = ':' if self.threads else ''
        line = '{indent}{bullet}{self.name}{suffix}'.format(**locals())

        yield line
        for n in self.threads:
            yield from n.format_tree(depth+1)


    def _postorder(self,
                   depth: int = 0,
                   visited: Set["Node"] = None,
                   node_key: Callable[["Node"], Any]=None,
                   ) -> Generator[Tuple[int, "Node"], None, Set["Node"]]:
        """Post-order traversal of graph rooted at node"""
        if visited is None:
            visited = set()

        children = self._threads
        if node_key is not None:
            children = sorted(self._threads, key=node_key)

        for child in children:
            if child not in visited:
                visited = yield from child._postorder(depth+1,
                                                      visited,
                                                      node_key)

        yield (depth, self)
        visited.add(self)

        return visited

    def todo(self) -> Iterator["Node"]:
        """Generate nodes in todo order

        Nodes are scheduled by weight and to resolve blocking tasks
        """
        # sorts by weight (2 before 1), then alphabetical
        def node_key(node):
            return (-node.weight, node.name)
        return (x[1] for x in self._postorder(node_key=node_key))

    def __str__(self) -> str:
        return dump(load(str(self.__repr__())), default_flow_style=False)

    @property
    def dependencies(self) -> List["Node"]:
        """ dependencies getter """
        return self._dependencies

    @property
    def name(self) -> str:
        """ name getter """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """ name setter """
        self._name = name

    @property
    def threads(self) -> List["Node"]:
        """ threads getter """
        return self._threads

    @property
    def weight(self) -> int:
        """ weight getter """
        return self._weight

    @weight.setter
    def weight(self, value: int) -> None:
        """ weight setter """
        self._weight = value


class Graph(Node):
    """A Graph model of the mind"""

    def __init__(self, name=None) -> None:
        Node.__init__(self, name)

    def to_yaml(self, filename=None) -> None:
        """ Write this Graph to a yaml file """
        with open(filename, 'w') as f:
            f.write(dump(self))


def read_yaml(filename: str = "") -> Graph:
    """ Load a Graph from a yaml file """
    with open(filename, 'r') as f:
        rv = load(f.read())
        if type(rv) is Graph:
            return rv
        else:
            raise TypeError(type(rv))
