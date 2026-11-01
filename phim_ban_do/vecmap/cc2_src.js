// ===== Cảnh riêng từng đoạn (mỗi cảnh chỉ dùng MỘT lần) — mini-DSL =====
const FT={
 v:(n,o)=>VF(n,Object.assign({flip:false},o)),
 s:(n,o)=>SF(n,o),
 d:(n,o)=>Object.assign({sz:66,col:n%2?'#8c7a58':'#9a7c52',trou:VI.trou,hat:'non',arm:'none'},o),
 w:(n,o)=>Object.assign({sz:66,col:'#8c7a58',trou:VI.trou,hat:'cap',arm:'none'},o),
 q:(n,o)=>Object.assign({sz:70,col:n%2?'#3d3a52':'#5a3b4a',trou:'#2b2218',hat:'quan',arm:'none'},o),
 qs:(n,o)=>Object.assign({sz:70,col:n%2?'#3d5a7a':'#2f4a6a',trou:'#1f2a3a',hat:'quan',arm:'none',flip:true},o),
 k:(n,o)=>Object.assign({sz:76,col:'#b3861e',trou:'#4a2a1a',hat:'quan',arm:'none'},o),
 L:(n,o)=>Object.assign({sz:86,col:'#7a3b1c',trou:'#4a2a1a',hat:'ltk',hatcol:'#b3261e',arm:'none',armor:true,pauld:true,acol:'#b08a3a',cape:true,beard:true},o)};
function runS(c,items){let n=0;const tau=c.tau;
 for(const q of items){n++;const k=q[0],u=q[1],v=q[2],a=q[3],b=q[4];const p=Lc(u,v);
  switch(k){
   case'h':c.push(p[1],()=>house(c.D,p[0],p[1],a||1.3,b?ease(cl((tau-b)/1.4)):0,0));break;
   case'g':c.push(p[1],()=>gateT(c.D,p[0],p[1],a||1.5));break;
   case't':c.push(p[1],()=>tent(c.D,p[0],p[1],a||1.5,b||'#a3aec4'));break;
   case'hl':c.push(p[1],()=>hill(c.D,p[0],p[1],a||2,b||'#8fa070'));break;
   case'tp':c.push(p[1],()=>temple(c.D,p[0],p[1],a||1.5));break;
   case'b':c.push(p[1],()=>boat(c.D,p[0],p[1],Object.assign({al:1},a)));break;
   case'e':c.push(p[1],()=>ele(c.D,p[0],p[1],K1*(a||1.1),tau*5+n,!!b));break;
   case'f':c.push(p[1],()=>flameC(c.D,p[0],p[1],W(a||12),tau+n,1));break;
   case'k':c.push(p[1],()=>stake(c.D,p[0],p[1],a||40,b||4,'#5a3b1c'));break;
   case'tr':c.push(p[1],()=>tree(c.D,p[0],p[1],a||1.1));break;
   case'fig':{const o=Object.assign({},FT[a](n,b&&b.o?{}:{}),b||{});if(o.w){o.walk=tau*7+n;delete o.w}if(o.sw){o.rot=Math.sin(tau*.8+n)*4;delete o.sw}
     const key=o.key;delete o.key;FG(c,u,v,o,key);break}
   case'col':{const [t,cnt,spd,gap,o]=[a,b,q[4],q[5],q[6]||{}];/*['col',u0,v,type,n,spd,gap,opts]*/break}
   case'vol':{const u2=a,v2=b,cnt=q[5]||6;for(let j=0;j<cnt;j++){const ts=j*.45,p0=((tau-ts)%2.6)/1.0;if(p0<=0||p0>=1)continue;c.arrows.push([Lc(u,v),Lc(u2+((j*7)%5)*50,v2+((j*3)%4)*14),p0,false])}break}
  }}}
// đoàn đi: ['mv', type, n, spd, v, gap, opts]
function mvS(c,type,cnt,spd,v,gap,o){column(c,cnt,spd,v,k=>FT[type](k,o||{}),{gap:gap||100})}
const R2=(name,gnd,items,badges,extra)=>{SCN[name]={gnd,build(c){scenery(c,extra&&extra.seed||name.length*7,{n:extra&&extra.trees!=null?extra.trees:10,vmin:extra&&extra.vmin||380});runS(c,items);if(extra&&extra.mv)for(const m of extra.mv)mvS(c,...m);if(extra&&extra.dyn)extra.dyn(c)},badges:()=>badges||[]}};
const LB=(sub,below)=>({key:'ltk',fh:86,kind:'v',name:'Lý Thường Kiệt',sub:sub||'Đại Việt',below:below!==false,t0:1.5});
const Lf=(u,v,o)=>['fig',u,v,'L',Object.assign({key:'ltk'},o||{})];
const F=(t,u,v,o)=>['fig',u,v,t,o||{}];
// 1 vượt biên đêm
R2('hoBien',{river:[-40,40],road:[130,130],rw:56,tint:'#cfd3b0'},[['hl',-760,-260,2.3],['hl',420,-300,2.5],['h',620,-190,1.4],['f',380,-120,14],['f',-520,-100,12],['k',150,30,70,5],F('v',-40,170,{w:1}),F('v',-170,190,{w:1}),F('v',-300,160,{w:1}),F('v',-440,185,{w:1}),F('v',90,175,{w:1}),F('s',470,-60,{arm:'spear'}),F('s',560,-40,{arm:'spear'})],[],{mv:[['v',7,-60,95,200,{arm:'spear'}]]});
// 2 lính canh Việt nhìn quân Tống từ xa
R2('canhGac',{river:[-120,-40],tint:'#dde0b8'},[['hl',-800,-300,2.4],['hl',-100,-340,2.1],['hl',620,-290,2.2],['t',-420,90,1.4,'#a8854e'],['f',-300,120,11],F('v',-120,130,{arm:'spear'}),F('v',60,160,{arm:'spear'}),F('v',-260,175,{arm:'bow'}),F('s',-300,-200,{walk:0}),F('s',-180,-210),F('s',40,-190),F('s',220,-215),F('s',400,-195),F('s',560,-220)],[],{mv:[['s',6,50,90,-170,{arm:'spear'}]]});
// 3-4 hai hướng: quân Việt tiến một bên sông, quân Tống đứng canh bên kia
R2('haiHuong',{river:[-20,70],tint:'#e3dcb8'},[['h',-640,-170,1.3],['h',660,-180,1.3],['b',200,10,{al:1}],['tp',-300,-220,1.2],F('L',-470,150,{arm:'point',key:'ltk'}),F('v',-600,180),F('v',-700,160),F('v',-340,200),F('s',470,-40),F('s',560,-10),F('s',650,-30),F('s',720,20)],[LB('chỉ huy',false)],{mv:[['v',4,70,90,230,{arm:'spear'}]]});
// 5-6 nhìn về phía bắc từ đồi
R2('nhinBac',{tint:'#e8dfb8',top:.7},[['hl',-700,-250,2.6,'#8da16e'],['hl',100,-330,3,'#97a97a'],['hl',700,-250,2.5],['g',480,-190,1.6],F('L',-120,150,{arm:'point',key:'ltk',flip:false}),F('v',-290,170),F('v',-360,200),F('v',140,190,{flip:true})],[LB('nhìn về phía bắc')]);
// 7 phường Thái Hòa: nhà, chợ
R2('phuong',{road:[150,150],rw:90,tint:'#e6dcb4'},[['h',-700,-170,1.4],['h',-380,-200,1.2],['h',200,-190,1.3],['h',560,-160,1.5],['t',-120,-80,1.0,'#b89862'],['t',360,-60,1.0,'#a8854e'],F('d',-60,-20,{sw:1}),F('d',-180,-10,{sw:1}),F('d',320,10,{sw:1}),F('w',420,20,{sw:1}),F('d',-560,60),F('d',-460,80,{flip:true})],[],{mv:[['d',5,40,110,200,{sack:true}],['q',2,-30,160,300]]});
// 8-9 gia đình quan: sân nhà, cha và con
R2('giaDinh',{tint:'#ead9b4',top:.7},[['h',-420,-180,1.9],['h',460,-200,1.7],['tp',0,-250,1.0],['tr',-760,-60,1.3],['tr',780,-30,1.2],F('q',-90,100,{sw:1}),F('d',30,120,{sz:52,flip:true}),F('d',-250,150,{flip:true}),F('w',320,140,{flip:true})],[]);
// 10-12 triều đường
R2('trieuDuong',{tint:'#e0cfa4',top:.8},[['g',0,-260,2.2],['h',-760,-160,1.6],['h',760,-160,1.6],F('k',0,-120,{arm:'none',sw:1}),F('q',-380,-10),F('q',-250,0),F('q',-120,10),F('q',120,10,{flip:true}),F('q',250,0,{flip:true}),F('q',380,-10,{flip:true}),Lf(-40,150),F('v',-500,160,{arm:'spear'}),F('v',500,160,{arm:'spear',flip:true})],[LB('trong triều')]);
// 13 hạm đội vua Lý ra khơi
R2('hamDoi',{sea:-90,tint:'#e3dcb8'},[['b',-500,-250,{}],['b',-120,-300,{}],['b',300,-230,{}],['b',640,-290,{}],['b',-260,-150,{}],F('L',-60,150,{arm:'point',key:'ltk'}),F('v',-180,170),F('v',70,180,{flip:true})],[LB('theo vua nam chinh')],{trees:3});
// 14 Chiêm Thành: thành đất bị chiếm, voi chiến
R2('chiemThanh',{tint:'#e9d8a8'},[['g',-360,-210,1.9],['h',-640,-130,1.1,2],['h',580,-190,1.2,3],['e',260,60,1.2,1],['e',480,100,1.2,0],F('v',-60,110,{arm:'spear'}),F('v',-180,130,{arm:'spear'}),F('v',60,160,{arm:'spear',flip:true}),F('d',360,-10,{flip:true,sz:60,hat:'cap'})],[]);
// 15-16 nhận chức Thái úy
R2('thaiUy',{tint:'#e6d3a8',top:.8},[['g',0,-240,1.8],['h',-740,-150,1.3],['h',740,-150,1.3],F('k',150,-60,{flip:true}),Lf(-60,60,{arm:'none'}),F('q',-300,100),F('q',-420,120),F('q',330,120,{flip:true}),F('v',-560,170,{arm:'spear'}),F('v',560,170,{arm:'spear',flip:true})],[LB('Thái úy, năm 1075')]);
// 17-18 quân Tống làm đường, dựng trại ở biên
R2('tongBien',{road:[60,60],rw:120,tint:'#d9dcb4'},[['t',-560,-130,1.3,'#8d9bb5'],['t',-300,-170,1.3,'#a3aec4'],['t',560,-150,1.3,'#8d9bb5'],['k',300,70,60,6],['k',360,60,60,6],F('s',-80,10,{arm:'flail',sw:1}),F('s',20,40,{arm:'flail'}),F('s',120,0,{arm:'spear'}),F('w',-200,160,{arm:'flail',sw:1}),F('w',420,160,{arm:'flail'})],[],{mv:[['w',4,60,100,180,{sack:true,sz:62}]]});
// 19-20 triều Tống
R2('trieuTong',{tint:'#d8dce6',top:.8},[['g',0,-250,2.2],['h',-720,-170,1.5],['h',720,-170,1.5],F('qs',-340,-20),F('qs',-210,0),F('qs',-90,10),F('qs',100,10,{flip:true}),F('qs',230,0,{flip:true}),F('qs',360,-20,{flip:true}),F('k',0,-100,{col:'#3d5a8a'}),F('s',-520,150,{arm:'spear'}),F('s',520,150,{arm:'spear',flip:false})],[]);
// 21 Vương An Thạch: bàn viết, người xếp hàng
R2('vuongAnThach',{tint:'#dde0e8',top:.8},[['h',-620,-170,1.6],['h',620,-190,1.6],['t',0,-70,1.5,'#6a6a7a'],F('qs',0,30,{key:'van',sw:1}),F('d',-200,150,{walk:0}),F('d',-300,170),F('d',-410,160),F('w',280,150,{flip:true}),F('qs',-120,70,{flip:true,sz:60})],[{key:'van',fh:70,kind:'s',name:'Vương An Thạch',sub:'người cải cách nhà Tống',t0:1.5,below:true}]);
// 22-23 lính Tống tập luyện
R2('taoLuyen',{tint:'#d9dcb4',road:[150,150]},[['t',-640,-150,1.4,'#8d9bb5'],['t',600,-170,1.4,'#a3aec4'],['hl',0,-340,2.6,'#8fa070']].concat([-380,-220,-60,100,260,420].map((u,i)=>F('s',u,40+(i%2)*14,{arm:'spear',rot:Math.sin(0+i)*4,sw:1}))).concat([F('qs',-60,-80,{sz:76,hat:'quan'}),F('s',-300,180,{arm:'bow'}),F('s',-120,200,{arm:'bow'})]),[]);
// 24 xưởng đóng thuyền
R2('xuongThuyen',{river:[-170,40],road:[140,150],tint:'#e3dcb8'},[['b',-420,-60,{al:.5}],['b',-40,-70,{al:.8}],['b',340,-60,{al:.35}],['h',-720,-230,1.3],['h',700,-240,1.3],F('qs',-250,120,{key:'tk',sw:1}),F('qs',250,130,{key:'ld',flip:true}),F('w',-100,60,{arm:'flail',sw:1}),F('w',60,80,{arm:'flail'}),F('w',-360,70,{arm:'flail'}),F('d',480,100,{sack:true,w:1})],[{key:'tk',fh:70,kind:'s',name:'Thẩm Khởi',sub:'quan nhà Tống',t0:1.5,below:true},{key:'ld',fh:70,kind:'s',name:'Lưu Di',sub:'quan nhà Tống',t0:2.5,below:true}]);
// 25-26 họp bàn trong triều Lý
R2('hopBan',{tint:'#e0cfa4',top:.8},[['h',-700,-170,1.5],['h',720,-170,1.5],['g',0,-250,1.7],['t',0,-30,1.8,'#9a6e3a'],F('k',0,-100,{sw:1}),Lf(-210,80,{arm:'point'}),F('q',-380,130),F('q',280,100,{flip:true}),F('q',420,130,{flip:true}),F('v',-520,170,{arm:'spear'})],[LB('bàn việc nước',false)]);
// 27 tháp canh đêm
R2('thapCanh',{tint:'#cfd3b0'},[['g',60,-200,2.0],['hl',-760,-250,2.4],['hl',700,-300,2.6],['f',-120,-60,12],['f',280,-40,12],Lf(-30,110,{arm:'point'}),F('v',-210,160,{flip:false}),F('v',150,170,{flip:true})],[LB('trước khi quyết định')]);
// 28-29 xuất quân
R2('xuatQuan',{road:[110,110],rw:80,tint:'#d9dcb4'},[['t',-700,-140,1.4,'#a3541e'],['t',-420,-190,1.4,'#8a5a2b'],['t',640,-180,1.4,'#a3541e'],Lf(-160,60,{arm:'point'}),F('v',-300,130,{arm:'spear'}),F('v',-40,130,{arm:'spear'}),F('v',80,110,{arm:'spear'}),F('q',300,60,{flip:true,sz:66})],[LB('chỉ huy chiến dịch',false)],{mv:[['v',9,80,88,190,{arm:'spear'}]]});
// 30 thanh miêu
R2('thanhMieu',{road:[160,160],tint:'#e3dcb8'},[['h',-560,-150,1.4],['h',-100,-190,1.3],['h',520,-150,1.5],['t',120,-30,1.5,'#6a6a7a'],F('qs',120,60,{key:'ts',flip:true,sw:1}),F('qs',250,90,{flip:true,sz:62}),F('d',-60,150,{w:0}),F('d',-170,170,{sz:60}),F('d',-290,150),F('w',20,170,{sack:true}),F('s',380,110,{arm:'spear',flip:true})],[]);
// 31-32 lều quân: bàn chiến lược
R2('leuQuan',{tint:'#d9dcb4'},[['t',-300,-170,2.4,'#a3541e'],['t',420,-150,1.6,'#8a5a2b'],['t',-740,-130,1.3,'#a3541e'],['f',100,90,12],Lf(-90,100,{arm:'point'}),F('v',-250,140,{sw:1}),F('v',60,150,{flip:true}),F('q',230,170,{flip:true}),F('v',-440,185,{arm:'spear'})],[LB('lập kế hoạch tiến công')]);
// 34 thuyền chiến Việt đánh vào bờ biển Tống
R2('duongBien',{sea:-100,tint:'#e3dcb8'},[['b',-560,-300,{}],['b',-120,-260,{}],['b',320,-320,{}],['b',620,-250,{}],['h',-560,60,1.2,2],['h',-80,40,1.3,4],['h',380,70,1.2,3],['h',700,50,1.1],F('v',-300,130,{arm:'spear',w:1}),F('v',-120,150,{arm:'spear',w:1}),F('v',140,150,{arm:'spear',w:1}),F('s',520,150,{arm:'flail'}),F('s',-400,175,{arm:'spear'})],[],{trees:2});
// 35 Khâm Châu, Liêm Châu: đổ bộ, thành nhỏ cháy
R2('khamChau',{sea:-60,tint:'#e9d8a8'},[['g',100,-190,1.7],['h',-640,-80,1.3,2.5],['h',-300,-100,1.2,3.5],['h',560,-100,1.4,4.5],['b',-480,-220,{}],['b',420,-240,{}],F('v',-120,100,{arm:'spear',w:1}),F('v',20,130,{arm:'spear',w:1}),F('v',200,110,{arm:'spear'}),F('s',-260,60,{arm:'spear',flip:true})],[],{trees:3});
// 36-37 hành quân qua núi
R2('duongNui',{road:[70,150],rw:60,tint:'#d4dfb0'},[['hl',-760,-260,3,'#8da16e'],['hl',-200,-330,3.2,'#7f9462'],['hl',420,-260,2.8,'#97a97a'],['hl',800,-330,2.6]],[],{trees:16,vmin:260,mv:[['v',13,-70,86,170,{arm:'spear'}],['d',3,-60,160,260,{sack:true}]]});
// 38-39 Côn Lôn: chặn viện binh (cảnh ải cũ)
// 40 đến sát Ung Châu (nhìn từ xa)
R2('ucXa',{river:[-220,-140],tint:'#e3dcb8'},[['g',0,-300,2.0],['h',-300,-300,1.2],['h',320,-310,1.2],['h',-600,-250,1.0],['h',620,-260,1.0],F('v',-280,60,{arm:'spear'}),F('v',-120,90,{arm:'spear'}),F('v',60,60,{arm:'spear'}),F('v',220,100,{arm:'spear'}),F('v',360,70,{arm:'spear'}),F('s',-120,-250,{arm:'bow'}),F('s',40,-260,{arm:'bow'}),F('s',200,-250,{arm:'bow'})],[],{mv:[['v',5,-30,90,170,{arm:'spear'}]]});
// 41 trên mặt thành: lính Tống phòng thủ
R2('mattThanh',{tint:'#d4d8e0',top:.8},[['g',0,-250,2.4],['k',-500,-200,50,5],['k',500,-200,50,5]].concat([-560,-420,-280,-140,140,280,420,560].map((u,i)=>F('s',u,-80+(i%2)*10,{arm:i%2?'bow':'spear',flip:false}))).concat([F('qs',0,40,{sz:78,flip:false}),F('s',-300,160,{arm:'spear'}),F('s',300,170,{arm:'spear'})]),[]);
// 42-43 đắp đồi đất, thang, đào
R2('daoDat',{tint:'#e3dcb8',road:[200,200]},[['hl',-100,-60,1.6,'#b4986a'],['hl',140,-40,1.3,'#b4986a'],['g',-480,-250,1.5],F('v',-20,60,{arm:'flail',sw:1}),F('v',120,70,{arm:'flail'}),F('v',-160,90,{arm:'flail'}),F('d',280,130,{sack:true,w:1}),F('d',420,150,{sack:true,w:1}),F('d',560,130,{sack:true,w:1})],[],{mv:[['d',6,70,100,210,{sack:true}]]});
// 44-46 đối đầu quanh chân thành: tên bay (cảnh uc gốc) -> dùng 'uc'
// 47 tờ lịch bốn mươi ngày: cắm cọc đếm (cảnh đồng không có người)
R2('doDem',{tint:'#e9dfbf'},[['g',480,-260,1.7],['k',-420,80,60,6],['k',-340,90,60,6],['k',-260,80,60,6],['k',-180,90,60,6],['k',-100,80,60,6],['k',-20,90,60,6],['k',60,80,60,6],['f',-520,140,11],['f',200,120,11],F('v',-420,160,{sw:1}),F('v',330,140,{flip:true,arm:'spear'})],[]);
// 48-49 thành sau trận: khói, dân tản
R2('thanhHoang',{tint:'#d9cfb0'},[['h',-560,-130,1.4,0.2],['h',-220,-170,1.3,0.2],['h',320,-150,1.5,0.2],['h',700,-180,1.2,0.2],['f',-560,-160,15],['f',320,-180,15],['g',60,-290,1.7],F('d',-100,80,{walk:0,sw:1}),F('d',20,110,{sz:58}),F('d',-250,130,{flip:true,sack:true,w:1}),F('w',150,140,{flip:true,sack:true,w:1}),F('v',420,130,{arm:'spear'})],[]);
// 50-51 rút quân với xe và lương
R2('rutQuan',{river:[-200,-110],road:[140,160],rw:70,tint:'#e3dcb8'},[['hl',-700,-330,2.2],['b',-100,-155,{al:.9}]],[],{mv:[['v',9,-90,88,170,{arm:'spear',sack:true}],['d',3,-70,110,260,{sack:true}]]});
// 52-53 trạm gác biên giới lúc hoàng hôn
R2('tramGac',{tint:'#e8d6a8',top:.7},[['g',420,-180,1.6],['k',-300,-50,90,6],['f',-200,70,14],F('L',-80,130,{arm:'none',key:'ltk'}),F('v',-300,110,{arm:'spear'}),F('v',60,185,{flip:true,arm:'spear'}),F('s',640,-80,{arm:'spear'})],[LB('nhìn lại phía sau',false)]);
// 54 trại Tống tập kết
R2('tongKetTap',{tint:'#d4d8e0'},[['t',-640,-180,1.6,'#8d9bb5'],['t',-340,-220,1.6,'#a3aec4'],['t',0,-240,1.8,'#8d9bb5'],['t',380,-210,1.6,'#a3aec4'],['t',680,-170,1.6,'#8d9bb5'],['f',-100,60,12],F('s',-380,70,{arm:'spear',sw:1}),F('s',-200,100,{arm:'spear'}),F('s',100,90,{arm:'spear'}),F('s',260,130,{arm:'spear'}),F('qs',-20,150,{sz:76})],[]);
// 55 Quách Quỳ cưỡi đi đầu bộ binh
R2('quachQuy',{road:[110,130],rw:56,tint:'#d9dcb4'},[['hl',-600,-330,2.4],['hl',500,-330,2.4],F('qs',-80,120,{key:'qq',sz:84,flip:false,w:1,plume:true})],[{key:'qq',fh:84,kind:'s',name:'Quách Quỳ',sub:'chỉ huy bộ binh nhà Tống',t0:1.5,below:true}],{mv:[['s',11,86,84,200,{flip:false}]]});
// 56 nhìn sông Như Nguyệt từ gò cao
R2('nhinSong',{river:[-210,-120],tint:'#e3dcb8'},[['hl',-600,-380,2.3],['hl',420,-380,2.3],Lf(-200,150,{arm:'point'}),F('v',-340,180),F('v',-70,190,{flip:true}),F('s',-140,-300,{arm:'spear'}),F('s',100,-290,{arm:'spear'}),F('s',380,-300,{arm:'spear'})],[LB('chọn nơi đón địch')],{trees:8});
// 58-60 phòng tuyến trên bản đồ (không cận cảnh) -- map only
// 61 đóng cọc, hàng rào bờ sông
R2('phongTuyen',{river:[-260,-150],tint:'#e3dcb8',road:[130,130]},[['b',-200,-205,{al:.4}]].concat([-760,-640,-520,-400,-280,-160,-40,80,200,320,440,560,680].map((u,i)=>['k',u,-130+(i%2)*6,48,5])).concat([F('v',-300,60,{arm:'flail',sw:1}),F('v',-120,80,{arm:'flail'}),F('v',100,60,{arm:'flail'}),F('d',320,120,{sack:true,w:1}),F('d',460,140,{sack:true,w:1}),F('v',-460,100,{arm:'spear'})]),[]);
// 62 gác đêm trên phòng tuyến
R2('gacDem',{river:[-230,-120],tint:'#cfd3b0'},[['f',-440,40,12],['f',200,50,12],['f',620,20,11]].concat([-760,-560,-360,-160,40,240,440,640].map((u,i)=>['k',u,-100,46,5])).concat([F('v',-300,80,{arm:'spear'}),F('v',-220,110,{arm:'spear',flip:true}),F('v',280,100,{arm:'bow'}),F('v',380,120,{arm:'bow'}),F('s',-120,-330,{arm:'spear'})]),[]);
// 65-66 quân dự bị chạy dọc bờ
R2('quanDuBi',{river:[-240,-130],road:[110,110],rw:60,tint:'#dde0b8'},[['h',560,-190,1.2]],[LB('điều quân dọc bờ sông',true)],{mv:[['v',8,130,80,100,{arm:'spear'}]],dyn:c=>FG(c,-300,170,{sz:86,col:'#7a3b1c',trou:'#4a2a1a',hat:'ltk',hatcol:'#b3261e',arm:'point',armor:true,pauld:true,acol:'#b08a3a',cape:true,beard:true},'ltk')});
// 69-70 đường đêm tới đền
R2('denDem',{road:[130,130],rw:40,tint:'#c9cfae'},[['tp',380,-180,1.6],['f',150,40,10],['f',-300,60,10],['hl',-700,-280,2.2],F('v',-120,130,{w:1,arm:'spear'}),F('v',-250,150,{w:1,arm:'spear'}),F('d',60,160,{flip:true,w:1})],[],{mv:[['v',6,50,100,200,{arm:'spear'}]]});
// 72-73 trong đền: hai vị thần, quân sĩ quỳ
R2('trongDen',{tint:'#c9cfae',top:.9},[['tp',0,-190,2.2],['f',-300,40,10],['f',300,40,10]].concat([-360,-200,-40,120,280,440].map((u,i)=>F('v',u,100+(i%2)*22,{arm:'none',rot:60*(i%3==0?0:1)*0,sw:1}))).concat([F('d',-100,190,{sw:1})]),[]);
// 74-77 rạng sáng bờ sông, quân đứng nghe
R2('binhMinh',{river:[-210,-100],tint:'#ecdcb4',top:.7},[['hl',-700,-380,2.6,'#9aa57a'],['hl',480,-390,2.8,'#97a97a'],['tp',-480,-260,1.1]].concat([-520,-380,-240,-100,40,180,320,460,600].map((u,i)=>F('v',u,70+(i%3)*30,{arm:i%2?'spear':'bow',d:0,sw:1}))).concat([Lf(-60,200,{arm:'none'})]),[LB('đọc bài thơ bên sông')]);
// 78 Việt nghỉ bên đống lửa
R2('nghiNgoi',{tint:'#d9dcb4'},[['f',-100,80,13],['f',360,100,12],['t',-520,-110,1.4,'#a3541e'],['t',600,-100,1.4,'#8a5a2b']].concat([-260,-180,-20,60,220,300,480].map((u,i)=>F('v',u,100+(i%3)*24,{arm:'none',rot:i%2?80:-80,flip:i%2==0,sw:0}))),[]);
// 79-80 lương Tống cạn: bao rỗng, ngựa mệt
R2('luongTong',{tint:'#d4d8e0'},[['t',-560,-140,1.4,'#8d9bb5'],['t',480,-150,1.4,'#a3aec4']].concat([-220,-100,40,160,300].map((u,i)=>F('s',u,50+(i%2)*30,{arm:'none',rot:i%2?70:-70,flip:i%2==0}))).concat([F('d',-340,160,{sack:true,w:0}),F('d',-440,180,{sack:true,sz:60}),F('qs',360,120,{sz:72})]),[]);
// 81-83 lều đêm: Lý Thường Kiệt suy nghĩ
R2('leuDem',{tint:'#cfd3b0',top:.9},[['t',-200,-170,2.6,'#a3541e'],['t',500,-120,1.4,'#8a5a2b'],['f',-60,70,14],Lf(-260,100,{arm:'none'}),F('v',80,110,{flip:true,sw:1}),F('q',240,150,{flip:true})],[LB('cân nhắc: đánh tiếp hay thương lượng')]);
// 84-85 đàm phán
R2('thuongLuong',{tint:'#e0d8b8'},[['t',0,-60,1.4,'#6a6a7a'],['h',-720,-180,1.3],['h',720,-190,1.3],Lf(-260,70,{arm:'none'}),F('v',-400,110,{arm:'spear'}),F('v',-520,150,{arm:'spear'}),F('qs',250,70,{flip:true}),F('s',380,110,{arm:'spear',flip:true}),F('s',500,150,{arm:'spear',flip:true})],[LB('đề nghị thương lượng',false)]);
// 86 quân Tống rút
R2('tongRut',{road:[110,130],rw:70,tint:'#dde0b8'},[['hl',-500,-330,2.4],['hl',600,-340,2.4],['t',-760,-160,1.1,'#8d9bb5']],[],{mv:[['s',10,-80,90,150,{arm:'spear',sack:true}]]});
// 87-88 sứ đoàn Việt: viết thư, bản đồ
R2('ngoaiGiao',{tint:'#e6d3a8',top:.8},[['g',0,-260,1.8],['h',-740,-150,1.3],['h',740,-150,1.3],['t',-100,10,1.3,'#9a6e3a'],F('q',-250,70,{sw:1}),F('q',60,70,{flip:true,sw:1}),F('q',-360,130),F('v',-560,170,{arm:'spear'}),F('v',560,170,{arm:'spear',flip:true})],[]);
// 90 trao đất: cột mốc, hai đoàn trao nhận
R2('traDat',{tint:'#e3dcb8',road:[120,120]},[['k',0,60,90,10],['hl',-760,-300,2.2],['hl',700,-300,2.2],F('q',-200,70,{key:'qa'}),F('qs',200,70,{flip:true}),F('v',-340,110,{arm:'spear'}),F('v',-420,140,{arm:'spear'}),F('s',340,110,{arm:'spear',flip:true}),F('s',420,140,{arm:'spear',flip:true})],[]);
// 91-92 trao đổi tù binh
R2('traTu',{road:[120,120],rw:60,tint:'#e3dcb8'},[['hl',-760,-300,2.2],['hl',700,-300,2.2],['k',0,40,90,8],F('v',-440,100,{arm:'spear'}),F('s',440,100,{arm:'spear',flip:true})],[],{mv:[['d',5,45,90,160,{sack:false,hat:'cap'}],['s',4,-40,90,240,{arm:'none',hat:'cap'}]]});
// 93-94 hội đàm Vĩnh Bình (nhà rạp)
R2('vinhBinh',{tint:'#e3dcb8'},[['tp',0,-190,1.5],['t',-520,-110,1.4,'#a3541e'],['t',520,-110,1.4,'#8d9bb5'],F('q',-220,50,{sw:1}),F('q',-340,90),F('qs',220,50,{flip:true,sw:1}),F('qs',340,90,{flip:true}),F('v',-560,150,{arm:'spear'}),F('s',560,150,{arm:'spear',flip:true})],[]);
// 98-99 Thái úy, người có thế lực trong chính sự (tl gốc dùng ở đây)
// 100 Lý Giác nổi dậy ở Diễn Châu
R2('dienChau',{tint:'#d9dcb4',road:[160,150]},[['h',-640,-100,1.3,3],['h',-260,-140,1.2,5],['h',480,-130,1.3],['f',-640,-120,14],F('d',-120,70,{arm:'spear',sz:66,hat:'cap'}),F('d',-20,100,{arm:'spear',hat:'cap'}),F('d',100,80,{arm:'flail',hat:'cap'}),F('v',380,120,{arm:'spear',flip:true}),F('v',480,150,{arm:'spear',flip:true})],[],{mv:[['v',6,-60,86,200,{arm:'spear'}]]});
// 103 tuổi già: triều đường buổi chiều
R2('tuoiGia',{tint:'#ecd9b4',top:.7},[['h',-480,-160,1.6],['g',380,-200,1.4],['tr',-760,0,1.4],Lf(-80,110,{arm:'none',sw:1}),F('q',140,140,{flip:true,sz:60}),F('v',-250,170,{arm:'spear'})],[LB('những năm cuối đời')]);
// 110-111 ngã ba: hai con đường
R2('nga3',{tint:'#e3dcb8'},[['hl',-640,-300,2.3],['hl',640,-300,2.3],['tr',0,-250,1.8],Lf(0,120,{arm:'none',sw:1}),F('v',-200,160,{arm:'spear'}),F('v',220,160,{arm:'spear',flip:true})],[LB('hai nước cờ')]);
// 112-113 hậu cần, địa hình, thời điểm: kho lương, sông, đồi
R2('hauCan',{river:[-230,-140],road:[130,130],rw:60,tint:'#e3dcb8'},[['h',-600,-80,1.4],['h',-360,-100,1.3],['h',520,-90,1.4],['hl',100,-380,2.6],['b',-60,-185,{al:.9}],F('d',-480,120,{sack:true,w:1}),F('d',-300,150,{sack:true,w:1}),F('v',360,120,{arm:'spear'})],[],{mv:[['d',4,60,100,190,{sack:true}]]});
// 114-115 kết: bờ sông lúc bình minh, đoàn quân đứng sau
R2('songSang',{river:[-210,-100],tint:'#f0e0b8',top:.6},[['hl',-640,-380,2.8,'#9aa57a'],['hl',560,-390,2.6,'#97a97a'],['tp',-440,-250,1.2]].concat([-420,-300,-180,-60,320,440,560].map((u,i)=>F('v',u,70+(i%2)*26,{arm:'spear',sw:1}))).concat([Lf(110,170,{arm:'none',sw:1})]),[LB('một người, hai nước cờ')]);
// ===== Cảnh chính video Nguyên Mông (nm5) =====
const NB_=(key,name,sub,t0)=>({key,fh:78,kind:'v',name,sub,below:true,t0:t0||1.5});
const NS_=(key,name,sub,t0)=>({key,fh:78,kind:'s',name,sub,below:true,t0:t0||1.5});
// đoạn 1: quân Mông Cổ mở kho lương ở Thăng Long, kho trống
R2('nmKho',{road:[150,150],rw:90,tint:'#e0d6b0',top:.8},[['h',-620,-180,1.5],['h',640,-190,1.5],['g',0,-250,2.6],['tp',-300,-260,1.1],['f',-200,70,10],F('s',-240,120,{arm:'spear'}),F('s',-120,150,{arm:'spear'}),F('s',120,150,{arm:'spear',flip:true}),F('s',240,120,{arm:'spear',flip:true}),F('qs',0,60,{key:'tuong',sw:1}),F('s',-40,190,{arm:'none'}),F('s',60,200,{arm:'none'})],[NS_('tuong','Quân Mông Cổ','mở cửa kho lương')],{trees:6});
// đoạn 22–23: Thăng Long vắng người
R2('nmPho',{road:[140,140],rw:100,tint:'#e6dcb4'},[['h',-700,-170,1.5],['h',-420,-190,1.3],['h',-160,-200,1.4],['h',220,-190,1.4],['h',500,-170,1.5],['h',760,-190,1.3],['tr',-860,-60,1.2],['tr',900,-40,1.2]],[NS_('t','Quân Mông Cổ','đi giữa phố không người',2.0)],{trees:4,mv:[['s',9,70,110,150,{arm:'spear'}],['s',4,-45,185,210,{arm:'none'}]]});
// đoạn 40: hội nghị Diên Hồng
R2('nmDienHong',{tint:'#e6d3a8',top:.8},[['tp',0,-250,2.0],['h',-760,-160,1.4],['h',760,-160,1.4],F('k',0,-70,{key:'vua',arm:'none',sw:1}),F('d',-380,60,{sw:1}),F('d',-260,80,{sw:1}),F('d',-140,60,{sw:1}),F('d',140,60,{flip:true,sw:1}),F('d',260,80,{flip:true,sw:1}),F('d',380,60,{flip:true,sw:1}),F('d',-320,170,{sw:1}),F('d',-180,190,{sw:1}),F('d',-40,170,{sw:1}),F('d',100,190,{flip:true,sw:1}),F('d',240,170,{flip:true,sw:1}),F('d',380,190,{flip:true,sw:1}),F('q',-520,120),F('q',520,120,{flip:true})],[NB_('vua','Vua Trần Nhân Tông','hỏi nên đánh hay hòa'),{key:'cu',fh:60,kind:'v',name:'Các bô lão',sub:'đồng thanh: đánh',below:true,t0:3.5}],{trees:4});
// đoạn 52–54: Trần Bình Trọng bị bắt ở bãi Đà Mạc
R2('nmBinhTrong',{river:[-230,-140],tint:'#d9dcb4'},[['t',-620,-100,1.5,'#8d9bb5'],['t',560,-110,1.5,'#a3aec4'],['f',-380,110,12],F('v',0,120,{key:'bt',arm:'none',armor:true,sz:76}),F('s',-120,130,{arm:'spear',flip:false}),F('s',130,130,{arm:'spear',flip:true}),F('qs',250,70,{flip:true}),F('s',-300,170,{arm:'spear'}),F('s',340,175,{arm:'spear',flip:true}),F('v',-640,190,{arm:'spear',rot:70}),F('v',-520,200,{arm:'none',rot:80})],[NB_('bt','Trần Bình Trọng','bị bắt ở bãi Đà Mạc')],{trees:6});
// đoạn 62–65: trận Hàm Tử, Chương Dương
R2('nmHamTu',{river:[-190,-90],tint:'#e3dcb8'},[['hl',-760,-330,2.3],['hl',640,-340,2.3],['b',-300,-140,{al:1}],['b',160,-130,{al:1}],['b',560,-150,{al:1,burn:.8}],['f',560,-110,10],F('v',-500,150,{arm:'bow'}),F('v',-380,170,{arm:'spear'}),F('v',-250,150,{arm:'spear'}),F('v',-130,175,{arm:'bow'}),F('L',-330,110,{key:'nd',arm:'point'}),F('s',250,150,{arm:'spear',flip:true}),F('s',370,170,{arm:'bow',flip:true}),F('s',490,150,{arm:'spear',flip:true}),F('s',130,170,{arm:'spear',flip:true}),['vol',-120,100,260,130,9],['vol',380,90,-120,120,7]],[NB_('nd','Trần Nhật Duật','đánh quân Toa Đô')],{trees:3});
// đoạn 83–84: Vân Đồn, đánh đoàn thuyền chở lương
R2('nmVanDon',{sea:-110,tint:'#e3dcb8'},[['b',-620,-300,{al:1}],['b',-240,-260,{al:1}],['b',160,-310,{al:1,burn:.9,rot:-3}],['b',520,-270,{al:1,burn:.6,rot:4}],['b',860,-320,{al:1,burn:.3}],['f',160,-270,16],['f',520,-240,14],F('v',-420,130,{arm:'bow'}),F('v',-300,160,{arm:'bow'}),F('v',-180,130,{arm:'spear'}),F('v',-540,170,{arm:'bow'}),F('v',-60,170,{arm:'bow'}),['vol',-320,100,200,-200,10],['vol',-180,110,520,-210,8]],[],{trees:3});
// đoạn 97–100: cọc ngầm dưới sông Bạch Đằng, nước đang lên
R2('nmCoc',{river:[-190,-20],tint:'#e3dcb8',top:.7},[['hl',-780,-330,2.4],['hl',760,-340,2.4]].concat([-700,-560,-420,-280,-140,0,140,280,420,560,700].map((u,i)=>['k',u,-120+(i%2)*30,56,5])).concat([['b',-760,-130,{al:.8,rot:-2}],['b',-420,-80,{al:.8}],F('v',-300,190,{arm:'spear'}),F('v',-160,205,{arm:'spear'}),F('L',-30,170,{key:'tqt',arm:'point'}),F('v',130,200,{arm:'bow'}),F('v',280,185,{arm:'spear'})]),[NB_('tqt','Trần Quốc Tuấn','cho đóng cọc nhọn bịt sắt')],{trees:3});
// đoạn 101–105: thủy triều rút, thuyền chiến mắc cọc
R2('nmBachDang',{river:[-190,-20],tint:'#e3dcb8',top:.7},[['hl',-780,-330,2.4],['hl',760,-340,2.4]].concat([-700,-560,-420,-280,-140,0,140,280,420,560,700].map((u,i)=>['k',u,-120+(i%2)*30,56,5])).concat([['b',-560,-100,{al:1,burn:.9,rot:6}],['b',-200,-70,{al:1,burn:.7,rot:-5}],['b',200,-110,{al:1,burn:.9,rot:7}],['b',600,-90,{al:1,burn:.5,rot:-4}],['f',-560,-90,16],['f',200,-100,16],['f',-200,-60,12],F('v',-420,190,{arm:'bow'}),F('v',-280,205,{arm:'bow'}),F('v',-120,190,{arm:'spear'}),F('v',60,205,{arm:'bow'}),F('v',320,190,{arm:'bow'}),['vol',-300,170,-200,-80,10],['vol',60,170,200,-100,10],['vol',320,170,600,-90,8]]),[],{trees:3});
