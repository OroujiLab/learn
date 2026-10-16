/**
 * Offline smoke test of the synthetic Hi-C lesson.
 * Requires only Node.js built-ins; no browser, network or dependencies.
 */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const source = fs.readFileSync(path.join(__dirname, "../interactives/hic-contact-lab.html"), "utf8");
const script = source.match(/<script>([\s\S]*?)<\/script>/);
assert(script, "inline simulation script must exist");
new vm.Script(script[1], { filename: "hic-contact-lab.js" }); // Syntax check.

let pixels = 0, drawings = 0;
const context2d = {};
for (const fn of ["clearRect", "strokeRect", "beginPath", "moveTo", "lineTo", "stroke",
 "fillText", "save", "restore", "translate", "rotate", "setLineDash"]) context2d[fn] = () => {};
context2d.fillRect = () => { pixels++; };
const registry = {};
function select(id, value = "") {
 const obj = {value, textContent:"", handlers:{}, addEventListener(type, fn){this.handlers[type]=fn}};
 registry[id] = obj;
 return obj;
}
const cv = select("heatmap");
cv.width = 600;
cv.height = 600;
cv.getContext = () => context2d;
cv.getBoundingClientRect = () => ({left:0,top:0,width:600,height:600});
select("resolution", "1");
select("depth", "1");
select("display", "raw");
select("markers", "hide");
select("selection");
select("inspect");
select("low");
select("high");

vm.runInNewContext(script[1], {
 document: {getElementById(id) {assert(registry[id], "Missing element " + id); return registry[id]}},
 Math, Array, Number, String, console
}, {timeout:2500});
assert(pixels > 24*24, "Initial map should render all 24² cells");
const first = pixels;
registry.inspect.handlers.click();
assert.match(registry.selection.textContent, /simulated contact counts/);
assert.match(registry.selection.textContent, /O\/E/);
registry.resolution.value = "4";
registry.resolution.handlers.change();
assert(pixels > first + 6*6, "Coarser matrix should redraw");
registry.markers.value = "show";
registry.markers.handlers.change();
registry.inspect.handlers.click();
assert.match(registry.selection.textContent, /Bins 40–80 kb/); // A 40-kb interval begins at 40 kb.
registry.depth.value = "0.15";
registry.depth.handlers.change();
registry.display.value = "oe";
registry.display.handlers.change();
assert.equal(registry.low.textContent, "Lower O/E");
registry.heatmap.handlers.click({clientX:180,clientY:180});
assert.match(registry.selection.textContent, /simulated contact counts/);
console.log("Hi-C interactive: syntax, rendering, rebinning, depth, O/E and inspection passed.");
