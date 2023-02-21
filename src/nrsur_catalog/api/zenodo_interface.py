"""Module to upload NRSur Catlog events to Zenodo
Used just by NRSur Catalog developers/maintainers
"""
import zenodopy
import os
import argparse
from zenodo_get.zget import zenodo_get
from ..logger import logger
from ..utils import get_event_name
from glob import glob
from tqdm.auto import tqdm

HERE = os.path.dirname(os.path.abspath(__file__))
URL_FILE = os.path.join(
    HERE, "zenodo_urls.txt"
)  # This file's contents are autogenerated

ZENODO_KEYS = dict(
    MAIN=dict(project_id=000, token_key="ZENODO_TOKEN"),
    SANDBOX=dict(project_id=1164736, token_key="SANDBOX_TOKEN")
)


def get_zenodo_access_token(token_key: str) -> str:
    """Get the zenodo access token from the environment variables"""
    access_token = os.environ.get(token_key, None)
    if access_token is None:
        raise RuntimeError(
            f"No Zenodo access token found: set the {access_token} environment variable, "
            "see https://zenodo.org/account/settings/applications/tokens/new/"
        )
    return access_token


def get_zenodo_project(sandbox=True) -> zenodopy.Client:
    """Get the write-access to zenodo project"""
    if sandbox:
        project_id, token_key = ZENODO_KEYS["SANDBOX"].values()
    else:
        project_id, token_key = ZENODO_KEYS["MAIN"].values()
    access_token = get_zenodo_access_token(token_key)
    zeno = zenodopy.Client(token=access_token, sandbox=sandbox)
    zeno.set_project(project_id)
    return zeno


def upload_files_to_zenodo(file_regex: str, sandbox=True) -> None:
    """Upload the NRSur Catlog events to Zenodo given the event name"""
    zeno = get_zenodo_project(sandbox)
    files = glob(file_regex)

    for filepath in tqdm(files, desc="Uploading to zenodo"):
        print(f"Uploading {filepath} to zenodo")
        zeno.upload_file(filepath)
    logger.info(f"Finished uploading {len(files)} files to Zenodo (project {zeno})")


def cache_zenodo_file_urls(sandbox=True) -> None:
    """Update the file URLs to the data on zenodo"""
    zeno = get_zenodo_project(sandbox)
    zenodo_get(argv=[f"--wget={URL_FILE}", "-s", "-r", zeno.deposition_id])
    file_contents = open(URL_FILE, "r").read()
    logger.info(f"Finished caching Zenodo URLs to {URL_FILE}: {file_contents}")


def get_zenodo_urls() -> dict:
    """Returns a dictionary of the analysed events and their urls"""
    # read in the zenodo_urls.txt file (each line is a url)
    with open(URL_FILE, "r") as f:
        urls = f.readlines()
        urls = [url.strip() for url in urls]

    if len(urls) == 0:
        raise RuntimeError(f"No URLs found in {URL_FILE}")

    # extract the event name from the url
    event_names = [get_event_name(url) for url in urls]
    return dict(zip(event_names, urls))


def main() -> None:
    """Main function to upload the NRSur Catlog events to Zenodo"""
    parser = argparse.ArgumentParser(
        description="Upload the NRSur Catlog events to Zenodo"
    )
    parser.add_argument(
        "path_regex",
        type=str,
        help="Path regex to the events to upload to Zenodo",
    )
    parser.add_argument(
        "--not-sandbox",
        help="Upload to the main zenodo page (not sandbox).",
        action="store_false",
    )
    args = parser.parse_args()
    sandbox = not args.not_sandbox
    upload_files_to_zenodo(args.path_regex, sandbox)
