import pytest
from version import get_version, increment_version
test_version = get_version(path='./tests/files/pyproject.toml')


def test_get_version_an_element_has_project_name():
    assert test_version['project_name'] != ''

def test_get_version_contains_project_ally_ai():
    assert test_version['project_name'] == 'test-project-name'

def test_get_version_contains_project_ally_ai():
    assert test_version['version'] == '0.0.7'


@pytest.mark.parametrize('current, location, increment, expected', 
                         [
                             ('0.0.1', 'major', 1, '1.0.1'),
                             ('0.0.1', 'minor', 1, '0.1.1'),
                             ('0.0.1', 'patch', 1, '0.0.2'),
                         ])
def test_increment_version_001_major_increment_1_becomes_101(current, location, increment, expected):
    assert increment_version(current, location=location, increment=increment) == expected

def test_get_version_contains_project_ally_ai():
    assert test_version['version'] == '0.0.7'