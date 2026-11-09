import React, {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';

const BE_VI = 'U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB';
const BE_EXT = 'U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF';
const LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD';

const css = `
@font-face{font-family:'BeVN';font-weight:800;src:url(${staticFile('be-vietnam-pro-vietnamese-800-normal.woff2')}) format('woff2');unicode-range:${BE_VI};}
@font-face{font-family:'BeVN';font-weight:800;src:url(${staticFile('be-vietnam-pro-latin-ext-800-normal.woff2')}) format('woff2');unicode-range:${BE_EXT};}
@font-face{font-family:'BeVN';font-weight:800;src:url(${staticFile('be-vietnam-pro-latin-800-normal.woff2')}) format('woff2');unicode-range:${LATIN};}
@font-face{font-family:'Cormorant';font-weight:600;src:url(${staticFile('cg-vi-600.woff2')}) format('woff2');unicode-range:${BE_VI};}
@font-face{font-family:'Cormorant';font-weight:600;src:url(${staticFile('cg-latin-600.woff2')}) format('woff2');unicode-range:${LATIN};}
@font-face{font-family:'Lora';font-style:italic;font-weight:400 700;src:url(${staticFile('Lora-Italic.ttf')}) format('truetype');}
`;

export const Fonts: React.FC = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const vi = 'Aăâđêôơư ếềểễệ ạảãấầẩẫậ 0123456789';
    Promise.all([
      document.fonts.load('800 40px BeVN', vi),
      document.fonts.load('600 40px Cormorant', vi),
      document.fonts.load('italic 400 40px Lora', 'H h S s ½ × ÷ ≈ 0123456789'),
    ])
      .then(() => continueRender(handle))
      .catch(() => continueRender(handle));
  }, [handle]);
  return <style>{css}</style>;
};
