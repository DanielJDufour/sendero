import json


def _stringify(it):
    if isinstance(it, str):
        return it
    elif isinstance(it, int) or isinstance(it, float):
        return str(it)
    else:
        return json.dumps(it)


def get(
    data,
    path,
    delimiter=[".", "__"],
    clean=False,
    sort=False,
    stringify=False,
    unique=False,
):
    if isinstance(path, str):
        if isinstance(delimiter, str):
            seps = [delimiter]
        elif isinstance(delimiter, list):
            seps = delimiter
        else:
            seps = [delimiter]

        if len(seps) > 1:
            results = []
            for sep in seps:
                split = path.lstrip(sep).split(sep)
                subresults = get(
                    data,
                    split,
                    delimiter=delimiter,
                    clean=clean,
                    sort=sort,
                    stringify=stringify,
                    unique=unique,
                )
                if len(subresults) > len(results):
                    results = subresults
            return results
        elif len(seps) == 1:
            sep = seps[0]
            path = path.lstrip(sep).split(sep)
    else:
        path = [it for it in path]  # clone
        if len(path) >= 1 and path[0] == "":
            path.pop(0)  # remove initial blank string

    previous = [data]
    while len(path) > 0:
        active = []
        key = path.pop(0)
        for obj in previous:
            if isinstance(obj, list) or isinstance(obj, dict):
                if isinstance(obj, list):
                    for item in obj:
                        if key in item:
                            value = item[key]
                            if isinstance(value, list):
                                active += value
                            else:
                                active.append(value)
                elif isinstance(obj, dict):
                    if key in obj:
                        value = obj[key]
                        if isinstance(value, list):
                            active += value
                        else:
                            active.append(value)
        previous = active

    results = previous

    if clean:
        results = [it for it in results if it != None and it != ""]

    if unique or sort or stringify:
        results = [[it, _stringify(it)] for it in results]

        # sort results by string version
        if sort:
            results = sorted(results, key=lambda it: it[1])

        if unique:
            final_results = []
            unique_strings = set()
            for item, item_string in results:
                if item_string not in unique_strings:
                    unique_strings.add(item_string)
                    final_results.append([item, item_string])
            results = final_results

        results = [str if stringify else it for it, str in results]

    return results


def find_paths(obj, prev="", delim="."):
    paths = set()
    if isinstance(obj, list):
        for item in obj:
            found = find_paths(item, prev=prev + delim if prev else "", delim=delim)
            if len(found) == 0:
                if isinstance(item, list) and len(item) > 0:
                    if prev:
                        paths.add(prev)
            else:
                paths |= found
    elif isinstance(obj, dict):
        for key, value in obj.items():
            next_prev = (prev + delim if prev else "") + key
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, list):
                        if len(item) >= 1:
                            found = find_paths(item, prev=next_prev, delim=delim)
                            if len(found) == 0:
                                paths.add(next_prev)
                            else:
                                paths |= found
                    elif isinstance(item, dict):
                        paths |= find_paths(item, prev=next_prev, delim=delim)
                    else:
                        paths.add(next_prev)
            elif isinstance(value, dict):
                paths |= find_paths(value, prev=next_prev, delim=delim)
            else:
                paths.add(next_prev)

    return paths


def list_paths(obj, prev="", delim="."):
    return sorted(list(find_paths(obj, prev=prev, delim=delim)))
