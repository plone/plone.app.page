from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='plone.app.page',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Rob Gietema',
      author_email='rob@fourdigits.nl',
      url='http://plone.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          'plone.app.deco',
          'plone.app.standardtiles',
          'plone.app.layoutbehavior',
          'plone.app.blocks',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
