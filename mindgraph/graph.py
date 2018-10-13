# -*- coding: utf-8 -*-
from typing import List, Optional
from yaml import dump, load


class Node(object):
    """node class"""

    def __init__(self, name: str = '', weight: int = 1) -> None:
        self._dependencies = list() # type: List[Node]
        self._threads = list() # type: List[Node]
        self._name = '' # type: str
        self._weight = weight # type: int
        if type(name) is str:
            self._name = name
        else:
            raise TypeError

    def append(self, nodeName: str) -> Node:
        if type(nodeName) is str:
            node = Node(nodeName)
            self._threads.append(node)
            return node
        else:
            raise TypeError

    def remove(self, nodeName: int) -> Node:
        threads_length = len(self._threads)
        if type(nodeName) is int and nodeName < threads_length:
            return self._threads.pop(nodeName)
        else:
            raise TypeError

    def blockedby(self, node: Node) -> None:
        if type(node) is Node:
            self._dependencies.append(node)
            return None
        else:
            raise TypeError

    def blocking(self, node: Node) -> None:
        if type(node) is Node:
            node._dependencies.append(self)
            return None
        else:
            raise TypeError

    def __getitem__(self, key: int) -> Node:
        return self._threads[key]

    def __repr__(self) -> str:
        if len(self.threads) > 0:
            # print('not self')
            return "".join(["{",
                            "{}:{}".format(self.name,
                                           self.threads),
                            "}"])
        # print('self')
        return "{}".format(self.name)

    def __str__(self) -> str:
        return dump(load(str(self.__repr__())), default_flow_style=False)

    @property
    def dependencies(self) -> List[Node]:
        return self._dependencies

    @property
    def name(self) -> str:
        return self._name

    @property
    def threads(self) -> List[Node]:
        return self._threads

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, value: int) -> None:
        self._weight = value


class Graph(Node):
    """A Graph model of the mind"""

    def __init__(self, name=None) -> None:
        Node.__init__(self, name)

    def to_yaml(self, filename=None) -> None:
        with open(filename, 'w') as f:
            f.write(dump(self))


def read_yaml(filename: str = "") -> Graph:
    with open(filename, 'r') as f:
        rv = load(f.read())
        if type(rv) is Graph:
            return rv
        else:
            raise TypeError(type(rv))
