from setuptools import setup


setup(
    name="tube_dream",
    version="1.0.4",
    packages=["tube_dream"],
    package_data={
        'tube_dream': [
            'downloads/*.txt',
            'img/*.png'
        ]
    },
    include_package_data=True,
    url="https://github.com/rootVIII/tube_dream",
    license="MIT",
    author="James Loye Colley",
    description="Download Audio from your favorite YouTube videos",
    entry_points={
        "console_scripts": [
            "tube_dream=tube_dream.tube_dream:main"
        ]
    },
    data_files=[
        (
            'tube_dream', [
                'img/froggy.png'
            ]
        )
    ]
)
