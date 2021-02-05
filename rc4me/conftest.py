import pytest


@pytest.fixture()
def bashrc_init():
    return "hello"


@pytest.fixture()
def bashprofile_init():
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
def rcinit(tmp_path, bashrc_init, bashprofile_init):
    """rc for intial setup, bashrc and bashprofile"""
    d = tmp_path
    d.mkdir(parents=True)
    # bashrc
    p = d / "bashrc"
    p.write_text(bashrc_init)
    p = d / "bashprofile"
    p.write_text(bashprofile_init)

    # verify
    assert rcinit.is_dir()
    assert (rcinit / "bashrc").is_file()
    assert (rcinit / "bashrc").read_text() == bashrc_init
    assert (rcinit / "bashprofile").is_file()
    assert (rcinit / "bashprofile").read_text() == bashprofile_init

    return d


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

    # verify
    assert rc1.is_dir()
    assert (rc1 / "bashrc").is_file()
    assert (rc1 / "bashrc").read_text() == bashrc1
    assert (rc1 / "vimrc").is_file()
    assert (rc1 / "vimrc").read_text() == vimrc1

    return d


@pytest.fixture()
def rc2(tmp_path, bashrc2):
    """rc repo 2, just a bashrc"""
    d = tmp_path / "jeffmm" / "rc"
    d.mkdir(parents=True)
    # bashrc
    p = d / "bashrc"
    p.write_text(bashrc2)
    assert rc2.is_dir()
    assert (rc2 / "bashrc").is_file()
    assert (rc2 / "bashrc").read_text() == bashrc2
    return d
