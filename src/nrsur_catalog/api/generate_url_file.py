import os
from typing import Dict
from nrsur_catalog.utils import get_event_name

HERE = os.path.dirname(os.path.abspath(__file__))
LVK_URL_FILE = os.path.join(HERE, "lvk_urls.txt")
NR_URL_FILE = os.path.join(
    HERE, "nrsur_urls.txt"
)  # This file's contents are autogenerated
TITLE = "NRSurrogate Catalog Posteriors"


def _commit_url_file():
    try:
        import git

        repo_root = os.path.join(HERE, "../../..")
        repo = git.Repo(repo_root)
        repo.git.add(NR_URL_FILE)
        repo.git.commit(m=f"update urls [automated]")
        repo.git.push()
    except Exception as e:
        pass


def cache_zenodo_urls_file(sandbox=True) -> None:
    """Update the file URLs to the data on zenodo"""
    from zenodo_python import Deposition

    zeno = Deposition.from_title(title=TITLE, test=sandbox)
    print(f"Zenodo {zeno} has {len(zeno.files)} files. Caching download URLs.")
    zeno.save_wget_file(NR_URL_FILE)
    file_contents = open(NR_URL_FILE, "r").read()
    print(f"Finished caching Zenodo URLs to {NR_URL_FILE}:\n{file_contents}")
    _commit_url_file()


def get_zenodo_urls(lvk_posteriors=False) -> Dict[str, str]:
    """Returns a dictionary of the analysed events and their urls"""

    url_file = NR_URL_FILE
    if lvk_posteriors:
        url_file = LVK_URL_FILE

    # read in the zenodo_urls.txt file (each line is a url)
    with open(url_file, "r") as f:
        urls = f.readlines()
        urls = [url.strip() for url in urls]

    if len(urls) == 0:
        raise RuntimeError(f"No URLs found in {url_file}")

    # extract the event name from the url
    event_urls = [u for u in urls if "GW" in u]
    event_names = [get_event_name(url) for url in event_urls]
    return dict(zip(event_names, event_urls))


def __write_url_dicts():
    lvk_urls = get_zenodo_urls(lvk_posteriors=True)
    nrsur_urls = get_zenodo_urls(lvk_posteriors=False)
    with open('urls.py', 'w') as f:
        f.write(f"LVK_URLS = {lvk_urls}\n")
        f.write(f"NR_URLS = {nrsur_urls}\n")


if __name__ == "__main__":
    __write_url_dicts()
