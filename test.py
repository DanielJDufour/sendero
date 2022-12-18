import unittest
from sendero import find_paths, list_paths

class PathSetsTests(unittest.TestCase):
  def test_simple(self):
    paths = find_paths({ "a": { "b": "c" }})
    self.assertEqual(paths, {"a.b"})

def test_top_level_array(self):
    paths = find_paths([{ "a": { "b": "c" }}, { "d": { "e": "f" }}])
    self.assertEqual(paths, {"a.b", "d.e"})
  
class ListPathTests(unittest.TestCase):
  def test_list_paths(self):
    paths = list_paths({ "a": { "b": "c" }})
    self.assertEqual(paths, ["a.b"])

  def test_top_level_list(self):
    paths = list_paths([{ "a": { "b": "c" }}, { "d": { "e": "f" }}])
    self.assertEqual(paths, ["a.b", "d.e"])

  def test_nested_array(self):
    paths = list_paths([{ "a": { "b": "c" }}, { "d": { "e": [ { "f": "g" }, { "h": "i" } ] }}])
    self.assertEqual(paths, ["a.b", "d.e.f", "d.e.h"])

class ExampleTest(unittest.TestCase):
  def test_list_paths(self):
    cars = [
      { "make": "Nissan", "model": "Altima", "year": 2022, "owners": [{ "id": 1, "name": "Juan" }, { "id": 2, "name": "Mark" }]},
      { "make": "Nissan", "model": "Kicks", "year": 2021, "owners": [{ "id": 3, "name": "Zach" }]},
      { "make": "Toyota", "model": "Camry", "year": 1995, "owners": [{ "id": 4, "name": "Tom" }]}
    ]
    paths = list_paths(cars)
    self.assertEqual(paths, ["make", "model", "owners.id", "owners.name", "year" ])

if __name__ == "__main__":
    unittest.main()
