import setuptools

setuptools.setup(
    name="SQLeasy", entry_points={"console_scripts": ["sqleasy=SQLeasy.cli:cli"]}
)
