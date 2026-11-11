// Xuất danh sách hiệu ứng âm thanh của một video khoa học 8–12: tên video lấy từ biến môi trường VID (sao, amthanh, ...).
import {sfxFor} from '../src/khoahoc/tl';
import * as sao from '../src/sao/content';
import * as am from '../src/amthanh/content';
import * as mt from '../src/mattroi/content';
import * as nk from '../src/nhietke/content';
import * as ql from '../src/quaclac/content';
import * as nc from '../src/nuicao/content';
import * as td from '../src/tuoitd/content';
const M: Record<string, {timeline: () => any}> = {sao, amthanh: am, mattroi: mt, nhietke: nk, quaclac: ql, nuicao: nc, tuoitd: td};
console.log(JSON.stringify(sfxFor(M[process.env.VID as string].timeline())));
