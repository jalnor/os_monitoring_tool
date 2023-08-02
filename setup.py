from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='os-monitoring-tool',
    version='1.0.dev1',
    packages=find_packages(where="src", exclude=["db.ReturnResultsThread.py", "db.page.txt", ]),
    url='https://github.com/jalnor/os_monitoring_tool.git',
    license='MIT',
    author='jalnor',
    author_email='',
    description='A process monitoring tool',
    python_requires=">=3.8"
)
