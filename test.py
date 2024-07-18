import json
import unittest
from sendero import find_paths, get, list_paths

with open("./data/code.json") as f:
    data = json.load(f)


class PathSetsTests(unittest.TestCase):
    def test_simple(self):
        paths = find_paths({"a": {"b": "c"}})
        self.assertEqual(paths, {"a.b"})


def test_top_level_array(self):
    paths = find_paths([{"a": {"b": "c"}}, {"d": {"e": "f"}}])
    self.assertEqual(paths, {"a.b", "d.e"})


class ListPathTests(unittest.TestCase):
    def test_list_paths(self):
        paths = list_paths({"a": {"b": "c"}})
        self.assertEqual(paths, ["a.b"])

    def test_top_level_list(self):
        paths = list_paths([{"a": {"b": "c"}}, {"d": {"e": "f"}}])
        self.assertEqual(paths, ["a.b", "d.e"])

    def test_nested_array(self):
        paths = list_paths([{"a": {"b": "c"}}, {"d": {"e": [{"f": "g"}, {"h": "i"}]}}])
        self.assertEqual(paths, ["a.b", "d.e.f", "d.e.h"])


class ExampleTest(unittest.TestCase):
    def test_list_paths(self):
        cars = [
            {
                "make": "Nissan",
                "model": "Altima",
                "year": 2022,
                "owners": [{"id": 1, "name": "Juan"}, {"id": 2, "name": "Mark"}],
            },
            {
                "make": "Nissan",
                "model": "Kicks",
                "year": 2021,
                "owners": [{"id": 3, "name": "Zach"}],
            },
            {
                "make": "Toyota",
                "model": "Camry",
                "year": 1995,
                "owners": [{"id": 4, "name": "Tom"}],
            },
        ]
        paths = list_paths(cars)
        self.assertEqual(paths, ["make", "model", "owners.id", "owners.name", "year"])


class CodeJson(unittest.TestCase):
    def test_array_path(self):
        self.assertEqual(get(data, ["agency"]), ["GSA"])

    def test_key(self):
        self.assertEqual(get(data, "agency"), ["GSA"])

    def test_initial_dot(self):
        self.assertEqual(get(data, ".agency"), ["GSA"])

    def test_initial_empty(self):
        self.assertEqual(get(data, ["", "agency"]), ["GSA"])

    def test_array_item_property(self):
        self.assertEqual(
            get(data, "releases.name", sort=False)[:3],
            ["usasearch", "cron_scripts", "mobile-fu"],
        )

    def test_releases_permissions_licenses_name(self):
        # releases.permissions.licenses.name
        self.assertEqual(
            sorted(list(set(get(data, "releases.permissions.licenses.name")))),
            [
                "CC0 1.0 Universal",
                "PD",
                "agpl-3.0",
                "apache-2.0",
                "bsd-2-clause",
                "bsd-3-clause",
                "cc0-1.0",
                "gpl-2.0",
                "gpl-3.0",
                "lgpl-2.1",
                "mit",
                "mpl-2.0",
                "other",
                "unlicense",
            ],
        )

    def test_delimiters(self):
        # releases.tags (default)
        self.assertEqual(get(data, "releases.tags")[:3], ["GSA", "GSA", "GSA"])

        # wrong seperator
        self.assertEqual(get(data, "releases__tags", delimiter="|"), [])

        # default delimiters
        self.assertEqual(
            get(data, "releases.tags", unique=True)[:3], ["GSA", "gsa", "socialmedia"]
        )
        self.assertEqual(
            get(data, "releases__tags", unique=True)[:3], ["GSA", "gsa", "socialmedia"]
        )

        # releases__tags
        self.assertEqual(
            get(data, "releases__tags", delimiter="__")[:3], ["GSA", "GSA", "GSA"]
        )

    def test_unique(self):
        self.assertEqual(
            get(data, "releases.tags", unique=True)[:4],
            ["GSA", "gsa", "socialmedia", "mobileapps"],
        )

    def test_sort(self):
        self.assertEqual(
            get(data, "releases.tags", sort=True)[:4],
            ["508", "API", "Bing", "DigitalGovSearch"],
        )

    def test_unique_and_sort_together(self):
        self.assertEqual(
            get(data, "releases.tags", sort=True, unique=True)[:3],
            ["508", "API", "Bing"],
        )
        self.assertEqual(
            get(data, "releases.contact.email", sort=True, unique=True)[:3],
            ["cloudmgmt@gsa.gov", "code@gsa.gov", "cto@gsa.gov"],
        )

    def test_list_paths(self):
        self.assertEqual(
            list_paths(data),
            [
                "agency",
                "measurementType.method",
                "releases.contact.email",
                "releases.description",
                "releases.governmentWideReuseProject",
                "releases.homepageURL",
                "releases.laborHours",
                "releases.languages",
                "releases.license",
                "releases.name",
                "releases.openSourceProject",
                "releases.organization",
                "releases.permissions.licenses",  # excluded in sendero.js probably because null treated as an empty object
                "releases.permissions.licenses.URL",
                "releases.permissions.licenses.name",
                "releases.permissions.usageType",
                "releases.repositoryURL",
                "releases.tags",
                "releases.vcs",
                "version",
            ],
        )

    def list_paths_with_delimiter(self):
        self.assertEqual(
            list_paths(data, delimiter="__"),
            [
                "agency",
                "measurementType__method",
                "releases__contact__email",
                "releases__description",
                "releases__governmentWideReuseProject",
                "releases__homepageURL",
                "releases__laborHours",
                "releases__languages",
                "releases__license",
                "releases__name",
                "releases__openSourceProject",
                "releases__organization",
                "releases__permissions__licenses__URL",
                "releases__permissions__licenses__name",
                "releases__permissions__usageType",
                "releases__repositoryURL",
                "releases__tags",
                "releases__vcs",
                "version",
            ],
        )

    def test_list_then_get(self):
        paths = list_paths(data)
        for path in paths:
            self.assertGreaterEqual(len(get(data, path, unique=True)), 1)

    def test_geojson_point(self):
        point = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [125.6, 10.1]},
            "properties": {"name": "Dinagat Islands"},
        }
        self.assertEqual(
            list_paths(point),
            ["geometry.coordinates", "geometry.type", "properties.name", "type"],
        )

    def test_multipoint_geometry(self):
        # from https://www.rfc-editor.org/rfc/rfc7946#appendix-A.4
        multipoint = {
            "type": "MultiPoint",
            "coordinates": [[100.0, 0.0], [101.0, 1.0]],
            "ignore_this": [],  # ignore empty arrays
            "ignore_that": [[], []],  # ignore empty multidimensional arrays
        }
        self.assertEqual(list_paths(multipoint), ["coordinates", "type"])

    def test_clean(self):
        self.assertFalse(None in get(data, "releases.permissions.licenses", clean=True))
        self.assertFalse(None in get(data, "releases.license", clean=True))

    def test_stringify(self):
        self.assertEqual(
            get(data, "releases.laborHours", stringify=True, unique=True), ["0"]
        )
        self.assertEqual(
            get(data, "releases.permissions", stringify=True, unique=True)[:3],
            [
                '{"licenses": null, "usageType": "governmentWideReuse"}',
                '{"licenses": [{"URL": "http://choosealicense.com/licenses/mit/", "name": "mit"}], "usageType": "openSource"}',
                '{"licenses": [{"URL": "http://choosealicense.com/licenses/gpl-3.0/", "name": "gpl-3.0"}], "usageType": "openSource"}',
            ],
        )


if __name__ == "__main__":
    unittest.main()
