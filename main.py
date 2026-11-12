import json,os,sys,urllib.request as R
V={1:100,2:320,3:330,4:500,5:900,6:2e4}
O=((-33,-31,-18,-14,14,18,31,33),(-17,-15,15,17),(-16,-1,1,16),(-17,-16,-15,-1,1,15,16,17))
def p(f):
 d,b=f.split(),[0]*128
 for r,w in enumerate(d[0].split("/")):
  c=0
  for x in w:
   if x.isdigit():c+=int(x)
   else:b[(7-r)*16+c]=" PNBRQK".find(x.upper())*(1 if x.isupper() else -1);c+=1
 return b,1 if d[1]=="w" else -1,d[2],-1 if d[3]=="-" else ord(d[3][0])-97+(int(d[3][1])-1)*16
def i(b,sq,by):
 for s,p in enumerate(b):
  if s&0x88 or p*by<=0:continue
  pt=abs(p)
  if pt==1 and sq in(s+16*by-1,s+16*by+1):return 1
  if pt==6 and abs((sq>>4)-(s>>4))<=1 and abs((sq&7)-(s&7))<=1:return 1
  if pt>1:
   for df in O[pt-2-(pt==6)]:
    c=s
    while 1:
     c+=df
     if c&0x88:break
     if c==sq:return 1
     if b[c]:break
     if pt in(2,6):break
 return 0
def d(b,m,t):
 f,to,pr,ef=m;cp=b[to];b[to]=b[f];b[f]=0
 if pr:b[to]=pr*t
 es,ep2=-1,0
 if ef:es=to-16*t;ep2=b[es];b[es]=0
 ik=abs(b[to])==6 and abs(f-to)==2;rt=rx=0
 if ik:rt=to+1 if to>f else to-2;rx=to-1 if to>f else to+1;rk=b[rt];b[rt]=0;b[rx]=rk
 return cp,es,ep2,ik,rt,rx
def u(b,m,t,cp,es,ep2,ik,rt,rx):
 f,to,pr,ef=m
 if ik:rk=b[rx];b[rx]=0;b[rt]=rk
 if ef:b[es]=ep2
 b[f]=b[to] if not pr else t;b[to]=cp
def g(b,t,cr,ep):
 ms=[]
 for sq,p in enumerate(b):
  if sq&0x88 or p*t<=0:continue
  pt=abs(p)
  if pt==1:
   d_=16*t;w=sq+d_
   if not(w&0x88) and not b[w]:
    if (w>>4)in(0,7):
     for r in(5,4,3,2):ms.append((sq,w,r,0))
    else:ms.append((sq,w,0,0))
    if (sq>>4)==(1 if t==1 else 6)and not(sq+2*d_&0x88) and not b[sq+2*d_]:ms.append((sq,sq+2*d_,0,0))
   for df in(-1,1):
    cap=sq+d_+df
    if not(cap&0x88):
     if b[cap]*t<0 and abs(b[cap])!=6:
      if (cap>>4)in(0,7):
       for r in(5,4,3,2):ms.append((sq,cap,r,0))
      else:ms.append((sq,cap,0,0))
     elif cap==ep:ms.append((sq,cap,0,1))
  else:
   for df in O[pt-2-(pt==6)]:
    c=sq
    while 1:
     c+=df
     if c&0x88:break
     tg=b[c]
     if not tg:
      ms.append((sq,c,0,0))
      if pt in(2,6):break
     else:
      if tg*t<0 and abs(tg)!=6:ms.append((sq,c,0,0))
      break
     if pt in(2,6):break
   if pt==6:
    ks=next(s for s,x in enumerate(b) if not(s&0x88) and x==6*t)
    if not i(b,ks,-t):
     if t==1:
      if"K"in cr and not b[5] and not b[6] and b[7]==4 and not i(b,5,-t) and not i(b,6,-t):ms.append((4,6,0,0))
      if"Q"in cr and not b[3] and not b[2] and not b[1] and b[0]==4 and not i(b,3,-t) and not i(b,2,-t):ms.append((4,2,0,0))
     else:
      if"k"in cr and not b[117] and not b[118] and b[119]==-4 and not i(b,117,-t) and not i(b,118,-t):ms.append((116,118,0,0))
      if"q"in cr and not b[115] and not b[114] and not b[113] and b[112]==-4 and not i(b,115,-t) and not i(b,114,-t):ms.append((116,114,0,0))
 l=[]
 for m in ms:
  st=d(b,m,t)
  ks=next(s for s,x in enumerate(b) if not(s&0x88) and x==6*t)
  if not i(b,ks,-t):l.append(m)
  u(b,m,t,*st)
 return l
def e(b,t):
 m=0
 for s,p in enumerate(b):
  if not(s&0x88)and p:m+=(V[abs(p)]+(((s>>4)-1 if p>0 else 6-(s>>4))*5)*(abs(p)==1))*(1 if p>0 else -1)
 return m*t
def s(b,t,cr,ep,d_,a,bt,nl):
 if d_<1 or nl<1:return e(b,t),nl
 ms=g(b,t,cr,ep)
 if not ms:return(-1e5 if i(b,next(s_ for s_,x in enumerate(b) if not(s_&0x88) and x==6*t),-t) else 0),nl
 bs=-1e9
 for m in ms:
  st=d(b,m,t)
  sc,nl=s(b,-t,cr,ep,d_-1,-bt,-a,nl-1)
  u(b,m,t,*st)
  sc=-sc
  if sc>bs:bs=sc
  if bs>a:a=bs
  if a>=bt:break
 return bs,nl
def ch(fen,l):
 b,t,cr,ep=p(fen);bm=l[0];bs=-1e9
 for m in g(b,t,cr,ep):
  st=d(b,m,t);sc,_=s(b,-t,cr,ep,2,-1e6,1e6,3e4);u(b,m,t,*st)
  if -sc>bs:bs=-sc;f,to,pr,_=m;bm=f"{chr(97+(f&7))}{1+(f>>4)}{chr(97+(to&7))}{1+(to>>4)}{'nbrq'[pr-2]if pr else''}"
 return bm
if __name__=="__main__":
 E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit(0)
 q=lambda x,y=None:json.load(R.urlopen(R.Request(E+x,data=json.dumps(y or {}).encode(),headers={"content-type":"application/json"})))
 while 1:
  g_=q("/game",{})
  if g_["status"]=="done":break
  while g_["status"]=="your_move":
   g_=q("/move",{"game":g_["game"],"move":ch(g_["fen"],g_["legal_moves"])})
