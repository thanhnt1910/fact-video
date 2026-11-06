import re,sys
D=__file__.rsplit('/',1)[0]
s=open(f'{D}/trang.html',encoding='utf-8').read()
i=s.index('// S1: chín quận');j=s.index('const bw=(960')
sc=open(f'{D}/scenes_tap2.js',encoding='utf-8').read()
s=s[:i]+sc+s[j:]
s=s.replace(r"txt.match(/[^,.;?]+[,.;?]?/g)",r"txt.match(/(?:[^,.;?]|(?<=\d)\.(?=\d))+[,.;?]?/g)")  # lookbehind: giữ số 2.000
s=s.replace('43000+n','44000+n').replace('· #01','· #02')
# sfx
a=s.index('const SFXQ=[];');b=s.index('window.SFX=SFXQ')
sfx='''const SFXQ=[];const sx=(t,k,p)=>SFXQ.push([t,k,p||{}]);
sx(R(1)+W(1,'đền',0,4.5),'chime',{f:660,g:.8});for(let i=0;i<4;i++)sx(R(1)+W(1,'Thậm',0,7.6)+i*.25,'pop',{f:520+i*60,g:.7});
sx(R(2)+W(2,'Đặng',0,2.6),'pop',{f:560});sx(R(2)+W(2,'cử',0,7.4),'whoosh',{d:.9,g:.5});
sx(R(3)+W(3,'Cửu',0,5.6),'tit',{f:1700,g:.9});sx(R(3)+W(3,'Cửu',0,5.6)+.25,'tit',{f:1900,g:.9});sx(R(3)+W(3,'Cửu',0,5.6)+.5,'tit',{f:2100,g:.9});
sx(R(4)+W(4,'đánh',0,3.0),'pop',{f:640,g:.6});sx(R(4)+W(4,'cày',0,4.6)+.5,'thud',{f:70,g:.7});
for(let i=0;i<5;i++)sx(R(5)+W(5,'khai',0,1.6)+i*.35,'pop',{f:480+i*40,g:.6});sx(R(5)+W(5,'đủ',0,6.0),'chime',{f:740,g:.7});
sx(R(6)+W(6,'sính',0,3.3)+.5,'thud',{f:60,g:.8});
for(let i=0;i<3;i++)sx(R(7)+W(7,'trích',0,3.6)+i*.35+.9,'ping',{f:900+i*80,g:.6});
for(let i=0;i<4;i++)sx(R(8)+W(8,'cách',0,.4)+i*.25+.3,'chime',{f:700+i*60,g:.5});
sx(R(9)+W(9,'đền',0,5.6),'chime',{f:660,g:.9});sx(R(9)+W(9,'đền',0,5.6)+.2,'swell',{d:1.4,g:.5});
for(let i=0;i<6;i++)sx(R(10)+W(10,'đặt',0,3.3)+i*.2,'pop',{f:500+i*50,g:.6});
sx(R(11)+W(11,'văn',0,5.0),'swell',{d:1.8,g:.5});
sx(R(12)+W(12,'lẽ',0,6.6),'question',{g:.8});
sx(R(13)+W(13,'chưa',0,1.6),'stamp',{g:.8});sx(R(13)+W(13,'Dù',0,4.6)+.2,'chime',{f:740,g:.8});
sx(R(14)+W(14,'Tô',0,5.0),'thud',{f:55,g:.9});sx(R(14)+W(14,'tham',0,6.2),'whoosh',{d:.6,g:.4});
for(let i=0;i<6;i++)sx(R(15)+.2+i*.2,'tit',{f:1500+i*130,g:.7});sx(R(15)+1.0,'question',{g:.8});
'''
s=s[:a]+sfx+s[b:]
open(f'{D}/trang_tap2.html','w',encoding='utf-8').write(s)
print('ok',len(s))
