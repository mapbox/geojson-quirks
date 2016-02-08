from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='geojson-quirks',
      version='0.0.2',
      description=u"Tweak your data to interoperate with quirky GeoJSON readers",
      long_description=long_description,
      classifiers=[],
      keywords='geojson',
      author=u"Matthew Perry",
      author_email='perry@mapbox.com',
      url='https://github.com/mapbox/geojson-quirks',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click', 'cligj'
      ],
      entry_points="""
      [console_scripts]
      geojson-quirks=geojson_quirks.scripts.cli:main
      """
      )
