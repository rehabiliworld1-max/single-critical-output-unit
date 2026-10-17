import numpy as np, pandas as pd, glob, re, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.stats import norm
def proportion_confint(k,n,method='wilson'):
    k=np.asarray(k,float); n=np.asarray(n,float); z=1.959964; ph=k/n; d=1+z*z/n; c=(ph+z*z/(2*n))/d; h=z*np.sqrt(ph*(1-ph)/n+z*z/(4*n*n))/d
    return c-h,c+h
import sys; D=sys.argv[1] if len(sys.argv)>1 else 'results'; O='figures/'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9})
p=pd.read_csv(f'{D}/P1_mechanism_summary.csv'); b=pd.read_csv(f'{D}/D_baseline_walk.csv')
RED,ORA='#c0392b','#e67e22'
fig,ax=plt.subplots(1,3,figsize=(10,3.3),sharey=True)
for a,(title,pairs) in zip(ax,[('A  Ankle pitch',[('right_ankle_pitch_joint','Right',RED),('left_ankle_pitch_joint','Left',ORA)]),
                               ('B  Hip pitch',[('right_hip_pitch_joint','Right',RED),('left_hip_pitch_joint','Left',ORA)]),
                               ('C  Right knee',[('right_knee_joint','Right',RED)])]):
    for i,(j,lab,c) in enumerate(pairs):
        g=p[p.joint==j].groupby('speed_mps').fell_over.agg(['sum','count'])
        lo,hi=proportion_confint(g['sum'],g['count'],method='wilson'); x=g.index.values+(i-0.5*(len(pairs)-1))*0.012; r=g['sum']/g['count']
        a.errorbar(x,r,yerr=[r-lo,hi-r],fmt='o-',color=c,label=lab,capsize=2,ms=4,lw=1.3)
    a.set_title(title,loc='left',fontweight='bold'); a.set_xlabel('Commanded forward speed (m/s)'); a.set_xticks(np.arange(0.2,1.01,0.2))
    a.set_ylim(-0.03,1.05); a.legend(frameon=False,loc='upper left' if 'knee' in title else 'lower right'); a.spines[['top','right']].set_visible(False)
ax[0].set_ylabel('Fraction of 8 seeds that fell')
fig.tight_layout(); [fig.savefig(O+'figure2_speed_sweep.'+e,dpi=300) for e in ['png','tiff']]
AB={'right_ankle_pitch_joint':10,'left_ankle_pitch_joint':4,'right_hip_pitch_joint':6,'left_hip_pitch_joint':0,'right_knee_joint':9}
names=[('right_ankle_pitch_joint','A  Right ankle pitch'),('left_ankle_pitch_joint','B  Left ankle pitch'),('right_hip_pitch_joint','C  Right hip pitch'),('left_hip_pitch_joint','D  Left hip pitch'),('right_knee_joint','E  Right knee')]
W=50; t=np.arange(-W+1,1)*0.02; base=b.q_all_walk.mean()
fig,ax=plt.subplots(1,5,figsize=(13,3.2),sharey=True)
for a,(jn,title) in zip(ax,names):
    j=AB[jn]; S={k:[] for k in ['abl','tgt','rk','lk','oth']}
    for fn in glob.glob(f'{D}/trajectories/P1_{jn}_seed*.npz'):
        z=np.load(fn); k=int(z['fall_step'])-1; q0=z['q0']
        d=np.degrees(np.abs(z['q']-q0)); dt=np.degrees(np.abs(z['target']-q0))
        def win(v):
            w=np.full(W,np.nan); s=v[max(0,k-W+1):k+1]; w[W-len(s):]=s; return w
        S['abl'].append(win(d[:,j])); S['tgt'].append(win(dt[:,j])); S['rk'].append(win(d[:,9])); S['lk'].append(win(d[:,3]))
        S['oth'].append(win(np.delete(d,[j,3,9],axis=1).mean(1)))
    n=len(S['abl'])
    for key,lab,c,ls in [('rk','Right knee','#2c3e50','-'),('lk','Left knee','#7f8c8d','-'),('oth','Other joints (mean)','#2980b9','-'),('abl','Ablated joint: actual','#c0392b','-'),('tgt','Ablated joint: target','#c0392b','--')]:
        if jn=='right_knee_joint' and key=='rk': continue
        A=np.array(S[key]); m,s=np.nanmean(A,0),np.nanstd(A,0)
        a.plot(t,m,color=c,ls=ls,lw=1.4,label=lab)
        if key!='tgt': a.fill_between(t,m-s,m+s,color=c,alpha=0.12,lw=0)
    a.axhline(base,color='k',ls=':',lw=1)
    a.set_title(f'{title} (n = {n})',loc='left',fontweight='bold',fontsize=9); a.set_xlabel('Time to fall onset (s)'); a.spines[['top','right']].set_visible(False)
ax[0].set_ylabel('|Deviation from default| (°)'); ax[0].legend(frameon=False,fontsize=7,loc='upper left')
fig.tight_layout(); [fig.savefig(O+'figure3_prefall_deviation.'+e,dpi=300) for e in ['png','tiff']]
print(base)
