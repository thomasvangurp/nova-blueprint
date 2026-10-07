import unittest

from sandbox.broker import validate_boltz2_options


class Boltz2OptionsTest(unittest.TestCase):
    def test_accepts_bounded_options(self):
        options = {
            "recycling_steps": 1,
            "sampling_steps": 50,
            "diffusion_samples": 1,
            "recycling_steps_affinity": 2,
            "sampling_steps_affinity": 50,
            "diffusion_samples_affinity": 1,
            "step_scale": 1.638,
        }
        self.assertEqual(validate_boltz2_options(options), options)

    def test_rejects_unknown_option(self):
        with self.assertRaisesRegex(ValueError, "unsupported"):
            validate_boltz2_options({"seed": 68})

    def test_rejects_out_of_bounds_and_bool(self):
        with self.assertRaisesRegex(ValueError, "between"):
            validate_boltz2_options({"sampling_steps": 0})
        with self.assertRaisesRegex(ValueError, "wrong type"):
            validate_boltz2_options({"diffusion_samples": True})


if __name__ == "__main__":
    unittest.main()
