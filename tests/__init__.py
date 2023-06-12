import unittest

if __name__ == "__main__":
    from tests.test_equatorial import EquatorialTest
    from tests.test_horizontal import HorizontalTest
    from tests.test_nvector import NVectorTest
    from tests.test_system_conversation import EquatorialToHorizontalTest, HorizontalToPointTest
    from tests.test_vector import VectorTest

    unittest.main()
