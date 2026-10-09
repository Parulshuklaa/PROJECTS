"""Leakage-safe training and a real multilayer neural autoencoder."""
from pathlib import Path
import json
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, roc_auc_score, precision_score, recall_score, confusion_matrix

ROOT = Path(__file__).parent
FEATURES = ['amount', 'hour', 'distance_km', 'transactions_1h', 'account_age_days', 'device_new']
LIMITS = [(0, 1000000), (0, 23), (0, 20000), (0, 1000), (0, 30000), (0, 1)]

def generate(n=6000, seed=42):
    rng = np.random.default_rng(seed)
    x = np.column_stack([rng.lognormal(6, 1.3, n), rng.integers(0,24,n), rng.exponential(40,n), rng.poisson(2,n), rng.integers(1,3000,n), rng.binomial(1,.12,n)]).astype(float)
    # Hidden synthetic risk process; imperfect signals, overlapping classes.
    logits = -5 + 1.1*np.log1p(x[:,0]/1000) + .8*(x[:,1]<5) + 1.5*(x[:,2]>90) + .55*x[:,3] + .9*(x[:,4]<100) + 1.3*x[:,5]
    y = rng.binomial(1, 1/(1+np.exp(-logits)))
    return x, y

def metrics(y, p, threshold):
    pred = p >= threshold
    return {'pr_auc': float(average_precision_score(y,p)), 'roc_auc': float(roc_auc_score(y,p)), 'precision': float(precision_score(y,pred,zero_division=0)), 'recall': float(recall_score(y,pred,zero_division=0)), 'confusion_matrix': confusion_matrix(y,pred).tolist()}

def train():
    x,y = generate()
    xt, xr, yt, yr = train_test_split(x,y,test_size=.4,stratify=y,random_state=42)
    xv, xs, yv, ys = train_test_split(xr,yr,test_size=.5,stratify=yr,random_state=43)
    scaler = StandardScaler().fit(xt[yt==0])
    zt,zv,zs = [scaler.transform(a) for a in (xt,xv,xs)]
    forest = RandomForestClassifier(n_estimators=160,max_depth=9,min_samples_leaf=8,class_weight='balanced',random_state=42,n_jobs=-1).fit(xt,yt)
    # Six inputs -> 16 -> 8 -> 3 bottleneck -> 8 -> 16 -> six reconstruction outputs.
    ae = MLPRegressor(hidden_layer_sizes=(16,8,3,8,16),activation='tanh',max_iter=180,early_stopping=True,random_state=42).fit(zt[yt==0],zt[yt==0])
    ev = np.mean((ae.predict(zv)-zv)**2,axis=1)
    cutoff = float(np.quantile(ev[yv==0],.95))
    thresholds = np.linspace(.05,.9,100)
    pv = forest.predict_proba(xv)[:,1]
    costs = [np.sum((pv>=t)&(yv==0)) + 5*np.sum((pv<t)&(yv==1)) for t in thresholds]
    threshold = float(thresholds[np.argmin(costs)])
    ps = forest.predict_proba(xs)[:,1]
    es = np.mean((ae.predict(zs)-zs)**2,axis=1)
    report = {'dataset':'Synthetic transactions; demonstration only', 'samples':len(x), 'split':{'train':len(xt),'validation':len(xv),'test':len(xs)}, 'fraud_rate':float(y.mean()), 'threshold':threshold,'threshold_policy':'Validation minimizes FP + 5 × FN; test used once', 'anomaly_cutoff':cutoff, 'classifier':metrics(ys,ps,threshold), 'autoencoder':{'pr_auc':float(average_precision_score(ys,es)),'roc_auc':float(roc_auc_score(ys,es))}, 'baseline_pr_auc':float(ys.mean()), 'features':FEATURES,'global_importance':dict(zip(FEATURES,forest.feature_importances_.tolist()))}
    (ROOT/'models').mkdir(exist_ok=True)
    joblib.dump({'forest':forest,'ae':ae,'scaler':scaler,'report':report,'medians':np.median(xt,axis=0)},ROOT/'models/bundle.joblib')
    (ROOT/'models/metrics.json').write_text(json.dumps(report,indent=2))
    return report

def validate(data):
    if not isinstance(data,dict): raise ValueError('Transaction must be a JSON object')
    row=[]
    for f,(low,high) in zip(FEATURES,LIMITS):
        try: v=float(data[f])
        except (KeyError,TypeError,ValueError): raise ValueError(f'{f}: numeric value required')
        if not np.isfinite(v) or not low<=v<=high: raise ValueError(f'{f}: expected {low} to {high}')
        if f in FEATURES[1:2]+FEATURES[3:] and v!=int(v): raise ValueError(f'{f}: integer required')
        row.append(v)
    return np.array([row])

class Engine:
    def __init__(self):
        path=ROOT/'models/bundle.joblib'
        if not path.exists(): raise RuntimeError('Run python train.py first')
        self.b=joblib.load(path) # Only load locally generated trusted artifacts.
    def score(self,data):
        x=validate(data); b=self.b
        p=float(b['forest'].predict_proba(x)[0,1]); z=b['scaler'].transform(x)
        error=float(np.mean((b['ae'].predict(z)-z)**2)); anomaly=error>b['report']['anomaly_cutoff']
        reasons=[]
        for i,f in enumerate(FEATURES):
            replaced=x.copy(); replaced[0,i]=b['medians'][i]
            delta=p-float(b['forest'].predict_proba(replaced)[0,1])
            reasons.append({'feature':f,'risk_delta':round(delta,4)})
        reasons.sort(key=lambda r:abs(r['risk_delta']),reverse=True)
        return {'fraud_probability':round(p,4),'reconstruction_error':round(error,4),'anomaly':bool(anomaly),'decision':'review' if p>=b['report']['threshold'] or anomaly else 'pass','reasons':reasons[:3]}
