# Caulk math

How much sealant the joint really takes, how many tubes to buy, and how long the bead needs to cure. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/caulkmath/

## The three tools

- **Bead plan** - `beadPlan(lengthM, widthMm, depthMm)`: 1 m of 1 x 1 mm bead is exactly 1 ml; adds the labeled 10% waste allowance and rounds up to labeled 300 ml tubes.
- **Joint plan** - `jointPlan(widthM, heightM, count)`: four-sided perimeter per opening, times the count.
- **Cure plan** - `curePlan(depthMm)`: labeled 2-3 mm a day cure rule, as a day range.

## Labeled norms (illustrative references, not rules)

- Tube size: 300 ml. Waste allowance: 10% for the gun, nozzle and starts/stops.
- Cure rule: about 2-3 mm of cure a day for silicone-type sealants, slower in cold rooms.
- Joint model: four-sided perimeter per opening.

Check the tube's own datasheet for cure and coverage claims.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (35 cases, 105 checks)

Regenerate the oracle expectations: `python3 oracle.py`
