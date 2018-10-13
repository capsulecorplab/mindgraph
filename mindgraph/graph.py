# -*- coding: utf-8 -*-
from yaml import dump, load


class Node(object):
    """node class"""

    def __init__(self, name=None):
        self._dependencies = list()
        self._threads = list()
        self._name = ''
        if type(name) is str:
            self._name = name
        else:
            raise TypeError

    def append(self, nodeName):
        if type(nodeName) is str:
            node = Node(nodeName)
            self._threads.append(node)
            return node
        else:
            raise TypeError

    def remove(self, nodeName):
        self._threads.pop(nodeName)

    def blockedby(self, node):
        if type(node) is Node:
            self._dependencies.append(node)

    def blocking(self, node):
        if type(node) is Node:
            node._dependencies.append(self)

    def __getitem__(self, key):
        return self._threads[key]

    def __repr__(self):
        if len(self.threads) > 0:
            # print('not self')
            return "".join(["{",
                            "{}:{}".format(self.name,
                                           self.threads),
                            "}"])
        # print('self')
        return "{}".format(self.name)

    def __str__(self):
        return dump(load(str(self.__repr__())), default_flow_style=False)

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def name(self):
        return self._name

    @property
    def threads(self):
        return self._threads


class Graph(Node):
    """A Graph model of the mind"""

    def __init__(self, name=None):
        Node.__init__(self, name)

    def to_yaml(self, filename=None):
        with open(filename, 'w') as f:
            f.write(dump(self))


def read_yaml(filename=None):
    with open(filename, 'r') as f:
        rv = load(f.read())
        if type(rv) is Graph:
            return rv
        else:
            raise TypeError(type(rv))
