#!/usr/bin/env python3
"""Oracle mirror of engine.js for Caulk math. Writes expected.json (with trailing newline)."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10

def jsnum(x):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return x

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)

def beadPlan(lengthM, widthMm, depthMm):
    if not (lengthM > 0) or not (widthMm > 0) or not (depthMm > 0):
        return {"error": "all bead inputs must be positive"}
    ml = lengthM * widthMm * depthMm
    withWaste = ml * 1.1
    tubes = math.ceil(withWaste / 300)
    return {"lengthM": jsnum(float(lengthM)), "widthMm": jsnum(float(widthMm)), "depthMm": jsnum(float(depthMm)),
            "ml": jsnum(r1(ml)), "withWasteMl": jsnum(r1(withWaste)), "tubes": tubes}

def jointPlan(widthM, heightM, count):
    if not (widthM > 0) or not (heightM > 0) or not (count > 0):
        return {"error": "opening size and count must be positive"}
    if count != math.floor(count + 0.5):
        return {"error": "opening count must be a whole number"}
    perOpening = 2 * (widthM + heightM)
    return {"widthM": jsnum(float(widthM)), "heightM": jsnum(float(heightM)), "count": jsnum(float(count)),
            "perOpeningM": jsnum(r1(perOpening)), "totalM": jsnum(r1(perOpening * count))}

def curePlan(depthMm):
    if not (depthMm > 0):
        return {"error": "bead depth must be positive"}
    return {"depthMm": jsnum(float(depthMm)), "minDays": jsnum(r1(depthMm / 3)), "maxDays": jsnum(r1(depthMm / 2))}

def renderBead(r):
    return (fmt(r["lengthM"]) + " m of " + fmt(r["widthMm"]) + " x " + fmt(r["depthMm"]) + " mm bead is " + fmt(r["ml"]) +
            " ml - with the labeled 10% waste allowance that is " + fmt(r["withWasteMl"]) + " ml, so " + str(r["tubes"]) +
            " labeled 300 ml tube" + ("" if r["tubes"] == 1 else "s") + ".")

def renderJoint(r):
    return (fmt(r["count"]) + " opening" + ("" if r["count"] == 1 else "s") + " of " + fmt(r["widthM"]) + " x " +
            fmt(r["heightM"]) + " m " + ("gives " if r["count"] == 1 else "give ") + fmt(r["totalM"]) + " m of joint to seal (labeled four-sided perimeter).")

def renderCure(r):
    return ("A " + fmt(r["depthMm"]) + " mm bead cures through in about " + fmt(r["minDays"]) + "-" + fmt(r["maxDays"]) +
            " days on the labeled 2-3 mm a day rule - cold rooms take longer.")

CASES = []
def add(fn, args): CASES.append({"fn": fn, "args": args})

for a in [(12, 5, 5), (7.5, 6, 4), (3, 4, 6), (25, 5, 5), (1.5, 3, 3), (8, 6, 6), (0.5, 10, 8), (30, 8, 6), (2, 5, 5), (0, 5, 5), (12, 0, 5), (12, 5, -3)]:
    add("beadPlan", list(a))
for a in [(1.2, 1.5, 3), (0.9, 2.1, 1), (1.5, 1.5, 4), (2, 1, 2), (0.6, 0.6, 6), (1, 2.1, 2.5), (1.2, 1.5, 0), (0, 1.5, 3), (1.2, -1, 3), (1, 1, 1), (0.8, 1.2, 5)]:
    add("jointPlan", list(a))
for a in [(5,), (3,), (6,), (2,), (10,), (4,), (8,), (12,), (1.5,), (0,), (-5,), (7,)]:
    add("curePlan", list(a))

out = []
for c in CASES:
    fn = {"beadPlan": beadPlan, "jointPlan": jointPlan, "curePlan": curePlan}[c["fn"]]
    res = fn(*c["args"])
    is_err = "error" in res
    if is_err:
        render = res["error"]
    else:
        render = {"beadPlan": renderBead, "jointPlan": renderJoint, "curePlan": renderCure}[c["fn"]](res)
    out.append({"fn": c["fn"], "args": c["args"], "result": res, "render": render, "isError": is_err})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
print("wrote", len(out), "cases")
