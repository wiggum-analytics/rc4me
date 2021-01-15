from rc4me.util import copyfiles


DESTINATION_DIR = "./"
SOURCE_DIR = "~/rc4me/"


def main():
    """Run copyfiles"""
    copyfiles(SOURCE_DIR, DESTINATION_DIR)


if __name__ == "__main__":
    main()
