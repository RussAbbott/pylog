from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pylog',
      version='1.1',
      description='Python implementation of Prolog features.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.com/RussAbbott/pylog',
      author='Russ Abbott, Jay Patel',
      author_email='Russ.Abbott@gmail.com, imjaypatel12@gmail.com',
      license='MIT',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='prolog python logic programming',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      python_requires='>=3.7',
      setup_requires=["pytest-runner"],
      tests_require=["pytest"])
