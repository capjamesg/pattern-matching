import re
from collections import Counter, OrderedDict, defaultdict

SUBPATH = "train"
DELIMITER = "-"


def longest_common_starting_substring(s1, s2):
    for i, (c1, c2) in enumerate(zip(s1, s2)):
        if c1 != c2:
            return s1[:i]
    return s1[: i + 1]


def get_patterns(examples, delimiter="-"):
    url_components = [r.split(delimiter) for r in examples]

    patterns = [["*" for _ in range(len(url))] for url in url_components]
    patterns = set(map(tuple, patterns))
    patterns = sorted(patterns, key=lambda x: len(x), reverse=False)

    # count # of urls that are same length
    url_length_counter = Counter(map(len, url_components))

    # within each length, find the most common words
    length = max(url_length_counter.keys())
    sequences = defaultdict(Counter)

    for url in url_components:
        if len(url) == length:
            for i in range(len(url)):
                sequences[i][url[i]] += 1

    # print max in each position, remove duplicates
    pattern = []
    for i in range(length):
        pattern.append(sequences[i].most_common(1)[0][0])

    main_pattern = pattern

    # get most common words in total
    total_sequences = Counter()

    for url in url_components:
        for i in range(len(url)):
            total_sequences[url[i]] += 1

    # replace value in pattern with ___ if a sequence is not in 950% of urls
    pattern = ["*"]
    max_iters = 100
    iters = 0

    candidates = OrderedDict()

    # check if all url components are same len
    all_url_same_len = all(len(url) == length for url in url_components)

    while all(pattern[i] == "*" for i in range(len(pattern))) and iters < max_iters:
        threshold = 1 - (0.05 * (iters + 1))

        if threshold < 0.5:
            candidates[1] = ["*"]
            pattern = ["*"]
            break

        pattern = [
            word if (total_sequences[word] / len(examples)) > threshold else "*"
            for word in main_pattern
        ]

        for i in range(len(pattern) - 1):
            if pattern[i] == pattern[i + 1]:
                pattern[i] = "*"

        # skip if all are *
        if all(pattern[i] == "*" for i in range(len(pattern))):
            iters += 1
            continue

        triggered_regex = False
        # if all in url components at idx are same length, add {n} to end
        component_lens = set()

        for url in url_components:
            component_lens.add(len(url[0]))


        for i, item in enumerate(pattern):
            if "*" in item:
                if i > min(url_length_counter.keys()):
                    pattern[i] = "(.*)"
                    continue

                triggered_regex = True
                start = []

                pattern[i] = ""
                print(url_components)
                # if all values are a-z
                matcher = ""
                # min is smallest in a-z order, max is largest
                # get min leter after start
                min_char_after_start = min(url_components[0][i][len(start) :])
                max_char_after_start = max(url_components[1][i][len(start) :])
                any_contains_caps = any(
                    c.isupper() for c in url_components[0][i][len(start) :]
                ) or any(c.isupper() for c in url_components[1][i][len(start) :])
                any_contains_lower = any(
                    c.islower() for c in url_components[0][i][len(start) :]
                ) or any(c.islower() for c in url_components[1][i][len(start) :])

                if min_char_after_start.isdigit() or max_char_after_start.isdigit():
                    smallest_num = min(
                        [
                            int(c)
                            for c in url_components[0][i][len(start) :]
                            if c.isdigit()
                        ]
                    )
                    largest_num = max(
                        [
                            int(c)
                            for c in url_components[1][i][len(start) :]
                            if c.isdigit()
                        ]
                    )
                    matcher = f"{smallest_num}-{largest_num}"

                if any_contains_caps:
                    matcher += "A-Z"
                if any_contains_lower:
                    matcher += "a-z"

                # get all special characters in all values
                special_chars = [
                    [c for c in url_components[x][i][len(start) :] if len(url_components[x]) > i and not c.isalnum()]
                    for x in range(len(url_components))
                ]
                special_chars = [c for sublist in special_chars for c in sublist]
                special_chars = set(special_chars)
                special_chars = "\\".join(special_chars)

                matcher += special_chars
                print(special_chars, matcher)

                matcher = f"[{matcher}]" if matcher else "."
                pattern[i] += matcher

                min_component_len = min(component_lens)
                max_component_len = max(component_lens)

                if min_component_len == max_component_len:
                    pattern[i] += "{" + f"{min_component_len}" + "}"
                else:
                    pattern[i] += "{" + f"{min_component_len},{max_component_len}" + "}"

                # get count of all values at i
                count = Counter(
                    [url_components[x][i] for x in range(len(url_components))]
                )

                # if are < 3 combinations, make (a|b|c) instead
                if len(count) < 3:
                    pattern[i] = "(" + "|".join(count.keys()) + ")"
                else:
                    pattern[i] = "(" + pattern[i] + ")"

        if triggered_regex:
            pattern[0] = "^" + pattern[0]
            pattern[-1] += "$"

        # if long sequence of * is found, remove, and string is not length of longest
        if len(pattern) > 1 and not all_url_same_len:
            for i in range(len(pattern) - 1):
                if pattern[i] == "*" and pattern[i + 1] == "*":
                    pattern[i] = ""

        # remove empty items
        pattern = list(filter(None, pattern))

        candidates[threshold] = pattern

        iters += 1

    return candidates


def calculate_matches_from_examples(pattern, examples, delimiter="-"):
    pattern = delimiter.join(pattern)
    pattern = re.compile(pattern)

    matches = 0
    fails = []

    values_by_wildcard_idx = defaultdict(dict)

    for example in examples:
        match = re.search(pattern, example)

        if match:
            for i, group in enumerate(match.groups()):
                if group not in values_by_wildcard_idx[i]:
                    values_by_wildcard_idx[i][group] = 0
                values_by_wildcard_idx[i][group] += 1
            matches += 1
        else:
            fails.append(example)

    return matches, values_by_wildcard_idx, fails
