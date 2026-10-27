from lh6_content import *
_u=[p for p in PROPS if p[2]=='granary' and abs(p[3]-105.95)<0.2]
for p in _u: PROPS.remove(p)
PROPS.append((R(101,0.3),E(101,0),'plough',105.95,20.63,'',1.15))
FOC.append((101,101,[(105.95,20.63)],True))
