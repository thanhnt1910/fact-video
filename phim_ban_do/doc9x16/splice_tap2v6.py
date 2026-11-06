import re,sys
D=__file__.rsplit('/',1)[0]
s=open(f'{D}/trang.html',encoding='utf-8').read()
i=s.index('// S1: chín quận');j=s.index('const bw=(960')
sc=open(f'{D}/scenes_tap2v6.js',encoding='utf-8').read()
s=s[:i]+sc+s[j:]
s=s.replace(r"txt.match(/[^,.;?]+[,.;?]?/g)",r"txt.match(/(?:[^,.;?]|(?<=\d)\.(?=\d))+[,.;?]?/g)")  # lookbehind: giữ số 2.000
s=s.replace('43000+n','49000+n').replace('· #01','· #02')
# sfx
a=s.index('const SFXQ=[];');b=s.index('window.SFX=SFXQ')
sfx='''const SFXQ=[];const sx=(t,k,p)=>SFXQ.push([t,k,p||{}]);
sx(R(1)+W(1,'đền',0,4.5),'chime',{f:660,g:.8});for(let i=0;i<4;i++)sx(R(2)+W(2,'Thậm',0,.3)+i*.25,'pop',{f:520+i*60,g:.7});
sx(R(3)+W(3,'Đặng',0,2.6),'pop',{f:560});sx(R(5)+W(5,'cử',0,3.2),'whoosh',{d:.9,g:.5});
for(let i=0;i<3;i++)sx(R(6)+W(6,'ba',0,5.0)+i*.25,'tit',{f:1700+i*200,g:.9});
sx(R(7)+W(7,'trâu',0,5.4),'pop',{f:300,g:.6});sx(R(9)+W(9,'đúc',0,1.8),'thud',{f:90,g:.7});
for(let i=0;i<5;i++)sx(R(9)+W(9,'khai',0,5.0)+i*.35,'pop',{f:480+i*40,g:.6});sx(R(10)+W(10,'đủ',0,3.6),'chime',{f:740,g:.7});
sx(R(12)+W(12,'chưa',0,3.0),'question',{g:.7});for(let i=0;i<3;i++)sx(R(13)+W(13,'huyện',0,2.0)+i*.2,'pop',{f:520+i*60});
for(let i=0;i<3;i++)sx(R(14)+W(14,'ghép',0,2.4)+i*.3,'chime',{f:700+i*60,g:.5});
for(let i=0;i<3;i++)sx(R(15)+W(15,'trích',0,6.4)+i*.35,'ping',{f:900+i*80,g:.6});
for(let i=0;i<4;i++)sx(R(16)+.4+i*.25,'chime',{f:700+i*60,g:.5});
sx(R(18)+W(18,'đền',0,2.4),'chime',{f:660,g:.9});for(let i=0;i<6;i++)sx(R(18)+W(18,'đặt',0,6.0)+i*.2,'pop',{f:500+i*50,g:.6});
sx(R(22)+W(22,'văn',0,4.4),'swell',{d:1.8,g:.5});sx(R(25)+W(25,'lẽ',0,.3),'question',{g:.8});
sx(R(26)+W(26,'chưa',0,3.6),'stamp',{g:.8});sx(R(29)+.8,'chime',{f:740,g:.8});
sx(R(31)+W(31,'Tô',0,2.2),'thud',{f:55,g:.9});sx(R(31)+W(31,'tham',0,4.4),'whoosh',{d:.6,g:.4});
for(let i=0;i<6;i++)sx(R(32)+.2+i*.2,'tit',{f:1500+i*130,g:.7});sx(R(32)+1.0,'question',{g:.8});
'''
s=s[:a]+sfx+s[b:]
open(f'{D}/trang_tap2v6.html','w',encoding='utf-8').write(s)
print('ok',len(s))
