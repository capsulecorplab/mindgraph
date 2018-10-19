# -*- coding: utf-8 -*-
import functools

from typing import List
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
        return self.custom_repr(self, 0)

    @staticmethod
    def custom_repr(node: "Node", depth: int = 0) -> str:

        if len(node.threads) > 0:

            if depth == 0:
                return node.name + ":\n" + '\n'.join(
                    map(functools.partial(node.custom_repr, depth=depth + 1),
                        node.threads))
            elif depth == 1:
                return '- ' + node.name + ":\n" + '\n'.join(
                    map(functools.partial(node.custom_repr, depth=depth + 1),
                        node.threads))
            else:
                return "    " * (depth - 1) + "- {}".format(node.name) + \
                       ":\n" + '\n'.join(map(
                                         functools.partial(node.custom_repr,
                                                           depth=depth + 1),
                                         node.threads))

        return "    " * (depth - 1) + "- {}".format(node.name)

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
