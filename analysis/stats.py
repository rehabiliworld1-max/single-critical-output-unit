import pandas as pd, numpy as np, glob, re, sys
from scipy.stats import wilcoxon, binomtest, rankdata
D=sys.argv[1] if len(sys.argv)>1 else "results"
p=pd.read_csv(f'{D}/P1_mechanism_summary.csv'); b=pd.read_csv(f'{D}/D_baseline_walk.csv')
p['surv']=p.fall_step.fillna(250)
J4=['right_ankle_pitch_joint','left_ankle_pitch_joint','right_hip_pitch_joint','left_hip_pitch_joint','right_knee_joint']
print('fall rate by speed'); print(p.pivot_table(index='speed_mps',columns='joint',values='fell_over',aggfunc='sum').astype(int).to_string())
def onset(g):
    f=g[g.fell_over]; return f.speed_mps.min() if len(f) else np.inf
h=p[p.joint.str.contains('hip')].groupby(['joint','seed']).apply(onset).unstack(0)
r,l=h['right_hip_pitch_joint'],h['left_hip_pitch_joint']
print('hip onsets\n',h.T.to_string()); nr,nl=(r<l).sum(),(l<r).sum()
print('right',nr,'left',nl,'tie',(r==l).sum(),'sign p',binomtest(int(nr),int(nr+nl)).pvalue)
a=p[(p.speed_mps.round(2)==0.2)&p.joint.str.contains('ankle')].pivot(index='seed',columns='joint',values='surv')
R,L=a['right_ankle_pitch_joint'].values,a['left_ankle_pitch_joint'].values; d=L-R
w=wilcoxon(L,R); rk=rankdata(np.abs(d)); rb=(rk[d>0].sum()-rk[d<0].sum())/rk.sum()
rng=np.random.default_rng(0); bs=np.percentile([rng.choice(d,8).mean() for _ in range(20000)],[2.5,97.5])
print(f'ankle surv R {R.mean():.1f}±{R.std(ddof=1):.1f} ({R.min():.0f}-{R.max():.0f}) L {L.mean():.1f}±{L.std(ddof=1):.1f} ({L.min():.0f}-{L.max():.0f}) Lgt {int((d>0).sum())} diff {d.mean():.1f} CI {bs.round(1)} p {w.pvalue:.3f} r {rb:.2f}')
f=p[p.fell_over]
print('falls per joint', f.groupby('joint').size().to_dict())
g=f.groupby('joint')
for c in ['q_other_at_fall','q_other_pre05','tgt_other_at_fall','q_knee_at_fall','q_abl_at_fall']:
    print(c, g[c].mean().round(1).to_dict())
print('walk q',b.groupby('speed_mps').q_all_walk.mean().agg(['min','max']).round(2).tolist(),'tgt',b.groupby('speed_mps').tgt_all_walk.mean().agg(['min','max']).round(2).tolist())
AB={'right_ankle_pitch_joint':10,'left_ankle_pitch_joint':4,'right_hip_pitch_joint':6,'left_hip_pitch_joint':0,'right_knee_joint':9}
rows=[]
for fn in glob.glob(f'{D}/trajectories/P1_*.npz'):
    m=re.match(r'.*P1_(.+)_seed(\d)_v(\d+)\.npz',fn); jn=m[1]; t=np.load(fn); k=int(t['fall_step'])-1
    q,q0=t['q'],t['q0']; dd=np.degrees(np.abs(q-q0)); j=AB[jn]
    if jn=='right_knee_joint': ip,co=9,3
    else: ip=3 if jn.startswith('left') else 9; co=9 if ip==3 else 3
    oth=[i for i in range(29) if i!=j]; o=dd[:,oth].mean(1); below=np.where(o[:k+1]<8)[0]
    rows.append(dict(joint=jn,ipsi=np.degrees(q[k,ip]-q0[ip]),contra=np.degrees(q[k,co]-q0[co]),onset=(k-below[-1])*0.02 if len(below) else np.nan,
      peak=dd[max(0,k-49):k+1,j].max(),h=t['height'][k],argknee=int(np.argmax(dd[k]) in (3,9)),
      within=int((dd[k,oth]<0.5).all())))
X=pd.DataFrame(rows); X4=X[X.joint!='right_knee_joint']
print('ipsi flexed all',(X4.ipsi>0).all(),'ipsi>contra',int((X4.ipsi.abs()>X4.contra.abs()).sum()),'/',len(X4),'argknee',X4.argknee.sum())
print('onset median by joint',X.groupby('joint').onset.median().round(2).to_dict())
print('ankle peak range',X4[X4.joint.str.contains('ankle')].peak.agg(['min','max']).round(1).tolist(),'height',X4.h.agg(['min','max']).round(2).tolist())
print('rknee', X[X.joint=='right_knee_joint'][['contra','onset','peak','h']].describe().round(1).to_string())
s=pd.read_csv(f'{D}/S_screen_1p0.csv') if glob.glob(f'{D}/S_screen_1p0.csv') else None
if s is not None: print('screen', s.groupby('joint').fell_over.sum()[lambda v:v>0].to_dict())
rk=p[p.joint=='right_knee_joint']; print('rknee seeds fell any', rk[rk.fell_over].seed.nunique(), rk[rk.fell_over][['seed','speed_mps','fall_step']].values.tolist())
