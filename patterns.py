import re
from collections import defaultdict, Counter, OrderedDict

SUBPATH = "train"
DELIMITER = "-"

def get_patterns(examples, delimiter = "-"):
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
        threshold = 1 - (0.05 * (iters + 1)) + 0.05

        if threshold < 0.5:
            candidates[1] = ["*"]
            pattern = ["*"]
            break
        
        pattern = [word if (total_sequences[word] / len(examples))
                    > threshold
                    else "*" for word in main_pattern]

        for i in range(len(pattern) - 1):
            if pattern[i] == pattern[i + 1]:
                pattern[i] = "*"

        # skip if all are *
        if all(pattern[i] == "*" for i in range(len(pattern))):
            iters += 1
            continue

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

def calculate_matches_from_examples(pattern, examples, delimiter = "-"):
    pattern = delimiter.join([f"{word}" if word != "*" else "(.*)" for word in pattern]).strip()

    pattern = re.compile(pattern)
    matches = 0

    values_by_wildcard_idx = defaultdict(lambda: defaultdict(int))

    for example in examples:
        match = re.search(pattern, example)

        if match:
            for i, group in enumerate(match.groups()):
                values_by_wildcard_idx[i][group] += 1
            matches += 1

    value_types_by_wildcard_idx = defaultdict(set)

    for i, values in values_by_wildcard_idx.items():
        for value in values:
            if value.isdigit():
                value_types_by_wildcard_idx[i].add(int)
            else:
                value_types_by_wildcard_idx[i].add(type(value))

    return matches, values_by_wildcard_idx
