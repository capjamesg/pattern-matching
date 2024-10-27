# Pattern Matching

```python
from .patterns import get_patterns, calculate_matches_from_examples

urls = []
top_candidate = max(get_patterns().values(), key=len)
examples = urls

matches, _ = calculate_matches_from_examples(top_candidate, examples)

print("# of examples: ", len(examples))
print(f"Pattern: {top_candidate}")
print(f"Match rate: {(matches / len(examples)) * 100:.2f}%")
```

## License

This project is licensed under an [MIT license](LICENSE).
