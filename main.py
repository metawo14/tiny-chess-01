import json as J,os,urllib.request as R
V=0,100,320,330,500,900,2e4;O=(-33,-31,-18,-14,14,18,31,33),(-17,-15,15,17),(-16,-1,1,16),(-17,-16,-15,-1,1,15,16,17)
KL=[0]*7
def K(b,t):return b.index(6*t)
S=lambda x:chr(x%8+97)+str(x//16+1)
def p(f):
 d,b=f.split(),[0]*128
 for r,w in enumerate(d[0].split("/")):
  n=0
  for x in w:
   if x<'A':n+=int(x)
   else:b[(7-r)*16+n]=" PNBRQK".find(x.upper())*(2*(x<'a')-1);n+=1
 return b,(d[1]>"v")*2-1,d[2],-1 if d[3]<"a" else ord(d[3][0])+16*int(d[3][1])-113
def i(b,sq,by):
 for q,w in enumerate(b):
  if q&136 or w*by<1:continue
  pt=abs(w)
  if pt==1 and abs(sq-q-16*by)==1:return 1
  if pt==6 and abs(sq-q)in(1,15,16,17):return 1
  if pt>1:
   for df in O[pt-2-(pt>5)]:
    c=q
    while 1:
     c+=df
     if c&136:break
     if c==sq:return 1
     if b[c] or pt%4==2:break
 return 0
def mv(b,m,t):
 f,to,pr,ef=m;cp=b[to];b[to]=b[f];b[f]=0
 es,ep2=-1,0
 if pr:b[to]=pr*t
 if ef:es=to-16*t;ep2=b[es];b[es]=0
 ik=abs(b[to])==6 and abs(f-to)==2;rt=rx=0
 if ik:rt=to+(1,-2)[to<f];rx=to+(-1,1)[to<f];rk=b[rt];b[rt]=0;b[rx]=rk
 return cp,es,ep2,ik,rt,rx
def un(b,m,t,cp,es,ep2,ik,rt,rx):
 f,to,pr,ef=m
 if ik:rk=b[rx];b[rx]=0;b[rt]=rk
 if ef:b[es]=ep2
 b[f]=pr and t or b[to];b[to]=cp
def e(b,t):
 r=0
 for q,w in enumerate(b):
  if w:r+=(V[abs(w)]+((q>>4)-1 if w>0 else 6-(q>>4))*5+(7-abs(2*(q&7)-7)-abs(2*(q>>4)-7))*(abs(w)<6)*2)*(w>0 or-1)
 return r*t
def up(c,m,b,t):
 f,to,pr,ef=m;p=b[f];nep=(f+to)//2 if abs(p)==1 and abs(f-to)==32 else -1;nc=c
 if abs(p)==6:
  for z in("KQ","kq")[t<0]:nc=nc.replace(z,"")
 for sq,ch_ in zip((0,7,112,119),"QKqk"):
  if sq in(f,to):nc=nc.replace(ch_,"")
 return nc,nep
def g(b,t,cr,ep):
 ms=[]
 for sq,p in enumerate(b):
  if sq&136 or p*t<=0:continue
  pt=abs(p)
  if pt==1:
   w=sq+16*t
   if w&136<1 and not b[w]:
    ms+=[(sq,w,r,0)for r in(5,4,3,2)]if w>>4 in(0,7)else[(sq,w,0,0)]
    if sq>>4==6-5*(t>0)and(w2:=sq+32*t)&136<1 and not b[w2]:ms.append((sq,w2,0,0))
   for df in(-1,1):
    cap=w+df
    if cap&136<1:
     if b[cap]*t<0 and abs(b[cap])^6:
      ms+=[(sq,cap,r,0)for r in(5,4,3,2)]if cap>>4 in(0,7)else[(sq,cap,0,0)]
     elif cap==ep:ms.append((sq,cap,0,1))
  else:
   for df in O[pt-2-(pt>5)]:
    c=sq
    while 1:
     c+=df
     if c&136:break
     v=b[c]
     if not v:
      ms.append((sq,c,0,0))
      if pt%4==2:break
     else:
      if v*t<0 and abs(v)^6:ms.append((sq,c,0,0))
      break
   if pt==6 and not i(b,K(b,t),-t):
    for a,b_,c_,d2,k in((4,6,5,7,"K"),(4,2,3,0,"Q"),(116,118,117,119,"k"),(116,114,115,112,"q")):
     if k in cr and b[b_]==b[c_]==0 and b[d2]==4*t and not(i(b,b_,-t)or i(b,c_,-t)) and (k in"Kk"or not b[a-3]):ms.append((a,b_,0,0))
 z=[]
 for m in ms:
  st=mv(b,m,t)
  if not i(b,K(b,t),-t):z.append(m)
  un(b,m,t,*st)
 z.sort(key=lambda m:-V[abs(b[m[1]])]-900*(m[2]>4))
 return z
def s(b,t,cr,ep,d,a,bt,nl):
 inc=i(b,K(b,t),-t)
 if min(d,nl)<1:
  ev=e(b,t)
  if ev>=bt:return bt,nl
  a=max(a,ev)
  ms=[m for m in g(b,t,cr,ep) if b[m[1]] or m[2] or inc]
  if not ms or d<-6:return ev,nl
 else:
  ms=g(b,t,cr,ep);d+=inc
  if(k:=KL[d])in ms:ms.remove(k);ms.insert(0,k)
  if not ms:return-1e5*inc,nl
  if d>2 and not inc:
   x,nl=s(b,-t,cr,-1,d-3,-bt,-a,nl-1)
   if-x>=bt:return-x,nl
 bs=-1e9
 for m in ms:
  ncr,nep=up(cr,m,b,t);st=mv(b,m,t)
  sc,nl=s(b,-t,ncr,nep,d-1,-bt,-a,nl-1)
  un(b,m,t,*st);sc=-sc
  bs=max(bs,sc)
  a=max(a,bs)
  if a>=bt:KL[d]=KL[d]if b[m[1]]else m;break
 return bs,nl
def ch(fen,l):
 b,t,cr,ep=p(fen);M=g(b,t,cr,ep);best=M[0]
 for d in range(6):
  nl=8e3;bs=-1e9;a=-1e6;bt=1e6;bb=best
  for m in M:
   ncr,nep=up(cr,m,b,t);st=mv(b,m,t)
   sc,nl=s(b,-t,ncr,nep,d,-bt,-a,nl)
   un(b,m,t,*st)
   if nl<0:break
   if-sc>bs:bs=a=-sc;bb=m
  if nl<0:break
  best=bb
  if bs>19e3:break
 f,to,pr,_=best
 return S(f)+S(to)+('nbrq'[pr-2]if pr else'')
if __name__=="__main__":
 E=os.getenv("MAKEFUN_ENV_URL")or exit()
 q=lambda x,y={}:J.load(R.urlopen(R.Request(E+x,J.dumps(y).encode())))
 while(g_:=q("/game"))["status"]!="done":
  while g_["status"]=="your_move":g_=q("/move",{"game":g_["game"],"move":ch(g_["fen"],g_["legal_moves"])})
