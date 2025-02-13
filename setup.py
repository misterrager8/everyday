import setuptools

setuptools.setup(
    name="everyday",
    entry_points={"console_scripts": ["everyday=everyday.__main__:cli"]},
    py_modules=["everyday"],
)
