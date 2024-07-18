# sendero
Data Filtering for Humans

## why sendero?
"sendero" means footpath in Spanish

## install
```bash
pip install sendero
```

## basic usage
```python
# in JSON-compatible format
data = {
  "agency": "GSA",
  "measurementType": {
    "method": "modules"
  },
  "version": "2.0.0",
  "releases": [
    {
      "name": "usasearch",
      "description": "System now maintained in open repo https://github.com/GSA/search-gov.",
      "permissions": {
        "licenses": None,
        "usageType": "governmentWideReuse"
      },
      "tags": [
        "GSA"
      ]
    },
    # ...
  ]
}
```

```python
from sendero import list_paths, get

list_paths(data, 'agency')
[
    "agency",
    "measurementType.method",
    "releases.contact.email",
    "releases.description",
    # ...
]

get(data, 'agency')
["GSA"]

# get nested properties using dot syntax
get(data, 'releases.permissions.licenses.name')
["CC0 1.0 Universal", "PD", "agpl-3.0", ... ]

# get nested properties using double underscore syntax
get(data, 'releases__permissions__licenses__name')
["CC0 1.0 Universal", "PD", "agpl-3.0", ... ]
```

# advanced usage
## clean
Filter out None and empty strings.
```python
from sendero import get

# dirty
get(data, "releases.license", clean=False)
[ null, 'https://creativecommons.org/publicdomain/zero/1.0', None, None, ... ]

# clean
get(data, "releases.license", clean=True)
[ 'https://creativecommons.org/publicdomain/zero/1.0', 'https://github.com/GSA/open.gsa.gov/blob/gh-pages/TERMS.md', ... ]
```

## unique
If you only want unique results returned:
```python
# default
get(data, 'releases.tags')
["GSA", "GSA", "GSA", ...]

# uniques only
get(data, 'releases.tags', unique=True)
["GSA","gsa","socialmedia", "mobileapps", ...]
```

## sort
If you want your results sorted
```python
get(data, 'releases.tags', sort=True)
["508", "API", "Bing", "DigitalGovSearch", ...]
```

## delimiter
By default, sendero tries syntax where the steps are separted by
`"."` or `"__"`.  If you'd like to restrict the syntax or use a custom delimiter:
```python
get(data, 'releases--tags', delimiter='--')

# accepts releases--tags and releases__tags
get(data, 'releases--tags', delimiter=['--', '__'])
```

## stringify
```python
# converts numbers to strings
get(data, "releases.laborHours", stringify=True, unique=True)
["0", "200", "12345" ]

# convert objects to JSON strings
get(data, "releases.permissions", stringify=True, unique=True)
[
  '{"licenses":null,"usageType":"governmentWideReuse"}',
  '{"licenses":[{"URL":"http://choosealicense.com/licenses/mit/","name":"mit"}],"usageType":"openSource"}',
  '{"licenses":[{"URL":"http://choosealicense.com/licenses/gpl-3.0/","name":"gpl-3.0"}],"usageType":"openSource"}',
  '{"licenses":null,"usageType":"openSource"}',
  # ...
]
```