// ===== TQ VIDEO ENGINE v2 — Three.js (WebGL) renderer driven by window.SPEC =====
// Same JSON spec as v1. Real 3D meshes, PBR lighting, fire point lights, mirror-water reflections, bloom.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { FXAAPass } from 'three/addons/postprocessing/FXAAPass.js';
import { Reflector } from 'three/addons/objects/Reflector.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

try {
await document.fonts.load('700 100px "Noto Serif CJK SC"');

const S = window.SPEC;
const W = S.size[0], H = S.size[1], FPS = S.fps || 30;
const Q = S.quality || {};
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
const rgb = (a) => new THREE.Color(a[0] / 255, a[1] / 255, a[2] / 255).convertSRGBToLinear();
const colArr = c => Array.isArray(c) ? c : [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)];

// ---------- renderer / scene ----------
const host = document.getElementById('stage');
const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(1); renderer.setSize(W, H, false);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = Q.exposure || 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
host.appendChild(renderer.domElement);
const ov = document.createElement('canvas'); ov.width = W; ov.height = H; host.appendChild(ov);
const ctx = ov.getContext('2d');

const scene = new THREE.Scene();
const FOG = new THREE.FogExp2(0x101420, Q.fog || 0.0009); scene.fog = FOG;
const camera = new THREE.PerspectiveCamera(50, W / H, 0.3, 9000);

const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: Q.msaa || 0 });
const composer = new EffectComposer(renderer, rt);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), Q.bloom ?? 0.55, 0.45, 1.0);
composer.addPass(bloom);
composer.addPass(new OutputPass());
if (!(Q.msaa > 0)) composer.addPass(new FXAAPass());

// ---------- textures ----------
function canvasTex(w, h, draw, srgb = true) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); if (srgb) t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
const radial = (stops) => canvasTex(128, 128, (g, w) => { const gr = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2); stops.forEach(s => gr.addColorStop(s[0], s[1])); g.fillStyle = gr; g.fillRect(0, 0, w, w); }, false);
const TEX_SOFT = radial([[0, 'rgba(255,255,255,1)'], [0.25, 'rgba(255,255,255,0.75)'], [0.6, 'rgba(255,255,255,0.2)'], [1, 'rgba(255,255,255,0)']]);
const TEX_FLAME = canvasTex(64, 128, (g, w, h) => { // soft tear-drop flame
  g.save(); g.translate(w / 2, h * 0.62); g.scale(1, 2.1);
  const gr = g.createRadialGradient(0, 0.06 * h, 0, 0, 0, w * 0.5); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.3, 'rgba(255,255,255,0.55)'); gr.addColorStop(0.7, 'rgba(255,255,255,0.12)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(-w, -h, 2 * w, 2 * h); g.restore(); }, false);
const TEX_SMOKE = canvasTex(128, 128, (g, w) => {
  for (let i = 0; i < 14; i++) { const x = w / 2 + (Math.random() - 0.5) * w * 0.35, y = w / 2 + (Math.random() - 0.5) * w * 0.35, r = w * (0.18 + Math.random() * 0.18);
    const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, w); } }, false);
const TEX_WOOD = canvasTex(256, 256, (g, w, h) => {
  g.fillStyle = '#8a5d38'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 8; i++) { const y = i * h / 8; g.fillStyle = `rgb(${120 + Math.random() * 30 | 0},${80 + Math.random() * 20 | 0},${48 + Math.random() * 14 | 0})`; g.fillRect(0, y + 2, w, h / 8 - 3);
    g.fillStyle = 'rgba(30,18,10,0.9)'; g.fillRect(0, y, w, 2);
    for (let k = 0; k < 30; k++) { g.fillStyle = `rgba(50,30,15,${Math.random() * 0.25})`; g.fillRect(Math.random() * w, y + 3 + Math.random() * (h / 8 - 6), 20 + Math.random() * 60, 1); } }
});
TEX_WOOD.wrapS = TEX_WOOD.wrapT = THREE.RepeatWrapping;
function sailTex(col) {
  return canvasTex(128, 256, (g, w, h) => {
    g.fillStyle = `rgb(${col[0]},${col[1]},${col[2]})`; g.fillRect(0, 0, w, h);
    for (let k = 0; k < 400; k++) { g.fillStyle = `rgba(${Math.random() < 0.5 ? '0,0,0' : '255,240,210'},${Math.random() * 0.06})`; g.fillRect(Math.random() * w, Math.random() * h, 3 + Math.random() * 14, 2 + Math.random() * 6); }
    g.fillStyle = 'rgba(25,16,10,0.85)'; for (let i = 0; i <= 6; i++) g.fillRect(0, i / 6 * h - 3, w, 6); // battens
    g.fillStyle = 'rgba(40,26,16,0.35)'; for (let i = 1; i < 4; i++) g.fillRect(i / 4 * w - 1, 0, 2, h);
  });
}
function flagTex(col, ch) {
  return canvasTex(128, 96, (g, w, h) => {
    g.fillStyle = `rgb(${col[0]},${col[1]},${col[2]})`; g.fillRect(0, 0, w, h);
    g.strokeStyle = 'rgba(230,200,120,0.8)'; g.lineWidth = 5; g.strokeRect(6, 6, w - 12, h - 12);
    if (ch) { g.fillStyle = 'rgba(245,232,200,0.95)'; g.font = `700 ${h * 0.66 | 0}px "Noto Serif CJK SC"`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(ch, w / 2, h / 2 + 2); }
  });
}

// ---------- sky, stars, moon, mountains ----------
const sky = new THREE.Mesh(new THREE.SphereGeometry(6000, 32, 16), new THREE.ShaderMaterial({
  side: THREE.BackSide, depthWrite: false, fog: false,
  uniforms: { fn: { value: 0 } },
  vertexShader: `varying vec3 vD; void main(){ vD = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `uniform float fn; varying vec3 vD;
    float h(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
    void main(){ float y = clamp(vD.y,-0.2,1.);
      vec3 zen = mix(vec3(0.004,0.006,0.02), vec3(0.03,0.008,0.004), fn);
      vec3 hor = mix(vec3(0.03,0.035,0.075), vec3(0.3,0.08,0.025), fn);
      vec3 c = mix(hor, zen, pow(smoothstep(-0.02,0.55,y),0.6));
      // stars
      vec2 g = vec2(atan(vD.z,vD.x)*220., asin(clamp(vD.y,-1.,1.))*220.); vec2 id = floor(g); float r = h(id);
      if (r > 0.985 && vD.y > 0.06) { float d = length(fract(g)-0.5); c += vec3(0.8,0.85,1.)*smoothstep(0.25,0.,d)*(r-0.985)*60.*(1.-fn*0.8); }
      gl_FragColor = vec4(c,1.); }`
}));
sky.renderOrder = -10; scene.add(sky);
const MOON_DIR = new THREE.Vector3(2600, 1500, 3800).normalize();
const moon = new THREE.Group();
const moonGlow = new THREE.Sprite(new THREE.SpriteMaterial({ map: TEX_SOFT, color: new THREE.Color(0.35, 0.42, 0.7), transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, fog: false }));
moonGlow.scale.set(900, 900, 1); moon.add(moonGlow);
const moonDisk = new THREE.Sprite(new THREE.SpriteMaterial({ map: canvasTex(128, 128, (g, w) => { g.fillStyle = '#f2f3fa'; g.beginPath(); g.arc(w / 2, w / 2, w * 0.46, 0, 7); g.fill();
  g.fillStyle = 'rgba(160,165,185,0.45)'; [[0.4, 0.4, 0.1], [0.6, 0.58, 0.08], [0.45, 0.65, 0.06], [0.62, 0.35, 0.05]].forEach(([x, y, r]) => { g.beginPath(); g.arc(x * w, y * w, r * w, 0, 7); g.fill(); }); }),
  color: new THREE.Color(2.2, 2.2, 2.4), transparent: true, depthWrite: false, fog: false }));
moonDisk.scale.set(130, 130, 1); moon.add(moonDisk); scene.add(moon);

function ridgePts(z, xMin, xMax, base, amp, n, so) {
  const pts = []; for (let i = 0; i <= n; i++) { const x = lerp(xMin, xMax, i / n);
    const y = base + amp * (0.55 * Math.sin(x * 0.011 + so) + 0.3 * Math.sin(x * 0.031 + so * 2) + 0.15 * Math.sin(x * 0.09 + so * 3)) + amp * 0.12 * Math.sin(x * 0.23 + so * 5);
    pts.push([x, Math.max(0, y), z + Math.sin(x * 0.02 + so) * 20]); } return pts;
}
function ridgeMesh(pts, col) {
  const pos = [], idx = [];
  pts.forEach((p, i) => { pos.push(p[0], -4, p[2] + 30, p[0], p[1], p[2]); if (i) { const a = (i - 1) * 2; idx.push(a, a + 2, a + 1, a + 1, a + 2, a + 3); } });
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
  const m = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: col, side: THREE.DoubleSide })); scene.add(m); return m;
}
const farRidge = ridgeMesh(ridgePts(1300, -2400, 2600, 70, 90, 220, 1.3), 0x0b0d16);
const midRidge = ridgeMesh(ridgePts(620, -1200, 1400, 22, 38, 200, 4.1), 0x07080d);

// ---------- lights ----------
const hemi = new THREE.HemisphereLight(0x3a4a78, 0x050608, 0.55); scene.add(hemi);
const moonLight = new THREE.DirectionalLight(0x9fb2e8, 0.55); moonLight.position.copy(MOON_DIR).multiplyScalar(500); scene.add(moonLight);
const fireKey = new THREE.DirectionalLight(0xff8a3a, 0); scene.add(fireKey); scene.add(fireKey.target);
const NFL = 8, fireLights = [];
for (let i = 0; i < NFL; i++) { const l = new THREE.PointLight(0xff7a2a, 0, 0, 1.25); scene.add(l); fireLights.push(l); }

// ---------- water (mirror reflection + waves + fire glow) ----------
const WaterShader = {
  name: 'TQWater',
  uniforms: { color: { value: null }, tDiffuse: { value: null }, textureMatrix: { value: null }, uTime: { value: 0 }, uFires: { value: Array.from({ length: NFL }, () => new THREE.Vector4()) },
    uFogColor: { value: new THREE.Color() }, uFogDensity: { value: 0.001 }, uFn: { value: 0 }, uMoon: { value: MOON_DIR.clone() } },
  vertexShader: `uniform mat4 textureMatrix; varying vec4 vUv; varying vec3 vW;
    void main(){ vUv = textureMatrix*vec4(position,1.); vW = (modelMatrix*vec4(position,1.)).xyz; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uFogDensity, uFn; uniform vec3 uFogColor, uMoon; uniform vec4 uFires[${NFL}];
    varying vec4 vUv; varying vec3 vW;
    vec2 wv(vec2 p, vec2 d, float f, float s, float a){ float ph = dot(p,d)*f + uTime*s; return d*cos(ph)*a*f; }
    void main(){
      vec2 p = vW.xz; vec2 g = vec2(0.);
      g += wv(p, normalize(vec2(1.,0.25)), 0.19, 1.2, 0.12); g += wv(p, normalize(vec2(0.6,1.)), 0.33, 1.6, 0.1); g += wv(p, normalize(vec2(-0.3,1.)), 0.53, 1.9, 0.07); g += wv(p, normalize(vec2(1.,-0.6)), 0.97, 2.6, 0.04);
      g += wv(p, normalize(vec2(-0.8,0.5)), 0.71, 2.3, 0.06); g += wv(p, normalize(vec2(0.2,-1.)), 1.31, 3.1, 0.035);
      g += wv(p, normalize(vec2(1.,0.9)), 2.7, 4.3, 0.016); g += wv(p, normalize(vec2(-1.,0.3)), 1.9, 3.7, 0.02); g += wv(p, normalize(vec2(0.4,-1.)), 3.6, 5.1, 0.01);
      vec3 n = normalize(vec3(-g.x, 1., -g.y));
      vec3 V = normalize(cameraPosition - vW); float dist = length(cameraPosition - vW);
      vec2 uv = vUv.xy / vUv.w + n.xz * 0.045 * clamp(30./dist, 0.25, 1.);
      vec3 refl = texture2D(tDiffuse, uv).rgb;
      float fres = 0.04 + 0.96*pow(1. - max(dot(n,V),0.), 4.);
      vec3 deep = vec3(0.004,0.008,0.016);
      vec3 col = mix(deep, refl, clamp(fres*1.15+0.18,0.,1.));
      vec3 glow = vec3(0.); vec3 Rv = reflect(-V, n);
      for (int i=0;i<${NFL};i++){ vec4 f = uFires[i]; if (f.w<=0.) continue; vec3 L = f.xyz - vW; float d2 = dot(L.xz,L.xz);
        glow += vec3(1.,0.42,0.12) * f.w * 0.045 / (1. + d2/220.);
        glow += vec3(1.,0.5,0.15) * f.w * pow(max(dot(Rv, normalize(L)),0.), 60.) * 0.6 / (1. + d2/1800.); }
      col += glow;
      col += vec3(0.6,0.7,1.) * pow(max(dot(Rv, uMoon),0.), 300.) * 1.2 * (1.-uFn*0.85);
      float ff = 1. - exp(-pow(uFogDensity*dist,2.));
      gl_FragColor = vec4(mix(col, uFogColor, ff), 1.);
    }`
};
const water = new Reflector(new THREE.PlaneGeometry(14000, 14000), { shader: WaterShader, textureWidth: Math.round(W * (Q.reflScale || 0.5)), textureHeight: Math.round(H * (Q.reflScale || 0.5)), clipBias: 0.003, multisample: 0 });
water.rotation.x = -Math.PI / 2; scene.add(water);
const WU = water.material.uniforms;

// ---------- billboard particle layer ----------
class Layer {
  constructor(max, tex, additive, fogMode) {
    const g = new THREE.InstancedBufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute([-0.5, -0.5, 0, 0.5, -0.5, 0, 0.5, 0.5, 0, -0.5, 0.5, 0], 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute([0, 0, 1, 0, 1, 1, 0, 1], 2)); g.setIndex([0, 1, 2, 0, 2, 3]);
    this.p = new Float32Array(max * 3); this.c = new Float32Array(max * 4); this.s = new Float32Array(max * 3);
    g.setAttribute('iP', new THREE.InstancedBufferAttribute(this.p, 3)); g.setAttribute('iC', new THREE.InstancedBufferAttribute(this.c, 4)); g.setAttribute('iS', new THREE.InstancedBufferAttribute(this.s, 3));
    ['iP', 'iC', 'iS'].forEach(k => g.attributes[k].setUsage(THREE.DynamicDrawUsage));
    this.g = g; this.max = max; this.n = 0;
    this.m = new THREE.ShaderMaterial({
      transparent: true, depthWrite: false, blending: additive ? THREE.AdditiveBlending : THREE.NormalBlending,
      uniforms: { map: { value: tex }, fogColor: { value: FOG.color }, fogDensity: { value: FOG.density } },
      vertexShader: `attribute vec3 iP; attribute vec4 iC; attribute vec3 iS; varying vec2 vUv; varying vec4 vC; varying float vFd;
        void main(){ vUv = uv; vC = iC; vec4 mv = modelViewMatrix*vec4(iP,1.); float c = cos(iS.z), s = sin(iS.z);
          vec2 q = position.xy * vec2(iS.x, iS.y); mv.xy += vec2(c*q.x - s*q.y, s*q.x + c*q.y); vFd = -mv.z; gl_Position = projectionMatrix*mv; }`,
      fragmentShader: `uniform sampler2D map; uniform vec3 fogColor; uniform float fogDensity; varying vec2 vUv; varying vec4 vC; varying float vFd;
        void main(){ vec4 t = texture2D(map, vUv); float ff = 1. - exp(-pow(fogDensity*vFd,2.));
          ${additive ? 'gl_FragColor = vec4(vC.rgb * t.a * vC.a * (1.-ff), 1.);' : 'gl_FragColor = vec4(mix(vC.rgb, fogColor, ff), t.a*vC.a);'} }`
    });
    if (additive) { this.m.blending = THREE.CustomBlending; this.m.blendSrc = THREE.OneFactor; this.m.blendDst = THREE.OneFactor; }
    this.mesh = new THREE.Mesh(g, this.m); this.mesh.frustumCulled = false; scene.add(this.mesh);
  }
  begin() { this.n = 0; }
  push(x, y, z, w, h, rot, r, g, b, a) {
    if (this.n >= this.max) return; const i = this.n++;
    this.p[i * 3] = x; this.p[i * 3 + 1] = y; this.p[i * 3 + 2] = z; this.s[i * 3] = w; this.s[i * 3 + 1] = h; this.s[i * 3 + 2] = rot;
    this.c[i * 4] = r; this.c[i * 4 + 1] = g; this.c[i * 4 + 2] = b; this.c[i * 4 + 3] = a;
  }
  end() { this.g.instanceCount = this.n; ['iP', 'iC', 'iS'].forEach(k => { this.g.attributes[k].needsUpdate = true; }); this.m.uniforms.fogDensity.value = FOG.density; }
}
const LsSmoke = new Layer(5000, TEX_SMOKE, false);
const LsFire = new Layer(9000, TEX_FLAME, true);
const LsGlow = new Layer(2000, TEX_SOFT, true);
LsSmoke.mesh.renderOrder = 2; LsFire.mesh.renderOrder = 3; LsGlow.mesh.renderOrder = 4;

// ---------- fleets ----------
const WIND = (S.world && S.world.wind) || [5.5, 0, 1.2];
const fleets = {}, allShips = [];
const MAT_MAST = new THREE.MeshStandardMaterial({ color: 0x3a2818, roughness: 0.9 });
const MAT_ROPE = new THREE.MeshStandardMaterial({ color: 0x1a120c, roughness: 1 });

function hullGeo(L, B, h) {
  const bowY = h + 1.2, sternY = h + 1.6;
  const deck = [[-L / 2, sternY, -B / 2 * 0.9], [L / 2 * 0.7, h, -B / 2], [L / 2, bowY, 0], [L / 2 * 0.7, h, B / 2], [-L / 2, sternY, B / 2 * 0.9]];
  const keel = [[-L / 2 * 0.85, -0.6, -B / 4], [L / 2 * 0.6, -0.6, -B / 4], [L / 2 * 0.9, 0.2, 0], [L / 2 * 0.6, -0.6, B / 4], [-L / 2 * 0.85, -0.6, B / 4]];
  const pos = [], uv = [];
  const quad = (a, b, c, d, len) => { pos.push(...a, ...b, ...c, ...a, ...c, ...d); uv.push(0, 1, len / 6, 1, len / 6, 0, 0, 1, len / 6, 0, 0, 0); };
  for (let i = 0; i < 5; i++) { const j = (i + 1) % 5; const len = Math.hypot(deck[j][0] - deck[i][0], deck[j][2] - deck[i][2]);
    quad(deck[j], deck[i], keel[i], keel[j], len); }
  // deck (fan) — slightly lowered so bulwark edge shows
  const dk = deck.map(p => [p[0] * 0.97, p[1] - 0.25, p[2] * 0.92]);
  for (let i = 1; i < 4; i++) { pos.push(...dk[0], ...dk[i + 1], ...dk[i]); uv.push(dk[0][0] / 6, dk[0][2] / 3, dk[i + 1][0] / 6, dk[i + 1][2] / 3, dk[i][0] / 6, dk[i][2] / 3); }
  // inner bulwark faces
  for (let i = 0; i < 5; i++) { const j = (i + 1) % 5; pos.push(...deck[i], ...deck[j], ...dk[j], ...deck[i], ...dk[j], ...dk[i]); uv.push(0, 0, 1, 0, 1, 0.1, 0, 0, 1, 0.1, 0, 0.1); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.computeVertexNormals();
  return g;
}
function gridGeo(nx, ny) { const g = new THREE.PlaneGeometry(1, 1, nx, ny); g.attributes.position.setUsage(THREE.DynamicDrawUsage); return g; }

(S.fleets || []).forEach(F => {
  const list = [];
  const rows = F.rows || 1, cols = F.cols || 1, sp = F.spacing || [17, 20];
  const sailCol = F.sailColor || (F.kind === 'fire' ? [150, 60, 40] : [168, 138, 96]);
  const sTex = sailTex(sailCol), fTex = flagTex(F.flagColor || [30, 40, 70], F.flag);
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const war = F.kind === 'war';
    const s = { fleet: F, kind: F.kind, row: r, col: c,
      bx: F.origin[0] + c * sp[0] + r * (F.stagger || 0) + R(-1.5, 1.5), bz: F.origin[1] + r * sp[1] + R(-2, 2),
      rotY: R(-0.06, 0.06), L: war ? R(13, 15) : F.kind === 'fire' ? 7.5 : 9, Bm: war ? R(4.2, 5) : 2.6, ign: 1e9, crew: [] };
    const ig = F.ignite;
    if (ig) s.ign = ig.at + c * (ig.spreadCol || 0) + Math.abs(r - (rows - 1) / 2) * (ig.spreadRow || 0) + R(0, ig.jitter || 0);
    const n = F.crew || 0;
    for (let i = 0; i < n; i++) s.crew.push({ lx: R(-s.L / 2 + 1.5, s.L / 2 - 2), lz: R(-s.Bm / 3, s.Bm / 3), h: R(1.6, 1.9), jumpAt: R(0.25, 0.75), state: 'deck', spear: rnd() < 0.5, ph: R(0, 6) });
    s.x = s.bx; s.z = s.bz;
    // --- build mesh ---
    const grp = new THREE.Group(); grp.rotation.y = s.rotY;
    const hullMat = new THREE.MeshStandardMaterial({ map: TEX_WOOD, color: 0xffffff, roughness: 0.85, emissive: 0xff5a10, emissiveIntensity: 0 });
    const h = war ? 2.2 : 1.2; s.h = h;
    const hull = new THREE.Mesh(hullGeo(s.L, s.Bm, h), hullMat); grp.add(hull);
    s.mats = [hullMat];
    if (war) { // cabin + roof
      const cab = new THREE.Group(); const cw = 4, cd = s.Bm * 0.65; cab.position.set(-s.L / 2 + 3.2, h + 1.4, 0);
      const box = new THREE.Mesh(new THREE.BoxGeometry(cw, 3.2, cd).translate(0, 1.6, 0), hullMat); cab.add(box);
      const roofMat = new THREE.MeshStandardMaterial({ color: 0x2e2422, roughness: 0.8, emissive: 0xff5a10, emissiveIntensity: 0 }); s.mats.push(roofMat);
      const roof = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 1, 1, 4, 1).rotateY(Math.PI / 4).scale(cw * 0.85, 0.9, cd * 0.9).translate(0, 3.65, 0), roofMat); cab.add(roof);
      // windows glow
      const win = new THREE.Mesh(new THREE.PlaneGeometry(cw * 0.7, 0.5), new THREE.MeshBasicMaterial({ color: new THREE.Color(1.6, 0.8, 0.3) }));
      win.position.set(0, 2.1, cd / 2 + 0.02); cab.add(win); const win2 = win.clone(); win2.position.z = -cd / 2 - 0.02; win2.rotation.y = Math.PI; cab.add(win2); s.win = win.material;
      grp.add(cab); s.cabin = cab;
    }
    if (F.kind === 'fire') { // straw + oil bundles
      const strawMat = new THREE.MeshStandardMaterial({ color: 0x8a7038, roughness: 1, emissive: 0xff5a10, emissiveIntensity: 0 }); s.mats.push(strawMat);
      const st = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 1, 1, 4, 1).rotateY(Math.PI / 4).scale(s.L * 0.8, 1.5, s.Bm * 0.75).translate(-0.4, h + 0.75, 0), strawMat); grp.add(st);
    }
    s.masts = []; s.sails = []; s.flag = null;
    const masts = war ? [[1.5, 13], [s.L / 2 * 0.45 - 0.2, 9]] : [[0.5, 7]];
    masts.forEach(([mx, mh], k) => {
      const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.2, 1, 6).translate(0, 0.5, 0), MAT_MAST); mast.position.set(mx, h, 0); mast.scale.y = mh; grp.add(mast);
      const sm = new THREE.MeshStandardMaterial({ map: sTex, roughness: 0.95, side: THREE.DoubleSide, emissive: 0xff6a20, emissiveIntensity: 0 });
      const sail = new THREE.Mesh(gridGeo(6, 8), sm); grp.add(sail);
      const edge = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: new THREE.Color(5, 1.6, 0.35), side: THREE.DoubleSide, transparent: true }));
      grp.add(edge);
      s.masts.push({ mesh: mast, mx, mh }); s.sails.push({ mesh: sail, edge, mx, mh, k, sw: mh * 0.62, mat: sm });
      if (k === 0) { const fl = new THREE.Mesh(gridGeo(6, 2), new THREE.MeshStandardMaterial({ map: fTex, side: THREE.DoubleSide, roughness: 0.9, emissive: 0xffffff, emissiveMap: fTex, emissiveIntensity: 0.08 }));
        grp.add(fl); s.flag = { mesh: fl, mx, mh, fw: war ? 3.2 : 2.6, fh: war ? 2.4 : 2.0 }; }
    });
    // rigging lines
    const rig = []; masts.forEach(([mx, mh]) => { rig.push(mx, h + mh, 0, -s.L / 2 + 0.3, h + 1.6, 0, mx, h + mh, 0, s.L / 2 - 0.3, h + 1.2, 0); });
    const rg = new THREE.BufferGeometry(); rg.setAttribute('position', new THREE.Float32BufferAttribute(rig, 3));
    grp.add(new THREE.LineSegments(rg, new THREE.LineBasicMaterial({ color: 0x15100c })));
    scene.add(grp); s.grp = grp;
    list.push(s); allShips.push(s);
  }
  fleets[F.id] = list;
});
function updateShipPos(t) {
  for (const s of allShips) {
    const m = s.fleet.move; let dx = 0, dz = 0;
    if (m) { const u = (EASE[m.ease || 'accel'])(clamp((t - m.t0) / (m.t1 - m.t0))); dx = m.by[0] * u; dz = m.by[1] * u; }
    s.x = s.bx + dx; s.z = s.bz + dz;
    s.bob = Math.sin(t * 1.1 + s.bz * 0.3 + s.bx * 0.1) * 0.15;
  }
}
function toWorld(s, p) { const c = Math.cos(s.rotY), sn = Math.sin(s.rotY);
  return [s.x + p[0] * c + p[2] * sn, p[1] + (s.bob || 0), s.z - p[0] * sn + p[2] * c]; }
function getTarget(ref) { const [id, i] = ref.split(':'); const l = fleets[id]; return l ? l[Math.min(l.length - 1, +i || 0)] : null; }

// chains between chained ships (static catenary tubes)
(S.fleets || []).forEach(F => { if (!F.chained) return; const l = fleets[F.id], geos = [];
  for (const s of l) for (const o of l) { if (!((o.row === s.row && o.col === s.col + 1) || (o.col === s.col && o.row === s.row + 1))) continue;
    const a = new THREE.Vector3(...toWorld(s, [o.col > s.col ? s.L / 2 - 1 : 0, s.h + 0.4, o.row > s.row ? s.Bm / 2 : 0])), b = new THREE.Vector3(...toWorld(o, [o.col > s.col ? -o.L / 2 + 1 : 0, o.h + 0.4, o.row > s.row ? -o.Bm / 2 : 0]));
    const pts = []; for (let i = 0; i <= 12; i++) { const u = i / 12; const p = a.clone().lerp(b, u); p.y -= Math.sin(Math.PI * u) * 1.6; pts.push(p); }
    geos.push(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 16, 0.13, 4)); }
  if (geos.length) scene.add(new THREE.Mesh(mergeGeometries(geos), new THREE.MeshStandardMaterial({ color: 0x18181a, metalness: 0.7, roughness: 0.5 })));
});

// ---------- people (instanced) ----------
const personGeo = mergeGeometries([
  new THREE.CylinderGeometry(0.17, 0.24, 0.85, 7).translate(0, 0.42, 0),           // legs/skirt
  new THREE.CylinderGeometry(0.22, 0.18, 0.62, 7).translate(0, 1.13, 0),           // torso (armour)
  new THREE.SphereGeometry(0.12, 8, 6).translate(0, 1.56, 0),                       // head
  new THREE.ConeGeometry(0.16, 0.2, 8).translate(0, 1.72, 0),                       // helmet
  new THREE.CylinderGeometry(0.02, 0.02, 2.6, 4).translate(0.3, 1.2, 0),           // spear shaft
  new THREE.ConeGeometry(0.05, 0.25, 4).translate(0.3, 2.6, 0)]);                  // spear tip
const allCrew = []; allShips.forEach(s => s.crew.forEach(c => { c.ship = s; allCrew.push(c); }));
const people = new THREE.InstancedMesh(personGeo, new THREE.MeshStandardMaterial({ color: 0x2a2220, roughness: 0.8 }), Math.max(1, allCrew.length));
people.instanceMatrix.setUsage(THREE.DynamicDrawUsage); people.frustumCulled = false; scene.add(people);
const _m = new THREE.Matrix4(), _q = new THREE.Quaternion(), _e = new THREE.Euler(), _v = new THREE.Vector3(), _s = new THREE.Vector3();

// ---------- rocks (cliff) ----------
const rocks = (S.rocks || []).map(r => {
  const n = 22, rings = [[-3, 1.18], [0.25, 1.06], [0.55, 0.98], [0.82, 0.93], [1.0, 0.8]], pos = [];
  const radius = []; for (let i = 0; i < n; i++) radius.push(0.78 + 0.32 * rnd());
  const P = (ri, i) => { const [hy, k] = rings[ri]; const a = i / n * Math.PI * 2, j = 1 + (ri > 0 && ri < 4 ? R(-0.08, 0.08) : 0);
    const y = ri === 0 ? hy : hy * r.size[1] * (ri === 4 ? 1 : 0.97 + 0.05 * Math.sin(i * 2.3 + ri));
    return [r.pos[0] + Math.cos(a) * r.size[0] / 2 * radius[i] * k * j, y, r.pos[2] + Math.sin(a) * r.size[2] / 2 * radius[i] * k * j]; };
  const grid = rings.map((_, ri) => Array.from({ length: n }, (_, i) => P(ri, i)));
  for (let ri = 0; ri < rings.length - 1; ri++) for (let i = 0; i < n; i++) { const j = (i + 1) % n;
    const a = grid[ri][i], b = grid[ri][j], c = grid[ri + 1][j], d = grid[ri + 1][i]; pos.push(...a, ...c, ...b, ...a, ...d, ...c); }
  const top = [r.pos[0], r.size[1], r.pos[2]]; for (let i = 0; i < n; i++) pos.push(...top, ...grid[4][(i + 1) % n], ...grid[4][i]);
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.computeVertexNormals();
  const mesh = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: 0x2b2420, roughness: 0.95, flatShading: true })); scene.add(mesh);
  // scrub on top
  for (let i = 0; i < 9; i++) { const a = rnd() * 6.28, d = rnd() * 0.6;
    const b = new THREE.Mesh(new THREE.IcosahedronGeometry(R(0.6, 1.4), 0), new THREE.MeshStandardMaterial({ color: 0x141a12, roughness: 1, flatShading: true }));
    b.position.set(r.pos[0] + Math.cos(a) * r.size[0] / 2 * d, r.size[1] + 0.2, r.pos[2] + Math.sin(a) * r.size[2] / 2 * d); b.scale.y = 0.6; scene.add(b); }
  return { ...r, mesh };
});

// ---------- hero figures ----------
const figures = (S.figures || []).map(fg => {
  const k = fg.height / 2, grp = new THREE.Group(); grp.position.set(...fg.pos); grp.scale.setScalar(k);
  const mat = new THREE.MeshStandardMaterial({ color: 0x1d1414, roughness: 0.7 }), armour = new THREE.MeshStandardMaterial({ color: 0x3a1c16, roughness: 0.45, metalness: 0.5 });
  grp.add(new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.27, 1.15, 12).translate(0, 0.58, 0), mat));       // robe
  grp.add(new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.16, 0.55, 12).translate(0, 1.42, 0), armour));   // chest
  grp.add(new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.19, 0.08, 12).translate(0, 1.16, 0), new THREE.MeshStandardMaterial({ color: 0x8a6a2a, metalness: 0.8, roughness: 0.3 }))); // belt
  grp.add(new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.07, 0.12, 8).translate(0, 1.72, 0), mat)); // neck
  grp.add(new THREE.Mesh(new THREE.SphereGeometry(0.12, 14, 12).scale(1, 1.15, 1.05).translate(0, 1.86, 0), mat));               // head
  grp.add(new THREE.Mesh(new THREE.SphereGeometry(0.06, 10, 8).translate(0, 2.01, -0.02), mat)); grp.add(new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.09, 0.16).translate(0, 2.03, -0.01), armour)); // hair bun + guan
  for (const sx of [-1, 1]) { grp.add(new THREE.Mesh(new THREE.SphereGeometry(0.11, 10, 8).scale(1.2, 0.8, 1).translate(sx * 0.22, 1.63, 0), armour)); // pauldrons
    grp.add(new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.045, 0.62, 8).translate(0, -0.31, 0).rotateZ(sx * 0.18).translate(sx * 0.25, 1.6, 0.02), mat)); } // arms
    if (fg.sword) { const sw = new THREE.Mesh(new THREE.BoxGeometry(0.04, 1.1, 0.02).translate(0, -0.55, 0), new THREE.MeshStandardMaterial({ color: 0x9aa0a8, metalness: 0.9, roughness: 0.25 }));
    sw.position.set(-0.28, 1.15, 0.05); sw.rotation.z = -0.55; grp.add(sw); }
  const cape = new THREE.Mesh(gridGeo(6, 10), new THREE.MeshStandardMaterial({ color: 0x9a1c14, emissive: 0x3a0604, roughness: 0.75, side: THREE.DoubleSide })); grp.add(cape);
  const look = fg.look || [fg.pos[0] + 60, fg.pos[1], fg.pos[2] + 40]; grp.rotation.y = Math.atan2(look[0] - fg.pos[0], look[2] - fg.pos[2]);
  scene.add(grp); return { ...fg, grp, cape };
});
function updateCape(f, t) { // cape hangs from shoulders (local z = -0.15, back) and blows with the wind
  const p = f.cape.geometry.attributes.position, nx = 7, ny = 11;
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const u = i / (nx - 1) - 0.5, v = j / (ny - 1);
    const fl = Math.sin(t * 3.2 - v * 4 + u * 2) * 0.1 * v + Math.sin(t * 5.1 - v * 6) * 0.05 * v;
    p.setXYZ(j * nx + i, u * (0.44 + v * 0.3) + v * v * 0.45 + fl * 0.4, 1.68 - v * 1.5 + v * v * 0.35, -0.16 - v * 0.4 - fl); }
  p.needsUpdate = true; f.cape.geometry.computeVertexNormals();
}

// ---------- arrows ----------
const volleys = [];
(S.volleys || []).forEach(v => {
  const tg = fleets[v.target] || [];
  for (let i = 0; i < v.count; i++) {
    const s = tg[Math.floor(rnd() * tg.length)]; if (!s) continue;
    const ts = v.at + rnd() * (v.dur || 1), fl = v.flight || 1.8;
    const a = { ts, te: ts + fl, s, from: [v.from[0] + R(-v.spread[0], v.spread[0]), v.from[1], v.from[2] + R(-v.spread[1], v.spread[1])], off: [R(-5, 5), R(2, 5), R(-2, 2)], h: v.height || 25 };
    volleys.push(a); LOG.arrows.push([ts, a.te]);
    if (v.ignites !== false) s.ign = Math.min(s.ign, a.te + 0.2);
  }
});
const arrowMesh = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.05, 0.05, 1.8, 4).rotateZ(Math.PI / 2), new THREE.MeshBasicMaterial({ color: new THREE.Color(3, 1.3, 0.4) }), Math.max(1, volleys.length));
arrowMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage); arrowMesh.frustumCulled = false; scene.add(arrowMesh);
function arrowPos(a, u) { const e = toWorld(a.s, a.off); const p = lerp3(a.from, e, u); p[1] += a.h * 4 * u * (1 - u); return p; }

// ---------- camp lights ----------
const campLights = []; ((S.world && S.world.lights) || []).forEach(L => { for (let i = 0; i < L.count; i++) { const u = rnd();
  campLights.push([lerp(L.from[0], L.to[0], u) + R(-4, 4), (L.y || 1) + R(0, 2), lerp(L.from[1], L.to[1], u) + R(-4, 4), R(0, 6)]); } });

// ---------- simulation (identical rules to v1) ----------
let fire = [], smoke = [], embers = [], jumpers = [], drops = [];
const burnOf = (s, t) => clamp((t - s.ign) / 3.2);
function emitters(s, b) {
  const L = s.L, pts = [], war = s.kind === 'war', n = war ? 5 : 3;
  for (let i = 0; i < n; i++) pts.push([lerp(-L / 2 + 1, L / 2 - 1, (i + 0.5) / n), war ? 3 : 2, 0]);
  if (war && b > 0.2) pts.push([1.5, 9 * (1 - b * 0.5), 0], [-L / 2 + 3, 5.5, 0]);
  return pts;
}
let T = 0;
function step(t, dt) {
  T = t; updateShipPos(t);
  let fa = 0;
  for (const s of allShips) {
    const b = burnOf(s, t); if (b <= 0) continue;
    if (!s.logged) { s.logged = true; LOG.ignite.push(t); }
    fa += b * (s.kind === 'war' ? 1 : 0.5);
    const rate = (Q.fireRate || 0.55) * (s.kind === 'war' ? 1 : 2.2) * Math.min(1, b * 2.2);
    for (const e of emitters(s, b)) {
      let k = rate * R(0.5, 1.2);
      while (k > 0) { if (k < 1 && rnd() > k) break; k--;
        const w = toWorld(s, [e[0] + R(-1.3, 1.3), e[1], e[2] + R(-1.2, 1.2)]);
        fire.push({ s, x: w[0], y: w[1], z: w[2], vx: R(-0.5, 0.5), vy: R(4, 8), vz: R(-0.5, 0.5), age: 0, life: R(0.5, 1.1), size: R(1.6, 3.0) * (s.kind === 'war' ? 1.2 : 0.9), rot: R(-0.3, 0.3) }); }
    }
    if (b > 0.15 && rnd() < (Q.smokeRate || 0.09) * b) { const w = toWorld(s, [R(-s.L / 2, s.L / 2), 8 + R(0, 5), 0]);
      smoke.push({ x: w[0], y: w[1], z: w[2], vx: R(1, 3), vy: R(2.5, 4), vz: R(-0.5, 0.5), age: 0, life: R(4, 6.5), size: R(5, 8), rot: R(0, 6), vr: R(-0.3, 0.3) }); }
    if (rnd() < 0.6 * b) { const w = toWorld(s, [R(-s.L / 2, s.L / 2), 4 + R(0, 6), R(-1, 1)]);
      embers.push({ x: w[0], y: w[1], z: w[2], vx: R(-1, 3), vy: R(4, 9), vz: R(-2, 2), age: 0, life: R(1.5, 3.5), ph: R(0, 6) }); }
    for (const c of s.crew) if (c.state === 'deck' && b > c.jumpAt) {
      c.state = 'air'; const w = toWorld(s, [c.lx, s.h + 0.3, c.lz]); const side = c.lz >= 0 ? 1 : -1;
      const j = { c, x: w[0], y: w[1], z: w[2], vx: R(-1, 1.5), vy: R(3, 5), vz: side * R(2.5, 4), rot: 0, h: c.h }; c.j = j; jumpers.push(j);
    }
  }
  LOG.fire.push(fa);
  for (const p of fire) { p.age += dt; p.x += (p.vx + WIND[0] * 0.25) * dt; p.y += p.vy * dt; p.z += p.vz * dt; p.vy *= 0.985; }
  for (const p of smoke) { p.age += dt; p.x += (p.vx + WIND[0] * 0.5) * dt; p.y += p.vy * dt; p.z += (p.vz + WIND[2]) * dt; p.size += dt * 2.2; p.rot += p.vr * dt; }
  for (const p of embers) { p.age += dt; p.x += (p.vx + WIND[0] * 0.6 + Math.sin(p.age * 3 + p.ph) * 1.5) * dt; p.y += p.vy * dt; p.z += p.vz * dt; p.vy -= 1.2 * dt; }
  for (const j of jumpers) { j.x += j.vx * dt; j.y += j.vy * dt; j.z += j.vz * dt; j.vy -= 9.8 * dt; j.rot += dt * 3;
    if (j.y <= 0 && !j.done) { j.done = true; j.c.state = 'gone'; LOG.splash.push(t);
      for (let i = 0; i < 30; i++) { const a = rnd() * 6.28, sp = R(0.5, 2.5); drops.push({ x: j.x, y: 0.1, z: j.z, vx: Math.cos(a) * sp, vy: R(3, 7), vz: Math.sin(a) * sp, age: 0, life: R(0.6, 1.1) }); } } }
  for (const d of drops) { d.age += dt; d.x += d.vx * dt; d.y += d.vy * dt; d.z += d.vz * dt; d.vy -= 9.8 * dt; }
  fire = fire.filter(p => p.age < p.life); smoke = smoke.filter(p => p.age < p.life); embers = embers.filter(p => p.age < p.life);
  jumpers = jumpers.filter(j => !j.done); drops = drops.filter(d => d.age < d.life && d.y > -0.2);
}

// ---------- per-frame scene update ----------
const CHAR = new THREE.Color(0.012, 0.008, 0.006), WHITE = new THREE.Color(1, 1, 1);
function updateShips(t) {
  for (const s of allShips) {
    const b = burnOf(s, t), flick = 0.6 + 0.4 * Math.sin(t * 17 + s.bx) * Math.sin(t * 7.3 + s.bz);
    s.grp.position.set(s.x, s.bob, s.z); s.grp.rotation.z = Math.sin(t * 0.9 + s.bx) * 0.012; s.grp.rotation.x = Math.sin(t * 0.7 + s.bz) * 0.015;
    for (const m of s.mats) { m.color.copy(WHITE).lerp(CHAR, b * 0.85); m.emissiveIntensity = b > 0 ? b * (0.12 + 0.2 * flick) : 0; }
    if (s.cabin) s.cabin.scale.y = 1 - 0.55 * b;
    if (s.win) s.win.color.setRGB(1.6 + 3 * b * flick, 0.8 + 1.0 * b * flick, 0.3);
    for (const m of s.masts) m.mesh.scale.y = m.mh * (b > 0.85 ? 1 - (b - 0.85) * 2.5 : 1);
    for (const sl of s.sails) {
      const sTop = s.h + sl.mh * 0.95, sBot = s.h + sl.mh * 0.25, burnt = clamp(b * 1.5 - sl.k * 0.15), bot = lerp(sBot, sTop, burnt);
      const vis = sTop - bot > 0.3; sl.mesh.visible = vis; sl.edge.visible = vis && burnt > 0.02;
      if (!vis) continue;
      const sw = sl.sw, mx = sl.mx, billow = 0.6 + Math.sin(t * 1.3 + s.bz) * 0.18;
      const TL = [mx - sw * 0.35, sTop], TR = [mx + sw * 0.55, sTop - 0.4], BR = [mx + sw * 0.7, bot], BL = [mx - sw * 0.3, bot];
      const p = sl.mesh.geometry.attributes.position, uv = sl.mesh.geometry.attributes.uv, nx = 7, ny = 9;
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const u = i / (nx - 1), v = j / (ny - 1); // v=0 top
        const x = lerp(lerp(TL[0], TR[0], u), lerp(BL[0], BR[0], u), v), y = lerp(lerp(TL[1], TR[1], u), lerp(BL[1], BR[1], u), v);
        const z = -0.25 - billow * Math.sin(Math.PI * u) * (0.5 + 0.5 * Math.sin(Math.PI * Math.min(1, v * 0.9 + 0.1))) - billow * 0.25 * u;
        p.setXYZ(j * nx + i, x, y, z); uv.setXY(j * nx + i, u, 1 - v * (1 - burnt)); }
      p.needsUpdate = true; uv.needsUpdate = true; sl.mesh.geometry.computeVertexNormals();
      sl.mat.color.copy(WHITE).lerp(CHAR, b * 0.5); sl.mat.emissiveIntensity = b > 0 ? 0.15 * b * flick : 0;
      if (sl.edge.visible) { sl.edge.position.set((BL[0] + BR[0]) / 2, bot, -0.25 - billow * 0.6); sl.edge.scale.set(BR[0] - BL[0], 0.35, 1); sl.edge.material.opacity = 0.7 + 0.3 * flick; }
    }
    if (s.flag) { const f = s.flag, vis = b < 0.6; f.mesh.visible = vis;
      if (vis) { const mtop = s.h + f.mh, p = f.mesh.geometry.attributes.position, nx = 7, ny = 3;
        for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const u = i / (nx - 1), v = j / (ny - 1);
          const wv = Math.sin(t * 6 + s.bx - u * 4) * 0.35 * u;
          p.setXYZ(j * nx + i, f.mx + 0.1 + u * f.fw * 0.95, mtop - v * f.fh + wv * 0.25 - u * 0.15, wv); }
        p.needsUpdate = true; f.mesh.geometry.computeVertexNormals(); } }
  }
  // people
  let i = 0;
  for (const c of allCrew) {
    if (c.state === 'deck') { const s = c.ship, w = toWorld(s, [c.lx, s.h - 0.2, c.lz]);
      _e.set(Math.sin(t * 2 + c.ph) * 0.05, s.rotY + (c.lz > 0 ? -0.3 : 0.3) + Math.sin(t * 0.7 + c.ph) * 0.4, 0); _q.setFromEuler(_e); _s.setScalar(c.h / 1.8);
      _m.compose(_v.set(...w), _q, _s); }
    else if (c.state === 'air') { const j = c.j; _e.set(j.rot * 0.6, 0, j.rot); _q.setFromEuler(_e); _s.setScalar(c.h / 1.8); _m.compose(_v.set(j.x, j.y, j.z), _q, _s); }
    else { _m.makeScale(0, 0, 0); }
    people.setMatrixAt(i++, _m);
  }
  people.instanceMatrix.needsUpdate = true;
}
function updateLights(t) {
  // pick the strongest burning ships near the camera for real point lights
  const cand = [];
  for (const s of allShips) { const b = burnOf(s, t); if (b <= 0) continue; const d = Math.hypot(s.x - camera.position.x, s.z - camera.position.z);
    cand.push({ s, b, score: b * (s.kind === 'war' ? 1 : 0.6) / (1 + d / 60) }); }
  cand.sort((a, b) => b.score - a.score);
  let total = 0, cx = 0, cz = 0;
  for (const s of allShips) { const b = burnOf(s, t); if (b > 0) { total += b; cx += s.x * b; cz += s.z * b; } }
  for (let i = 0; i < NFL; i++) { const L = fireLights[i], c = cand[i], u = WU.uFires.value[i];
    if (c) { const fl = 0.75 + 0.25 * Math.sin(t * 13 + c.s.bz) * Math.sin(t * 5.7 + c.s.bx); L.position.set(c.s.x, 7, c.s.z);
      L.intensity = (Q.fireLight || 180) * c.b * fl * (c.s.kind === 'war' ? 1 : 0.6); u.set(c.s.x, 7, c.s.z, c.b * fl * 1.6); }
    else { L.intensity = 0; u.set(0, 0, 0, 0); } }
  const fn = clamp(total / 18);
  if (total > 0) { cx /= total; cz /= total; fireKey.position.set(cx, 25, cz); fireKey.target.position.set(camera.position.x, 0, camera.position.z); }
  fireKey.intensity = fn * 1.6 * (0.9 + 0.1 * Math.sin(t * 9));
  hemi.color.setRGB(0.23 + 0.5 * fn, 0.29 + 0.12 * fn, 0.47 - 0.2 * fn);
  sky.material.uniforms.fn.value = fn;
  FOG.color.setRGB(lerp(0.03, 0.12, fn), lerp(0.035, 0.04, fn), lerp(0.075, 0.03, fn));
  WU.uFogColor.value.copy(FOG.color); WU.uFogDensity.value = FOG.density; WU.uFn.value = fn; WU.uTime.value = t;
  farRidge.material.color.setRGB(0.03 + 0.12 * fn, 0.032 + 0.03 * fn, 0.06);
  midRidge.material.color.setRGB(0.012 + 0.09 * fn, 0.012 + 0.025 * fn, 0.025);
  return fn;
}
function updateParticles(t) {
  LsFire.begin(); LsSmoke.begin(); LsGlow.begin();
  for (const p of fire) { const a = p.age / p.life, sz = p.size * (1 - a * 0.55) * 1.6;
    let r, g, b; if (a < 0.2) { r = 1.6; g = 0.95; b = 0.4; } else if (a < 0.55) { r = 1.3; g = 0.42; b = 0.07; } else { r = 0.55; g = 0.1; b = 0.015; }
    LsFire.push(p.x, p.y, p.z, sz * 0.6, sz * 1.45, p.rot, r, g, b, Math.min(1, (1 - a) * 1.3) * (Q.fireAlpha || 0.2) * (p.s.kind === 'war' ? 1 : 1.3)); }
  for (const p of smoke) { const a = p.age / p.life, warm = clamp(1 - (p.y - 6) / 18);
    LsSmoke.push(p.x, p.y, p.z, p.size * 1.5, p.size * 1.5, p.rot, 0.02 + 0.07 * warm, 0.016 + 0.02 * warm, 0.016 + 0.006 * warm, Math.sin(Math.PI * a) * 0.65); }
  for (const p of embers) { const a = p.age / p.life, tw = 0.6 + 0.4 * Math.sin(p.age * 20 + p.ph);
    LsGlow.push(p.x, p.y, p.z, 0.16, 0.16, 0, 6, 2.4 + Math.sin(p.ph) * 0.8, 0.6, (1 - a) * tw); }
  for (const d of drops) LsGlow.push(d.x, d.y, d.z, 0.22, 0.32, 0, 0.9, 0.75, 0.6, 1 - d.age / d.life);
  for (const l of campLights) LsGlow.push(l[0], l[1], l[2], 3, 3, 0, 2.2, 1.0, 0.35, 0.5 + 0.3 * Math.sin(t * 7 + l[3]));
  // burning glow halo at each ship base
  // arrows
  let n = 0;
  for (const a of volleys) { if (t < a.ts || t > a.te) continue; const u = (t - a.ts) / (a.te - a.ts);
    const p = arrowPos(a, u), p2 = arrowPos(a, Math.min(1, u + 0.01));
    _v.set(p2[0] - p[0], p2[1] - p[1], p2[2] - p[2]).normalize(); _q.setFromUnitVectors(new THREE.Vector3(1, 0, 0), _v); _m.compose(new THREE.Vector3(...p), _q, _s.set(1, 1, 1));
    arrowMesh.setMatrixAt(n++, _m); LsGlow.push(p[0], p[1], p[2], 1.6, 1.6, 0, 5, 2, 0.6, 0.8); }
  arrowMesh.count = n; arrowMesh.instanceMatrix.needsUpdate = true;
  LsFire.end(); LsSmoke.end(); LsGlow.end();
}

// ---------- camera ----------
function camForTime(t) {
  let sh = S.shots.find(s => t >= s.t0 && t < s.t1) || S.shots[S.shots.length - 1];
  const c = sh.cam, u = (EASE[c.ease || 'inout'])(clamp((t - sh.t0) / sh.dur));
  let pos = lerp3(c.from.pos, c.to ? c.to.pos : c.from.pos, u), look = lerp3(c.from.look, c.to ? c.to.look : c.from.look, u);
  if (c.follow) { const o = getTarget(c.follow); if (o) { pos = [pos[0] + o.x, pos[1], pos[2] + o.z]; look = [look[0] + o.x, look[1], look[2] + o.z]; } }
  const sk = (c.shake || 0); if (sk) { pos[0] += Math.sin(t * 23) * sk * 0.3; pos[1] += Math.sin(t * 31 + 1) * sk * 0.3; }
  pos[0] += Math.sin(t * 0.7) * 0.15; pos[1] += Math.sin(t * 0.9) * 0.1;
  const fov = c.fov ? (Array.isArray(c.fov) ? lerp(c.fov[0], c.fov[1], u) : c.fov) : 50;
  camera.position.set(...pos); camera.lookAt(...look); camera.fov = fov; camera.updateProjectionMatrix();
  sky.position.copy(camera.position); moon.position.copy(camera.position).addScaledVector(MOON_DIR, 4000);
  return sh;
}

// ---------- 2D overlay: vignette, letterbox, captions, fades ----------
function drawOverlay(sh, t) {
  ctx.clearRect(0, 0, W, H);
  let g = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.35, W / 2, H / 2, Math.max(W, H) * 0.62);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0.6)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  if (S.letterbox !== false) { const lb = Math.round(H * 0.061); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, lb); ctx.fillRect(0, H - lb, W, lb); }
  const k = H / 1080;
  for (const c of sh.captions || []) {
    const lt = t - sh.t0, at = c.at || 0, du = c.dur || (sh.dur - at);
    const a = ss(at, at + 0.8, lt) * (1 - ss(at + du - 0.6, at + du, lt)); if (a <= 0) continue;
    ctx.globalAlpha = a; ctx.shadowColor = 'rgba(0,0,0,0.85)'; ctx.shadowBlur = 24 * k;
    if (c.style === 'title') { ctx.textAlign = 'center';
      if (c.cn) { ctx.fillStyle = '#f3e6c8'; ctx.font = `700 ${120 * k | 0}px "Noto Serif CJK SC"`; ctx.fillText(c.cn, W / 2, H * 0.28); }
      ctx.font = `600 ${52 * k | 0}px Lora`; ctx.fillStyle = '#e9c98f'; ctx.fillText(c.text, W / 2, H * 0.28 + 85 * k);
      if (c.sub) { ctx.font = `italic 400 ${28 * k | 0}px Lora`; ctx.fillStyle = '#cbbd9f'; ctx.fillText(c.sub, W / 2, H * 0.28 + 135 * k); }
    } else { ctx.textAlign = W > H ? 'left' : 'center'; const x = W > H ? 120 * k : W / 2;
      ctx.fillStyle = '#e8dcc0'; ctx.font = `500 ${30 * k | 0}px Lora`; ctx.fillText(c.text, x, H - 150 * k);
      if (c.sub) { ctx.font = `italic 400 ${26 * k | 0}px Lora`; ctx.fillStyle = '#b9ad94'; ctx.fillText(c.sub, x, H - 108 * k); } }
    ctx.shadowBlur = 0; ctx.globalAlpha = 1;
  }
  let fade = 0; const lt = t - sh.t0;
  if (sh.fadeIn) fade = Math.max(fade, 1 - ss(0, sh.fadeIn, lt));
  if (sh.fadeOut) fade = Math.max(fade, ss(sh.dur - sh.fadeOut, sh.dur, lt));
  if (fade > 0) { ctx.fillStyle = `rgba(0,0,0,${fade})`; ctx.fillRect(0, 0, W, H); }
}

function render(t) {
  const sh = camForTime(t);
  updateShips(t); updateLights(t); updateParticles(t);
  for (const f of figures) updateCape(f, t);
  composer.render();
  drawOverlay(sh, t);
}

let frame = 0;
window.DUR = DUR; window.FPS = FPS;
window.goto = function (target) { while (frame < target) { step(frame / FPS, 1 / FPS); frame++; } render(frame / FPS); return frame; };
window.simAll = function () { while (frame < Math.round(DUR * FPS)) { step(frame / FPS, 1 / FPS); frame++; } return LOG; };
const comp = document.createElement('canvas'); comp.width = W; comp.height = H; const cctx = comp.getContext('2d');
window.grab = function (q) { cctx.drawImage(renderer.domElement, 0, 0); cctx.drawImage(ov, 0, 0); return comp.toDataURL('image/jpeg', q || 0.92); };
window.__dbg = { water, LsFire, LsSmoke, LsGlow, bloom, renderer, composer, scene };
window.ready = true;
} catch (e) { window.__err = String(e && e.stack || e); console.error(e); }
