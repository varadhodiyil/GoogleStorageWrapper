import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


path = os.path.dirname(os.path.abspath(__file__))


def package_files(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filename = os.path.join(root, filename)
            result.append(os.path.abspath(filename))
    return result


setup(
    name="GoogleStorage",
    version="1.0",
    author="Sachin Edward",
    author_email="edward9494@gmail.com",
    description="Google Cloud storage Wrapper",
    url="https://github.com/sachinedward/GoogleStorageWrapper",
    packages=['GoogleStorage'],
    include_package_data=True,
    package_dir={'GoogleStorage': "src/"},
    package_data={'GoogleStorage': package_files('src/')},
    install_requires=['google-cloud', 'google-api-python-client']
)
