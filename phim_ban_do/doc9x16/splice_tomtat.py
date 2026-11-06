D=__file__.rsplit('/',1)[0]
s=open(f'{D}/trang.html',encoding='utf-8').read()
i=s.index('// S1: chín quận');j=s.index('const bw=(960')
s=s[:i]+open(f'{D}/scenes_tomtat.js',encoding='utf-8').read()+s[j:]
s=s.replace(r"txt.match(/[^,.;?]+[,.;?]?/g)",r"txt.match(/(?:[^,.;?]|(?<=\d)\.(?=\d))+[,.;?]?/g)")
s=s.replace('43000+n','47000+n').replace('· #01','· TÓM TẮT')
a=s.index('const SFXQ=[];');b=s.index('window.SFX=SFXQ')
sfx='''const SFXQ=[];const sx=(t,k,p)=>SFXQ.push([t,k,p||{}]);
sx(R(1)+1.0,'question',{g:.8});sx(R(2)+W(2,'thôn',0,3.2),'stamp',{g:1.0});sx(R(3)+W(3,'cày',0,4.8),'pop',{f:520});
sx(R(4)+W(4,'tham',0,2.8),'coin',{});sx(R(5)+W(5,'sáu',0,5.0),'chime',{f:700,g:.8});sx(R(6)+W(6,'cột',0,5.2),'thud',{f:60,g:.8});
sx(R(7)+W(7,'hàng',0,5.4),'flag',{});for(let i=0;i<6;i++)sx(R(8)+.2+i*.55,'pop',{f:480+i*60});
'''
s=s[:a]+sfx+s[b:]
open(f'{D}/trang_tomtat.html','w',encoding='utf-8').write(s);print('ok')
