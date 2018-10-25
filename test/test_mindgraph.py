import os
from random import choice
import string
from argparse import Namespace

import pytest
from unittest.mock import mock_open, patch
import yaml

from mindgraph import *


@pytest.fixture(scope="module")
def graph():
    graph = Project('learn all the things')
    return graph


@pytest.fixture
def task_graph():
    # setup example graph from issue #14
    g = Project('build a thing')

    t1 = g.append('task 1')
    t1.priority = 3
    t11 = t1.append('task 1.1')
    t12 = t1.append('task 1.2')
    t13 = t1.append('task 1.3')
    t13.priority = 3

    t2 = g.append('task 2')
    t2.priority = 2
    t21 = t2.append('task 2.1')
    t22 = t2.append('task 2.2')
    t221 = t22.append('task 2.2.1')
    t222 = t22.append('task 2.2.2')

    t3 = g.append('task 3')
    t31 = t3.append('task 3.1')
    t32 = t3.append('task 3.2')

    t32.subtasks.append(t22)
    t12.subtasks.append(t22)
    return g


def test_todo_high_prioritys_win(task_graph):
    """High prioritys are scheduled before low prioritys"""
    todo = [n.name for n in task_graph.todo()]
    assert todo.index('task 1') < todo.index('task 2')
    assert todo.index('task 1') < todo.index('task 3')
    assert todo.index('task 1.3') < todo.index('task 1.1')


def test_todo_blocking_tasks_win(task_graph):
    """Blocking tasks are scheduled before blocked tasks"""
    todo = [n.name for n in task_graph.todo()]
    assert todo.index('task 2.2') < todo.index('task 3.2')
    assert todo.index('task 2.2') < todo.index('task 1.2')
    assert todo.index('task 1.1') < todo.index('task 1.2')


def test_postorder_default_prioritys_ignored(task_graph):
    """Post-order traversal ignores node prioritys by default"""
    po = [n.name for _, n in task_graph._postorder()]
    assert po.index('task 1.1') < po.index('task 1.3')


def test_node_init_typeerror():
    with pytest.raises(TypeError) as info:
        node = Task(47)
        assert "" in str(info.value)


def test_node_append_node():
    rootTask = Task('root node')
    subTask1 = rootTask.append(Task('sub node'))
    subTask2 = rootTask.append(Task('sub node 2'))
    assert rootTask[0] is subTask1
    assert rootTask[1] is subTask2


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


def test_node_pop(graph):
    assert graph[2].name == '3rd thing'
    graph.pop(2)
    with pytest.raises(IndexError) as info:
        thing3 = graph[2]
        assert "" in str(info.value)


def test_node_pop_fail1(graph):
    with pytest.raises(IndexError):
        graph.pop(20000)


def test_node_append_TypeError():
    with pytest.raises(TypeError) as info:
        node = Task('mynode')
        node.append(47)
        assert "" in str(info.value)


def test_blockedby(graph):
    thing1 = graph[0]
    thing1_1 = thing1.append('thing within a thing')
    thing1_2 = thing1.append('thing blocking a thing')
    thing1_1.blockedby(thing1_2)
    assert thing1_1.blockers[0].name == 'thing blocking a thing'


def test_blocking(graph):
    thing2 = graph[1]
    thing2_1 = thing2.append('another thing within a thing')
    thing2_2 = thing2.append('another thing blocking a thing')
    thing2_2.blocking(thing2_1)
    assert thing2_1.blockers[0].name == 'another thing blocking a thing'


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
        "learn all the things:\n",
        "- 1st thing:\n",
        "  - thing within a thing\n",
        "  - thing blocking a thing\n",
        "- 2nd thing:\n"
        "  - another thing within a thing\n",
        "  - another thing blocking a thing\n",
    ])


def test_deep_repr(graph):

    thing2_1 = graph[1][0]
    assert thing2_1.name == 'another thing within a thing'

    thing2_1.append('super deep thing')

    assert str(graph) == "".join([
        "learn all the things:\n",
        "- 1st thing:\n",
        "  - thing within a thing\n",
        "  - thing blocking a thing\n",
        "- 2nd thing:\n"
        "  - another thing within a thing:\n",
        "    - super deep thing\n"
        "  - another thing blocking a thing\n",
    ])

    thing2_1.pop(0)


def test_priority_getter_setter():
    node = Task('myTask')
    default_priority = node.priority
    node.priority = 5

    assert default_priority == 1
    assert node.priority == 5


def test_name_getter_setter():
    node = Task()
    default_name = node.name
    node.name = 'a new name'

    assert default_name == ''
    assert node.name == 'a new name'


def test_to_yaml(graph):
    assert graph.name == 'learn all the things'
    assert graph[0].name == '1st thing'
    graph.to_yaml('mindgraph.yaml')
    graph2 = read_yaml('mindgraph.yaml')
    test_repr(graph2)
    assert repr(graph) == repr(graph2)
    os.remove('mindgraph.yaml')


def test_to_yaml_TypeError():
    not_a_graph = yaml.dump("not a graph")
    with open('not_a_graph.yaml', 'w') as f:
        f.write(not_a_graph)
    with pytest.raises(TypeError) as info:
        read_yaml('not_a_graph.yaml')
        assert "" in str(info.value)
    os.remove('not_a_graph.yaml')


def test_parser():
    file_list = [choice(string.ascii_letters) for _ in range(5)]
    parser = arg_parser(["-f"]+file_list)
    assert parser.files == file_list


@patch("builtins.open", new_callable=mock_open,
       read_data="learn all the things")
@patch("mindgraph.mindgraph_cli.arg_parser")
@patch("mindgraph.mindgraph_cli.read_yaml")
def test_main(mock_read_yaml, mock_arg_parse, mock_file):
    file_list = [choice(string.ascii_letters) for _ in range(5)]
    mock_arg_parse.return_value = Namespace(files=file_list)
    mock_read_yaml.return_value = "read yaml file"
    main()
    for file in file_list:
        mock_file.assert_any_call(file, "r")
        mock_read_yaml.assert_any_call(file)
        assert open(file).read() == "learn all the things"

    mock_open(mock_file,
              read_data="Not Yaml format\n\t\t{learn all the things}")
    mock_read_yaml.reset_mock()
    main()
    mock_read_yaml.assert_not_called()


if __name__ == '__main__':
    print(__doc__)
    pytest.main(args=['-v'])
