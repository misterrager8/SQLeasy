import setuptools

setuptools.setup(
    name="SQLeasy",
    license=open("LICENSE.md").read(),
    long_description=open("README.md").read(),
    entry_points={"console_scripts": ["sqleasy=SQLeasy.cli:cli"]},
)
