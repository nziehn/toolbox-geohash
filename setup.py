from os import path
import setuptools

# read the contents of your README file
# this_directory = path.abspath(path.dirname(__file__))
# with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

dependencies = [
    'numpy',
]

setuptools.setup(
    name='toolbox-geohash',
    version='0.1.0',
    description=(
        'Module to encode any coordinate on earth to an integer and back to coordinates.\n'
        'In comparison to typical geohashing approaches in this library you can configure the '
        'accuracy of the hashing be defining the desired size of the triangles that are used.'
    ),
    # long_description=description,
    # long_description_content_type='text/markdown',
    url='http://github.com/nziehn/toolbox-geohash',
    author='Nils Ziehn',
    author_email='nziehn@gmail.com',
    license='MIT',
    packages=[
        package for package in setuptools.find_packages() if package.startswith('toolbox')
    ],
    namespace_packages=['toolbox'],
    install_requires=dependencies,
    zip_safe=False
)