from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parents[2]

SOURCES_DIR = PROJECT_ROOT_DIR.joinpath('sources')
BUILD_DIR = PROJECT_ROOT_DIR.joinpath('build')
