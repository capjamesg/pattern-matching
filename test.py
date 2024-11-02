from patterns import get_patterns, calculate_matches_from_examples

urls = ["tea-is-gr.eat", "tea-is-good", "tea-is-cool"]
top_candidate = max(get_patterns(urls, delimiter = "-").values(), key=len)
matches, _ = calculate_matches_from_examples(top_candidate, urls, delimiter = "-")

import re
top_candidate = "-".join(top_candidate)
print(re.match(top_candidate, "tea-is-great"))

# print("# of examples: ", len(examples))
# print(f"Pattern: {top_candidate}")
# print(f"Match rate: {(matches / len(examples)) * 100:.2f}%")