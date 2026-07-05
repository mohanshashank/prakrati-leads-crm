import json, re
import phonenumbers as pn
from phonenumbers import is_valid_number, parse, region_code_for_number

FLAG={c:''.join(chr(0x1F1E6+ord(x)-65) for x in c) for c in ['AE','RU','NG','EG','DE','AU','JP','ES','PY','IN','PK','GB','US','FR','KZ','SA','QA','KW','OM','BH','TR','UA','BY','IT','CA','PH','LB','SY','IQ','JO','MA','DZ','TN','ID','CN','ZA','NL','CH','PL']}
NAME={'AE':'UAE','RU':'Russia','NG':'Nigeria','EG':'Egypt','DE':'Germany','AU':'Australia','JP':'Japan','ES':'Spain','PY':'Paraguay','IN':'India','PK':'Pakistan','GB':'UK','US':'USA','FR':'France','KZ':'Kazakhstan','SA':'Saudi Arabia','QA':'Qatar','KW':'Kuwait','OM':'Oman','BH':'Bahrain','TR':'Turkey','UA':'Ukraine','BY':'Belarus','IT':'Italy','CA':'Canada','PH':'Philippines','LB':'Lebanon','SY':'Syria','IQ':'Iraq','JO':'Jordan','MA':'Morocco','DZ':'Algeria','TN':'Tunisia','ID':'Indonesia','CN':'China','ZA':'South Africa','NL':'Netherlands','CH':'Switzerland','PL':'Poland'}
GTMAP={'australia':'AU','paraguay':'PY','spain':'ES','uae':'AE','egypt':'EG','japan':'JP','germany':'DE'}
CC={'AE':'971','RU':'7','NG':'234','IN':'91','EG':'20','DE':'49','AU':'61','JP':'81','ES':'34','PY':'595'}

SLAV=('ov','ova','ev','eva','iev','ieva','in','ina','sky','skaya','enko','vich','uk','yan','ova','ько')
IND_TOKENS=set("gurav shinde nighot nomulwar lengare mujumdar patel kumar singh sharma reddy rao gupta nair menon iyer pillai desai joshi mehta shah verma yadav khan das bose roy naidu chowdhury patil jadhav pawar deshmukh kulkarni bhosale more shetty hegde acharya swapnil amol amit sachin abhijeet sanjyoti rahul rohit vijay ajay sanjay anil sunil ramesh suresh mahesh".split())

def name_origin(name):
    n=(name or '').lower()
    toks=re.split(r'[\s]+',n)
    for t in toks:
        if t in IND_TOKENS: return 'IN'
    for t in toks:
        for s in SLAV:
            if t.endswith(s) and len(t)>4: return 'RU'
    return None

def valid(e164):
    try:
        num=parse(e164,None); return is_valid_number(num), region_code_for_number(num)
    except: return False,None

def classify(d, name='', gt=None):
    d=re.sub(r'\D','',d or '')
    if not d: return '','','none'
    if gt and gt.lower() in GTMAP:
        reg=GTMAP[gt.lower()]
        try:
            n=parse(d,reg)
            if is_valid_number(n): return pn.format_number(n,pn.PhoneNumberFormat.E164),reg,'high'
        except: pass
        return '+'+CC.get(reg,'')+d.lstrip('0'), reg,'low'
    # explicit intl prefixes
    opts=[]
    if d.startswith('971') and len(d)>=11: opts.append(('+'+d,'AE','high'))
    if len(d)==9 and d[0]=='5': opts.append(('+971'+d,'AE','high'))
    if len(d)==10 and d[:2]=='05': opts.append(('+971'+d[1:],'AE','high'))
    if len(d)==11 and d[0]=='0': opts.append(('+234'+d[1:],'NG','high'))
    # 10-digit India/Russia ambiguity
    if len(d)==10 and d[0] in '678': opts.append(('+91'+d,'IN','medium'))
    if len(d)==10 and d[0]=='9':
        o=name_origin(name)
        if o=='IN': opts.append(('+91'+d,'IN','medium'))
        elif o=='RU': opts.append(('+7'+d,'RU','medium'))
        else:
            opts.append(('+7'+d,'RU','low')); opts.append(('+91'+d,'IN','low'))
    if len(d)==11 and d[0] in '78': opts.append(('+7'+d[1:],'RU','high'))
    for cc,reg in [('20','EG'),('49','DE'),('61','AU'),('81','JP'),('34','ES'),('595','PY'),('44','GB'),('91','IN'),('92','PK'),('90','TR'),('966','SA'),('974','QA'),('965','KW'),('968','OM'),('973','BH'),('7','RU')]:
        if d.startswith(cc) and len(d)>=10: opts.append(('+'+d,reg,'high'))
    opts.append(('+'+d,None,'low')); opts.append(('+971'+d,'AE','low'))
    for e164,reg,conf in opts:
        ok,r=valid(e164)
        if ok: return e164, r or reg, conf
    if len(d)==9 and d[0]=='5': return '+971'+d,'AE','medium'
    return '+'+d, None, 'low'

excel=json.load(open('/tmp/leads_final.json'))
imgs=json.load(open('/tmp/img_leads.json'))
import collections
ctry=collections.Counter(); conf=collections.Counter()
recs=[]; i=0
def build(f,src,gt=None):
    global i; i+=1
    res=[classify(p,f['name'],gt) for p in f['phones']] or []
    prim=res[0] if res else ('',None,'none')
    ctry[prim[1]]+=1; conf[prim[2]]+=1
    return {'id':i,'name':f['name'],'first_name':f.get('first_name') or f['name'],
        'phone_primary':prim[0],'phone_all':' , '.join(x[0] for x in res),
        'phone_raw':str(f['phone_raw']) if f.get('phone_raw') is not None else '',
        'country_iso':prim[1] or '','country':NAME.get(prim[1],''),'flag':FLAG.get(prim[1],''),
        'phone_confidence':('verify' if (src=='Photo (OCR)' and prim[0]) else prim[2]),
        'responsible':' / '.join(f['responsibles']) if f.get('responsibles') else '',
        'stage':(' , '.join(f['stages']) if f.get('stages') else 'Photo list'),
        'status':'New','last_contacted':'','source':src,'notes':('code:'+f['extra']) if f.get('extra') else '',
        'source_image':f.get('source_image','')}
for f in excel: recs.append(build(f,'Excel'))
for f in imgs: recs.append(build(f,'Photo (OCR)',f.get('country','')))
print('total',len(recs))
print('country:',ctry.most_common())
print('confidence:',conf.most_common())
json.dump(recs, open('/tmp/records_classified.json','w'), ensure_ascii=False)
# show the india ones now
print('India leads:', [r['name'] for r in recs if r['country_iso']=='IN'][:12])
