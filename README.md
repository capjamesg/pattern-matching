# Pattern Matching

Find a pattern that matches a string.

This project can take a list of strings and find common patterns of words. For example, given the titles:

```
This is a test
This is a coffee
This is a tea
```

This project would return:

```
This is a *
```

Where `*` denotes the presence of any word.

Or, given:

```
This is a test
This isn't a test
This is of course a test
```

The script will return:

```
This * a test
```

This project was designed to find patterns in URL slugs.

## How to Use

To use this project, first clone this repository. Then, create a new Python file and add the code below:

```python
from .patterns import get_patterns, calculate_matches_from_examples

urls = []
top_candidate = max(get_patterns(delimiter = "-").values(), key=len)
matches, _ = calculate_matches_from_examples(top_candidate, urls, delimiter = "-")

print("# of examples: ", len(examples))
print(f"Pattern: {top_candidate}")
print(f"Match rate: {(matches / len(examples)) * 100:.2f}%")

# # of examples:  50
# Pattern: ['*', 'and', '*']
# Match rate: 74.00%
```

Add a value for `urls`, then run the code. You can use any sequence of strings where there is a delimiter. If you use plain text, the delimiter should be a space.

## License

This project is licensed under an [MIT license](LICENSE).
