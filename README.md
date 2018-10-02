# mindgraph

    > A graph data structure, for task management, in python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

## Usage

Install mindgraph from source code:

```
$ pip install git+https://github.com/capsulecorplab/mindgraph.git
```

### Example usage

```
>>> import mindgraph as mg

>>> graph = mg.Graph('learn all the things')
>>> thing1 = graph.append('1st thing')
>>> thing2 = graph.append('2nd thing')
>>> thing3 = graph.append('3rd thing')

>>> graph.remove(2)

>>> thing1 = graph[0]
>>> thing1_1 = thing1.append('thing within a thing')
>>> thing1_2 = thing1.append('thing blocking a thing')
>>> thing1_1.blockedby(thing1_2)

>>> thing2_1 = thing2.append('another thing within a thing')
>>> thing2_2 = thing2.append('another thing blocking a thing')
>>> thing2_2.blocking(thing2_1)

>>> print(graph)
name: learn all the things
threads:
- name: 1st thing
  threads:
  - thing within a thing
  - thing blocking a thing
- name: 2nd thing
  threads:
  - another thing within a thing
  - another thing blocking a thing
```

`Graph` objects can be exported to, and imported from, a yaml file for storage:

```
>>> graph.to_yaml('mygraph.yaml')
>>> graph2 = mg.read_yaml('mygraph.yaml')
```

## Contribute

Optional (but recommended for viewing GitHub issues): Install the [ZenHub for GitHub](https://chrome.google.com/webstore/detail/zenhub-for-github/ogcgkffhplmphkaahpmffcafajaocjbd?hl=en-US) chrome extension.

1. Fork it (<https://github.com/yourusername/mindgraph/fork>)
2. Create your feature branch (`git checkout -b feature/logarithms`)
3. Commit your changes (`git commit -am 'Add some logarithms'`)
4. Push to the branch (`git push origin feature/logarithms`)
5. Create a new Pull Request
