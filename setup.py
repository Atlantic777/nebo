from setuptools import setup

setup(
        name = "nebo",
        packages = ["nebo"],
        version = "0.1",
        url = "github.com/atlantic777/nebo",
        description = "New EC2 Big-Data Orchestrator",
        author = "Nikola Hardi",
        author_email = "atlantic777@lugons.org",
        keywords = ["aws", "ec", "big-data", "distributed computing"],
        classifiers = [
            "Programming Language :: Python",
            "Programming Language :: python :: 3",
            "Development Status :: 4 - Beta",
            ],
        entry_points={
            'console_scripts': [
                'nebo=nebo.__main__:main',
                ],
            },
        zip_safe=False,
)
