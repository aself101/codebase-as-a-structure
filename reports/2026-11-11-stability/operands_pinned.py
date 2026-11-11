"""Feasibility read (read-only): candidate stability operands on the 8 pinned comparisons."""
import json, sys, math
from pathlib import Path
from repo_substrate.mapper.diff import (_transition_context, _feature_sets, touched_between, canonicalize, feature_kinds_from_skeleton)
from repo_substrate.mapper.engine import _resolve_thresholds, _node_value, _cmp
ROOT=Path('.'); v=json.load(open('out/validation-k25k/validation.json')); fp=v['substrate_config_fingerprint'][:12]
SHORT={'uluops-registry-api':'registry'}
def fires(ctx, node, thresholds):
    nd=ctx['nodes'].get(node)
    if nd is None: return None
    for t in ctx['terms']:
        val=_node_value(nd,t.signal); thr=thresholds.get((t.signal,t.percentile)) if t.percentile is not None else t.value
        if val is None or thr is None or not math.isfinite(thr): return None
        if not _cmp(float(val),t.op,float(thr)): return False
    return True
print('| repo | untouched | O0 current | O1 one count per predicate | O2 cutoff held | O3 cutoffs over untouched rooms |'); print('|---|---|---|---|---|---|')
for r in v['reference_repos']:
    name=r['name']; short=SHORT.get(name,name); tip,pert=r['head_sha'][:12],r['asserted']['perturbed_sha'][:12]
    a=json.load(open(f'out/m2x-2026-11-11-d080/{short}.layer.pert.skeleton.json')); b=json.load(open(f'out/m2x-2026-11-11-d080/{short}.layer.head.skeleton.json'))
    sa_=json.load(open(f'out/cache/{name}-{pert}-trunc-{fp}.substrate.json')); sb_=json.load(open(f'out/cache/{name}-{tip}-tip-{fp}.substrate.json'))
    ren=sb_.get('renames') or {}
    if isinstance(ren,list): ren={x['from']:x['to'] for x in ren}
    touched,_=touched_between(sa_,sb_,ren)
    an={canonicalize(n,ren):n for n in a['strata']['by_node']}; common=set(an)&set(b['strata']['by_node']); unt=common-touched
    kinds=feature_kinds_from_skeleton(a,b); fa=_feature_sets(a); fb=_feature_sets(b)
    res={k:[0,0] for k in ('O0','O1','O2','O3')}; seen=set(); mism=0
    for key in sorted(set(fa)|set(fb)):
        if kinds.get(f'{key[0]}/{key[1]}','rank') not in ('rank','mixed'): continue
        A={canonicalize(n,ren) for n in fa.get(key,set())}&unt; B=fb.get(key,set())&unt
        res['O0'][0]+=len(A^B); res['O0'][1]+=len(A|B)
        ca=_transition_context(a,sa_,*key); cb=_transition_context(b,sb_,*key)
        pred=ca['definition']['predicate']
        # reproduction check of fired sets by predicate
        A2={n for n in unt if fires(ca,an[n],ca['thresholds'])}; B2={n for n in unt if fires(cb,n,cb['thresholds'])}
        if A2!=A or B2!=B: mism+=1
        if pred not in seen:
            seen.add(pred); res['O1'][0]+=len(A^B); res['O1'][1]+=len(A|B)
        # O2: after values against before cutoffs
        B_held={n for n in unt if fires(cb,n,ca['thresholds'])}
        res['O2'][0]+=len(A^B_held); res['O2'][1]+=len(A|B_held)
        # O3: cutoffs resolved over untouched rooms only, each frame
        ta=_resolve_thresholds(ca['terms'],[ca['nodes'][an[n]] for n in unt]); tb=_resolve_thresholds(cb['terms'],[cb['nodes'][n] for n in unt])
        A3={n for n in unt if fires(ca,an[n],ta)}; B3={n for n in unt if fires(cb,n,tb)}
        res['O3'][0]+=len(A3^B3); res['O3'][1]+=len(A3|B3)
    cell=lambda k: f"{res[k][0]}/{res[k][1]} = {res[k][0]/res[k][1]:.3f}" if res[k][1] else '0/0'
    print(f"| {short} | {len(unt)} | {cell('O0')} | {cell('O1')} | {cell('O2')} | {cell('O3')} |" + (f"  (predicate reproduction mismatches: {mism})" if mism else ''))
