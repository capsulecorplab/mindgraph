from setuptools import setup

setup(
    name='mindgraph',
    version='0.0.1',
    packages=['mindgraph'],
    author="Sean Marquez",
    author_email="capsulecorplab@gmail.com",
    description="A graph data structure, for task management, in python",
    url="https://github.com/capsulecorplab/mindgraph",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['pytest-runner'],
    install_requires=['pyyaml'],
    test_require=['os', 'pytest', 'pyyaml'],
)
