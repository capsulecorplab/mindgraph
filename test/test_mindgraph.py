from mindgraph import *
import pytest
import yaml
import os


@pytest.fixture(scope="module")
def graph():
    graph = Graph('learn all the things')
    return graph


def test_node_init_typeerror():
    with pytest.raises(TypeError) as info:
        node = Node(47)
        assert "" in str(info.value)


def test_node_append(graph):
    thing1 = graph.append('1st thing')
    thing2 = graph.append('2nd thing')
    thing3 = graph.append('3rd thing')

    assert thing1 is graph[0]
    assert thing2 is graph[1]
    assert thing3 is graph[2]

    assert thing1.name == '1st thing'
    assert thing2.name == '2nd thing'
    assert thing3.name == '3rd thing'


def test_node_remove(graph):
    assert graph[2].name == '3rd thing'
    graph.remove(2)
    with pytest.raises(IndexError) as info:
        thing3 = graph[2]
        assert "" in str(info.value)


def test_node_append_TypeError():
    with pytest.raises(TypeError) as info:
        node = Node('mynode')
        node.append(47)
        assert "" in str(info.value)


def test_blockedby(graph):
    thing1 = graph[0]
    thing1_1 = thing1.append('thing within a thing')
    thing1_2 = thing1.append('thing blocking a thing')
    thing1_1.blockedby(thing1_2)
    assert thing1_1.dependencies[0].name == 'thing blocking a thing'


def test_blocking(graph):
    thing2 = graph[1]
    thing2_1 = thing2.append('another thing within a thing')
    thing2_2 = thing2.append('another thing blocking a thing')
    thing2_2.blocking(thing2_1)
    assert thing2_1.dependencies[0].name == 'another thing blocking a thing'


def test_repr(graph):
    assert graph.name == 'learn all the things'

    thing1 = graph[0]
    thing2 = graph[1]

    with pytest.raises(IndexError) as info:
        thing3 = graph[2]
        assert "" in str(info.value)

    assert thing1.name == '1st thing'
    assert thing2.name == '2nd thing'

    assert str(graph) == "".join([
                                  "name: learn all the things\n",
                                  "threads:\n",
                                  "- name: 1st thing\n",
                                  "  threads:\n",
                                  "  - thing within a thing\n",
                                  "  - thing blocking a thing\n",
                                  "- name: 2nd thing\n"
                                  "  threads:\n",
                                  "  - another thing within a thing\n",
                                  "  - another thing blocking a thing\n",
                                ])


def test_to_yaml(graph):
    assert graph.name == 'learn all the things'
    assert graph[0].name == '1st thing'
    graph.to_yaml('mindgraph.yaml')
    graph2 = read_yaml('mindgraph.yaml')
    test_repr(graph2)
    os.remove('mindgraph.yaml')


def test_to_yaml_TypeError():
    not_a_graph = yaml.dump("not a graph")
    with open('not_a_graph.yaml', 'w') as f:
        f.write(not_a_graph)
    with pytest.raises(TypeError) as info:
        read_yaml('not_a_graph.yaml')
        assert "" in str(info.value)
    os.remove('not_a_graph.yaml')


if __name__ == '__main__':
    print(__doc__)
    pytest.main(args=['-v'])
