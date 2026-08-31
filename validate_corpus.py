import csv, json, re, collections

rows = list(csv.DictReader(open('labels200.csv')))

BIG9 = {
 'milk':      ['milk','cream','butter','whey','casein','caseinate','lactose','cheese','yogurt','ghee','curd','custard'],
 'egg':       ['egg','albumen','ovalbumin','mayonnaise','meringue'],
 'fish':      ['anchovy','anchovies','tuna','salmon','cod','tilapia','sardine','fish sauce','fish oil','bonito'],
 'shellfish': ['shrimp','prawn','crab','lobster','crayfish','oyster','clam','mussel','scallop','squid','octopus','krill'],
 'tree nuts': ['almond','cashew','walnut','pecan','pistachio','hazelnut','macadamia','brazil nut','filbert','praline'],
 'peanuts':   ['peanut','groundnut','arachis'],
 'wheat':     ['wheat','semolina','durum','farina','spelt','gluten','couscous','bulgur'],
 'soy':       ['soy','soya','soybean','tofu','edamame','miso','tempeh'],
 'sesame':    ['sesame','tahini','benne','sesamum'],
}
# tokens that must NOT count as milk / tree nut
NEG = ['peanut butter','shea butter','cocoa butter','apple butter','nut butter','almond butter',
       'coconut','butterfly','buttermilk substitute','soy butter','sunflower butter','butternut']

def tags(text):
    t = text.lower()
    masked = t
    for n in NEG:
        masked = masked.replace(n, ' ')
    if 'buttermilk' in t:            # buttermilk IS milk; restore
        masked += ' buttermilk milk '
    out = set()
    for a, syns in BIG9.items():
        for s in syns:
            if a == 'soy' and s == 'soy':
                if re.search(r'\bsoy\b', masked) or 'soybean' in masked or 'soya' in masked:
                    out.add(a); break
            elif s in masked:
                out.add(a); break
    return out

def parse_ing(s):
    s = (s or '').strip()
    if not s: return None
    try:
        v = json.loads(s)
        if isinstance(v, list): return [str(x) for x in v]
    except Exception:
        pass
    return [s]

stat = collections.defaultdict(lambda: collections.Counter())
prev = collections.Counter(); prev_by_prov = collections.defaultdict(collections.Counter)
degenerate = collections.Counter(); totals = collections.Counter()
contains_decl = collections.Counter()
ing_counts = collections.defaultdict(list)
missing_ing = collections.Counter()

for r in rows:
    prov = r['provenance']
    totals[prov] += 1
    lst = parse_ing(r['ingredients'])
    if lst is None:
        missing_ing[prov] += 1; continue
    flat = ' ; '.join(lst)
    ing_counts[prov].append(len(lst))
    # degenerate = whole statement crammed into one element while clearly multi-ingredient
    if len(lst) == 1 and (flat.count(',') >= 3):
        degenerate[prov] += 1
    if re.search(r'\bcontains\b\s*:', flat, re.I):
        contains_decl[prov] += 1
    tg = tags(flat)
    for a in tg:
        prev[a] += 1; prev_by_prov[prov][a] += 1

print("=== AnonLabelsLabels-200: what the released file supports ===")
print("rows:", len(rows), "| own-photography:", totals['own-photography'], "| openfoodfacts:", totals['openfoodfacts'])
print()
print("--- Big-9 allergen prevalence (rule-based, whole 200) ---")
for a,_ in sorted(prev.items(), key=lambda x:-x[1]):
    o = prev_by_prov['own-photography'][a]; f = prev_by_prov['openfoodfacts'][a]
    print(f"  {a:<10} total {prev[a]:>3}   own {o:>3}/{totals['own-photography']}   OFF {f:>3}/{totals['openfoodfacts']}")
print("  products with >=1 Big-9 tag:", sum(1 for r in rows if (lambda l: l and tags(' ; '.join(l)))(parse_ing(r['ingredients']))))
print()
print("--- Statement degeneracy: whole ingredient list stored as ONE element ---")
for p in ('own-photography','openfoodfacts'):
    n = totals[p]; d = degenerate[p]
    print(f"  {p:<16} {d}/{n} = {100*d/n:.1f}%")
print()
print("--- Explicit 'CONTAINS:' allergen declaration retained in the structured record ---")
for p in ('own-photography','openfoodfacts'):
    n = totals[p]; c = contains_decl[p]
    print(f"  {p:<16} {c}/{n} = {100*c/n:.1f}%")
print()
print("--- Ingredient-list length ---")
for p in ('own-photography','openfoodfacts'):
    v = sorted(ing_counts[p])
    print(f"  {p:<16} n={len(v)} mean={sum(v)/len(v):.1f} median={v[len(v)//2]} max={max(v)}")
print("  missing/empty ingredients:", dict(missing_ing))
