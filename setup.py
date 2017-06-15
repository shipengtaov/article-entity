#!/usr/bin/env python

from setuptools import setup, find_packages
import article_entity


with open('README.md', 'r') as f:
    long_description = f.read().strip()

setup(
    name='article_entity',
    version=article_entity.__version__,
    description="extract article's entity",
    long_description=long_description,
    keywords='extract article entity',
    author='PengTao Shi',
    author_email='shispt18@gmail.com',
    url='https://github.com/shispt/article-entity',
    license='MIT',
    packages=find_packages(),
)
