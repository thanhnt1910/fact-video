// ===== ARCH3D ENGINE v1 — 3D diorama of traditional / historic architecture, driven by window.SPEC =====
// Kit: curved Vietnamese tile roofs (1 or 2 tiers), halls, tam-quan gates, Khue Van Cac pavilion, walls, stelae on tortoises,
// reflecting ponds, trees, houses, walking people, birds. Tilt-shift + soft shadows for a miniature (sa bàn) look.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { FXAAPass } from 'three/addons/postprocessing/FXAAPass.js';
import { HorizontalTiltShiftShader } from 'three/addons/shaders/HorizontalTiltShiftShader.js';
import { VerticalTiltShiftShader } from 'three/addons/shaders/VerticalTiltShiftShader.js';
import { Reflector } from 'three/addons/objects/Reflector.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

try {
await document.fonts.load('700 100px "Noto Serif CJK SC"');
const S = window.SPEC, WD = S.world || {};
const W = S.size[0], H = S.size[1], FPS = S.fps || 30, Q = S.quality || {};
let acc = 0; S.shots.forEach(s => { s.t0 = acc; acc += s.dur; s.t1 = acc; });
const DUR = acc;
const LOG = { fire: [], splash: [], arrows: [], ignite: [] }; window.LOG = LOG;

// ---------- utils ----------
let seed = S.seed || 12345;
function rnd() { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
const R = (a, b) => a + (b - a) * rnd();
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const lerp3 = (a, b, t) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
const ss = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
const EASE = { linear: u => u, inout: u => u * u * (3 - 2 * u), out: u => 1 - (1 - u) * (1 - u), in: u => u * u, accel: u => 1 - Math.pow(1 - u, 1.6) };
const inRect = (x, z, r, m = 0) => x > r[0] - m && x < r[2] + m && z > r[1] - m && z < r[3] + m;

// ---------- renderer ----------
const host = document.getElementById('stage');
const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true, logarithmicDepthBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H, false);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = Q.exposure || 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; renderer.shadowMap.autoUpdate = false;
host.appendChild(renderer.domElement);
const ov = document.createElement('canvas'); ov.width = W; ov.height = H; host.appendChild(ov);
const ctx = ov.getContext('2d');

const scene = new THREE.Scene();
const HAZE = new THREE.Color(...(WD.haze || [0.78, 0.74, 0.66]));
scene.fog = new THREE.FogExp2(HAZE, WD.fog || 0.0022);
const camera = new THREE.PerspectiveCamera(45, W / H, 0.5, 9000);
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType }));
composer.addPass(new RenderPass(scene, camera));
const tiltH = new ShaderPass(HorizontalTiltShiftShader), tiltV = new ShaderPass(VerticalTiltShiftShader);
composer.addPass(tiltH); composer.addPass(tiltV);
composer.addPass(new OutputPass()); composer.addPass(new FXAAPass());

// ---------- textures ----------
function canvasTex(w, h, draw, rep) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  if (rep) t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
}
const noise = (g, w, h, n, cols, a) => { for (let i = 0; i < n; i++) { g.fillStyle = cols[i % cols.length].replace('A', (Math.random() * a).toFixed(3)); g.fillRect(Math.random() * w, Math.random() * h, 1 + Math.random() * 3, 1 + Math.random() * 3); } };
const TEX = {
  tile: canvasTex(128, 64, (g, w, h) => { g.fillStyle = '#6e3524'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 8; i++) { const x = i * w / 8, gr = g.createLinearGradient(x, 0, x + w / 8, 0);
      gr.addColorStop(0, 'rgba(25,8,4,0.55)'); gr.addColorStop(0.35, 'rgba(160,80,55,0.35)'); gr.addColorStop(0.6, 'rgba(120,50,30,0.1)'); gr.addColorStop(1, 'rgba(25,8,4,0.55)'); g.fillStyle = gr; g.fillRect(x, 0, w / 8, h); }
    for (let j = 0; j < 4; j++) { g.fillStyle = 'rgba(20,6,2,0.35)'; g.fillRect(0, j * h / 4, w, 2); }
    noise(g, w, h, 600, ['rgba(40,20,10,A)', 'rgba(140,110,80,A)'], 0.25); }, true),
  brick: canvasTex(128, 128, (g, w, h) => { g.fillStyle = '#5a3a2e'; g.fillRect(0, 0, w, h);
    for (let j = 0; j < 8; j++) for (let i = -1; i < 4; i++) { const x = i * 32 + (j % 2) * 16, y = j * 16;
      g.fillStyle = `rgb(${130 + Math.random() * 40 | 0},${62 + Math.random() * 18 | 0},${44 + Math.random() * 12 | 0})`; g.fillRect(x + 1, y + 1, 30, 14); }
    noise(g, w, h, 800, ['rgba(0,0,0,A)', 'rgba(255,230,200,A)'], 0.15); }, true),
  pave: canvasTex(128, 128, (g, w, h) => { g.fillStyle = '#6a4636'; g.fillRect(0, 0, w, h);
    for (let j = 0; j < 4; j++) for (let i = 0; i < 4; i++) { g.fillStyle = `rgb(${150 + Math.random() * 30 | 0},${70 + Math.random() * 16 | 0},${48 + Math.random() * 12 | 0})`; g.fillRect(i * 32 + 1, j * 32 + 1, 30, 30); }
    noise(g, w, h, 1200, ['rgba(30,20,10,A)', 'rgba(230,200,160,A)', 'rgba(60,80,40,A)'], 0.2); }, true),
  grass: canvasTex(128, 128, (g, w, h) => { g.fillStyle = '#5f7a3a'; g.fillRect(0, 0, w, h);
    noise(g, w, h, 4000, ['rgba(40,70,20,A)', 'rgba(140,160,70,A)', 'rgba(90,110,40,A)'], 0.5); }, true),
  road: canvasTex(128, 128, (g, w, h) => { g.fillStyle = '#6d6a64'; g.fillRect(0, 0, w, h); noise(g, w, h, 3000, ['rgba(30,30,30,A)', 'rgba(200,200,190,A)'], 0.25); }, true),
  plaster: canvasTex(128, 128, (g, w, h) => { g.fillStyle = '#e6dcc4'; g.fillRect(0, 0, w, h); noise(g, w, h, 2500, ['rgba(120,100,70,A)', 'rgba(255,255,240,A)', 'rgba(70,80,50,A)'], 0.12); }, true),
  wood: canvasTex(64, 256, (g, w, h) => { g.fillStyle = '#7a2a1c'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 60; i++) { g.fillStyle = `rgba(${Math.random() < 0.5 ? '30,8,4' : '170,70,40'},${Math.random() * 0.2})`; g.fillRect(Math.random() * w, 0, 1 + Math.random() * 2, h); } }, true),
  stone: canvasTex(128, 128, (g, w, h) => { g.fillStyle = '#8b8a80'; g.fillRect(0, 0, w, h); noise(g, w, h, 4000, ['rgba(40,40,40,A)', 'rgba(220,220,210,A)', 'rgba(80,90,70,A)'], 0.2); }, true),
  lattice: canvasTex(64, 128, (g, w, h) => { g.fillStyle = '#1e0c06'; g.fillRect(0, 0, w, h); g.fillStyle = '#7a2e1c';
    for (let i = 0; i <= 8; i++) g.fillRect(i * w / 8 - 1.5, 0, 3, h); for (let j = 0; j <= 16; j++) g.fillRect(0, j * h / 16 - 1.5, w, 3); g.fillRect(0, h * 0.62, w, 10); g.fillRect(0, 0, 6, h); g.fillRect(w - 6, 0, 6, h); }, true),
  thatch: canvasTex(128, 64, (g, w, h) => { g.fillStyle = '#8f7a48'; g.fillRect(0, 0, w, h); for (let i = 0; i < 900; i++) { g.strokeStyle = `rgba(${Math.random() < 0.5 ? '60,45,20' : '190,165,105'},${Math.random() * 0.5})`; g.lineWidth = 1; const x = Math.random() * w, y = Math.random() * h; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.random() * 3 - 1.5, y + 6 + Math.random() * 8); g.stroke(); } }, true),
  dirt: canvasTex(128, 128, (g, w, h) => { g.fillStyle = '#8a7656'; g.fillRect(0, 0, w, h); noise(g, w, h, 3000, ['rgba(60,50,30,A)', 'rgba(200,180,140,A)'], 0.3); }, true),
};
const M = {
  tile: new THREE.MeshStandardMaterial({ map: TEX.tile, roughness: 0.75 }),
  under: new THREE.MeshStandardMaterial({ color: 0x3a1a10, roughness: 0.9, side: THREE.BackSide }),
  ridge: new THREE.MeshStandardMaterial({ color: 0x8a7a68, roughness: 0.8 }),
  brick: new THREE.MeshStandardMaterial({ map: TEX.brick, roughness: 0.9 }),
  plaster: new THREE.MeshStandardMaterial({ map: TEX.plaster, roughness: 0.9 }),
  wood: new THREE.MeshStandardMaterial({ map: TEX.wood, roughness: 0.55 }),
  darkwood: new THREE.MeshStandardMaterial({ color: 0x2a120a, roughness: 0.7 }),
  stone: new THREE.MeshStandardMaterial({ map: TEX.stone, roughness: 0.85 }),
  gold: new THREE.MeshStandardMaterial({ color: 0xc8a050, roughness: 0.35, metalness: 0.7 }),
  hole: new THREE.MeshBasicMaterial({ color: 0x0a0604 }),
  lattice: new THREE.MeshStandardMaterial({ map: TEX.lattice, roughness: 0.6 }),
  thatch: new THREE.MeshStandardMaterial({ map: TEX.thatch, roughness: 1 }),
};
const groundMat = (k, sx, sz, tile = 4) => { const t = TEX[k].clone(); t.needsUpdate = true; t.repeat.set(sx / tile, sz / tile); return new THREE.MeshStandardMaterial({ map: t, roughness: 0.95 }); };
function add(parent, geo, mat, x = 0, y = 0, z = 0, cast = true) { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = cast; m.receiveShadow = true; parent.add(m); return m; }
function boxUV(w, h, d, s = 3) { const g = new THREE.BoxGeometry(w, h, d); const uv = g.attributes.uv, n = g.attributes.normal;
  for (let i = 0; i < uv.count; i++) { const ax = Math.abs(n.getX(i)), ay = Math.abs(n.getY(i)); const a = ax > 0.5 ? [d, h] : ay > 0.5 ? [w, d] : [w, h]; uv.setXY(i, uv.getX(i) * a[0] / s, uv.getY(i) * a[1] / s); } return g; }

// ---------- sky / light ----------
const SUN = new THREE.Vector3(...(WD.sun || [-0.55, 0.42, -0.35])).normalize();
const sky = new THREE.Mesh(new THREE.SphereGeometry(5000, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false,
  uniforms: { sun: { value: SUN }, top: { value: new THREE.Color(...(WD.skyTop || [0.22, 0.38, 0.62])) }, hor: { value: HAZE }, night: { value: 0 } },
  vertexShader: `varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `uniform vec3 sun, top, hor; uniform float night; varying vec3 vD; float h(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
  void main(){ float y = clamp(vD.y,0.,1.);
    vec3 c = mix(hor, top, pow(smoothstep(0.,0.6,y),0.7)); float s = max(dot(vD,sun),0.);
    c += (1.-night)*(vec3(1.,0.8,0.55)*(pow(s,6.)*0.35 + pow(s,60.)*0.8) + vec3(1.,0.95,0.85)*pow(s,2500.)*30.);
    c += night*vec3(0.85,0.88,1.)*pow(s,900.)*6.;
    vec2 g = vec2(atan(vD.z,vD.x)*260., asin(clamp(vD.y,-1.,1.))*260.); float r = h(floor(g));
    if (night > 0.3 && r > 0.986 && vD.y > 0.08) c += vec3(0.9,0.92,1.)*smoothstep(0.3,0.,length(fract(g)-0.5))*(r-0.986)*50.*night;
    gl_FragColor = vec4(c,1.); }` }));
scene.add(sky);
const hemi = new THREE.HemisphereLight(new THREE.Color(...(WD.skyLight || [0.65, 0.75, 0.95])), new THREE.Color(0.35, 0.3, 0.2), WD.ambient || 1.1); scene.add(hemi);
const sunL = new THREE.DirectionalLight(new THREE.Color(...(WD.sunColor || [1.0, 0.86, 0.66])), WD.sunPower || 3.0);
const SC = WD.center || [0, 0, 0];
sunL.target.position.set(...SC); sunL.position.set(SC[0] + SUN.x * 500, SUN.y * 500, SC[2] + SUN.z * 500);
sunL.castShadow = true; sunL.shadow.mapSize.set(Q.shadow || 2048, Q.shadow || 2048);
const sr = WD.shadowRange || 220; Object.assign(sunL.shadow.camera, { left: -sr, right: sr, top: sr, bottom: -sr, near: 50, far: 1200 });
sunL.shadow.bias = -0.0004; sunL.shadow.normalBias = 0.35; sunL.shadow.radius = 3;
scene.add(sunL); scene.add(sunL.target);
// clouds
const cloudTex = canvasTex(256, 128, (g, w, h) => { for (let i = 0; i < 18; i++) { const x = w * (0.2 + Math.random() * 0.6), y = h * (0.45 + Math.random() * 0.25), r = h * (0.15 + Math.random() * 0.2);
  const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, 'rgba(255,255,255,0.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); } });
const clouds = new THREE.Group(); scene.add(clouds);
for (let i = 0; i < (WD.clouds ?? 14); i++) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: cloudTex, color: 0xfff4e6, transparent: true, opacity: 0.7, fog: false, depthWrite: false }));
  const a = R(0, Math.PI * 2), d = R(1500, 2600); sp.position.set(Math.cos(a) * d, R(320, 620), Math.sin(a) * d); sp.scale.set(R(500, 900), R(150, 250), 1); clouds.add(sp); }

// ---------- ROOF ----------
// Hip roof (mái chảy) with concave slope and upturned corners (đầu đao). r: 0 = eave, 1 = ridge.
function roofGeo(w, d, h, ovh, curl, r0 = 0, r1 = 1, N = 10, Mr = 9) {
  const rl = Math.max(0.06, (w - d) / 2);
  const ring = (r) => { const hx = lerp(w / 2 + ovh, rl, r), hz = lerp(d / 2 + ovh, 0.06, r), y = h * Math.pow(r, 1.35);
    const C = [[hx, hz], [-hx, hz], [-hx, -hz], [hx, -hz]], pts = [];
    for (let s = 0; s < 4; s++) { const a = C[s], b = C[(s + 1) % 4];
      for (let i = 0; i <= N; i++) { if (i === N && s < 3) continue; const u = i / N; const c = Math.pow(Math.max(0, 1 - Math.min(u, 1 - u) / 0.32), 2.2), k = c * Math.pow(1 - r, 1.6);
        pts.push([lerp(a[0], b[0], u) * (1 + 0.05 * k), y + curl * k, lerp(a[1], b[1], u) * (1 + 0.05 * k)]); } }
    pts.push(pts[0].slice()); return pts; };
  const rings = []; for (let j = 0; j <= Mr; j++) rings.push(ring(lerp(r0, r1, j / Mr)));
  const pos = [], uv = [], idx = [], P = rings[0].length;
  rings.forEach((rg, j) => { let acc = 0; rg.forEach((p, k) => { if (k) acc += Math.hypot(p[0] - rg[k - 1][0], p[2] - rg[k - 1][2]); pos.push(...p); uv.push(k / (P - 1) * (2 * (w + d) + 8 * ovh) / 1.6, j / Mr * h * 0.6); }); });
  for (let j = 0; j < Mr; j++) for (let k = 0; k < P - 1; k++) { const a = j * P + k, b = a + 1, c = a + P, e = c + 1; idx.push(a, c, b, b, c, e); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals();
  const corners = [0, N, 2 * N, 3 * N].map(ci => rings.map(rg => new THREE.Vector3(...rg[ci])));
  return { g, corners, rl, h };
}
function roof(parent, o, y) { // o: {w,d,h,ov,curl,r0,r1,finial}
  const grp = new THREE.Group(); grp.position.y = y; parent.add(grp);
  const R0 = roofGeo(o.w, o.d, o.h, o.ov ?? 1.6, o.curl ?? 0.8, o.r0 ?? 0, o.r1 ?? 1);
  add(grp, R0.g, M[o.mat || 'tile']); add(grp, R0.g, M.under, 0, -0.14, 0, false);
  if (!o.plain) for (const c of R0.corners) { add(grp, new THREE.TubeGeometry(new THREE.CatmullRomCurve3(c.map(v => v.clone().add(new THREE.Vector3(0, 0.12, 0)))), 12, 0.17, 5), M.ridge);
    const tip = c[0], dir = new THREE.Vector3(tip.x, 0, tip.z).normalize(); // curled đầu đao tip
    const curve = new THREE.CatmullRomCurve3([tip.clone(), tip.clone().add(dir.clone().multiplyScalar(0.5)).add(new THREE.Vector3(0, 0.45, 0)), tip.clone().add(dir.clone().multiplyScalar(0.6)).add(new THREE.Vector3(0, 1.0, 0))]);
    add(grp, new THREE.TubeGeometry(curve, 8, 0.14, 5), M.ridge); }
  if ((o.r1 ?? 1) >= 1 && !o.plain) {
    const top = o.h + 0.15;
    if (R0.rl > 0.4) { add(grp, boxUV(2 * R0.rl + 0.8, 0.55, 0.5), M.ridge, 0, top, 0);
      for (const s of [-1, 1]) { const c = new THREE.CatmullRomCurve3([new THREE.Vector3(s * (R0.rl + 0.3), top, 0), new THREE.Vector3(s * (R0.rl + 0.8), top + 0.5, 0), new THREE.Vector3(s * (R0.rl + 0.6), top + 1.3, 0)]);
        add(grp, new THREE.TubeGeometry(c, 8, 0.22, 6), M.ridge); }
      if (o.pearl) { add(grp, new THREE.SphereGeometry(0.45, 12, 10), M.gold, 0, top + 0.7, 0); } }
    else { add(grp, new THREE.CylinderGeometry(0.3, 0.45, 0.6, 8), M.ridge, 0, top + 0.2, 0); add(grp, new THREE.SphereGeometry(0.38, 12, 10), M.gold, 0, top + 0.75, 0); add(grp, new THREE.SphereGeometry(0.22, 12, 10), M.gold, 0, top + 1.2, 0); }
  }
  return R0;
}
// inner ring extents of a roof at parameter r (to fit an upper storey into a skirt roof)
const ringExt = (w, d, ovh, r) => [2 * lerp(w / 2 + ovh, Math.max(0.06, (w - d) / 2), r), 2 * lerp(d / 2 + ovh, 0.06, r)];

// ---------- BUILDINGS ----------
function columns(g, w, d, y0, h, spacing = 3.4, rad = 0.22) {
  const nx = Math.max(1, Math.round(w / spacing)), nz = Math.max(1, Math.round(d / spacing)), pts = [];
  for (let i = 0; i <= nx; i++) for (let j = 0; j <= nz; j++) { if (i > 0 && i < nx && j > 0 && j < nz && !(j === 1 || j === nz - 1)) continue; pts.push([-w / 2 + i * w / nx, -d / 2 + j * d / nz]); }
  const geo = mergeGeometries(pts.map(p => new THREE.CylinderGeometry(rad, rad * 1.1, h, 10).translate(p[0], y0 + h / 2, p[1])));
  add(g, geo, M.wood);
  add(g, mergeGeometries(pts.map(p => new THREE.CylinderGeometry(rad * 1.6, rad * 1.8, 0.3, 8).translate(p[0], y0 + 0.15, p[1]))), M.stone);
  // tie beams
  add(g, boxUV(w + 0.5, 0.45, 0.35), M.wood, 0, y0 + h - 0.2, d / 2); add(g, boxUV(w + 0.5, 0.45, 0.35), M.wood, 0, y0 + h - 0.2, -d / 2);
  add(g, boxUV(0.35, 0.45, d + 0.5), M.wood, w / 2, y0 + h - 0.2, 0); add(g, boxUV(0.35, 0.45, d + 0.5), M.wood, -w / 2, y0 + h - 0.2, 0);
  return { nx, nz };
}
function hall(o) {
  const g = new THREE.Group(), w = o.w, d = o.d, base = o.base ?? 0.9, ch = o.colH ?? 4.2, ovh = o.ov ?? 1.8;
  add(g, boxUV(w + 2.4, base, d + 2.4), M.stone, 0, base / 2, 0);
  if (o.steps !== false) add(g, boxUV(Math.min(6, w * 0.5), base * 0.5, 1.4), M.stone, 0, base * 0.25, d / 2 + 1.9);
  const cn = columns(g, w, d, base, ch, o.spacing || 3.4);
  const walls = o.walls || 'back';
  if (walls !== 'none') { // brick/wood infill: back & sides solid; front = lattice doors
    add(g, boxUV(w, ch + 0.3, 0.25), M.wood, 0, base + (ch + 0.3) / 2, -d / 2 + 0.05);
    add(g, boxUV(0.25, ch + 0.3, d), M.wood, -w / 2 + 0.05, base + (ch + 0.3) / 2, 0); add(g, boxUV(0.25, ch + 0.3, d), M.wood, w / 2 - 0.05, base + (ch + 0.3) / 2, 0);
    if (walls === 'all') { const inset = Math.min(1.8, d * 0.18); add(g, boxUV(w - 0.3, ch - 0.5, 0.15, 3.2), M.lattice, 0, base + (ch - 0.5) / 2, d / 2 - inset);
      add(g, boxUV(w - 0.3, 0.12, inset), M.wood, 0, base + ch - 0.06, d / 2 - inset / 2, false); }
  }
  const top = base + ch;
  if ((o.tiers || 1) === 1) roof(g, { w, d, h: o.roofH ?? Math.max(3, d * 0.45), ov: ovh, curl: o.curl ?? 0.9, pearl: o.pearl, mat: o.roofMat, plain: o.roofMat === 'thatch' }, top);
  else { const rcut = 0.42, sk = { w, d, h: o.roofH ?? 3, ov: ovh, curl: o.curl ?? 0.9, r0: 0, r1: rcut };
    roof(g, sk, top); const [uw, ud] = ringExt(w, d, ovh, rcut), skTop = sk.h * Math.pow(rcut, 1.35), uh = o.upperH ?? 2.6;
    add(g, boxUV(uw, uh + skTop, ud), o.upperMat ? M[o.upperMat] : M.wood, 0, top + (uh + skTop) / 2, 0);
    roof(g, { w: uw, d: ud, h: o.roofH2 ?? Math.max(2.4, ud * 0.55), ov: ovh * 0.85, curl: o.curl ?? 0.9, pearl: o.pearl }, top + skTop + uh); }
  return g;
}
function gate(o) { // tam quan: central tall bay (1–2 tier roof) + two side bays, masonry with dark openings
  const g = new THREE.Group(), cw = o.cw || 8, ch = o.ch || 5.5, d = o.d || 6, sw = o.sw || 5, sh = o.sh || 3.8;
  const mat = M[o.mat || 'plaster'];
  add(g, boxUV(cw, ch, d), mat, 0, ch / 2, 0);
  const arch = (x, y, wd, ht) => { const s = new THREE.Shape(); s.moveTo(-wd / 2, 0); s.lineTo(-wd / 2, ht - wd / 2); s.absarc(0, ht - wd / 2, wd / 2, Math.PI, 0, true); s.lineTo(wd / 2, 0); s.lineTo(-wd / 2, 0);
    const sg = new THREE.ShapeGeometry(s, 12); for (const z of [d / 2 + 0.02, -d / 2 - 0.02]) { const m = add(g, sg, M.hole, x, y, z, false); if (z < 0) m.rotation.y = Math.PI; } };
  arch(0, 0, cw * 0.38, ch * 0.62);
  for (const s of [-1, 1]) if (o.sides !== false) { add(g, boxUV(sw, sh, d * 0.85), mat, s * (cw / 2 + sw / 2), sh / 2, 0); arch(s * (cw / 2 + sw / 2), 0, sw * 0.42, sh * 0.6);
    roof(g, { w: sw + 0.6, d: d * 0.85, h: 1.8, ov: 0.9, curl: 0.6 }, sh).corners; }
  if ((o.tiers || 2) === 2) { const sk = { w: cw, d, h: 2.0, ov: 1.3, curl: 0.8, r0: 0, r1: 0.42 }; roof(g, sk, ch);
    const [uw, ud] = ringExt(cw, d, 1.3, 0.42), skTop = 2.0 * Math.pow(0.42, 1.35); add(g, boxUV(uw, 2.0 + skTop, ud), M.wood, 0, ch + (2 + skTop) / 2, 0);
    roof(g, { w: uw, d: ud, h: 2.4, ov: 1.1, curl: 0.85, pearl: true }, ch + skTop + 2.0); }
  else roof(g, { w: cw, d, h: 2.4, ov: 1.3, curl: 0.85, pearl: true }, ch);
  if (o.plaque) { const t = canvasTex(256, 96, (c, w2, h2) => { c.fillStyle = '#2a1408'; c.fillRect(0, 0, w2, h2); c.strokeStyle = '#c8a050'; c.lineWidth = 6; c.strokeRect(5, 5, w2 - 10, h2 - 10);
      c.fillStyle = '#e8c870'; c.font = `700 ${h2 * 0.6 | 0}px "Noto Serif CJK SC"`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(o.plaque, w2 / 2, h2 / 2 + 2); });
    add(g, new THREE.PlaneGeometry(cw * 0.42, cw * 0.16), new THREE.MeshStandardMaterial({ map: t, roughness: 0.6 }), 0, ch * 0.8, d / 2 + 0.05, false); }
  return g;
}
function khueVanCac(o) { // square two-storey pavilion: 4 brick pillars, wooden upper floor with round "sun" windows, 8 roofs
  const g = new THREE.Group(), s = o.s || 7.2;
  add(g, boxUV(s + 1.6, 0.8, s + 1.6), M.stone, 0, 0.4, 0);
  for (const x of [-1, 1]) for (const z of [-1, 1]) add(g, boxUV(1.4, 4.0, 1.4), M.plaster, x * (s / 2 - 0.7), 0.8 + 2.0, z * (s / 2 - 0.7));
  add(g, boxUV(s + 0.4, 0.4, s + 0.4), M.wood, 0, 5.0, 0);
  const sk = { w: s + 0.4, d: s + 0.4, h: 2.1, ov: 1.25, curl: 0.95, r0: 0, r1: 0.44 }; roof(g, sk, 5.1);
  const [uw] = ringExt(s + 0.4, s + 0.4, 1.25, 0.44), skTop = 2.1 * Math.pow(0.44, 1.35), uh = 2.9;
  add(g, boxUV(uw, uh + skTop, uw), M.wood, 0, 5.1 + (uh + skTop) / 2, 0);
  const wy = 5.1 + skTop + uh * 0.5, rad = Math.min(1.15, uw * 0.3);
  for (let k = 0; k < 4; k++) { const grp = new THREE.Group(); grp.rotation.y = k * Math.PI / 2; grp.position.y = wy; g.add(grp); const z = uw / 2 + 0.03;
    add(grp, new THREE.CircleGeometry(rad, 32), M.hole, 0, 0, z, false);
    add(grp, new THREE.TorusGeometry(rad, 0.11, 8, 32), M.gold, 0, 0, z + 0.03, false);
    for (let i = 0; i < 8; i++) { const sp = add(grp, boxUV(0.06, rad * 2, 0.05), M.gold, 0, 0, z + 0.04, false); sp.rotation.z = i * Math.PI / 8; } }
  roof(g, { w: uw, d: uw, h: 2.6, ov: 1.15, curl: 0.95 }, 5.1 + skTop + uh);
  return g;
}
function wall(o) { // straight wall segment from [x,z] to [x,z] with tiled coping
  const g = new THREE.Group(), a = o.from, b = o.to, len = Math.hypot(b[0] - a[0], b[1] - a[1]), h = o.h || 2.6, t = o.t || 0.6;
  g.position.set((a[0] + b[0]) / 2, 0, (a[1] + b[1]) / 2); g.rotation.y = -Math.atan2(b[1] - a[1], b[0] - a[0]);
  add(g, boxUV(len, h, t), M[o.mat || 'brick'], 0, h / 2, 0);
  const cop = new THREE.CylinderGeometry(0.01, 1, 1, 3, 1).rotateZ(Math.PI / 2).rotateX(Math.PI / 6).scale(len + 0.3, 0.45, t + 0.6);
  add(g, cop, M.tile, 0, h + 0.2, 0);
  return g;
}
const stelaGeo = mergeGeometries([new THREE.SphereGeometry(0.5, 12, 8).scale(1, 0.5, 1.35).translate(0, 0.25, 0), new THREE.SphereGeometry(0.16, 10, 8).scale(1, 0.8, 1.3).translate(0, 0.3, 0.75),
  new THREE.BoxGeometry(0.95, 1.55, 0.2).translate(0, 1.2, -0.05), new THREE.CylinderGeometry(0.475, 0.475, 0.2, 16, 1, false, -Math.PI / 2, Math.PI).rotateX(-Math.PI / 2).translate(0, 1.97, -0.05)]);
function stelae(o) { // rows of stelae on tortoises between from->to, facing `face` (+1 = +x, -1 = -x)
  const n = o.count, rows = o.rows || 2, per = Math.ceil(n / rows), im = new THREE.InstancedMesh(stelaGeo, M.stone, n); im.castShadow = im.receiveShadow = true;
  const m = new THREE.Matrix4(), q = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), (o.face || 1) * Math.PI / 2);
  for (let i = 0; i < n; i++) { const r = Math.floor(i / per), k = i % per, u = per > 1 ? k / (per - 1) : 0.5;
    m.compose(new THREE.Vector3(lerp(o.from[0], o.to[0], u) + r * (o.rowGap || 2.4) * -(o.face || 1), 0.55, lerp(o.from[1], o.to[1], u)), q, new THREE.Vector3(1, 1, 1)); im.setMatrixAt(i, m); }
  scene.add(im); return im;
}
const reflectors = [];
function pond(o) {
  const g = new THREE.Group(), [w, d] = o.size, y = o.y ?? 0.15;
  const rf = new Reflector(new THREE.PlaneGeometry(w, d), { color: new THREE.Color(...(o.tint || [0.55, 0.62, 0.55])), textureWidth: Math.round(W * (Q.reflScale || 0.5)), textureHeight: Math.round(H * (Q.reflScale || 0.5)), clipBias: 0.003, multisample: 0 });
  rf.rotation.x = -Math.PI / 2; rf.position.y = y; g.add(rf); reflectors.push(rf);
  const rim = o.rim ?? 0.9, rh = 0.55;
  for (const [x, z, sx, sz] of [[0, d / 2 + rim / 2, w + 2 * rim, rim], [0, -d / 2 - rim / 2, w + 2 * rim, rim], [w / 2 + rim / 2, 0, rim, d], [-w / 2 - rim / 2, 0, rim, d]]) add(g, boxUV(sx, rh, sz), M.stone, x, rh / 2, z);
  if (o.rail) { const posts = []; const per = (a, b) => { const L = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.round(L / 2.2); for (let i = 0; i <= n; i++) posts.push([lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n)]); };
    const hw = w / 2 + rim / 2, hd = d / 2 + rim / 2; per([-hw, hd], [hw, hd]); per([-hw, -hd], [hw, -hd]); per([hw, -hd], [hw, hd]); per([-hw, -hd], [-hw, hd]);
    add(g, mergeGeometries(posts.map(p => new THREE.BoxGeometry(0.22, 0.75, 0.22).translate(p[0], rh + 0.37, p[1]))), M.stone);
    for (const [x, z, sx, sz] of [[0, hd, 2 * hw, 0.14], [0, -hd, 2 * hw, 0.14], [hw, 0, 0.14, 2 * hd], [-hw, 0, 0.14, 2 * hd]]) add(g, boxUV(sx, 0.12, sz), M.stone, x, rh + 0.62, z); }
  return g;
}
function groundPatch(o) { const [x0, z0, x1, z1] = o.rect, w = x1 - x0, d = z1 - z0;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), groundMat(o.mat || 'grass', w, d, o.tile || 4)); m.rotation.x = -Math.PI / 2; m.position.set((x0 + x1) / 2, o.y ?? 0.03, (z0 + z1) / 2); m.receiveShadow = true; scene.add(m); }

// ---------- ground height (terrains) ----------
const TERR = [];
function hash2(x, y) { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); }
function vnoise(x, y) { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  return lerp(lerp(hash2(xi, yi), hash2(xi + 1, yi), u), lerp(hash2(xi, yi + 1), hash2(xi + 1, yi + 1), u), v); }
function fbm(x, y, o = 5) { let a = 0, f = 1, w = 0.5; for (let i = 0; i < o; i++) { a += w * vnoise(x * f, y * f); f *= 2.03; w *= 0.5; } return a; }
function segDist(px, pz, pts) { let best = 1e9; for (let i = 0; i < pts.length - 1; i++) { const [ax, az] = pts[i], [bx, bz] = pts[i + 1], dx = bx - ax, dz = bz - az;
  const u = clamp(((px - ax) * dx + (pz - az) * dz) / (dx * dx + dz * dz + 1e-9)); best = Math.min(best, Math.hypot(px - ax - u * dx, pz - az - u * dz)); } return best; }
function groundH(x, z) { let h = 0; for (const T of TERR) if (Math.abs(x - T.cx) < T.w / 2 && Math.abs(z - T.cz) < T.d / 2) h = Math.max(h, T.h(x, z)); return h; }

const OCEANS = [];
function terrain(o) { // {pos:[cx,cz], size:[w,d], height, scale, mount:'west'|'all'|'ring', coast:{x0,amp,freq} (sea to the +x side), rivers:[[[x,z]...],w], flat:[[x,z,r]], seg}
  const [cx, cz] = o.pos, [w, d] = o.size, H0 = o.height || 30, sc = o.scale || 0.004, seed = o.seed || 1;
  const coastX = z => o.coast ? cx + o.coast.x0 + (o.coast.amp || 0) * Math.sin((z - cz) * (o.coast.freq || 0.0006) + 1.3) + (o.coast.tilt || 0) * (z - cz) : 1e9;
  const h = (x, z) => {
    const n = fbm((x + seed * 97) * sc, (z - seed * 53) * sc);
    let m = 1;
    if (o.mount === 'west') m = clamp(((cx + w * 0.1) - x) / (w * 0.45)) ** 1.3 * 0.9 + 0.1;
    else if (o.mount === 'ring') m = clamp(Math.hypot(x - cx, z - cz) / (Math.min(w, d) * 0.45)) ** 1.5;
    let y = H0 * m * Math.pow(n, 1.6) * 1.8 - 0.5;
    if (o.peak) { const [px, pz, pr, ph] = o.peak; y = Math.max(y, ph * Math.exp(-((x - px) ** 2 + (z - pz) ** 2) / (pr * pr)) * (0.75 + 0.5 * n)); }
    const cxz = coastX(z); if (x > cxz) y = Math.min(y, -2 - (x - cxz) * 0.02); else y = Math.min(y, y * clamp((cxz - x) / 120));
    for (const [pts, rw] of (o.rivers || [])) { const dd = segDist(x, z, pts); if (dd < rw * 3) y = Math.min(y, lerp(-1.6, y, ss(rw * 0.5, rw * 3, dd))); }
    for (const [fx, fz, fr] of (o.flat || [])) { const dd = Math.hypot(x - fx, z - fz); y = lerp(Math.min(y, 0.6), y, ss(fr, fr * 1.8, dd)); }
    return y;
  };
  const seg = o.seg || 180, g = new THREE.PlaneGeometry(w, d, seg, seg).rotateX(-Math.PI / 2), p = g.attributes.position, col = [];
  for (let i = 0; i < p.count; i++) { const x = p.getX(i) + cx, z = p.getZ(i) + cz, y = h(x, z); p.setY(i, y);
    const t = clamp(y / (H0 * 1.2)), sand = y < 0.8 && y > -1.6 && o.coast && x > coastX(z) - 40;
    const c = sand ? [0.76, 0.68, 0.48] : y < -0.4 ? [0.3, 0.38, 0.3] : o.vivid ? (t < 0.35 ? [lerp(0.25, 0.36, t / 0.35), lerp(0.5, 0.46, t / 0.35), lerp(0.16, 0.18, t / 0.35)] : [lerp(0.36, 0.46, (t - 0.35) / 0.65), lerp(0.46, 0.34, (t - 0.35) / 0.65), lerp(0.18, 0.22, (t - 0.35) / 0.65)]) : [lerp(0.33, 0.42, t), lerp(0.5, 0.4, t), lerp(0.22, 0.32, t)];
    if (t > 0.7) { const k = (t - 0.7) / 0.3; c[0] = lerp(c[0], 0.5, k); c[1] = lerp(c[1], 0.48, k); c[2] = lerp(c[2], 0.44, k); }
    col.push(...c); }
  g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); g.computeVertexNormals();
  const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.95, flatShading: !!o.flatShading })); m.position.set(cx, 0, cz); m.receiveShadow = true; m.castShadow = true;
  m.geometry.translate(-cx * 0, 0, 0); m.position.set(0, 0, 0); g.translate(cx, 0, cz); scene.add(m);
  const water = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshStandardMaterial({ color: o.waterColor ? new THREE.Color(...o.waterColor) : 0x3c6f86, roughness: 0.25, metalness: 0.1 }));
  water.rotation.x = -Math.PI / 2; water.position.set(cx, -0.7, cz); water.receiveShadow = true; scene.add(water);
  if (o.ocean) { const sea = new THREE.Mesh(new THREE.PlaneGeometry(w * 8, d * 4), new THREE.MeshStandardMaterial({ color: 0x2c5a74, roughness: 0.35, metalness: 0.05 })); sea.rotation.x = -Math.PI / 2; sea.position.set(cx, -0.9, cz); scene.add(sea); OCEANS.push({ cx, cz, w, d }); }
  TERR.push({ cx, cz, w, d, h });
  return m;
}

// ---------- trees, houses (instanced) ----------
const treeTrunk = new THREE.CylinderGeometry(0.22, 0.38, 1, 7).translate(0, 0.5, 0);
const treeCrown = mergeGeometries([[0, 0, 0, 1], [0.55, -0.15, 0.2, 0.75], [-0.5, -0.1, -0.25, 0.8], [0.1, 0.35, -0.4, 0.7], [-0.15, -0.2, 0.55, 0.7], [0.4, 0.3, 0.35, 0.55], [-0.45, 0.25, 0.3, 0.5]].map(([x, y, z, r]) => new THREE.IcosahedronGeometry(r, 1).translate(x, y, z)));
const treeList = [];
function trees(o) { for (let i = 0; i < o.count; i++) { let x, z, ok = false; for (let k = 0; k < 30 && !ok; k++) { x = R(o.rect[0], o.rect[2]); z = R(o.rect[1], o.rect[3]); ok = !(o.avoid || []).some(r => inRect(x, z, r, 1.5)); }
  if (ok) treeList.push({ x, z, y: groundH(x, z), h: R(...(o.h || [7, 14])), c: R(0, 1), lean: R(-0.08, 0.08), w: o.wide || 1, hue: o.hue }); } }
function buildTrees() { if (!treeList.length) return; const n = treeList.length;
  const tr = new THREE.InstancedMesh(treeTrunk, new THREE.MeshStandardMaterial({ color: 0x4a3a2c, roughness: 1 }), n), cr = new THREE.InstancedMesh(treeCrown, new THREE.MeshStandardMaterial({ roughness: 0.9, flatShading: true }), n);
  tr.castShadow = cr.castShadow = true; tr.receiveShadow = cr.receiveShadow = true; const m = new THREE.Matrix4(), q = new THREE.Quaternion(), col = new THREE.Color();
  treeList.forEach((t, i) => { q.setFromEuler(new THREE.Euler(t.lean, t.c * 6, -t.lean)); m.compose(new THREE.Vector3(t.x, t.y - 0.3, t.z), q, new THREE.Vector3(t.w, t.h * 0.55, t.w)); tr.setMatrixAt(i, m);
    const s = t.h * 0.33; m.compose(new THREE.Vector3(t.x + t.lean * t.h * 0.5, t.y + t.h * 0.62, t.z), q, new THREE.Vector3(s * 1.15 * t.w, s * 0.85, s * 1.15 * t.w)); cr.setMatrixAt(i, m);
    col.setHSL(t.hue ?? (0.22 + t.c * 0.08), 0.38 + t.c * 0.15, 0.2 + t.c * 0.1); cr.setColorAt(i, col); });
  scene.add(tr); scene.add(cr); }
const houseList = [];
function houses(o) { for (let i = 0; i < o.count; i++) { let x, z, ok = false; for (let k = 0; k < 40 && !ok; k++) { x = R(o.rect[0], o.rect[2]); z = R(o.rect[1], o.rect[3]); ok = !(o.avoid || []).some(r => inRect(x, z, r, 4)); }
  if (ok) houseList.push({ x, z, y: groundH(x, z), w: R(...(o.w || [5, 10])), d: R(...(o.d || [8, 14])), h: R(...(o.hgt || [3.5, 10])), rot: (rnd() < 0.5 ? 0 : Math.PI / 2) + R(-0.05, 0.05), c: rnd(), style: o.style || 'town' }); } }
function buildHouses() { if (!houseList.length) return; const n = houseList.length;
  const body = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1).translate(0, 0.5, 0), new THREE.MeshStandardMaterial({ roughness: 0.95 }), n);
  const rf = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.01, 0.75, 1, 4, 1).rotateY(Math.PI / 4).translate(0, 0.5, 0), new THREE.MeshStandardMaterial({ roughness: 0.9 }), n);
  body.castShadow = rf.castShadow = body.receiveShadow = rf.receiveShadow = true; const m = new THREE.Matrix4(), q = new THREE.Quaternion(), col = new THREE.Color();
  const walls = { town: [[0.88, 0.8, 0.6], [0.9, 0.86, 0.78], [0.82, 0.72, 0.52], [0.75, 0.75, 0.72]], village: [[0.62, 0.5, 0.36], [0.55, 0.45, 0.33], [0.68, 0.58, 0.42], [0.6, 0.52, 0.4]] };
  const roofs = { town: [[0.45, 0.2, 0.14], [0.35, 0.3, 0.28], [0.5, 0.28, 0.18]], village: [[0.62, 0.52, 0.3], [0.56, 0.47, 0.27], [0.66, 0.57, 0.34]] };
  houseList.forEach((h, i) => { q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), h.rot); m.compose(new THREE.Vector3(h.x, h.y, h.z), q, new THREE.Vector3(h.w, h.h, h.d)); body.setMatrixAt(i, m);
    m.compose(new THREE.Vector3(h.x, h.y + h.h, h.z), q, new THREE.Vector3(h.w * 1.3, h.style === 'village' ? 3.2 : 2.4, h.d * 1.2)); rf.setMatrixAt(i, m);
    body.setColorAt(i, col.setRGB(...walls[h.style][Math.floor(h.c * 4)])); rf.setColorAt(i, col.setRGB(...roofs[h.style][Math.floor(h.c * 3)])); });
  scene.add(body); scene.add(rf); }

// ---------- small props ----------
function boxProp(o) { const g = new THREE.Group(); add(g, boxUV(...o.size, o.uv || 3), M[o.mat || 'wood'], 0, o.size[1] / 2 + (o.y || 0), 0); return g; }
function tents(o) { // lều thi: rows x cols of A-frame tents in rect, cloth colours
  const geo = mergeGeometries([new THREE.CylinderGeometry(0.01, 1, 1, 3, 1).rotateZ(Math.PI / 2).rotateX(Math.PI / 6).scale(3.0, 2.3, 2.6).translate(0, 1.15, 0)]);
  const n = o.rows * o.cols, im = new THREE.InstancedMesh(geo, new THREE.MeshStandardMaterial({ roughness: 1, side: THREE.DoubleSide }), n); im.castShadow = im.receiveShadow = true;
  const m = new THREE.Matrix4(), q = new THREE.Quaternion(), col = new THREE.Color(); let i = 0;
  for (let r = 0; r < o.rows; r++) for (let c = 0; c < o.cols; c++) { const x = o.rect[0] + (c + 0.5) * (o.rect[2] - o.rect[0]) / o.cols + R(-0.6, 0.6), z = o.rect[1] + (r + 0.5) * (o.rect[3] - o.rect[1]) / o.rows + R(-0.6, 0.6);
    q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), R(-0.15, 0.15) + (o.rot || 0)); m.compose(new THREE.Vector3(x, groundH(x, z), z), q, new THREE.Vector3(1, R(0.9, 1.1), 1)); im.setMatrixAt(i, m);
    const k = rnd(); im.setColorAt(i++, col.setRGB(...(k < 0.4 ? [0.58, 0.47, 0.32] : k < 0.7 ? [0.46, 0.38, 0.27] : k < 0.85 ? [0.3, 0.34, 0.42] : [0.62, 0.52, 0.36]))); }
  const g = new THREE.Group(); g.add(im); return g;
}
function desks(o) { // bàn học thấp + chiếu theo hàng
  const n = o.rows * o.cols, dk = new THREE.InstancedMesh(mergeGeometries([new THREE.BoxGeometry(1.0, 0.06, 0.45).translate(0, 0.32, 0), new THREE.BoxGeometry(0.06, 0.3, 0.4).translate(-0.44, 0.15, 0), new THREE.BoxGeometry(0.06, 0.3, 0.4).translate(0.44, 0.15, 0),
    new THREE.BoxGeometry(0.34, 0.012, 0.24).translate(-0.1, 0.36, 0)]), M.darkwood, n);
  const mat = new THREE.InstancedMesh(new THREE.BoxGeometry(1.1, 0.02, 1.0), new THREE.MeshStandardMaterial({ color: 0xb59a5c, roughness: 1 }), n);
  dk.castShadow = dk.receiveShadow = mat.receiveShadow = true; const m = new THREE.Matrix4(), q = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), o.rot || 0); let i = 0;
  for (let r = 0; r < o.rows; r++) for (let c = 0; c < o.cols; c++) { const x = o.origin[0] + c * (o.dx || 1.6), z = o.origin[1] + r * (o.dz || 1.7), y = o.y || 0;
    m.compose(new THREE.Vector3(x, y, z), q, new THREE.Vector3(1, 1, 1)); dk.setMatrixAt(i, m); m.compose(new THREE.Vector3(x, y + 0.01, z - 0.65), q, new THREE.Vector3(1, 1, 1)); mat.setMatrixAt(i++, m); }
  const g = new THREE.Group(); g.add(dk); g.add(mat); return g;
}
function fence(o) { // hàng rào tre quanh rect
  const [x0, z0, x1, z1] = o.rect, posts = [], rails = [];
  const side = (ax, az, bx, bz) => { const L = Math.hypot(bx - ax, bz - az), n = Math.max(1, Math.round(L / 2)); for (let i = 0; i <= n; i++) posts.push(new THREE.CylinderGeometry(0.06, 0.07, 1.6, 5).translate(lerp(ax, bx, i / n), 0.8, lerp(az, bz, i / n)));
    for (const y of [0.5, 1.2]) rails.push(new THREE.CylinderGeometry(0.04, 0.04, L, 5).rotateZ(Math.PI / 2).rotateY(-Math.atan2(bz - az, bx - ax)).translate((ax + bx) / 2, y, (az + bz) / 2)); };
  side(x0, z0, x1, z0); side(x1, z0, x1, z1); side(x1, z1, x0, z1); side(x0, z1, x0, z0);
  const g = new THREE.Group(); add(g, mergeGeometries([...posts, ...rails]), new THREE.MeshStandardMaterial({ color: 0x8a7a48, roughness: 1 })); return g;
}
function scaffold(o) { // giàn giáo tre bao quanh một khối
  const [w, d, h] = o.size, parts = [], st = 2.2;
  for (const [ax, az, bx, bz] of [[-w / 2, -d / 2, w / 2, -d / 2], [w / 2, -d / 2, w / 2, d / 2], [w / 2, d / 2, -w / 2, d / 2], [-w / 2, d / 2, -w / 2, -d / 2]]) {
    const L = Math.hypot(bx - ax, bz - az), n = Math.max(1, Math.round(L / st)), ang = -Math.atan2(bz - az, bx - ax);
    for (let i = 0; i <= n; i++) parts.push(new THREE.CylinderGeometry(0.06, 0.06, h, 4).translate(lerp(ax, bx, i / n), h / 2, lerp(az, bz, i / n)));
    for (let y = 1.6; y < h; y += 1.8) { parts.push(new THREE.CylinderGeometry(0.05, 0.05, L, 4).rotateZ(Math.PI / 2).rotateY(ang).translate((ax + bx) / 2, y, (az + bz) / 2));
      parts.push(new THREE.BoxGeometry(L, 0.05, 0.6).rotateY(ang).translate((ax + bx) / 2, y, (az + bz) / 2)); } }
  const g = new THREE.Group(); add(g, mergeGeometries(parts), new THREE.MeshStandardMaterial({ color: 0xa08a52, roughness: 1 })); return g;
}
function board(o) { // bảng vàng trên hai cột
  const g = new THREE.Group(), w = o.w || 6, h = o.h || 3;
  for (const s of [-1, 1]) add(g, new THREE.CylinderGeometry(0.12, 0.14, h + 2, 8), M.wood, s * (w / 2 + 0.1), (h + 2) / 2, 0);
  const t = canvasTex(256, 128, (c, W2, H2) => { c.fillStyle = '#d9b44a'; c.fillRect(0, 0, W2, H2); c.strokeStyle = '#7a1a10'; c.lineWidth = 6; c.strokeRect(4, 4, W2 - 8, H2 - 8);
    c.fillStyle = 'rgba(60,20,10,0.75)'; for (let i = 0; i < 14; i++) for (let j = 0; j < 7; j++) c.fillRect(18 + i * 16.5, 18 + j * 14, 8, 9); });
  add(g, new THREE.BoxGeometry(w, h, 0.12), new THREE.MeshStandardMaterial({ map: t, roughness: 0.6 }), 0, 2 + h / 2, 0);
  roof(g, { w: w + 0.6, d: 1.0, h: 0.7, ov: 0.4, curl: 0.4 }, 2 + h + 0.05);
  return g;
}
function stela1(o) { const g = new THREE.Group(); add(g, stelaGeo, M.stone, 0, 0.55, 0); g.scale.setScalar(o.scale || 1); return g; }
function label(o) { // nhãn chữ 3D (sprite) luôn quay về máy quay
  const fs = 64, c = document.createElement('canvas'), g2 = c.getContext('2d'); g2.font = `600 ${fs}px Lora`; const tw = Math.ceil(g2.measureText(o.text).width) + 40;
  c.width = tw; c.height = fs + 36; const g = c.getContext('2d'); g.font = `600 ${fs}px Lora`; g.fillStyle = 'rgba(20,12,6,0.55)'; g.beginPath(); g.roundRect(0, 0, tw, fs + 36, 18); g.fill();
  g.fillStyle = '#f6e3b0'; g.textBaseline = 'middle'; g.fillText(o.text, 20, (fs + 36) / 2 + 2);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, depthTest: false, transparent: true, fog: false })); const k = o.size || 30; sp.scale.set(k * tw / (fs + 36), k, 1); sp.position.y = o.y || 0; sp.renderOrder = 20;
  const g3 = new THREE.Group(); g3.add(sp); return g3;
}
function marker(o) { // cột sáng đánh dấu địa điểm trên sa bàn
  const g = new THREE.Group(), h = o.h || 120;
  add(g, new THREE.CylinderGeometry(o.r || 6, o.r || 6, h, 16).translate(0, h / 2, 0), new THREE.MeshBasicMaterial({ color: new THREE.Color(3, 2.2, 0.9), transparent: true, opacity: 0.55, depthWrite: false }), 0, 0, 0, false);
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: TEX_GLOW, color: new THREE.Color(1, 0.75, 0.35), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, fog: false }));
  sp.scale.set(h * 1.4, h * 1.4, 1); sp.position.y = h * 0.2; g.add(sp);
  if (o.text) { const L = label({ text: o.text, size: o.size || 40, y: h + 30 }); g.add(L); }
  return g;
}
function route(o) { // đường đi phát sáng, hiện dần theo `grow`
  const pts = o.points.map(([x, z]) => new THREE.Vector3(x, groundH(x, z) + (o.lift || 8), z));
  const geo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 400, o.r || 5, 6);
  const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: new THREE.Color(2.6, 1.8, 0.6) })); m.userData.grow = o.grow; m.userData.total = geo.index.count;
  const g = new THREE.Group(); g.add(m); GROW.push(m); return g;
}
const GROW = [];
const TEX_GLOW = canvasTex(128, 128, (g, w) => { const gr = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.3, 'rgba(255,255,255,0.4)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, w); });

// ---------- lanterns (đèn lồng, sáng theo mức đêm) ----------
const lanternList = [];
function lanterns(o) { for (const p of o.points) lanternList.push(p); }
let LANT = null, LGLOW = null; const LPL = [];
function buildLanterns() { if (!lanternList.length) return; const n = lanternList.length;
  const geo = mergeGeometries([new THREE.SphereGeometry(0.32, 12, 10).scale(1, 1.25, 1), new THREE.CylinderGeometry(0.2, 0.2, 0.08, 10).translate(0, 0.42, 0), new THREE.CylinderGeometry(0.2, 0.2, 0.08, 10).translate(0, -0.42, 0)]);
  LANT = new THREE.InstancedMesh(geo, new THREE.MeshStandardMaterial({ color: 0xb02418, emissive: 0xff5a20, emissiveIntensity: 0, roughness: 0.6 }), n);
  const m = new THREE.Matrix4(); lanternList.forEach((p, i) => { m.makeTranslation(p[0], p[1], p[2]); LANT.setMatrixAt(i, m); }); scene.add(LANT);
  LGLOW = lanternList.map(p => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: TEX_GLOW, color: new THREE.Color(1, 0.55, 0.25), blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0 }));
    s.position.set(...p); s.scale.set(1.6, 1.6, 1); scene.add(s); return s; });
  for (let i = 0; i < 6; i++) { const l = new THREE.PointLight(0xff8a40, 0, 18, 1.6); scene.add(l); LPL.push(l); } }
function updateLanterns(night, t) { if (!LANT) return; LANT.material.emissiveIntensity = night * 2.2; LGLOW.forEach((s, i) => { s.material.opacity = night * (0.45 + 0.06 * Math.sin(t * 3 + i)) * clamp((s.position.distanceTo(camera.position) - 3) / 14); s.visible = night > 0.02; });
  const near = lanternList.map((p, i) => [i, (p[0] - camera.position.x) ** 2 + (p[2] - camera.position.z) ** 2]).sort((a, b) => a[1] - b[1]).slice(0, LPL.length);
  LPL.forEach((l, k) => { const it = near[k]; if (!it || night < 0.02) { l.intensity = 0; return; } l.position.set(...lanternList[it[0]]); l.intensity = night * 14 * (0.9 + 0.1 * Math.sin(t * 5 + k)); }); }

// ---------- people: articulated figures (đi, đứng, quỳ, viết, vái, giảng, đục đá, khiêng) ----------
const COSTUME = {
  scholar: { robe: [[0.13, 0.17, 0.33], [0.36, 0.24, 0.15], [0.2, 0.3, 0.24], [0.3, 0.32, 0.4], [0.42, 0.36, 0.28]], legs: [[0.12, 0.1, 0.09]], hat: 'khan', long: true },
  teacher: { robe: [[0.12, 0.12, 0.14], [0.3, 0.2, 0.14]], legs: [[0.1, 0.08, 0.08]], hat: 'khan', long: true, beard: true },
  prince: { robe: [[0.75, 0.55, 0.12], [0.62, 0.14, 0.1], [0.7, 0.45, 0.15]], legs: [[0.3, 0.1, 0.08]], hat: 'crown', long: true },
  king: { robe: [[0.85, 0.65, 0.1]], legs: [[0.4, 0.2, 0.05]], hat: 'crown', long: true },
  official: { robe: [[0.55, 0.1, 0.1], [0.12, 0.2, 0.45], [0.15, 0.35, 0.2], [0.45, 0.12, 0.3]], legs: [[0.1, 0.08, 0.08]], hat: 'quan', long: true },
  monk: { robe: [[0.55, 0.36, 0.14], [0.45, 0.3, 0.15], [0.62, 0.42, 0.18]], legs: [[0.4, 0.28, 0.14]], hat: 'bald', long: true },
  commoner: { robe: [[0.36, 0.26, 0.16], [0.2, 0.22, 0.3], [0.3, 0.28, 0.2], [0.5, 0.42, 0.28]], legs: [[0.1, 0.09, 0.08], [0.22, 0.18, 0.12]], hat: ['non', 'khan', 'hair'], long: false },
  child: { robe: [[0.42, 0.3, 0.18], [0.3, 0.3, 0.36]], legs: [[0.15, 0.12, 0.1]], hat: 'hair', long: false, scale: 0.68 },
  laureate: { robe: [[0.62, 0.1, 0.1]], legs: [[0.1, 0.08, 0.08]], hat: 'quan', long: true },
  student_girl: { robe: [[0.95, 0.95, 0.94]], legs: [[0.9, 0.9, 0.9]], hat: 'hair', long: true, slim: true },
  student_boy: { robe: [[0.94, 0.94, 0.95]], legs: [[0.12, 0.14, 0.24]], hat: 'hair', long: false },
  graduate: { robe: [[0.08, 0.08, 0.1]], legs: [[0.1, 0.1, 0.12]], hat: 'mortar', long: true },
  tourist: { robe: [[0.75, 0.3, 0.25], [0.25, 0.45, 0.6], [0.9, 0.85, 0.7], [0.3, 0.5, 0.35]], legs: [[0.2, 0.22, 0.3], [0.5, 0.45, 0.38]], hat: ['hair', 'hair', 'non'], long: false },
};
const PG = { // part geometries (person ~1.75 tall, hip at y = 0.85)
  robeL: new THREE.CylinderGeometry(0.19, 0.33, 1.23, 12, 1, false).translate(0, -0.115, 0),
  robeS: mergeGeometries([new THREE.CylinderGeometry(0.19, 0.25, 0.75, 12).translate(0, 0.125, 0)]),
  head: mergeGeometries([new THREE.SphereGeometry(0.115, 12, 10).scale(1, 1.12, 1.05).translate(0, 0.72, 0), new THREE.CylinderGeometry(0.05, 0.06, 0.1, 8).translate(0, 0.6, 0)]),
  arm: mergeGeometries([new THREE.CylinderGeometry(0.06, 0.085, 0.6, 8).translate(0, -0.3, 0), new THREE.SphereGeometry(0.045, 8, 6).translate(0, -0.62, 0)]),
  leg: mergeGeometries([new THREE.CylinderGeometry(0.06, 0.05, 0.82, 8).translate(0, -0.41, 0), new THREE.BoxGeometry(0.09, 0.05, 0.2).translate(0, -0.83, 0.05)]),
  khan: new THREE.CylinderGeometry(0.125, 0.125, 0.09, 14).translate(0, 0.81, 0),
  quan: mergeGeometries([new THREE.CylinderGeometry(0.12, 0.13, 0.16, 12).translate(0, 0.84, 0), new THREE.SphereGeometry(0.09, 10, 6, 0, Math.PI * 2, 0, Math.PI / 2).translate(0, 0.9, -0.03), new THREE.BoxGeometry(0.5, 0.06, 0.02).translate(0, 0.86, -0.1)]),
  crown: mergeGeometries([new THREE.CylinderGeometry(0.11, 0.12, 0.12, 12).translate(0, 0.84, 0), new THREE.BoxGeometry(0.3, 0.025, 0.36).translate(0, 0.91, 0)]),
  non: new THREE.ConeGeometry(0.3, 0.17, 16).translate(0, 0.86, 0),
  hair: new THREE.SphereGeometry(0.075, 10, 8).translate(0, 0.79, -0.07),
  mortar: mergeGeometries([new THREE.CylinderGeometry(0.11, 0.12, 0.08, 12).translate(0, 0.8, 0), new THREE.BoxGeometry(0.34, 0.025, 0.34).translate(0, 0.85, 0)]),
  beard: new THREE.ConeGeometry(0.06, 0.2, 8).rotateX(Math.PI).translate(0, 0.58, 0.08),
  parasol: mergeGeometries([new THREE.CylinderGeometry(0.025, 0.025, 2.6, 6).translate(0, 1.3, 0), new THREE.ConeGeometry(0.85, 0.35, 16, 1, true).translate(0, 2.55, 0), new THREE.CylinderGeometry(0.86, 0.86, 0.22, 16, 1, true).translate(0, 2.3, 0)]),
  flag: mergeGeometries([new THREE.CylinderGeometry(0.025, 0.025, 2.8, 6).translate(0, 1.4, 0), new THREE.BoxGeometry(0.02, 1.2, 0.55).translate(0, 2.1, 0.3)]),
  chisel: new THREE.BoxGeometry(0.05, 0.05, 0.3).translate(0, -0.65, 0.12),
  staff: new THREE.CylinderGeometry(0.025, 0.03, 1.6, 6).translate(0, -0.2, 0.1),
};
const people = [];
function pickC(c, i) { return Array.isArray(c[0]) ? c[i % c.length] : c; }
function addPerson(o) { const C = COSTUME[o.costume || 'scholar']; const k = people.length;
  const hat = o.hat || (Array.isArray(C.hat) ? C.hat[Math.floor(rnd() * C.hat.length)] : C.hat);
  people.push({ ...o, C, hat, robe: o.robe || pickC(C.robe, Math.floor(rnd() * 97)), legs: o.legsC || pickC(C.legs, Math.floor(rnd() * 13)), ph: o.ph ?? R(0, 100), sc: (o.h || R(0.95, 1.05)) * (C.scale || 1), sp: o.speed ?? R(0.8, 1.2), vis: o.vis, k }); }
function crowd(o) { // vùng chữ nhật (đi lại / đứng) hoặc lưới (hàng lối)
  const cs = Array.isArray(o.costume) ? o.costume : [o.costume || 'scholar'];
  if (o.grid) { const G = o.grid; for (let r = 0; r < G.rows; r++) for (let c = 0; c < G.cols; c++) addPerson({ ...o, costume: cs[(r * G.cols + c) % cs.length], pos: [G.origin[0] + c * G.dx + R(-0.05, 0.05), G.origin[1] + r * G.dz], face: o.face ?? 0, still: true, grid: undefined }); return; }
  if (o.line) { const L = o.line, n = o.count; for (let i = 0; i < n; i++) { const u = n > 1 ? i / (n - 1) : 0.5; addPerson({ ...o, costume: cs[i % cs.length], pos: [lerp(L[0][0], L[1][0], u) + R(-0.3, 0.3), lerp(L[0][1], L[1][1], u) + R(-0.3, 0.3)], face: o.face ?? 0, still: true, line: undefined }); } return; }
  for (let i = 0; i < o.count; i++) { const along = rnd() < (o.alongZ ?? 0.6), x0 = R(o.rect[0], o.rect[2]), z0 = R(o.rect[1], o.rect[3]), L = R(6, 22);
    const x1 = along ? x0 + R(-1, 1) : clamp(x0 + (rnd() < 0.5 ? -L : L), o.rect[0], o.rect[2]), z1 = along ? clamp(z0 + (rnd() < 0.5 ? -L : L), o.rect[1], o.rect[3]) : z0 + R(-1, 1);
    addPerson({ ...o, costume: cs[i % cs.length], path: o.still ? null : [[x0, z0], [x1, z1]], pos: [x0, z0], face: o.face ?? R(0, 6.28), rect: undefined }); }
}
let PM = null;
function buildPeople() { if (!people.length) return; const n = people.length, mk = (geo, mat, cnt) => { const im = new THREE.InstancedMesh(geo, mat, Math.max(1, cnt)); for (let i = 0; i < Math.max(1, cnt); i++) im.setMatrixAt(i, ZERO); im.castShadow = true; im.receiveShadow = true; im.instanceMatrix.setUsage(THREE.DynamicDrawUsage); im.frustumCulled = false; scene.add(im); return im; };
  const cloth = () => new THREE.MeshStandardMaterial({ roughness: 0.8, color: 0xffffff });
  PM = { robeL: mk(PG.robeL, cloth(), n), robeS: mk(PG.robeS, cloth(), n), head: mk(PG.head, new THREE.MeshStandardMaterial({ color: 0xc8996f, roughness: 0.7 }), n), arm: mk(PG.arm, cloth(), n * 2), leg: mk(PG.leg, cloth(), n * 2) };
  const hatMat = { khan: 0x141010, quan: 0x0c0c0c, crown: 0xc8a050, non: 0xd8c48a, hair: 0x101010, mortar: 0x0b0b0d, bald: 0, beard: 0xe8e4dc };
  for (const h of ['khan', 'quan', 'crown', 'non', 'hair', 'mortar', 'beard']) PM[h] = mk(PG[h], new THREE.MeshStandardMaterial({ color: hatMat[h], roughness: h === 'crown' ? 0.35 : 0.8, metalness: h === 'crown' ? 0.6 : 0 }), people.filter(p => p.hat === h || (h === 'beard' && p.C.beard) || (h === 'hair' && p.C.slim)).length);
  for (const h of ['parasol', 'flag', 'chisel', 'staff']) PM[h] = mk(PG[h], new THREE.MeshStandardMaterial({ color: h === 'parasol' ? 0xd6a02c : h === 'flag' ? 0xb82418 : 0x6b5a40, roughness: 0.7, side: THREE.DoubleSide }), people.filter(p => p.carry === h).length);
  const col = new THREE.Color();
  people.forEach((p, i) => { PM.robeL.setColorAt(i, col.setRGB(...p.robe)); PM.robeS.setColorAt(i, col.setRGB(...p.robe)); PM.arm.setColorAt(2 * i, col); PM.arm.setColorAt(2 * i + 1, col);
    PM.leg.setColorAt(2 * i, col.setRGB(...p.legs)); PM.leg.setColorAt(2 * i + 1, col); });
}
const _M = new THREE.Matrix4(), _Q = new THREE.Quaternion(), _E = new THREE.Euler(), _V = new THREE.Vector3(), _S = new THREE.Vector3(), _P = new THREE.Matrix4(), _H = new THREE.Matrix4(), _L = new THREE.Matrix4(), ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
function inWin(win, t) { if (!win) return true; const W = typeof win[0] === 'number' ? [win] : win; return W.some(w => t >= w[0] && t < w[1]); }
function updatePeople(t) { if (!PM) return; const cnt = {};
  const put = (key, m) => { const i = cnt[key] = (cnt[key] ?? -1) + 1; PM[key].setMatrixAt(i, m); };
  people.forEach((p, i) => {
    const vis = inWin(p.vis, t); let x = p.pos[0], z = p.pos[1], ang = p.face ?? 0, moving = false;
    if (vis && p.path && p.sp > 0) { const pts = p.path; let L = 0; const seg = []; for (let k = 0; k < pts.length - 1; k++) { const l = Math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]); seg.push(l); L += l; }
      const t0 = p.t0 ?? 0; let d = Math.max(0, t - t0) * p.sp + (p.once ? 0 : p.ph); let dir = 1;
      if (p.once) d = Math.min(d, L); else { d = d % (2 * L); if (d > L) { d = 2 * L - d; dir = -1; } }
      moving = !(p.once && d >= L);
      let k = 0; while (k < seg.length - 1 && d > seg[k]) { d -= seg[k]; k++; } const u = seg[k] ? d / seg[k] : 0, A = pts[k], B = pts[k + 1];
      x = lerp(A[0], B[0], u); z = lerp(A[1], B[1], u); ang = Math.atan2((B[0] - A[0]) * dir, (B[1] - A[1]) * dir); }
    const pose = moving ? (p.pose === 'carry' ? 'carry' : 'walk') : (p.pose || 'stand'); const s = p.sc, ph = t * (p.sp * 4.2) + p.ph;
    const kneel = pose === 'kneel' || pose === 'write' || pose === 'hammer'; const y0 = groundH(x, z) + (p.y || 0) + (kneel ? -0.42 : 0) + (pose === 'walk' || pose === 'carry' ? Math.abs(Math.sin(ph)) * 0.035 : 0);
    if (!vis) { for (const key of ['robeL', 'robeS', 'head']) put(key, ZERO); put('arm', ZERO); put('arm', ZERO); put('leg', ZERO); put('leg', ZERO);
      if (p.hat !== 'bald') put(p.hat, ZERO); if (p.C.beard) put('beard', ZERO); if (p.C.slim && p.hat !== 'hair') put('hair', ZERO); if (p.carry) put(p.carry, ZERO); return; }
    _Q.setFromAxisAngle(_V.set(0, 1, 0), ang); _P.compose(_V.set(x, y0, z), _Q, _S.set(s, s, s));
    const bow = pose === 'bow' ? 0.55 * (0.5 + 0.5 * Math.sin(t * 1.6 + p.ph)) : pose === 'write' ? 0.25 : kneel ? 0.08 : 0;
    _H.copy(_P).multiply(_L.makeTranslation(0, 0.85, 0)).multiply(new THREE.Matrix4().makeRotationX(bow));
    const robeKey = p.C.long ? 'robeL' : 'robeS';
    put(robeKey, kneel ? _M.copy(_H).multiply(new THREE.Matrix4().compose(_V.set(0, 0.2, 0.05), _Q.identity(), _S.set(1.15, 0.62, 1.2))) : _H);
    put(robeKey === 'robeL' ? 'robeS' : 'robeL', ZERO);
    put('head', _H); if (p.hat !== 'bald') put(p.hat, _H); if (p.C.beard) put('beard', _H); if (p.C.slim && p.hat !== 'hair') put('hair', _H);
    // arms
    let aL = 0.08, aR = 0.08, zL = 0.12, zR = -0.12;
    if (pose === 'walk') { aL = Math.sin(ph) * 0.45; aR = -aL; }
    else if (pose === 'carry') { aL = aR = -1.15; }
    else if (pose === 'write') { aR = -0.95 + Math.sin(t * 6 + p.ph) * 0.05; aL = -0.6; }
    else if (pose === 'teach') { aR = -1.2 + Math.sin(t * 2.2 + p.ph) * 0.35; zR = -0.35; aL = -0.25; }
    else if (pose === 'hammer') { aR = -1.4 + Math.abs(Math.sin(t * 7 + p.ph)) * 0.9; aL = -1.1; }
    else if (pose === 'bow' || pose === 'stand' || pose === 'kneel') { aL = aR = pose === 'stand' ? -0.25 : -0.55; zL = 0.32; zR = -0.32; }
    for (const [sd, a, zz] of [[1, aL, zL], [-1, aR, zR]]) { _M.copy(_H).multiply(_L.makeTranslation(sd * 0.24, 0.47, 0)).multiply(new THREE.Matrix4().makeRotationFromEuler(_E.set(a, 0, zz))); put('arm', _M);
      if (sd === -1 && p.carry === 'chisel') put('chisel', _M); }
    // legs
    for (const sd of [1, -1]) { let a = 0; if (pose === 'walk' || pose === 'carry') a = Math.sin(ph) * 0.42 * sd; if (kneel) a = -1.45;
      _M.copy(_P).multiply(_L.makeTranslation(sd * 0.09, 0.85 + (kneel ? 0.25 : 0), 0)).multiply(new THREE.Matrix4().makeRotationX(a)); put('leg', _M); }
    if (p.carry === 'parasol' || p.carry === 'flag' || p.carry === 'staff') { if (p.carry === 'staff') { _M.copy(_H).multiply(_L.makeTranslation(-0.3, 0.2, 0.12)); put('staff', _M); }
      else { _M.copy(_P).multiply(_L.makeTranslation(-0.32, 0.3, 0.15)); put(p.carry, _M); } }
  });
  for (const k in PM) PM[k].instanceMatrix.needsUpdate = true;
}

// ---------- birds ----------
const birdGeo = new THREE.BufferGeometry(); birdGeo.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0.3, -0.9, 0.25, -0.1, 0, 0, -0.25, 0, 0, 0.3, 0.9, 0.25, -0.1, 0, 0, -0.25], 3)); birdGeo.computeVertexNormals();
const flocks = [];
function birds(o) { const im = new THREE.InstancedMesh(birdGeo, new THREE.MeshBasicMaterial({ color: 0x2a2620, side: THREE.DoubleSide }), o.count); im.frustumCulled = false; scene.add(im);
  flocks.push({ ...o, im, off: Array.from({ length: o.count }, () => [R(-1, 1) * (o.spread || 12), R(-1, 1) * 3, R(-1, 1) * (o.spread || 12), R(0, 6)]) }); }
function updateBirds(t) { const m = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), s = new THREE.Vector3();
  for (const f of flocks) { const u = clamp((t - f.t0) / (f.t1 - f.t0)), dir = new THREE.Vector3(f.to[0] - f.from[0], 0, f.to[2] - f.from[2]).normalize();
    q.setFromUnitVectors(new THREE.Vector3(0, 0, 1), dir); const sc = f.size || 1.2;
    f.off.forEach((o, i) => { const p = lerp3(f.from, f.to, u); const flap = 0.25 + 0.75 * Math.abs(Math.sin(t * 9 + o[3]));
      m.compose(v.set(p[0] + o[0], p[1] + o[1] + Math.sin(t * 2 + o[3]) * 0.6, p[2] + o[2]), q, s.set(sc, sc * flap * (u > 0 && u < 1 ? 1 : 0), sc)); f.im.setMatrixAt(i, m); });
    f.im.instanceMatrix.needsUpdate = true; } }

// ---------- build world from spec ----------
const big = new THREE.Mesh(new THREE.PlaneGeometry(6400, 6400, 64, 64), groundMat(WD.groundMat || 'grass', 6400, 6400, 8)); big.rotation.x = -Math.PI / 2; big.position.y = -0.02; big.receiveShadow = true; scene.add(big);
(S.terrains || []).forEach(terrain);
(S.ground || []).forEach(groundPatch);
const KIT = { hall, gate, khueVanCac, wall, pond, box: boxProp, tents, desks, fence, scaffold, board, stela1, label, marker, route };
const SHOWN = [];   // {g, win, rise, base}
(S.buildings || []).forEach(b => {
  let g;
  if (b.type === 'stelae') { const im = stelae(b); g = new THREE.Group(); scene.remove(im); g.add(im); }
  else g = KIT[b.type](b);
  if (b.pos) { g.position.x += b.pos[0]; g.position.z += b.pos[b.pos.length - 1]; g.position.y += (b.pos.length === 3 ? b.pos[1] : 0) + (b.onGround ? groundH(b.pos[0], b.pos[b.pos.length - 1]) : 0); }
  if (b.rot) g.rotation.y = b.rot * Math.PI / 180;
  if (b.scale) g.scale.multiplyScalar(b.scale);
  scene.add(g); if (b.show) SHOWN.push({ g, win: typeof b.show[0] === 'number' ? [b.show] : b.show, rise: b.rise ?? 0, sink: b.sink ?? 0, base: g.scale.y, y0: g.position.y });
});
(S.trees || []).forEach(trees); buildTrees();
(S.houses || []).forEach(houses); buildHouses();
(S.crowds || []).forEach(crowd); (S.people || []).forEach(addPerson); buildPeople();
(S.birds || []).forEach(birds);
(S.lanterns || []).forEach(lanterns); buildLanterns();
renderer.shadowMap.needsUpdate = true;
function updateShown(t) { // công trình mọc lên từ nền (rise giây) và lún xuống khi hết khoảng hiển thị
  for (const s of SHOWN) { let k = 0; for (const w of s.win) { const [a, b] = w, ri = w[2] ?? s.rise, si = w[3] ?? s.sink; if (t >= a && t < b) k = Math.max(k, Math.min(ri > 0 ? ss(a, a + ri, t) : 1, si > 0 ? 1 - ss(b - si, b, t) : 1)); }
    s.g.visible = k > 0.003; s.g.scale.y = s.base * Math.max(0.003, k); }
  for (const m of GROW) { const g = m.userData.grow; const u = g ? clamp((t - g[0]) / (g[1] - g[0])) : 1; m.geometry.setDrawRange(0, Math.floor(m.userData.total * u / 3) * 3); m.visible = u > 0; }
}

// ---------- environment presets per shot ----------
const ENV = {
  day: { sun: WD.sun || [-0.55, 0.42, -0.3], sunColor: [1.0, 0.88, 0.7], sunPower: WD.sunPower || 3.2, ambient: 1.1, skyTop: [0.24, 0.4, 0.66], haze: [0.8, 0.74, 0.64], fog: WD.fog || 0.0012, exposure: 1.0, night: 0 },
  dawn: { sun: [0.75, 0.16, -0.25], sunColor: [1.0, 0.68, 0.45], sunPower: 2.4, ambient: 0.75, skyTop: [0.3, 0.38, 0.6], haze: [0.92, 0.72, 0.6], fog: 0.0026, exposure: 1.05, night: 0 },
  dusk: { sun: [-0.8, 0.12, 0.2], sunColor: [1.0, 0.55, 0.3], sunPower: 2.3, ambient: 0.65, skyTop: [0.22, 0.26, 0.5], haze: [0.9, 0.6, 0.45], fog: 0.0022, exposure: 1.05, night: 0.25 },
  night: { sun: [0.3, 0.6, 0.4], sunColor: [0.55, 0.65, 0.95], sunPower: 0.55, ambient: 0.32, skyTop: [0.02, 0.03, 0.08], haze: [0.07, 0.08, 0.14], fog: 0.0028, exposure: 1.25, night: 1 },
  mist: { sun: [0.5, 0.35, -0.4], sunColor: [0.95, 0.9, 0.82], sunPower: 1.6, ambient: 1.05, skyTop: [0.62, 0.66, 0.72], haze: [0.78, 0.8, 0.82], fog: 0.0024, exposure: 1.0, night: 0 },
  gray: { sun: [-0.3, 0.6, -0.3], sunColor: [0.85, 0.85, 0.85], sunPower: 1.4, ambient: 0.9, skyTop: [0.45, 0.48, 0.52], haze: [0.62, 0.62, 0.62], fog: 0.0025, exposure: 0.95, night: 0 },
  map: { sun: [-0.45, 0.6, -0.25], sunColor: [1.0, 0.92, 0.8], sunPower: 3.0, ambient: 0.85, skyTop: [0.3, 0.45, 0.7], haze: [0.7, 0.76, 0.84], fog: 0.00009, exposure: 1.0, night: 0 },
  inside: { sun: [-0.4, 0.5, 0.6], sunColor: [1.0, 0.85, 0.65], sunPower: 2.6, ambient: 0.95, skyTop: [0.3, 0.45, 0.7], haze: [0.75, 0.7, 0.62], fog: 0.0015, exposure: 1.15, night: 0 },
};
const _c1 = new THREE.Color(), _c2 = new THREE.Color();
function mixEnv(a, b, u) { const o = {}; for (const k in a) o[k] = Array.isArray(a[k]) ? a[k].map((v, i) => lerp(v, b[k][i], u)) : lerp(a[k], b[k], u); return o; }
let NIGHT = 0;
function applyEnv(E, look) {
  const sd = new THREE.Vector3(...E.sun).normalize(); SUN.copy(sd);
  sunL.color.setRGB(...E.sunColor); sunL.intensity = E.sunPower; hemi.intensity = E.ambient;
  hemi.color.setRGB(...(E.night > 0.5 ? [0.35, 0.42, 0.7] : WD.skyLight || [0.65, 0.75, 0.95]));
  sky.material.uniforms.top.value.setRGB(...E.skyTop); HAZE.setRGB(...E.haze); scene.fog.color.copy(HAZE); scene.fog.density = E.fog;
  sky.material.uniforms.night.value = E.night; renderer.toneMappingExposure = E.exposure * (Q.exposure || 1);
  sunL.target.position.set(look[0], 0, look[2]); sunL.position.set(look[0] + sd.x * 500, sd.y * 500, look[2] + sd.z * 500); sunL.target.updateMatrixWorld();
  NIGHT = E.night;
}

// ---------- camera ----------
function camForTime(t) {
  const sh = S.shots.find(s => t >= s.t0 && t < s.t1) || S.shots[S.shots.length - 1];
  const c = sh.cam, u = (EASE[c.ease || 'inout'])(clamp((t - sh.t0) / sh.dur));
  let pos, look;
  if (c.orbit) { const o = c.orbit, a = (lerp(o.a[0], o.a[1], u)) * Math.PI / 180, r = Array.isArray(o.r) ? lerp(o.r[0], o.r[1], u) : o.r, y = Array.isArray(o.y) ? lerp(o.y[0], o.y[1], u) : o.y;
    pos = [o.center[0] + Math.sin(a) * r, y, o.center[2] + Math.cos(a) * r]; look = o.look ? lerp3(o.look[0], o.look[1] || o.look[0], u) : o.center; }
  else if (c.path) { const P = new THREE.CatmullRomCurve3(c.path.map(k => new THREE.Vector3(...k.pos))), L = new THREE.CatmullRomCurve3(c.path.map(k => new THREE.Vector3(...k.look)));
    pos = P.getPoint(u).toArray(); look = L.getPoint(u).toArray(); }
  else { pos = lerp3(c.from.pos, c.to ? c.to.pos : c.from.pos, u); look = lerp3(c.from.look, c.to ? c.to.look : c.from.look, u); }
  if (c.ground) { pos[1] += groundH(pos[0], pos[2]) + (c.yOff ?? 2.4); look[1] += groundH(look[0], look[2]) + 1.6; }
  pos[1] += Math.sin(t * 0.8) * 0.03;
  const fov = c.fov ? (Array.isArray(c.fov) ? lerp(c.fov[0], c.fov[1], u) : c.fov) : 45;
  camera.position.set(...pos); camera.lookAt(...look); camera.fov = fov; camera.far = c.far || 9000; camera.updateProjectionMatrix();
  sky.position.copy(camera.position); clouds.position.set(camera.position.x, 0, camera.position.z);
  big.visible = !OCEANS.some(o => Math.abs(camera.position.x - o.cx) < o.w * 3 && Math.abs(camera.position.z - o.cz) < o.d * 1.5); big.position.x = Math.round(camera.position.x / 8) * 8; big.position.z = Math.round(camera.position.z / 8) * 8;
  const tilt = c.tilt ?? 0.6, tv = Array.isArray(tilt) ? lerp(tilt[0], tilt[1], u) : tilt, focus = c.focus ?? 0.55;
  tiltH.uniforms.h.value = tv * 3.2 / W; tiltV.uniforms.v.value = tv * 3.2 / H; tiltH.uniforms.r.value = tiltV.uniforms.r.value = focus;
  let E = ENV[sh.env || 'day']; if (sh.env2) E = mixEnv(E, ENV[sh.env2], u); applyEnv(E, look);
  const sr = sh.shadow || c.shadow || 120; Object.assign(sunL.shadow.camera, { left: -sr, right: sr, top: sr, bottom: -sr }); sunL.shadow.camera.updateProjectionMatrix();
  return sh;
}

// ---------- overlay: vignette, letterbox, captions, subtitles, fades ----------
function wrap(text, maxW) { const words = text.split(' '), lines = []; let cur = ''; for (const w of words) { const t2 = cur ? cur + ' ' + w : w; if (ctx.measureText(t2).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t2; } if (cur) lines.push(cur); return lines; }
function drawOverlay(sh, t) {
  ctx.clearRect(0, 0, W, H);
  const g = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.4, W / 2, H / 2, Math.max(W, H) * 0.65);
  g.addColorStop(0, 'rgba(20,12,4,0)'); g.addColorStop(1, 'rgba(20,12,4,0.42)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  if (S.letterbox !== false) { const lb = Math.round(H * 0.061); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, lb); ctx.fillRect(0, H - lb, W, lb); }
  const k = H / 1080, left = W > H, maxW = W - 2 * 80 * k;
  for (const c of sh.captions || []) {
    const lt = t - sh.t0, at = c.at || 0, du = c.dur || (sh.dur - at), a = ss(at, at + 0.8, lt) * (1 - ss(at + du - 0.6, at + du, lt)); if (a <= 0) continue;
    const rise = (1 - ss(at, at + 1.2, lt)) * 14 * k;
    ctx.globalAlpha = a; ctx.shadowColor = 'rgba(0,0,0,0.75)'; ctx.shadowBlur = 22 * k;
    if (c.style === 'title') { ctx.textAlign = 'center'; ctx.save(); ctx.shadowBlur = 0; const bg = ctx.createRadialGradient(W / 2, H * 0.36, 0, W / 2, H * 0.36, W * 0.38); bg.addColorStop(0, 'rgba(15,8,2,0.55)'); bg.addColorStop(1, 'rgba(15,8,2,0)'); ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H); ctx.restore();
      let y = H * 0.3 + rise;
      if (c.over) { ctx.font = `500 ${30 * k | 0}px Lora`; ctx.fillStyle = '#e9dcc0'; ctx.fillText(c.over, W / 2, y - (c.cn ? 110 : 70) * k); }
      if (c.cn) { ctx.fillStyle = '#fbf1da'; ctx.font = `700 ${96 * k | 0}px "Noto Serif CJK SC"`; ctx.fillText(c.cn, W / 2, y); y += 88 * k; }
      ctx.font = `600 ${56 * k | 0}px Lora`; ctx.fillStyle = '#f1d9a0'; for (const ln of wrap(c.text, maxW)) { ctx.fillText(ln, W / 2, y); y += 64 * k; }
      if (c.sub) { ctx.font = `italic 400 ${30 * k | 0}px Lora`; ctx.fillStyle = '#f3ead6'; for (const ln of wrap(c.sub, maxW)) { ctx.fillText(ln, W / 2, y - 8 * k); y += 40 * k; } }
    } else if (c.style === 'year') { ctx.textAlign = 'left'; const x = 110 * k; let y = 190 * k + rise;
      ctx.fillStyle = '#f1d9a0'; ctx.font = `600 ${96 * k | 0}px Lora`; ctx.fillText(c.year, x, y); y += 52 * k;
      ctx.fillStyle = '#fbf3e2'; ctx.font = `500 ${32 * k | 0}px Lora`; for (const ln of wrap(c.text, W * 0.45)) { ctx.fillText(ln, x, y); y += 40 * k; } }
    else { ctx.textAlign = 'left'; const x = 110 * k; let y = 150 * k + rise; ctx.fillStyle = '#fbf3e2'; ctx.font = `600 ${34 * k | 0}px Lora`; for (const ln of wrap(c.text, W * 0.5)) { ctx.fillText(ln, x, y); y += 42 * k; }
      if (c.sub) { ctx.font = `italic 400 ${26 * k | 0}px Lora`; ctx.fillStyle = '#e9dcc0'; for (const ln of wrap(c.sub, W * 0.5)) { ctx.fillText(ln, x, y); y += 34 * k; } } }
    ctx.shadowBlur = 0; ctx.globalAlpha = 1;
  }
  // phụ đề lời đọc (giữa, dưới), tự xuống dòng trong lề 80 px
  for (const sb of S.subs || []) { if (t < sb.t0 || t >= sb.t1) continue; const a = ss(sb.t0, sb.t0 + 0.15, t) * (1 - ss(sb.t1 - 0.15, sb.t1, t));
    ctx.font = `500 ${36 * k | 0}px Lora`; const lines = wrap(sb.text, Math.min(maxW, 1500 * k)); const lh = 46 * k, y0 = H - Math.round(H * 0.061) - 26 * k - (lines.length - 1) * lh;
    ctx.globalAlpha = a; ctx.textAlign = 'center';
    for (let i = 0; i < lines.length; i++) { const tw = ctx.measureText(lines[i]).width; ctx.fillStyle = 'rgba(8,6,4,0.55)'; ctx.fillRect(W / 2 - tw / 2 - 16 * k, y0 + i * lh - 36 * k, tw + 32 * k, lh); ctx.fillStyle = '#fbf6ea'; ctx.fillText(lines[i], W / 2, y0 + i * lh); }
    ctx.globalAlpha = 1; }
  let fade = 0; const lt = t - sh.t0;
  if (sh.fadeIn) fade = Math.max(fade, 1 - ss(0, sh.fadeIn, lt));
  if (sh.fadeOut) fade = Math.max(fade, ss(sh.dur - sh.fadeOut, sh.dur, lt));
  if (fade > 0) { ctx.fillStyle = `rgba(0,0,0,${fade})`; ctx.fillRect(0, 0, W, H); }
}
function render(t) {
  const sh = camForTime(t); updateShown(t); updatePeople(t); updateBirds(t); updateLanterns(NIGHT, t);
  renderer.shadowMap.needsUpdate = true;
  composer.render(); drawOverlay(sh, t);
}
let frame = 0;
window.DUR = DUR; window.FPS = FPS;
window.goto = function (target) { frame = target; render(frame / FPS); return frame; };
window.simAll = function () { return LOG; };
const comp = document.createElement('canvas'); comp.width = W; comp.height = H; const cctx = comp.getContext('2d');
window.grab = function (q) { cctx.drawImage(renderer.domElement, 0, 0); cctx.drawImage(ov, 0, 0); return comp.toDataURL('image/jpeg', q || 0.92); };
window.__dbg = { scene, THREE };
window.ready = true;
} catch (e) { window.__err = String(e && e.stack || e); console.error(e); }
