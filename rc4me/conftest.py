import pytest


@pytest.fixture()
def bashrc_starting():
    return "hello"


@pytest.fixture()
def bashprofile_starting():
    return "world"


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
def startingfiles(tmp_path, bashrc_starting, bashprofile_starting):
    """rc for intial setup, bashrc and bashprofile

    Note, this isn't save in init folder
    """
    d = tmp_path
    # bashrc
    p = d / "bashrc"
    p.write_text(bashrc_starting)
    p = d / "bashprofile"
    p.write_text(bashprofile_starting)

    # verify
    assert (d / "bashrc").is_file()
    assert (d / "bashrc").read_text() == bashrc_starting
    assert (d / "bashprofile").is_file()
    assert (d / "bashprofile").read_text() == bashprofile_starting

    return d


@pytest.fixture()
def rc1(tmp_path, bashrc1, vimrc1):
    """rc repo 1, bashrc and vimrc"""
    d = tmp_path / "mstefferson_rc"
    d.mkdir()
    # bashrc
    p = d / "bashrc"
    p.write_text(bashrc1)
    # add vimrc
    p = d / "vimrc"
    p.write_text(vimrc1)

    # verify
    assert d.is_dir()
    assert (d / "bashrc").is_file()
    assert (d / "bashrc").read_text() == bashrc1
    assert (d / "vimrc").is_file()
    assert (d / "vimrc").read_text() == vimrc1

    return d


@pytest.fixture()
def rc2(tmp_path, bashrc2):
    """rc repo 2, just a bashrc"""
    d = tmp_path / "jeffmm_rc"
    d.mkdir()
    # bashrc
    p = d / "bashrc"
    p.write_text(bashrc2)
    assert d.is_dir()
    assert (d / "bashrc").is_file()
    assert (d / "bashrc").read_text() == bashrc2
    return d
