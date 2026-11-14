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
const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
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
const camera = new THREE.PerspectiveCamera(45, W / H, 0.5, 6000);
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
};
const groundMat = (k, sx, sz, tile = 4) => { const t = TEX[k].clone(); t.needsUpdate = true; t.repeat.set(sx / tile, sz / tile); return new THREE.MeshStandardMaterial({ map: t, roughness: 0.95 }); };
function add(parent, geo, mat, x = 0, y = 0, z = 0, cast = true) { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = cast; m.receiveShadow = true; parent.add(m); return m; }
function boxUV(w, h, d, s = 3) { const g = new THREE.BoxGeometry(w, h, d); const uv = g.attributes.uv, n = g.attributes.normal;
  for (let i = 0; i < uv.count; i++) { const ax = Math.abs(n.getX(i)), ay = Math.abs(n.getY(i)); const a = ax > 0.5 ? [d, h] : ay > 0.5 ? [w, d] : [w, h]; uv.setXY(i, uv.getX(i) * a[0] / s, uv.getY(i) * a[1] / s); } return g; }

// ---------- sky / light ----------
const SUN = new THREE.Vector3(...(WD.sun || [-0.55, 0.42, -0.35])).normalize();
const sky = new THREE.Mesh(new THREE.SphereGeometry(5000, 32, 16), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false, fog: false,
  uniforms: { sun: { value: SUN }, top: { value: new THREE.Color(...(WD.skyTop || [0.22, 0.38, 0.62])) }, hor: { value: HAZE } },
  vertexShader: `varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `uniform vec3 sun, top, hor; varying vec3 vD; void main(){ float y = clamp(vD.y,0.,1.);
    vec3 c = mix(hor, top, pow(smoothstep(0.,0.6,y),0.7)); float s = max(dot(vD,sun),0.);
    c += vec3(1.,0.8,0.55)*(pow(s,6.)*0.35 + pow(s,60.)*0.8) + vec3(1.,0.95,0.85)*pow(s,2500.)*30.;
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
for (let i = 0; i < (WD.clouds ?? 14); i++) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: cloudTex, color: 0xfff4e6, transparent: true, opacity: 0.75, fog: false, depthWrite: false }));
  const a = R(0, Math.PI * 2), d = R(900, 1800); sp.position.set(SC[0] + Math.cos(a) * d, R(220, 420), SC[2] + Math.sin(a) * d); sp.scale.set(R(400, 800), R(130, 220), 1); scene.add(sp); }

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
  add(grp, R0.g, M.tile); const u = add(grp, R0.g, M.under, 0, -0.14, 0, false);
  for (const c of R0.corners) { add(grp, new THREE.TubeGeometry(new THREE.CatmullRomCurve3(c.map(v => v.clone().add(new THREE.Vector3(0, 0.12, 0)))), 12, 0.17, 5), M.ridge);
    const tip = c[0], dir = new THREE.Vector3(tip.x, 0, tip.z).normalize(); // curled đầu đao tip
    const curve = new THREE.CatmullRomCurve3([tip.clone(), tip.clone().add(dir.clone().multiplyScalar(0.5)).add(new THREE.Vector3(0, 0.45, 0)), tip.clone().add(dir.clone().multiplyScalar(0.6)).add(new THREE.Vector3(0, 1.0, 0))]);
    add(grp, new THREE.TubeGeometry(curve, 8, 0.14, 5), M.ridge); }
  if ((o.r1 ?? 1) >= 1) {
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
    add(g, boxUV(w, ch - 0.6, 0.25), M.wood, 0, base + (ch - 0.6) / 2, -d / 2 + 0.05);
    add(g, boxUV(0.25, ch - 0.6, d), M.wood, -w / 2 + 0.05, base + (ch - 0.6) / 2, 0); add(g, boxUV(0.25, ch - 0.6, d), M.wood, w / 2 - 0.05, base + (ch - 0.6) / 2, 0);
    if (walls === 'all') { const inset = Math.min(1.8, d * 0.18); add(g, boxUV(w - 0.3, ch - 0.5, 0.15, 3.2), M.lattice, 0, base + (ch - 0.5) / 2, d / 2 - inset);
      add(g, boxUV(w - 0.3, 0.12, inset), M.wood, 0, base + ch - 0.06, d / 2 - inset / 2, false); }
  }
  const top = base + ch;
  if ((o.tiers || 1) === 1) roof(g, { w, d, h: o.roofH ?? Math.max(3, d * 0.45), ov: ovh, curl: o.curl ?? 0.9, pearl: o.pearl }, top);
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

// ---------- trees, houses (instanced) ----------
const treeTrunk = new THREE.CylinderGeometry(0.22, 0.38, 1, 7).translate(0, 0.5, 0);
const treeCrown = mergeGeometries([[0, 0, 0, 1], [0.55, -0.15, 0.2, 0.75], [-0.5, -0.1, -0.25, 0.8], [0.1, 0.35, -0.4, 0.7], [-0.15, -0.2, 0.55, 0.7]].map(([x, y, z, r]) => new THREE.IcosahedronGeometry(r, 1).translate(x, y, z)));
const treeList = [];
function trees(o) { for (let i = 0; i < o.count; i++) { let x, z, ok = false; for (let k = 0; k < 30 && !ok; k++) { x = R(o.rect[0], o.rect[2]); z = R(o.rect[1], o.rect[3]); ok = !(o.avoid || []).some(r => inRect(x, z, r, 1.5)); }
  if (ok) treeList.push({ x, z, h: R(...(o.h || [7, 14])), c: R(0, 1), lean: R(-0.08, 0.08) }); } }
function buildTrees() { if (!treeList.length) return; const n = treeList.length;
  const tr = new THREE.InstancedMesh(treeTrunk, new THREE.MeshStandardMaterial({ color: 0x4a3a2c, roughness: 1 }), n), cr = new THREE.InstancedMesh(treeCrown, new THREE.MeshStandardMaterial({ roughness: 0.9, flatShading: true }), n);
  tr.castShadow = cr.castShadow = true; tr.receiveShadow = cr.receiveShadow = true; const m = new THREE.Matrix4(), q = new THREE.Quaternion(), col = new THREE.Color();
  treeList.forEach((t, i) => { q.setFromEuler(new THREE.Euler(t.lean, t.c * 6, -t.lean)); m.compose(new THREE.Vector3(t.x, 0, t.z), q, new THREE.Vector3(1, t.h * 0.55, 1)); tr.setMatrixAt(i, m);
    const s = t.h * 0.33; m.compose(new THREE.Vector3(t.x + t.lean * t.h * 0.5, t.h * 0.62, t.z), q, new THREE.Vector3(s * 1.15, s * 0.85, s * 1.15)); cr.setMatrixAt(i, m);
    col.setHSL(0.22 + t.c * 0.08, 0.38 + t.c * 0.15, 0.2 + t.c * 0.1); cr.setColorAt(i, col); });
  scene.add(tr); scene.add(cr); }
const houseList = [];
function houses(o) { for (let i = 0; i < o.count; i++) { let x, z, ok = false; for (let k = 0; k < 40 && !ok; k++) { x = R(o.rect[0], o.rect[2]); z = R(o.rect[1], o.rect[3]); ok = !(o.avoid || []).some(r => inRect(x, z, r, 4)); }
  if (ok) houseList.push({ x, z, w: R(5, 10), d: R(8, 14), h: R(3.5, 10), rot: (rnd() < 0.5 ? 0 : Math.PI / 2) + R(-0.05, 0.05), c: rnd() }); } }
function buildHouses() { if (!houseList.length) return; const n = houseList.length;
  const body = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1).translate(0, 0.5, 0), new THREE.MeshStandardMaterial({ roughness: 0.95 }), n);
  const rf = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.01, 0.75, 1, 4, 1).rotateY(Math.PI / 4).translate(0, 0.5, 0), new THREE.MeshStandardMaterial({ roughness: 0.8 }), n);
  body.castShadow = rf.castShadow = body.receiveShadow = rf.receiveShadow = true; const m = new THREE.Matrix4(), q = new THREE.Quaternion(), col = new THREE.Color();
  const walls = [[0.88, 0.8, 0.6], [0.9, 0.86, 0.78], [0.82, 0.72, 0.52], [0.75, 0.75, 0.72]], roofs = [[0.45, 0.2, 0.14], [0.35, 0.3, 0.28], [0.5, 0.28, 0.18]];
  houseList.forEach((h, i) => { q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), h.rot); m.compose(new THREE.Vector3(h.x, 0, h.z), q, new THREE.Vector3(h.w, h.h, h.d)); body.setMatrixAt(i, m);
    m.compose(new THREE.Vector3(h.x, h.h, h.z), q, new THREE.Vector3(h.w * 1.25, 2.4, h.d * 1.15)); rf.setMatrixAt(i, m);
    body.setColorAt(i, col.setRGB(...walls[Math.floor(h.c * 4)])); rf.setColorAt(i, col.setRGB(...roofs[Math.floor(h.c * 3)])); });
  scene.add(body); scene.add(rf); }

// ---------- people & birds ----------
const personParts = [
  [mergeGeometries([new THREE.CylinderGeometry(0.16, 0.34, 1.15, 10).translate(0, 0.58, 0), new THREE.CylinderGeometry(0.2, 0.17, 0.35, 10).translate(0, 1.3, 0)]), 'robe'],
  [new THREE.SphereGeometry(0.12, 10, 8).translate(0, 1.6, 0), 'skin'],
  [mergeGeometries([new THREE.CylinderGeometry(0.13, 0.14, 0.12, 10).translate(0, 1.71, 0), new THREE.SphereGeometry(0.1, 8, 6).translate(0, 1.66, -0.07)]), 'hat']];
const people = [];
function crowd(o) { for (let i = 0; i < o.count; i++) { const along = rnd() < (o.alongZ ?? 0.6);
  const x0 = R(o.rect[0], o.rect[2]), z0 = R(o.rect[1], o.rect[3]); const L = R(6, 22);
  const x1 = along ? x0 + R(-1, 1) : clamp(x0 + (rnd() < 0.5 ? -L : L), o.rect[0], o.rect[2]), z1 = along ? clamp(z0 + (rnd() < 0.5 ? -L : L), o.rect[1], o.rect[3]) : z0 + R(-1, 1);
  people.push({ a: [x0, z0], b: [x1, z1], sp: o.still ? 0 : R(0.7, 1.3), ph: R(0, 100), h: R(1.55, 1.8), c: Math.floor(rnd() * 5), still: o.still, face: R(0, 6.28) }); } }
let PM = [];
function buildPeople() { if (!people.length) return; const robes = [[0.12, 0.16, 0.32], [0.35, 0.22, 0.14], [0.85, 0.82, 0.74], [0.1, 0.1, 0.1], [0.25, 0.3, 0.45]];
  PM = personParts.map(([geo, k]) => { const im = new THREE.InstancedMesh(geo, new THREE.MeshStandardMaterial({ roughness: 0.8, color: k === 'skin' ? 0xc89a74 : k === 'hat' ? 0x141010 : 0xffffff }), people.length);
    im.castShadow = true; im.instanceMatrix.setUsage(THREE.DynamicDrawUsage); im.frustumCulled = false; if (k === 'robe') people.forEach((p, i) => im.setColorAt(i, new THREE.Color(...robes[p.c]))); scene.add(im); return im; }); }
function updatePeople(t) { if (!PM.length) return; const m = new THREE.Matrix4(), q = new THREE.Quaternion(), v = new THREE.Vector3(), s = new THREE.Vector3();
  people.forEach((p, i) => { const L = Math.hypot(p.b[0] - p.a[0], p.b[1] - p.a[1]) || 1; let u = 0, dir = 1;
    if (!p.still) { const d = (t * p.sp + p.ph) % (2 * L); u = d < L ? d / L : 2 - d / L; dir = d < L ? 1 : -1; }
    const x = lerp(p.a[0], p.b[0], u), z = lerp(p.a[1], p.b[1], u), ang = p.still ? p.face : Math.atan2((p.b[0] - p.a[0]) * dir, (p.b[1] - p.a[1]) * dir);
    const bob = p.still ? 0 : Math.abs(Math.sin(t * p.sp * 5 + p.ph)) * 0.04;
    q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), ang); m.compose(v.set(x, 0.03 + bob + (p.y || 0), z), q, s.setScalar(p.h / 1.75)); PM.forEach(im => im.setMatrixAt(i, m)); });
  PM.forEach(im => { im.instanceMatrix.needsUpdate = true; }); }
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
const big = new THREE.Mesh(new THREE.PlaneGeometry(6000, 6000), groundMat(WD.groundMat || 'dirt', 6000, 6000, 8)); big.rotation.x = -Math.PI / 2; big.receiveShadow = true; scene.add(big);
(S.ground || []).forEach(groundPatch);
const KIT = { hall, gate, khueVanCac, wall, pond };
(S.buildings || []).forEach(b => { if (b.type === 'stelae') return stelae(b); const g = KIT[b.type](b); g.position.x += b.pos ? b.pos[0] : 0; g.position.z += b.pos ? b.pos[b.pos.length - 1] : 0;
  if (b.rot) g.rotation.y = b.rot * Math.PI / 180; scene.add(g); });
(S.trees || []).forEach(trees); buildTrees();
(S.houses || []).forEach(houses); buildHouses();
(S.crowds || []).forEach(crowd); buildPeople();
(S.birds || []).forEach(birds);
renderer.shadowMap.needsUpdate = true;

// ---------- camera ----------
function camForTime(t) {
  const sh = S.shots.find(s => t >= s.t0 && t < s.t1) || S.shots[S.shots.length - 1];
  const c = sh.cam, u = (EASE[c.ease || 'inout'])(clamp((t - sh.t0) / sh.dur));
  let pos, look;
  if (c.orbit) { const o = c.orbit, a = (lerp(o.a[0], o.a[1], u)) * Math.PI / 180, r = Array.isArray(o.r) ? lerp(o.r[0], o.r[1], u) : o.r, y = Array.isArray(o.y) ? lerp(o.y[0], o.y[1], u) : o.y;
    pos = [o.center[0] + Math.sin(a) * r, y, o.center[2] + Math.cos(a) * r]; look = o.look ? lerp3(o.look[0], o.look[1] || o.look[0], u) : o.center; }
  else { pos = lerp3(c.from.pos, c.to ? c.to.pos : c.from.pos, u); look = lerp3(c.from.look, c.to ? c.to.look : c.from.look, u); }
  pos[1] += Math.sin(t * 0.8) * 0.04;
  const fov = c.fov ? (Array.isArray(c.fov) ? lerp(c.fov[0], c.fov[1], u) : c.fov) : 45;
  camera.position.set(...pos); camera.lookAt(...look); camera.fov = fov; camera.updateProjectionMatrix();
  sky.position.copy(camera.position);
  const tilt = c.tilt ?? 0.6, tv = Array.isArray(tilt) ? lerp(tilt[0], tilt[1], u) : tilt, focus = c.focus ?? 0.55;
  tiltH.uniforms.h.value = tv * 3.2 / W; tiltV.uniforms.v.value = tv * 3.2 / H; tiltH.uniforms.r.value = tiltV.uniforms.r.value = focus;
  return sh;
}

// ---------- overlay ----------
function drawOverlay(sh, t) {
  ctx.clearRect(0, 0, W, H);
  const g = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.4, W / 2, H / 2, Math.max(W, H) * 0.65);
  g.addColorStop(0, 'rgba(20,12,4,0)'); g.addColorStop(1, 'rgba(20,12,4,0.45)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  if (S.letterbox !== false) { const lb = Math.round(H * 0.061); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, lb); ctx.fillRect(0, H - lb, W, lb); }
  const k = H / 1080, left = W > H;
  for (const c of sh.captions || []) {
    const lt = t - sh.t0, at = c.at || 0, du = c.dur || (sh.dur - at), a = ss(at, at + 0.8, lt) * (1 - ss(at + du - 0.6, at + du, lt)); if (a <= 0) continue;
    const rise = (1 - ss(at, at + 1.2, lt)) * 14 * k;
    ctx.globalAlpha = a; ctx.shadowColor = 'rgba(0,0,0,0.75)'; ctx.shadowBlur = 22 * k;
    if (c.style === 'title') { ctx.textAlign = 'center'; ctx.save(); ctx.shadowBlur = 0; const bg = ctx.createRadialGradient(W / 2, H * 0.3 + 40 * k, 0, W / 2, H * 0.3 + 40 * k, W * 0.36); bg.addColorStop(0, 'rgba(15,8,2,0.5)'); bg.addColorStop(1, 'rgba(15,8,2,0)'); ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H); ctx.restore();
      if (c.cn) { ctx.fillStyle = '#fbf1da'; ctx.font = `700 ${96 * k | 0}px "Noto Serif CJK SC"`; ctx.fillText(c.cn, W / 2, H * 0.3 + rise); }
      ctx.font = `600 ${56 * k | 0}px Lora`; ctx.fillStyle = '#f1d9a0'; ctx.fillText(c.text, W / 2, H * 0.3 + 88 * k + rise);
      if (c.sub) { ctx.font = `italic 400 ${30 * k | 0}px Lora`; ctx.fillStyle = '#f3ead6'; ctx.fillText(c.sub, W / 2, H * 0.3 + 140 * k + rise); }
    } else if (c.style === 'year') { ctx.textAlign = left ? 'left' : 'center'; const x = left ? 120 * k : W / 2, y = H - 210 * k + rise;
      ctx.fillStyle = '#f1d9a0'; ctx.font = `600 ${104 * k | 0}px Lora`; ctx.fillText(c.year, x, y);
      ctx.fillStyle = '#fbf3e2'; ctx.font = `500 ${34 * k | 0}px Lora`; ctx.fillText(c.text, x, y + 56 * k);
      if (c.sub) { ctx.font = `italic 400 ${27 * k | 0}px Lora`; ctx.fillStyle = '#e9dcc0'; ctx.fillText(c.sub, x, y + 98 * k); }
    } else { ctx.textAlign = left ? 'left' : 'center'; const x = left ? 120 * k : W / 2;
      ctx.fillStyle = '#fbf3e2'; ctx.font = `500 ${34 * k | 0}px Lora`; ctx.fillText(c.text, x, H - 150 * k + rise);
      if (c.sub) { ctx.font = `italic 400 ${27 * k | 0}px Lora`; ctx.fillStyle = '#e9dcc0'; ctx.fillText(c.sub, x, H - 108 * k + rise); } }
    ctx.shadowBlur = 0; ctx.globalAlpha = 1;
  }
  let fade = 0; const lt = t - sh.t0;
  if (sh.fadeIn) fade = Math.max(fade, 1 - ss(0, sh.fadeIn, lt));
  if (sh.fadeOut) fade = Math.max(fade, ss(sh.dur - sh.fadeOut, sh.dur, lt));
  if (fade > 0) { ctx.fillStyle = `rgba(0,0,0,${fade})`; ctx.fillRect(0, 0, W, H); }
}
function render(t) {
  const sh = camForTime(t); updatePeople(t); updateBirds(t);
  renderer.shadowMap.needsUpdate = true;
  composer.render(); drawOverlay(sh, t);
}
let frame = 0;
window.DUR = DUR; window.FPS = FPS;
window.goto = function (target) { frame = target; render(frame / FPS); return frame; };
window.simAll = function () { return LOG; };
const comp = document.createElement('canvas'); comp.width = W; comp.height = H; const cctx = comp.getContext('2d');
window.grab = function (q) { cctx.drawImage(renderer.domElement, 0, 0); cctx.drawImage(ov, 0, 0); return comp.toDataURL('image/jpeg', q || 0.92); };
window.ready = true;
} catch (e) { window.__err = String(e && e.stack || e); console.error(e); }
