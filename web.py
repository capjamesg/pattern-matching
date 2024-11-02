from flask import Flask, jsonify, render_template, request

from patterns import calculate_matches_from_examples, get_patterns

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pattern = request.form.get("pattern")
        delimiter = request.form.get("delimiter")

        if pattern:
            data = request.form.get("data1")
        else:
            data = request.form.get("data")

        data = [i.strip() for i in data.split("\n")][:5000]

        if not pattern:
            top_candidate = max(
                get_patterns(data, delimiter=delimiter).values(), key=len
            )
            tab = "calculate"
        else:
            top_candidate = pattern.split(delimiter)
            tab = "run"

        matches, results, fails = calculate_matches_from_examples(
            top_candidate, data, delimiter=delimiter
        )

        return render_template(
            "index.html",
            data="\n".join(data),
            pattern=delimiter.join(top_candidate),
            match_rate=(matches / len(data)) * 100,
            results=results,
            tab=tab,
            fails=fails,
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
