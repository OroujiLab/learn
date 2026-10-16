"use strict";
const fs=require("node:fs"),path=require("node:path"),vm=require("node:vm"),assert=require("node:assert/strict");
const file=fs.readFileSync(path.join(__dirname,"../interactives/genome-track-studio.html"),"utf8");
const match=file.match(/<script>([\s\S]*?)<\/script>/);
assert(match,"Missing inline code");new vm.Script(match[1],{filename:"genome-track-studio.js"});
assert.match(file,/File API|f\.text|file\.text/);
assert.match(file,/bigwig|\.bw/i);
assert.match(file,/gosling\.embed/);
console.log("Genome Track Studio JavaScript syntax and data-boundary documentation checks passed.");

assert.match(file,/function previewGosling\(/,"Offline schematic must exist");
assert.match(file,/function activateGosling\(/,"Optional live Gosling bridge must exist");
assert.match(file,/Gosling 1\.0\.6/,"Pinned Gosling dependency must be documented");
assert.doesNotMatch(file,/@0\.12\.3/,"Legacy broken CDN reference should be gone");
assert.match(file,/External Gosling scripts are blocked/,"Friendly offline fallback is required");
