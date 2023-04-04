from setuptools import setup, find_packages

import sys
if not sys.version_info[0] == 3:
  sys.exit("Sorry, only Python 3 is supported")

def readme():
  with open('README.md') as f:
    return f.read()

setup(name='ec_finder',
      version='0.1',
      description='Find suitable EC numbers from enzyme names',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url="https://github.com/ggonnella/ec_finder",
      keywords="bioinformatics",
      author='Giorgio Gonnella and and others (see CONTRIBUTORS)',
      author_email='gonnella@zbh.uni-hamburg.de',
      license='ISC',
      # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries',
      ],
      packages=find_packages(),
      scripts=['bin/ec-find'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['loguru>=0.5.1', 'docopt>=0.6.2',
         "sh>=1.14.2", "thefuzz", "PlatformDirs", "python-Levenshtein"],
      setup_requires=['PlatformDirs'],
    )
