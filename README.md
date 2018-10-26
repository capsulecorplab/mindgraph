# mindgraph

> A graph data structure, for task management, in python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.com/capsulecorplab/mindgraph.svg?branch=master)](https://travis-ci.com/capsulecorplab/mindgraph)
[![Coverage Status](https://coveralls.io/repos/github/capsulecorplab/mindgraph/badge.svg?branch=master)](https://coveralls.io/github/capsulecorplab/mindgraph?branch=master)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

## Usage

Install mindgraph from source code:

```
$ pip install git+https://github.com/capsulecorplab/mindgraph.git
```

### Example usage

```
>>> import mindgraph as mg

>>> project = mg.Project('learn all the things')
>>> thing1 = project.append('1st thing')
>>> thing2 = project.append('2nd thing')
>>> thing3 = project.append('3rd thing')

>>> project.remove(2)

>>> thing1 = project[0]
>>> thing1_1 = thing1.append('thing within a thing')
>>> thing1_2 = thing1.append('thing blocking a thing')
>>> thing1_1.blockedby(thing1_2)

>>> thing2_1 = thing2.append('another thing within a thing')
>>> thing2_2 = thing2.append('another thing blocking a thing')
>>> thing2_2.blocking(thing2_1)

>>> print(project)
learn all the things:
- 1st thing:
  - thing within a thing
  - thing blocking a thing
- 2nd thing:
  - another thing within a thing
  - another thing blocking a thing
```

Projects can be exported to, or imported from, a yaml file for external storage:

```
>>> project.to_yaml('myproject.yaml')
>>> revivedproject = mg.read_yaml('myproject.yaml')
```

## Contribute

Optional (but recommended for viewing GitHub issues): Install the [ZenHub for GitHub](https://chrome.google.com/webstore/detail/zenhub-for-github/ogcgkffhplmphkaahpmffcafajaocjbd?hl=en-US) chrome extension.

1. Fork it (<https://github.com/yourusername/mindgraph/fork>)
2. Create your feature branch (`git checkout -b feature/logarithms`)
3. Commit your changes (`git commit -am 'Add some logarithms'`)
4. Push to the branch (`git push origin feature/logarithms`)
5. Create a new Pull Request
