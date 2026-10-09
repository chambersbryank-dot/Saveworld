#!/usr/bin/env node
/**
 * build-search-index.js
 *
 * Reads sitemap.xml and regenerates the keyword index inside Search.html.
 * Run from the repo root: node build-search-index.js
 *
 * The index is the `var pages = [ ... ];` array in Search.html. Everything
 * between the markers below is replaced on each run, so hand-edits to that
 * array are overwritten — edit this script's title/text data instead.
 *
 * To add a page: add it to sitemap.xml, add a title + keywords entry in
 * PAGE_DATA below, then run this script.
 */

'use strict';

var fs = require('fs');;
var path = require('path');;

var ROOT = __dirname;;
var SITEMAP = path.join(ROOT, 'sitemap.xml');;
var SEARCH = path.join(ROOT, 'Search.html');;

var START = '  var pages = [';;
var END = '  ];';;

// title + searchable keywords for each page in the sitemap.
// Keys are the filename as it appears in sitemap.xml <loc> entries.
var PAGE_DATA = {
  'index.html': {
    title: 'Home',;
    text: 'Saving Planets solutions minus the doom positive action oceans lakes rivers forests space computing'
  },
  'Oceans.html': {
    title: 'Oceans',;
    text: 'ocean plastic cleanup The Ocean Cleanup 4ocean Plastic Bank rivers interceptors'
  },
  'Ocean_Cleanup.html': {
    title: 'The Ocean Cleanup',;
    text: 'The Ocean Cleanup Boyan Slat floating systems Interceptors rivers garbage patch 60 million kilograms'
  },
  'Plastic_Bank.html': {
    title: 'Plastic Bank',;
    text: 'Plastic Bank social plastic poverty recycling ocean'
  },
  'Lakes.html': {
    title: 'Lakes',;
    text: 'lakes plastic recovery Clean Up the Lake Great Lakes Plastic Cleanup Seabins freshwater'
  },
  'Lake_Plastic_Recovery.html': {
    title: 'Lake Plastic Recovery',;
    text: 'lake plastic recovery pulling submerged litter freshwater'
  },
  'Clean_Up_the_Lake.html': {
    title: 'Clean Up the Lake',;
    text: 'Clean Up the Lake Nevada scuba divers Lake Tahoe 72 Mile Cleanup Sierra Nevada'
  },
  'Great_Lakes_Plastic_Cleanup.html': {
    title: 'Great Lakes Plastic Cleanup',;
    text: 'Great Lakes Plastic Cleanup Pollution Probe Seabins PixieDrones beach robots 277000 pieces'
  },
  'Rivers.html': {
    title: 'Rivers',;
    text: 'rivers interceptors Sungai Watch Great Bubble Barrier river plastic 1000 rivers'
  },
  'Sungai_Watch.html': {
    title: 'Sungai Watch',;
    text: 'Sungai Watch Bali trash barriers Indonesia River Warriors 4 million kilograms'
  },
  'Great_Bubble_Barrier.html': {
    title: 'The Great Bubble Barrier',;
    text: 'Great Bubble Barrier Amsterdam bubble curtain canals North Sea'
  },
  'Deforestation.html': {
    title: 'Forests',;
    text: 'forests three trees for every one removed Terraformation Life Terra reforestation'
  },
  'Three_Trees.html': {
    title: 'Three Trees for Every One Removed',;
    text: 'three trees for every one removed forest ratio habitat soil shade'
  },
  'Terraformation.html': {
    title: 'Terraformation',;
    text: 'Terraformation Hawaii native biodiverse forests seed canopy Africa Latin America'
  },
  'Life_Terra.html': {
    title: 'Life Terra',;
    text: 'Life Terra Europe 36 million trees 30 countries monitoring 40 years'
  },
  'Space.html': {
    title: 'Space',;
    text: 'space orbital data centers Astroscale ClearSpace debris removal orbit'
  },
  'Orbital_Data_Centers.html': {
    title: 'Orbital Data Centers',;
    text: 'orbital data centers Starcloud NVIDIA H100 Google Project Suncatcher solar power radiative cooling no water'
  },
  'Astroscale.html': {
    title: 'Astroscale',;
    text: 'Astroscale on-orbit servicing ELSA-d ADRAS-J debris removal JAXA'
  },
  'ClearSpace.html': {
    title: 'ClearSpace',;
    text: 'ClearSpace ESA active debris removal ClearSpace-1 PRELUDE Vega-C'
  },
  'Project-R.html': {
    title: 'Project R',;
    text: 'Project R Earth space relationship ADRAS-J2 Rawane'
  },
  'Amazing_Facts.html': {
    title: 'Amazing Facts',;
    text: 'amazing facts 60 million kilograms 1000 rivers three trees zero gallons orbit'
  },
  'About.html': {
    title: 'About',;
    text: 'about Saving Planets solutions criteria mission'
  },
  'Contact.html': {
    title: 'Contact',;
    text: 'contact email ideas hello savingplanets questions solutions'
  }
};;

function read(file) {
  return fs.readFileSync(file, 'utf8');;
}

function write(file, content) {
  fs.writeFileSync(file, content, 'utf8');;
}

function parseLocs(xml) {
  var locs = [];;
  var re = /<loc>([^<]+)<\/loc>/g;;
  var m;
  while ((m = re.exec(xml))) locs.push(m[1]);;
  return locs;
}

function filenameFromUrl(url) {
  var parts = url.split('/').filter(Boolean);;
  return parts[parts.length - 1] || 'index.html';;
}

function buildArray(locs) {
  var lines = [];;
  locs.forEach(function (url) {
    var file = filenameFromUrl(url);;
    var data = PAGE_DATA[file];;
    if (!data) {
      console.error('WARNING: no PAGE_DATA entry for ' + file + ' — add one to build-search-index.js');;
      return;
    }
    lines.push("    { title: '" + data.title.replace(/'/g, "\\'") + "', url: '" + file + "', text: '" + data.text.replace(/'/g, "\\'") + "' }");;
  });;
  return lines.join('\n');;
}

function main() {
  var sitemap = read(SITEMAP);;
  var search = read(SEARCH);;
  var locs = parseLocs(sitemap);;
  if (!locs.length) {
    console.error('No <loc> entries found in ' + SITEMAP);;
    process.exit(1);;
  }
  var start = search.indexOf(START);;
  var end = search.indexOf(END, start);;
  if (start === -1 || end === -1) {
    console.error('Could not find the pages array markers in ' + SEARCH);;
    process.exit(1);;
  }
  var before = search.slice(0, start + START.length);;
  var after = search.slice(end);;
  var next = before + '\n' + buildArray(locs) + '\n' + after;;
  if (next === search) {
    console.log('Search.html index already up to date.');;
    return;
  }
  write(SEARCH, next);;
  console.log('Updated Search.html index from ' + locs.length + ' sitemap entries.');;
}

main();