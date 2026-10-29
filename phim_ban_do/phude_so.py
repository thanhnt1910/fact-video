"""Phụ đề hiện SỐ cho ngày, tháng, năm (giọng vẫn đọc bằng chữ). Quy tắc CLAUDE.md 28–29/10/2026.
chuyen(chunks) nhận danh sách đoạn phụ đề của một câu [[text, ...], ...] và trả về bản sao đã đổi chữ thành số (kể cả khi số bị tách qua hai đoạn)."""
import re
_D={'một':1,'mốt':1,'hai':2,'ba':3,'bốn':4,'tư':4,'năm':5,'lăm':5,'sáu':6,'bảy':7,'tám':8,'chín':9}
def _g(tk,j): return re.sub(r'[^\w]','',tk[j].lower()) if 0<=j<len(tk) else ''
def _small(tk,i):
    """1–99 bắt đầu ở tk[i]: (giá trị, số chữ) hoặc None."""
    g=lambda j:_g(tk,j)
    if g(i)=='mười':
        if g(i+1) in ('lăm','một','hai','ba','bốn','sáu','bảy','tám','chín'): return 10+_D[g(i+1)],2
        return 10,1
    if g(i) in _D and g(i+1)=='mươi':
        if g(i+2) in _D and not(g(i+2)=='năm' and g(i+3) in('tuổi','sau','trước')): return _D[g(i)]*10+_D[g(i+2)],3
        return _D[g(i)]*10,2
    if g(i) in _D: return _D[g(i)],1
    return None
def _nam(tk,i):
    g=lambda j:_g(tk,j); k=i; v=0
    if g(k) in _D and g(k+1)=='nghìn': v=_D[g(k)]*1000; k+=2
    if v and g(k)=='không' and g(k+1)=='trăm': k+=2
    elif g(k) in _D and g(k+1)=='trăm': v+=_D[g(k)]*100; k+=2
    elif v==0: return None
    if g(k) in('linh','lẻ') and g(k+1) in _D: return v+_D[g(k+1)],k+2-i
    s=_small(tk,k) if g(k) in('mười',) or (g(k) in _D and g(k+1)=='mươi') else None
    if s: return v+s[0],k+s[1]-i
    return v,k-i
def _thang(tk,i):
    g=_g(tk,i)
    if g=='giêng': return 1,1
    if g=='chạp': return 12,1
    s=_small(tk,i)
    if s and s[0]<=12: return s
    return None
def _ngay(tk,i):
    s=_small(tk,i)
    if s and 1<=s[0]<=31: return s
    return None
def _tok(words):
    """Gộp token: trả về danh sách (chữ hiển thị, chỉ số chữ đầu, số chữ gốc đã dùng)."""
    out=[];i=0;n=len(words)
    while i<n:
        g=_g(words,i)
        if g in('ngày','mồng') and i+1<n:
            d=_ngay(words,i+1)
            if d:
                j=i+1+d[1]; txt=f'{words[i]} {d[0]}'; used=1+d[1]
                if _g(words,j)=='tháng':
                    m=_thang(words,j+1)
                    if m:
                        j2=j+1+m[1]; txt=f'{words[i]} {d[0]}/{m[0]}'; used=j2-i
                out.append((txt,i,used)); i+=used; continue
        if g=='tháng' and i+1<n:
            m=_thang(words,i+1)
            if m: out.append((f'{words[i]} {m[0]}',i,1+m[1])); i+=1+m[1]; continue
        if g=='năm' and i+1<n:
            y=_nam(words,i+1)
            if y: out.append((f'{words[i]} {y[0]}',i,1+y[1])); i+=1+y[1]; continue
        out.append((words[i],i,1)); i+=1
    return out
def _punct(w):
    m=re.search(r'[^\w]+$',w); return m.group(0) if m else ''
def chuyen(chunks):
    flat=[];owner=[]
    for ci,c in enumerate(chunks):
        for w in c[0].split(): flat.append(w); owner.append(ci)
    toks=_tok(flat); newtxt=[[] for _ in chunks]
    for txt,i,used in toks:
        end_p=_punct(flat[i+used-1]) 
        if used>1:
            txt=re.sub(r'[^\w/]+$','',txt)+end_p
        newtxt[owner[i]].append(txt)
    out=[]
    for c,t in zip(chunks,newtxt):
        c2=list(c); c2[0]=' '.join(t); out.append(c2)   # đoạn rỗng (chữ đã gộp sang đoạn trước): build2.sub_at dùng lại chữ của đoạn trước
    return out
if __name__=='__main__':
    import json,sys
    d=json.load(open(sys.argv[1]))
    for n,cl in d.items():
        a=' '.join(c[0] for c in cl); b=' '.join(c[0] for c in chuyen(cl) if c[0])
        if a!=b: print(n,'\n  ',a,'\n  ',b)
