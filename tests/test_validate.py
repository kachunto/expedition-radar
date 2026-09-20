import copy, json, os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from validate import validate

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = json.load(open(os.path.join(ROOT, "content", "items.json"), encoding="utf-8"))


def broken(fn):
    d = copy.deepcopy(DATA)
    fn(d["items"][0])
    return validate(d)[0]


class ValidatorTests(unittest.TestCase):
    def test_real_data_has_no_errors(self):
        self.assertEqual(validate(DATA)[0], [])

    def test_severity_must_not_increase(self):
        def f(it): it["tiers"]["t1"]["sev"] = [0, 2, 0, 0]
        self.assertTrue(broken(f))

    def test_higher_tier_not_milder(self):
        def f(it):
            it["tiers"]["t1"]["sev"] = [2, 2, 2, 2]
            it["tiers"]["t2"]["sev"] = [1, 1, 1, 1]
        self.assertTrue(broken(f))

    def test_impact_keys_match_lenses(self):
        def f(it): it["impact"] = {}
        self.assertTrue(broken(f))

    def test_out_of_scope_window(self):
        def f(it): it["window"]["from"] = "act2"
        self.assertTrue(any("outside MVP scope" in " ".join(map(str, e)) for e in broken(f)))

    def test_spoiler_term_in_tier1_needs_severity(self):
        def f(it):
            it["tiers"]["t1"]["text"] = "Ask Verso about it."
            it["tiers"]["t1"]["sev"] = [0, 0, 0, 0]
        self.assertTrue(broken(f))

    def test_source_verified_needs_two_sources(self):
        def f(it):
            it["status"] = "source_verified"
            it["sources"] = it["sources"][:1]
            it["conflict"] = None
        self.assertTrue(broken(f))

    def test_later_act_in_tier_text_needs_severity(self):
        def f(it):
            it["tiers"]["t1"]["text"] = "Come back in Act 2."
            it["tiers"]["t1"]["sev"] = [0, 0, 0, 0]
        self.assertTrue(broken(f))

    def test_later_act_in_pnr(self):
        def f(it): it["window"]["pnr"] = "before Act 2 starts"
        self.assertTrue(broken(f))


if __name__ == "__main__":
    unittest.main()
