import pytest
import filecmp # use .samefile

@pytest.fixture()
def bashrc1():
    return "foo"

@pytest.fixture()
def vimrc1():
    return "blahblah"

@pytest.fixture()
def bashrc2():
    return "bar"

@pytest.fixture()
def rc1(tmp_path, bashrc1, vimrc1):
    """rc repo 1, bashrc and vimrc"""
    d = tmp_path / "mstefferson" / "rc"
    d.mkdir(parents=True)
    # bashrc
    p = d / "bashrc"
    p.write_text(bashrc1)
    # add vimrc
    p = d / "vimrc"
    p.write_text(vimrc1)
    return d


@pytest.fixture()
def rc2(tmp_path, bashrc2):
    """rc repo 2, just a bashrc"""
    d = tmp_path / "jeffmm" / "rc"
    d.mkdir(parents=True)
    # bashrc
    p = d / "bashrc"
    p.write_text(bashrc2)
    return d


def test_verify_build1(rc1, vimrc1, bashrc1):
    """Verify build of rc repo1"""
    assert rc1.is_dir()
    assert (rc1 / "bashrc").is_file()
    assert (rc1 / "bashrc").read_text() == bashrc1
    assert (rc1 / "vimrc").is_file()
    assert (rc1 / "vimrc").read_text() == vimrc1


def test_verify_build2(rc2, bashrc2):
    """Verify build of rc repo2"""
    assert rc2.is_dir()
    assert (rc2 / "bashrc").is_file()
    assert (rc2 / "bashrc").read_text() == bashrc2

def test_different_builds(rc1, rc2):
    """Make sure builds are different"""
    assert not (rc1 / "bashrc").samefile(rc2 / "bashrc")
