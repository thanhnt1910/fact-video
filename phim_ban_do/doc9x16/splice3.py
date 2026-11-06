D=__file__.rsplit('/',1)[0]
s=open(f'{D}/trang.html',encoding='utf-8').read()
i=s.index('// S1: chín quận');j=s.index('const bw=(960')
s=s[:i]+open(f'{D}/scenes_tap3.js',encoding='utf-8').read()+s[j:]
s=s.replace(r"txt.match(/[^,.;?]+[,.;?]?/g)",r"txt.match(/(?:[^,.;?]|(?<=\d)\.(?=\d))+[,.;?]?/g)")
s=s.replace('43000+n','45000+n').replace('· #01','· #03')
a=s.index('const SFXQ=[];');b=s.index('window.SFX=SFXQ')
sfx='''const SFXQ=[];const sx=(t,k,p)=>SFXQ.push([t,k,p||{}]);
sx(R(1)+W(1,'khiến',0,5.6),'chime',{f:660,g:.8});for(let i=0;i<8;i++)sx(R(1)+W(1,'khiến',0,5.6)+i*.3,'tit',{f:1500+i*110,g:.7});
sx(R(2)+W(2,'Tô',0,3.4),'thud',{f:55,g:.9});sx(R(2)+W(2,'tham',0,5.2),'whoosh',{d:.6,g:.4});
sx(R(3)+W(3,'Trưng',0,3.0),'pop',{f:560});sx(R(4)+W(4,'Hai',0,4.6),'chime',{f:700,g:.7});
sx(R(5)+W(5,'giết',0,5.0),'thud',{f:60,g:.9});sx(R(6)+W(6,'phất',0,4.4),'flag',{});
sx(R(7)+W(7,'đem',0,1.6),'steps',{n:6,g:.6});sx(R(7)+W(7,'Tô',0,5.0),'whoosh',{d:.8,g:.5});
sx(R(8)+W(8,'Cửu',0,2.4),'pop',{f:520});sx(R(8)+W(8,'Nhật',0,3.5),'pop',{f:600});sx(R(8)+W(8,'Hợp',0,4.4),'pop',{f:680});
for(let i=0;i<10;i++)sx(R(9)+W(9,'Nhờ',0,.4)+i*.24,'tit',{f:1500+i*90,g:.7});sx(R(9)+W(9,'tự',0,5.0),'stamp',{g:1.1});
sx(R(10)+W(10,'hô',0,4.5),'swell',{d:1.6,g:.5});sx(R(11)+W(11,'dựng',0,2.6),'chime',{f:740,g:.8});
sx(R(12)+W(12,'chấp',0,1.2),'stamp',{g:.8});sx(R(13)+W(13,'thành',0,5.4),'flag',{});
sx(R(15)+W(15,'xe',0,5.0),'pop',{f:480});sx(R(16)+W(16,'tích',0,1.4),'thud',{f:70,g:.7});
sx(R(17)+W(17,'dẫn',0,6.0),'flag',{g:1.2});sx(R(18)+.8,'question',{g:.8});
'''
s=s[:a]+sfx+s[b:]
open(f'{D}/trang_tap3.html','w',encoding='utf-8').write(s);print('ok')
