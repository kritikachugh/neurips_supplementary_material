import csv, json, re, collections

rows = list(csv.DictReader(open('labels200.csv')))
BIG9 = {
 'milk':['milk','cream','butter','whey','casein','lactose','cheese','yogurt','ghee','curd'],
 'egg':['egg','albumen','ovalbumin','mayonnaise','meringue'],
 'fish':['anchov','tuna','salmon','tilapia','sardine','fish'],
 'shellfish':['shrimp','prawn','crab','lobster','crayfish','oyster','clam','mussel','scallop','squid','krill'],
 'tree nuts':['almond','cashew','walnut','pecan','pistachio','hazelnut','macadamia','brazil nut','filbert'],
 'peanuts':['peanut','groundnut','arachis'],
 'wheat':['wheat','semolina','durum','farina','spelt','gluten','couscous','bulgur'],
 'soy':['soy','soya','soybean','tofu','edamame','miso','tempeh'],
 'sesame':['sesame','tahini','benne'],
}
NEG=['peanut butter','shea butter','cocoa butter','apple butter','nut butter','almond butter',
     'sunflower butter','soy butter','butternut','coconut','cream of tartar']

def toks(raw):
    try:
        v=json.loads(raw)
        if isinstance(v,list): return [str(x) for x in v]
    except Exception: pass
    return [raw] if raw else []

def hits(tok,a):
    t=tok.lower()
    for n in NEG: t=t.replace(n,' ')
    if 'buttermilk' in tok.lower(): t+=' milk '
    for s in BIG9[a]:
        if a=='soy' and s=='soy':
            if re.search(r'\bsoy\b',t) or 'soybean' in t or 'soya' in t: return True
        elif s in t: return True
    return False

kdist=collections.Counter(); pairs=0; prods=set()
per_allergen=collections.defaultdict(lambda: collections.Counter())
by_prov=collections.defaultdict(collections.Counter)
degenerate=0
for r in rows:
    tl=toks(r['ingredients'])
    if not tl: continue
    if len(tl)==1 and tl[0].count(',')>=3: degenerate+=1
    for a in BIG9:
        k=sum(1 for tok in tl if hits(tok,a))
        if k>0:
            pairs+=1; prods.add(r['Barcode'])
            kdist[min(k,4)]+=1
            per_allergen[a]['n']+=1
            if k==1: per_allergen[a]['k1']+=1
            by_prov[r['provenance']]['n']+=1
            if k==1: by_prov[r['provenance']]['k1']+=1

print(f"true (product, allergen) pairs : {pairs}   across {len(prods)} products")
tot=sum(kdist.values())
for k in sorted(kdist):
    lab = f"k={k}" if k<4 else "k>=4"
    print(f"  {lab:<6} {kdist[k]:>4}  = {100*kdist[k]/tot:5.1f}%")
print(f"\nk=1 share : {100*kdist[1]/tot:.1f}%   <-- fragility headline")
print("\nby provenance (k=1 share):")
for p,c in by_prov.items():
    print(f"  {p:<16} {c['k1']}/{c['n']} = {100*c['k1']/c['n']:.1f}%")
print("\nper allergen  n / k=1 / share:")
for a in sorted(per_allergen, key=lambda x:-per_allergen[x]['n']):
    c=per_allergen[a]
    print(f"  {a:<10} {c['n']:>3} / {c['k1']:>3} = {100*c['k1']/c['n']:5.1f}%")
print(f"\nproducts with >=1 fragile (k=1) allergen: ", end="")
frag=set()
for r in rows:
    tl=toks(r['ingredients'])
    for a in BIG9:
        k=sum(1 for tok in tl if hits(tok,a))
        if k==1: frag.add(r['Barcode']); break
print(f"{len(frag)}/200")
print(f"degenerate single-element statements: {degenerate}/200")
