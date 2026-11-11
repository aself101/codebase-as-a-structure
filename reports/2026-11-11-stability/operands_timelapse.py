import json, sys, math, glob, os
from repo_substrate.mapper.diff import (_transition_context, _feature_sets, touched_between, canonicalize, feature_kinds_from_skeleton)
from repo_substrate.mapper.engine import _resolve_thresholds, _node_value, _cmp
def fires(ctx, node, thresholds):
    nd=ctx['nodes'].get(node)
    if nd is None: return None
    for t in ctx['terms']:
        val=_node_value(nd,t.signal); thr=thresholds.get((t.signal,t.percentile)) if t.percentile is not None else t.value
        if val is None or thr is None or not math.isfinite(thr): return None
        if not _cmp(float(val),t.op,float(thr)): return False
    return True
def sub_for(sha):
    c=[f for f in glob.glob(f'out/cache/mcp-secure-server-{sha[:12]}-*-298696064105.substrate.json')]
    return json.load(open(sorted(c)[0])) if c else None
for d in sys.argv[1:]:
    print('==',os.path.basename(d)); sks=sorted(glob.glob(d+'/f*.skeleton.json'))
    for pa,pb in zip(sks,sks[1:]):
        a=json.load(open(pa)); b=json.load(open(pb)); sa_=sub_for(a['repo']['head_sha']); sb_=sub_for(b['repo']['head_sha'])
        if not sa_ or not sb_: print('no cache',pb); continue
        ren=sb_.get('renames') or {}
        if isinstance(ren,list): ren={x['from']:x['to'] for x in ren}
        touched,k=touched_between(sa_,sb_,ren)
        an={canonicalize(n,ren):n for n in a['strata']['by_node']}; common=set(an)&set(b['strata']['by_node']); unt=common-touched
        kinds=feature_kinds_from_skeleton(a,b); fa=_feature_sets(a); fb=_feature_sets(b)
        o0=[0,0]; o3=[0,0]; rooms0=set(); rooms3=set()
        for key in sorted(set(fa)|set(fb)):
            if kinds.get(f'{key[0]}/{key[1]}','rank') not in ('rank','mixed'): continue
            A={canonicalize(n,ren) for n in fa.get(key,set())}&unt; B=fb.get(key,set())&unt
            o0[0]+=len(A^B); o0[1]+=len(A|B); rooms0|=A^B
            ca=_transition_context(a,sa_,*key); cb=_transition_context(b,sb_,*key)
            if ca['availability']!='available' or cb['availability']!='available' or not unt: continue
            ta=_resolve_thresholds(ca['terms'],[ca['nodes'][an[n]] for n in unt]); tb=_resolve_thresholds(cb['terms'],[cb['nodes'][n] for n in unt])
            A3={n for n in unt if fires(ca,an[n],ta)}; B3={n for n in unt if fires(cb,n,tb)}
            o3[0]+=len(A3^B3); o3[1]+=len(A3|B3); rooms3|=A3^B3
        r=lambda x: f"{x[0]}/{x[1]}={x[0]/x[1]:.3f}" if x[1] else '0/0'
        print(os.path.basename(pb)[:13],'K',k,'untouched',len(unt),'touched',len(touched&common),'| current',r(o0),'rooms',len(rooms0),'| untouched-cutoffs',r(o3),'rooms',len(rooms3))
