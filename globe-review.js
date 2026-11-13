(function () {
  /* Official pages and films checked against globe.gov, observer.globe.gov, and YouTube oEmbed.
     Windows Media files are GLOBE's own protocol videos. YouTube films use youtube-nocookie. */
  var VIDEOS = 'https://www.globe.gov/community-resources/learning-and-facilitation-resources/teaching-resources/globe-videos';
  var ETRAIN = 'https://www.globe.gov/get-involved/training/globe-etraining';
  var NGSS = 'https://www.globe.gov/documents/2629866/0/ConnectionsGLOBE_NGSS.pdf';
  var APP = 'https://observer.globe.gov/';
  var CHANNEL = 'https://www.youtube.com/user/globeprogram';
  var TOPICS = [
    {id:'clouds', sphere:'atm', elem:'https://www.globe.gov/web/elementary-globe/overview/clouds',
      page:'https://www.globe.gov/web/atmosphere/protocols/clouds', train:'https://www.globe.gov/get-involved/training/globe-etraining/atmosphere',
      docs:[
        ['https://www.globe.gov/documents/348614/7b79ee82-ebd6-4382-9283-181a412f063f','Clouds protocol PDF'],
        ['https://www.globe.gov/documents/348614/139cd526-ca0b-4192-9659-ad9ee5a5c893','Cloud type field guide'],
        ['https://www.globe.gov/documents/348614/782194b1-b5c3-4416-b3aa-b4a208ea5812','GLOBE cloud chart'],
        ['https://www.globe.gov/documents/348614/624fab53-4159-438e-b974-4a79c402c3cb','Clouds 1-day data sheet'],
        ['https://observer.globe.gov/do-globe-observer/clouds/resource-library','Clouds resource library']
      ],
      films:[
        {yt:'vpYXh3xHoS4', title:'Do You Know that Clouds Have Names?', by:'NASA Video', grades:['k2','g35']},
        {yt:'5kjrPUP9X1g', title:'Make Your Own Cloud (in a Bottle) with #NASAatHome', by:'NASA Video', grades:['k2','g35']},
        {yt:'AhSjFSMC8K0', title:'GLOBE Observer: Clouds - Getting Started - Narrated Version', by:'GLOBE Implementation Office', grades:['k2','g35','g68','g912']},
        {yt:'cZM3PO5hoHU', title:'GLOBE Observer Clouds: Getting Started', by:'NASA GLOBE Observer', grades:['g35','g68','g912']},
        {yt:'dyeOzaPoXiY', title:'Cloud Cover Estimation Activity Demo', by:'GLOBE Implementation Office', grades:['g35','g68','g912']},
        {yt:'FNmjBD52DC4', title:'Satellite Matching', by:'GLOBE Implementation Office', grades:['g68','g912']},
        {file:'https://www.globe.gov/documents/10157/372522/Cloud_Cover_Type.wmv', title:'Cloud Cover and Cloud Type', by:'The GLOBE Program', grades:['g68','g912']}
      ]},
    {id:'airtemp', sphere:'atm',
      page:'https://www.globe.gov/web/atmosphere/protocols/air-temperature', train:'https://www.globe.gov/get-involved/training/globe-etraining/atmosphere',
      docs:[],
      films:[
        {file:'https://www.globe.gov/documents/10157/372522/Max-Min-Current_Temperature.wmv', title:'Air Temperature', by:'The GLOBE Program', grades:['k2','g35','g68','g912']}
      ]},
    {id:'precip', sphere:'atm',
      page:'https://www.globe.gov/web/atmosphere/protocols/precipitation', train:'https://www.globe.gov/get-involved/training/globe-etraining/atmosphere',
      docs:[],
      films:[
        {yt:'46otS0Wjz-E', title:'NASA | Anatomy of a Raindrop', by:'NASA Goddard', grades:['k2','g35','g68','g912']},
        {file:'https://www.globe.gov/documents/10157/372522/Rainfall-Solid_Precipitation-PH.wmv', title:'Precipitation', by:'The GLOBE Program', grades:['g35','g68','g912']}
      ]},
    {id:'watertemp', sphere:'hyd', elem:'https://www.globe.gov/web/elementary-globe/overview/water',
      page:'https://www.globe.gov/web/hydrosphere/protocols/water-temperature', train:'https://www.globe.gov/get-involved/training/globe-etraining/hydrosphere',
      docs:[],
      films:[
        {file:'https://www.globe.gov/documents/10157/372522/Water_Transparency.wmv', title:'Water Transparency and Temperature', by:'The GLOBE Program', grades:['k2','g35','g68','g912']}
      ]},
    {id:'ph', sphere:'hyd', elem:'https://www.globe.gov/web/elementary-globe/overview/water',
      page:'https://www.globe.gov/web/hydrosphere/protocols/ph', train:'https://www.globe.gov/get-involved/training/globe-etraining/hydrosphere',
      docs:[],
      films:[
        {file:'https://www.globe.gov/documents/10157/372522/Water_PH.wmv', title:'Water pH', by:'The GLOBE Program', grades:['g35','g68','g912']}
      ]},
    {id:'mosquito', sphere:'hyd',
      page:'https://www.globe.gov/web/hydrosphere/protocols/mosquito-habitat-mapper', train:'https://www.globe.gov/get-involved/training/globe-etraining/hydrosphere',
      docs:[['https://observer.globe.gov/do-globe-observer/mosquito-habitats','Mosquito Habitats in GLOBE Observer']],
      films:[
        {yt:'2Q0BvgRxxoE', title:'GLOBE Observer: Mosquito Habitat Mapper - Getting Started (Basic) - Narrated Version', by:'GLOBE Implementation Office', grades:['g35','g68','g912']},
        {yt:'Jh_chDc_HCE', title:"GLOBE Observer's Basic Mosquito Habitat Mapper: Getting Started", by:'NASA Goddard', grades:['g35','g68','g912']},
        {yt:'eiIYh2TmuZc', title:'Mosquito Habitats and Hideouts', by:'GLOBE Implementation Office', grades:['k2','g35','g68']},
        {yt:'bPBomfbLpWY', title:'Build a Mosquito Larvae Trap', by:'GLOBE Implementation Office', grades:['g68','g912']}
      ]},
    {id:'soil', sphere:'ped', elem:'https://www.globe.gov/web/elementary-globe/overview/soils',
      page:'https://www.globe.gov/web/soil/protocols/soil-characterization', train:ETRAIN,
      docs:[['https://www.globe.gov/web/soil','Pedosphere (Soil)']],
      films:[
        {file:'https://www.globe.gov/documents/10157/372522/Soil_Char-Field_Measurements.wmv', title:'Soil Characterization - Field Measurements', by:'The GLOBE Program', grades:['g35','g68','g912']}
      ]},
    {id:'landcover', sphere:'bio',
      page:'https://www.globe.gov/web/biosphere/protocols/land-cover-classification', train:'https://www.globe.gov/get-involved/training/globe-etraining/biosphere',
      docs:[['https://observer.globe.gov/do-globe-observer/land-cover/resource-library','Land Cover resource library']],
      films:[
        {yt:'V1n29KHC09s', title:'GLOBE Observer: Land Cover - Getting Started - Narrated Version', by:'GLOBE Implementation Office', grades:['k2','g35','g68','g912']},
        {yt:'PSCEpPlfGMs', title:'GLOBE Observer Land Cover: Getting Started', by:'NASA GLOBE Observer', grades:['g35','g68','g912']},
        {yt:'vHmwHBFHCQE', title:'Why Observe: Land Cover', by:'GLOBE Implementation Office', grades:['g68','g912']},
        {file:'https://www.globe.gov/documents/10157/372522/Land_Cover.wmv', title:'Land Cover - Field Measurements', by:'The GLOBE Program', grades:['g68','g912']}
      ]},
    {id:'trees', sphere:'bio',
      page:'https://www.globe.gov/web/biosphere/protocols/biometry-including-tree-height-', train:'https://www.globe.gov/get-involved/training/globe-etraining/biosphere',
      docs:[
        ['https://observer.globe.gov/do-globe-observer/trees/resource-library','Trees resource library'],
        ['https://www.globe.gov/web/trees-around-the-globe/overview','Trees Around the GLOBE']
      ],
      films:[
        {yt:'DdPXm8Gmsj0', title:'GLOBE Observer: Trees - Introduction - Narrated Version', by:'GLOBE Implementation Office', grades:['k2','g35','g68','g912']},
        {yt:'ZaUxc-AaI4Y', title:'How To Take A Trees Observation', by:'GLOBE Implementation Office', grades:['g35','g68','g912']},
        {yt:'pMV9COMYtSg', title:'GLOBE Observer: Tree Height', by:'GLOBE Implementation Office', grades:['g68','g912']},
        {yt:'Ky6KhGLw1AU', title:'Paper Clinometer Activity Video', by:'GLOBE Implementation Office', grades:['g35','g68','g912']}
      ]},
    {id:'greenup', sphere:'bio',
      page:'https://www.globe.gov/web/biosphere/protocols/green-up-green-down', train:'https://www.globe.gov/get-involved/training/globe-etraining/biosphere',
      docs:[],
      films:[]},
    {id:'observer', sphere:'obs',
      page:APP, train:ETRAIN,
      docs:[
        ['https://observer.globe.gov/do-globe-observer/clouds/resource-library','Clouds'],
        ['https://observer.globe.gov/do-globe-observer/land-cover/resource-library','Land Cover'],
        ['https://observer.globe.gov/do-globe-observer/trees/resource-library','Trees'],
        ['https://observer.globe.gov/do-globe-observer/mosquito-habitats','Mosquito Habitats']
      ],
      films:[
        {yt:'AhSjFSMC8K0', title:'GLOBE Observer: Clouds - Getting Started - Narrated Version', by:'GLOBE Implementation Office', grades:['k2','g35','g68','g912']},
        {yt:'V1n29KHC09s', title:'GLOBE Observer: Land Cover - Getting Started - Narrated Version', by:'GLOBE Implementation Office', grades:['k2','g35','g68','g912']},
        {yt:'DdPXm8Gmsj0', title:'GLOBE Observer: Trees - Introduction - Narrated Version', by:'GLOBE Implementation Office', grades:['k2','g35','g68','g912']},
        {yt:'2Q0BvgRxxoE', title:'GLOBE Observer: Mosquito Habitat Mapper - Getting Started (Basic) - Narrated Version', by:'GLOBE Implementation Office', grades:['g35','g68','g912']}
      ]}
  ];

  var dataEl = document.getElementById('gr-i18n');
  var form = document.getElementById('lb');
  var out = document.getElementById('lb-plan');
  if (!dataEl || !form || !out) return;
  var t = JSON.parse(dataEl.textContent);
  var band = form.querySelector('[name=band]');
  var topic = form.querySelector('[name=topic]');
  var length = form.querySelector('[name=length]');

  var sphere = '', html = '';
  TOPICS.forEach(function (tp) {
    if (tp.sphere !== sphere) {
      if (sphere) html += '</optgroup>';
      sphere = tp.sphere;
      html += '<optgroup label="' + t.spheres[sphere] + '">';
    }
    html += '<option value="' + tp.id + '">' + t.topics[tp.id] + '</option>';
  });
  html += '</optgroup>';
  topic.innerHTML = html;

  function params() {
    var q = new URLSearchParams(location.search);
    return {band: q.get('band') || 'k2', topic: q.get('topic') || 'clouds', length: q.get('len') || 'class'};
  }
  function writeUrl() {
    var q = new URLSearchParams();
    q.set('band', band.value); q.set('topic', topic.value); q.set('len', length.value);
    history.replaceState(null, '', location.pathname + '?' + q.toString());
    var share = document.getElementById('gr-classroom');
    if (share) share.href = 'https://classroom.google.com/share?url=' + encodeURIComponent(location.href);
  }
  function find(id) { for (var i = 0; i < TOPICS.length; i++) if (TOPICS[i].id === id) return TOPICS[i]; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function link(href, label) { return '<a href="' + esc(href) + '" target="_blank" rel="noopener noreferrer">' + esc(label) + '</a>'; }
  function fill(s, name) { return s.replace(/\{name\}/g, name).replace(/\{band\}/g, t.bands[band.value]).replace(/\{length\}/g, t.lengths[length.value]); }

  function filmHref(f) { return f.yt ? ('https://www.youtube.com/watch?v=' + f.yt) : f.file; }
  function filmFor(list, n) { return list[n] || list[0] || null; }
  function videoBlock(title, text, film) {
    var href = film ? filmHref(film) : VIDEOS;
    var label = film ? (film.title + ' — ' + film.by) : href;
    return '<h3>' + esc(title) + '</h3><p>' + text + '</p><p class="lb-small"><a dir="ltr" href="' + esc(href) + '" target="_blank" rel="noopener noreferrer">' + esc(label) + '</a></p>';
  }
  function render() {
    writeUrl();
    var tp = find(topic.value);
    var name = t.topics[tp.id];
    var films = tp.films.filter(function (f) { return f.grades.indexOf(band.value) >= 0; });
    var docs = '<ul><li>' + link(tp.page, t.openProtocol) + '</li>';
    tp.docs.forEach(function (d) { docs += '<li>' + link(d[0], d[1]) + '</li>'; });
    docs += '<li>' + link(tp.train, t.openTrain) + '</li>';
    if ((band.value === 'k2' || band.value === 'g35') && tp.elem) docs += '<li>' + link(tp.elem, t.openElem) + '</li>';
    docs += '<li>' + link(APP, 'GLOBE Observer') + '</li></ul>';
    var ngss = (tp.id === 'clouds' ? t.ngssClouds : t.ngssGeneric) + ' ' + NGSS;
    var steps = fill(t.steps, name).split('|').map(function (step) { return '<li>' + esc(step) + '</li>'; }).join('');
    out.innerHTML =
      '<h2>' + esc(name) + '</h2>' +
      '<p class="lb-meta">' + esc(t.bands[band.value] + ' · ' + t.lengths[length.value]) + '</p>' +
      '<p>' + fill(t.obj, name) + '</p>' +
      '<h3>' + esc(t.objH) + '</h3><ul><li>' + fill(t.obj, name) + '</li></ul>' +
      '<h3>' + esc(t.matH) + '</h3>' + docs +
      '<h3>' + esc(t.stepsH) + '</h3><ol>' + steps + '</ol>' +
      videoBlock(t.vidH, fill(t.filmLead, name), filmFor(films, 0)) +
      videoBlock(t.dataLab, fill(t.dataLead, name), filmFor(films, 1)) +
      videoBlock(t.qLab, fill(t.talkLead, name), filmFor(films, 2)) +
      '<h3>' + esc(t.ngssH) + '</h3><p>' + esc(ngss) + '</p>' +
      '<p class="lb-small">' + esc(t.cite) + '</p><p class="lb-small">' + esc(t.credit) + '</p>';
    out.hidden = false;
  }

  var start = params();
  if (band.querySelector('option[value="' + start.band + '"]')) band.value = start.band;
  if (topic.querySelector('option[value="' + start.topic + '"]')) topic.value = start.topic;
  if (length.querySelector('option[value="' + start.length + '"]')) length.value = start.length;
  writeUrl();
  form.addEventListener('submit', function (e) { e.preventDefault(); render(); });
  function copyText(btn, text) {
    var done = function () { btn.textContent = t.copied; };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, done);
    else done();
  }
  document.getElementById('gr-copy').addEventListener('click', function (e) {
    writeUrl();
    copyText(e.currentTarget, location.href);
  });
  document.getElementById('lb-print').addEventListener('click', function () {
    if (out.hidden) return;
    window.print();
  });
})();
