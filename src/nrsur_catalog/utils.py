import os

import numpy as np
import re


def get_size_of_file(filename: str) -> str:
    """Get the size of a file in human-readable format"""
    size = os.path.getsize(filename)
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


def get_1d_summary_str(x: np.ndarray):
    q_lo, q_mid, q_hi = np.quantile(x, [0.16, 0.5, 0.84])
    q_m, q_p = q_mid - q_lo, q_hi - q_mid
    fmt = "{{0:{0}}}".format(".2f").format
    summary = r"${{{0}}}_{{-{1}}}^{{+{2}}}$"
    return summary.format(fmt(q_mid), fmt(q_m), fmt(q_p))


def get_event_name(s: str):
    """Get the event name from a string using a regex
    e.g.
    'GW170817' from 'GW170817_4.5_0.1.hdf5'
    'GW150914' from "https://sandbox.zenodo.org/record/1164558/files/GW150914_result.json"
    'GW200224_222234'  from  "GW200224_222234_NRSur7dq4_merged_result.json"
    """
    try:
        return re.findall(r"(GW\d{6}\_\d{6}|GW\d{6})", s)[0]
    except IndexError:
        raise ValueError(f"Could not parse event name from {s}")
