import {Easing} from 'remotion';

export const W = 1920;
export const H = 1080;
export const FPS = 30;

export const C = {
  bg1: '#2b1e15',
  bg2: '#130c08',
  cream: '#f4e9d0',
  amber: '#f2b35a',
  amberDeep: '#e8913a',
  dim: '#d9ccb0',
  ink: '#1a120d',
};

// Hình học chung của cảnh kim tự tháp (đơn vị: điểm ảnh, khung 1920x1080)
export const GY = 760; // mặt đất
export const PX = 640; // tâm đáy kim tự tháp
export const PH = 380; // chiều cao vẽ
export const PB = 298; // nửa cạnh đáy (tỉ lệ thật 115,15 / 146,6 = 0,785)
export const APEX_Y = GY - PH;

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const seg = (f: number, a: number, b: number) => clamp01((f - a) / Math.max(1, b - a));
export const eo = Easing.out(Easing.cubic);
export const eio = Easing.inOut(Easing.cubic);
/** Tiến độ có làm mượt (ra chậm) từ khung a đến khung b */
export const sp = (f: number, a: number, b: number) => eo(seg(f, a, b));
export const sec = (s: number) => Math.round(s * FPS);
