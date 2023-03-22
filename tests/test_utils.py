import unittest
from nrsur_catalog.utils import get_event_name


class TestUtils(unittest.TestCase):
    def test_get_event_name(self):
        self.assertEqual(
            get_event_name("GW170817_NRSur7dq4_merged_result.json"), "GW170817"
        )
        self.assertEqual(get_event_name("GW170817_4.5_0.1.hdf5"), "GW170817")
        self.assertEqual(
            get_event_name(
                "https://sandbox.zenodo.org/record/1164558/files/GW150914_result.json"
            ),
            "GW150914",
        )
        self.assertEqual(
            get_event_name(
                "https://zenodo.org/record/5546663/files/IGWN-GWTC3p0-v1-GW200209_085452_PEDataRelease_mixed_cosmo.h5"
            ), "GW200209_085452"
        )


if __name__ == "__main__":
    unittest.main()
