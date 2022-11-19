import setuptools


name = 'datatrans-api-python-types'
dependencies = ['openapi3~=1.7.0']
dependencies_dev = ['pytest']
console_scripts = ['datatrans-api-python-types = datatrans_api_python_types:entry_point']

setuptools.setup(
    name=name,
    entry_points=dict(console_scripts=console_scripts),
    install_requires=dependencies,
    extras_require={'dev': dependencies_dev},
    setup_requires=['setuptools>=42', 'wheel', 'setuptools_scm[toml]>=3.4'],
    use_scm_version=True,
    include_package_data=True,
    packages=setuptools.find_packages(exclude=['tests']))
