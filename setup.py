from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pylog',
      version='0.1',
      description='Python implementation of Prolog features.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='prolog python logic programming',
      url='https://github.com/RussAbbott/pylog',
      author='Russ Abbott',
      author_email='Russ.Abbott@gmail.com',
      license='MIT',
      packages=['pylog'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      python_requires='>=3.7')
