# app.py
# The single entry point for the whole site.
# Run with:  python app.py
# Then open: http://127.0.0.1:5000

import re

from flask import Flask, render_template, request, jsonify, abort

from story_model import TOPICS, get_story
from quiz import get_quiz_node, QUIZ_DATA  # quiz_data/*.json is already loaded when quiz.py is imported

app = Flask(__name__)


def resolve_quiz_topic_key(topic_param):
    """
    Front-end pages pass a URL-friendly slug (e.g. 'buddhism-jainism'),
    but quiz.py keys its data by the raw quiz_data/<file>.json filename
    (e.g. 'Buddhism___Jainism' - every non-alphanumeric character in the
    display name became its own underscore). Try, in order:
      1. topic_param used as-is (already an exact quiz_data key)
      2. topic_param mapped through SLUG_TO_TOPIC, then converted to the
         underscore filename pattern
    Returns None if nothing matches a loaded topic.
    """
    if not topic_param:
        return None

    if topic_param in QUIZ_DATA:
        return topic_param

    display_name = SLUG_TO_TOPIC.get(topic_param)
    if display_name:
        candidate = re.sub(r"[^A-Za-z0-9]", "_", display_name)
        if candidate in QUIZ_DATA:
            return candidate

    return None


# ---------- page routes ----------
@app.route("/")
def home():
    # index.html - topic menu / map
    return render_template("index.html", topics=list(TOPICS.keys()))


@app.route("/universe.html")
def universe():
    return render_template("universe.html")

@app.route("/simulation.html")
def simulation():
    quiz_slug = request.args.get("quiz")
    quiz_key = resolve_quiz_topic_key(quiz_slug)
    if quiz_slug and not quiz_key:
        return render_template("simulation.html", error=f'No quiz found for "{quiz_slug}"')
    return render_template("simulation.html", quiz_key=quiz_key)

@app.route("/mysteries.html")
def mysteries():
    return render_template("mysteries.html")

@app.route("/map_explorer.html")
def map_explorer():
    return render_template("map_explorer.html")


SLUG_TO_TOPIC = {
    "mughal-empire": "Mughal Empire",
    "delhi-sultanate": "Delhi Sultanate",
    "vijayanagara-empire": "Vijayanagara Empire",
    "chola-empire": "Chola Empire",
    "maratha-empire": "Maratha Empire",
    "rajput-kingdoms": "Rajput Kingdoms",
    "sikh-empire": "Sikh Empire",
    "east-india-company": "British East India Company & Expansion",
    "revolt-1857": "Revolt of 1857",
    "early-nationalism": "Indian National Congress & Early Nationalism",
    "swadeshi-movement": "Swadeshi Movement",
    "gandhian-era": "Gandhian Era & Non-Cooperation Movement",
    "civil-disobedience": "Civil Disobedience & Quit India Movement",
    "independence-partition": "Indian Independence & Partition",
    "indus-valley": "Indus Valley Civilization",
    "vedic-period": "Vedic Period",
    "mahajanapadas": "Mahajanapadas & Rise of Magadha",
    "maurya-empire": "Maurya Empire",
    "gupta-empire": "Gupta Empire",
    "buddhism-jainism": "Buddhism & Jainism",
    "sangam-age": "Sangam Age & Ancient South India",
}

def resolve_quiz_topic_key(topic_param):
    """
    Accepts either a URL slug (e.g. 'buddhism-jainism') or an exact
    quiz_data key already, and returns the real key QUIZ_DATA uses -
    or None if nothing matches.
    """
    if not topic_param:
        return None
    if topic_param in QUIZ_DATA:
        return topic_param
    mapped = SLUG_TO_QUIZ_KEY.get(topic_param)
    if mapped in QUIZ_DATA:
        return mapped
    return None


SLUG_TO_TOPIC = {
    "mughal-empire": "Mughal Empire",
    "delhi-sultanate": "Delhi Sultanate",
    "vijayanagara-empire": "Vijayanagara Empire",
    "chola-empire": "Chola Empire",
    "maratha-empire": "Maratha Empire",
    "rajput-kingdoms": "Rajput Kingdoms",
    "sikh-empire": "Sikh Empire",
    "east-india-company": "British East India Company & Expansion",
    "revolt-1857": "Revolt of 1857",
    "early-nationalism": "Indian National Congress & Early Nationalism",
    "swadeshi-movement": "Swadeshi Movement",
    "gandhian-era": "Gandhian Era & Non-Cooperation Movement",
    "civil-disobedience": "Civil Disobedience & Quit India Movement",
    "independence-partition": "Indian Independence & Partition",
    "indus-valley": "Indus Valley Civilization",
    "vedic-period": "Vedic Period",
    "mahajanapadas": "Mahajanapadas & Rise of Magadha",
    "maurya-empire": "Maurya Empire",
    "gupta-empire": "Gupta Empire",
    "buddhism-jainism": "Buddhism & Jainism",
    "sangam-age": "Sangam Age & Ancient South India",
}

SLUG_TO_QUIZ_KEY = {
    "mughal-empire": "mughal-empire",
    "delhi-sultanate": "Delhi-sultanate",
    "vijayanagara-empire": "Vijayanagara-empire",
    "chola-empire": "chola-empire",
    "maratha-empire": "maratha_empire",
    "rajput-kingdoms": "rajput kingdoms",
    "sikh-empire": "sikh_empire",
    "east-india-company": "British East India Company & Expansion",
    "revolt-1857": "revolt_1857",
    "early-nationalism": "indian_national_congress",
    "swadeshi-movement": "swadeshi_movement",
    "gandhian-era": "Gandhian Era & Non-Cooperation Movement",
    "civil-disobedience": "Civil Disobedience & Quit India Movement",
    "independence-partition": "Indian Independence & Partition",
    "indus-valley": "Indus Valley Civilization",
    "vedic-period": "Vedic Period",
    "mahajanapadas": "Mahajanapadas & Rise of Magadha",
    "maurya-empire": "Maurya Empire",
    "gupta-empire": "Gupta Empire",
    "buddhism-jainism": "Buddhism & Jainism",
    "sangam-age": "Sangam Age & Ancient South India",
}


@app.route("/timeline.html")
def timeline():
    topic_slug = request.args.get("topic")
    era = request.args.get("era")
    topic_display_name = SLUG_TO_TOPIC.get(topic_slug)
    return render_template(
        "timeline.html",
        topic=topic_slug,
        era=era,
        topic_display_name=topic_display_name,
    )

@app.route("/story/<topic>")
def story_page(topic):
    if topic not in TOPICS:
        abort(404)
    # timeline.html - your existing template for showing a single topic;
    # it can call /generate-story and /get-quiz-question via fetch()
    return render_template("timeline.html", topic=topic)


# ---------- JSON API routes (called by your front-end JS) ----------
@app.route("/api/topics")
def api_topics():
    return jsonify(list(TOPICS.keys()))


@app.route("/generate-story", methods=["POST"])
def generate_story_route():
    data = request.json
    topic = data.get("topic")
    if not topic or topic not in TOPICS:
        return jsonify({"error": "Invalid or missing topic"}), 400
    story = get_story(topic)  # hits Wikipedia + Gemini live - can take a few seconds
    return jsonify({"story": story})


@app.route("/get-quiz-question", methods=["POST"])
def get_quiz_question():
    data = request.json
    topic_param = data.get("topic")
    path = data.get("path", "round1")

    quiz_key = resolve_quiz_topic_key(topic_param)
    if not quiz_key:
        return jsonify({
            "error": f'No quiz data found for topic "{topic_param}"',
            "available_topics": list(QUIZ_DATA.keys())
        }), 404

    node = get_quiz_node(quiz_key, path)
    if not node:
        return jsonify({"error": f'Question not found for path "{path}"'}), 404
    return jsonify(node)


if __name__ == "__main__":
    app.run(debug=True)
