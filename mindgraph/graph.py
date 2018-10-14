# -*- coding: utf-8 -*-
from typing import List, Any
from yaml import dump, load
from bisect import bisect_left





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

    def append(self, nodeName: str) -> "Node":
        """ Creates a new Node and appends it to threads """
        if type(nodeName) is str:
            node = Node(nodeName)
            self._threads.append(node)
            return node
        else:
            raise TypeError

    def _linear_search(self, name: str) -> int:
        """ find a node index by name in self._threads """
        for i, node in enumerate(self._threads):
            if node.name == name:
                return i
        return -1

    def pop(self, item = None) -> "Node":
        """ Pops the Node from threads[index] """
        if type(item) == int:
            return self._threads.pop(item)
        if item == None:
            return self._threads.pop()
        index = self._linear_search(item)
        if index == -1:
            raise NameError
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

    def __len__(self) -> int:
        return len(self._threads)

    @property
    def dependencies(self) -> List["Node"]:
        """ dependencies getter """
        return self._dependencies

    @property
    def name(self) -> str:
        """ name getter """
        return self._name

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
