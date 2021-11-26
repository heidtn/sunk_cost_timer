#!/usr/bin/env python

from distutils.core import setup

setup(name='sunk_cost_timer',
      version='1.0',
      description='A timer to manage project time investment',
      install_requires=[
          'PySide2',
      ],
      author='Nathan Heidt',
      author_email='strigusconsilium@gmail.com',
      packages=['sunk_cost_timer'],
      entry_points={
          'console_scripts': [
              'sunk_cost_timer = sunk_cost_timer.timer:main',
          ],
      },
      )
