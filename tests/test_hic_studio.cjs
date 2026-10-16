"use strict";
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");

for (const filename of ["hic-feature-lab.html", "hic-sample-compare.html"]) {
 const src = fs.readFileSync(path.join(__dirname,"../interactives",filename),"utf8");
 const match = src.match(/<script>([\s\S]*?)<\/script>/i);
 assert.ok(match, "Missing script in "+filename);
 assert.doesNotThrow(()=>new vm.Script(match[1],{filename}), filename+" has invalid JavaScript");
 assert.match(src,/synthetic|conceptual/i);
 assert.match(src,/aria-live="polite"/);
}
const atlas = fs.readFileSync(path.join(__dirname,"../lessons/hic-structures.qmd"),"utf8");
const compare = fs.readFileSync(path.join(__dirname,"../lessons/comparing-hic-samples.qmd"),"utf8");
assert.match(atlas,/hic-feature-lab.html/);
assert.match(compare,/hic-sample-compare.html/);
console.log("New Hi-C interactives: script syntax, embedded references and feedback containers validated.");
