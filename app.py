from flask import Flask, render_template, request, jsonify
import itertools, time

app = Flask(__name__)

PRODUCTS = [
    {"name":"Headphones","sales":120000,"margin":25},
    {"name":"Smartwatch","sales":180000,"margin":18},
    {"name":"Backpack","sales":90000,"margin":35},
    {"name":"Keyboard","sales":110000,"margin":30},
]
SEGMENTS = [
    {"name":"Students","interest":"Accessories","conversion":8},
    {"name":"Gamers","interest":"Electronics","conversion":12},
    {"name":"Professionals","interest":"Premium products","conversion":6},
    {"name":"Families","interest":"General products","conversion":5},
]
CHANNELS = [
    {"name":"Instagram","cost":20000,"reach":40000},
    {"name":"YouTube","cost":30000,"reach":70000},
    {"name":"Email","cost":5000,"reach":15000},
    {"name":"Search ads","cost":25000,"reach":50000},
]
DISCOUNTS = [5, 10, 15]

def campaign_score(p, s, c, d):
    # A transparent simulated business score for the demo.
    fit = 1.0
    if p == "Headphones" and s == "Gamers": fit = 1.22
    elif p == "Keyboard" and s == "Gamers": fit = 1.12
    elif p == "Backpack" and s == "Students": fit = 1.18
    elif p == "Smartwatch" and s == "Professionals": fit = 1.10
    discount_factor = 1 + (d * 0.018)
    channel_factor = {"Instagram":1.00,"YouTube":1.08,"Email":0.82,"Search ads":1.04}[c]
    prod = next(x for x in PRODUCTS if x["name"]==p)
    seg = next(x for x in SEGMENTS if x["name"]==s)
    ch = next(x for x in CHANNELS if x["name"]==c)
    revenue = prod["sales"] * (1 + seg["conversion"]/100) * fit * discount_factor * channel_factor
    revenue -= (ch["cost"] + d*800)
    return round(revenue)

def best_strategy():
    best = None
    for p,s,c,d in itertools.product(
        [x["name"] for x in PRODUCTS],
        [x["name"] for x in SEGMENTS],
        [x["name"] for x in CHANNELS],
        DISCOUNTS):
        ch = next(x for x in CHANNELS if x["name"]==c)
        if ch["cost"] + d*800 <= 50000:
            score = campaign_score(p,s,c,d)
            if best is None or score > best["score"]:
                best = {"product":p,"segment":s,"channel":c,"discount":d,"score":score}
    return best

@app.route("/")
def index():
    return render_template("index.html",
        products=PRODUCTS, segments=SEGMENTS, channels=CHANNELS, discounts=DISCOUNTS)

@app.post("/api/score")
def score():
    data = request.json
    try:
        score = campaign_score(data["product"], data["segment"], data["channel"], int(data["discount"]))
        return jsonify(ok=True, score=score)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 400

@app.get("/api/agent")
def agent():
    b = best_strategy()
    steps = [
        ("🎯","Goal received","Maximize expected weekend revenue under ₹50,000."),
        ("🗂️","Query sales database","Comparing product sales and margins."),
        ("👥","Query customer analytics","Matching products to high-conversion segments."),
        ("💰","Check campaign costs","Filtering strategies within budget."),
        ("🧮","Run simulator","Testing feasible product × segment × channel × discount combinations."),
        ("🔄","Evaluate alternatives","Selecting the highest expected outcome."),
        ("✅","Complete","Best strategy selected.")
    ]
    return jsonify(ok=True, strategy=b, steps=steps)

@app.post("/api/finalize")
def finalize():
    data = request.json
    b = best_strategy()
    human_score = campaign_score(data["product"], data["segment"], data["channel"], int(data["discount"]))
    return jsonify(ok=True, human=human_score, ai=b["score"], ai_strategy=b)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
