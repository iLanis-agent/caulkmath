/* Caulk math engine - pure arithmetic, every borrowed number labeled. */
(function (root) {
  "use strict";
  function r1(x) { return Math.round(x * 10) / 10; }

  function beadPlan(lengthM, widthMm, depthMm) {
    if (!(lengthM > 0) || !(widthMm > 0) || !(depthMm > 0)) return { error: "all bead inputs must be positive" };
    var ml = lengthM * widthMm * depthMm;
    var withWaste = ml * 1.1;
    var tubes = Math.ceil(withWaste / 300);
    return { lengthM: lengthM, widthMm: widthMm, depthMm: depthMm, ml: r1(ml), withWasteMl: r1(withWaste), tubes: tubes };
  }

  function jointPlan(widthM, heightM, count) {
    if (!(widthM > 0) || !(heightM > 0) || !(count > 0)) return { error: "opening size and count must be positive" };
    if (count !== Math.round(count)) return { error: "opening count must be a whole number" };
    var perOpening = 2 * (widthM + heightM);
    return { widthM: widthM, heightM: heightM, count: count, perOpeningM: r1(perOpening), totalM: r1(perOpening * count) };
  }

  function curePlan(depthMm) {
    if (!(depthMm > 0)) return { error: "bead depth must be positive" };
    return { depthMm: depthMm, minDays: r1(depthMm / 3), maxDays: r1(depthMm / 2) };
  }

  function renderBead(r) {
    return r.lengthM + " m of " + r.widthMm + " x " + r.depthMm + " mm bead is " + r.ml + " ml - with the labeled 10% waste allowance that is " + r.withWasteMl + " ml, so " + r.tubes + " labeled 300 ml tube" + (r.tubes === 1 ? "" : "s") + ".";
  }

  function renderJoint(r) {
    return r.count + " opening" + (r.count === 1 ? "" : "s") + " of " + r.widthM + " x " + r.heightM + " m " + (r.count === 1 ? "gives" : "give") + " " + r.totalM + " m of joint to seal (labeled four-sided perimeter).";
  }

  function renderCure(r) {
    return "A " + r.depthMm + " mm bead cures through in about " + r.minDays + "-" + r.maxDays + " days on the labeled 2-3 mm a day rule - cold rooms take longer.";
  }

  var api = { beadPlan: beadPlan, jointPlan: jointPlan, curePlan: curePlan, renderBead: renderBead, renderJoint: renderJoint, renderCure: renderCure };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.CaulkMath = api;
})(typeof window !== "undefined" ? window : this);
