D=__file__.rsplit('/',1)[0]
s=open(f'{D}/trang.html',encoding='utf-8').read()
i=s.index('// S1: chín quận');j=s.index('const bw=(960')
s=s[:i]+open(f'{D}/scenes_cot.js',encoding='utf-8').read()+s[j:]
s=s.replace(r"txt.match(/[^,.;?]+[,.;?]?/g)",r"txt.match(/(?:[^,.;?]|(?<=\d)\.(?=\d))+[,.;?]?/g)")
s=s.replace('43000+n','48000+n').replace('· #01','· TẬP 4 · DEMO')
a=s.index('const SFXQ=[];');b=s.index('window.SFX=SFXQ')
sfx='''const SFXQ=[];const sx=(t,k,p)=>SFXQ.push([t,k,p||{}]);
sx(R(1)+W(1,'dựng',0,2.8)+.4,'stamp',{g:1.0});sx(R(2)+W(2,'gãy',0,3.8),'thud',{f:60,g:.8});sx(R(3)+.3,'steps',{n:6,g:.5});
'''
s=s[:a]+sfx+s[b:]
open(f'{D}/trang_cot.html','w',encoding='utf-8').write(s);print('ok')
