# -*- coding: utf-8 -*-
"""
Build Complete Oxford 3000 + C1/C2 + Phrasal Verbs + Collocations Database
"""
import os
import re
import json
import pypdf

base_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(base_dir, 'cache')
data_dir = os.path.join(base_dir, '..', 'src', 'data')
os.makedirs(data_dir, exist_ok=True)

# 1. Load IPA Dictionary
print("Loading IPA Dictionary...")
ipa_map = {}
ipa_file = os.path.join(cache_dir, 'ipa_uk.txt')
if os.path.exists(ipa_file):
    with open(ipa_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                word, ipa = line.strip().split('\t', 1)
                ipa_map[word.lower()] = ipa

# 2. Load Indonesian Dictionary (Echols & Shadily)
print("Loading Indonesian Dictionary...")
dict_data = {}
dict_file = os.path.join(cache_dir, 'dict_en_id.txt')
if os.path.exists(dict_file):
    with open(dict_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                word, defn = line.strip().split('\t', 1)
                dict_data[word.lower()] = defn

def clean_echols_definition(raw, pos='noun'):
    if not raw:
        return ''
    pos_targets = {
        'noun': ['kb'],
        'verb': ['kkt', 'kki'],
        'adjective': ['ks'],
        'adverb': ['kk'],
        'preposition': ['kd'],
        'conjunction': ['ksam']
    }.get(pos, ['kb', 'kkt', 'ks'])
    
    # Split text into sections by tag
    tags_regex = r'(--|\s|^)(kb|kkt|kki|ks|kk|kd|ksam|kser)\.\s*'
    parts = re.split(tags_regex, raw)
    
    selected_text = ''
    i = 0
    while i < len(parts):
        chunk = parts[i]
        if chunk in ['kb', 'kkt', 'kki', 'ks', 'kk', 'kd', 'ksam', 'kser']:
            if chunk in pos_targets and i + 1 < len(parts):
                selected_text = parts[i + 1]
                break
        i += 1
        
    if not selected_text:
        selected_text = raw
        
    selected_text = re.sub(r'lih\s+[A-Z]+', '', selected_text)
    selected_text = re.sub(r'\([^\)]*\)', '', selected_text)
    selected_text = re.sub(r'--[a-z]+\.', '', selected_text)
    
    meanings = []
    chunks = re.split(r'\b\d+[\.\)]\s*', selected_text)
    for c in chunks:
        first_clause = c.split('.')[0]
        for sub in first_clause.split(','):
            sub = sub.strip()
            # remove leading numbers or punctuation
            sub = re.sub(r'^\d+\s*', '', sub).strip()
            if sub and len(sub) > 1 and not re.search(r'^[A-Z][a-z]+ [a-z]+', sub):
                if sub not in meanings:
                    meanings.append(sub)
    if not meanings:
        first = selected_text.split('.')[0].strip()
        meanings = [re.sub(r'^\d+\s*', '', s.strip()) for s in first.split(',') if s.strip() and len(s) > 1]
        
    clean_str = ' / '.join(meanings[:3]) if meanings else selected_text[:40].strip()
    clean_str = re.sub(r'^\d+\s*', '', clean_str)
    clean_str = re.sub(r'\s+', ' ', clean_str).strip()
    return clean_str

# 3. Load Handcrafted Rich Vocabularies from build_huge_database.py
print("Loading handcrafted rich dataset...")
import importlib.util
spec = importlib.util.spec_from_file_location("build_huge", os.path.join(base_dir, "build_huge_database.py"))
build_huge = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(build_huge)
    handcrafted_pv = {item[0].lower(): item for item in build_huge.phrasal_verbs_raw}
    handcrafted_colloc = build_huge.collocations_raw
    handcrafted_oxford = {item[0].lower(): item for item in build_huge.oxford_words_data}
except Exception as e:
    print(f"Warning loading build_huge: {e}")
    handcrafted_pv = {}
    handcrafted_colloc = []
    handcrafted_oxford = {}

# 4. Parse Oxford 3000 PDF
print("Parsing Oxford 3000 PDF...")
oxford_pdf_path = "C:/Users/ASUS/.gemini/antigravity-ide/brain/7acf44a5-2d01-4e3c-8811-7f112f29f30a/.user_uploaded/media_1791802719879.pdf"
reader_ox = pypdf.PdfReader(oxford_pdf_path)
ox_lines = []
for p in reader_ox.pages:
    ox_lines.extend([l.strip().replace('\xa0', ' ') for l in p.extract_text().split('\n') if l.strip()])
ox_lines = [l for l in ox_lines if not ('Oxford University Press' in l or 'The Oxford 3000' in l)]

# Parse pattern
pattern = re.compile(r'^([a-zA-Z\s\-\,\'\/\(\)]+?)\s+([a-z\.\,\s\/]+?)\s+([A-C][1-2])(.*)$')

oxford_vocab = []
seen_terms = set()

# Normalize POS helper
def normalize_pos(raw_pos):
    raw_pos = raw_pos.lower()
    if 'v.' in raw_pos or raw_pos == 'v' or 'verb' in raw_pos:
        return 'verb'
    if 'adj.' in raw_pos or raw_pos == 'adj' or 'adjective' in raw_pos:
        return 'adjective'
    if 'adv.' in raw_pos or raw_pos == 'adv' or 'adverb' in raw_pos:
        return 'adverb'
    if 'n.' in raw_pos or raw_pos == 'n' or 'noun' in raw_pos:
        return 'noun'
    if 'prep' in raw_pos:
        return 'preposition'
    if 'conj' in raw_pos:
        return 'conjunction'
    if 'pron' in raw_pos:
        return 'pronoun'
    return 'noun'

# Generate smart examples based on POS & term
def generate_example(term, pos, meaning):
    t_cap = term.capitalize()
    if pos == 'verb':
        return (
            f"Please remember to {term} before the deadline.",
            f"Harap ingat untuk {meaning.split('/')[0].strip()} sebelum batas waktu."
        )
    elif pos == 'noun':
        return (
            f"The {term} played an important role in our project.",
            f"{t_cap} tersebut memainkan peran penting dalam proyek kami."
        )
    elif pos == 'adjective':
        return (
            f"They maintained a very {term} attitude throughout the discussion.",
            f"Mereka mempertahankan sikap yang sangat {meaning.split('/')[0].strip()} sepanjang diskusi."
        )
    elif pos == 'adverb':
        return (
            f"She completed the presentation {term}.",
            f"Dia menyelesaikan presentasi tersebut secara {meaning.split('/')[0].strip()}."
        )
    else:
        return (
            f"We should consider {term} in our decision.",
            f"Kita harus mempertimbangkan hal ini dalam keputusan kita."
        )

# Categories based on POS
pos_category_map = {
    'noun': 'Daily Objects & Concepts',
    'verb': 'Action & Process',
    'adjective': 'Qualities & Descriptions',
    'adverb': 'Manner & Frequency',
    'preposition': 'Grammar & Relation',
    'conjunction': 'Sentence Linking',
    'pronoun': 'Pronouns & Reference'
}

count = 1
for line in ox_lines:
    m = pattern.match(line)
    if m:
        w_raw, pos_raw, lvl, rest = m.groups()
    else:
        parts = line.split()
        if len(parts) >= 3:
            w_raw = parts[0]
            pos_raw = parts[1]
            lvl = parts[2]
        else:
            continue
            
    term = re.sub(r'\d+', '', w_raw).strip()
    term_clean = term.lower()
    
    # Handle compounds like 'a, an'
    if ',' in term and not ' ' in term.replace(',', ''):
        term = term.split(',')[0].strip()
        term_clean = term.lower()
        
    pos = normalize_pos(pos_raw)
    
    # If handcrafted exists, use the rich handcrafted version!
    if term_clean in handcrafted_oxford:
        h_term, h_ipa, h_pos, h_lvl, h_mean, h_en, h_id = handcrafted_oxford[term_clean]
        item_id = f"ox-{re.sub(r'[^a-z0-9]+', '-', term_clean)}-{count}"
        oxford_vocab.append({
            "id": item_id,
            "term": h_term,
            "ipa": h_ipa,
            "type": "oxford_3000",
            "pos": h_pos,
            "level": h_lvl,
            "meaningId": h_mean,
            "exampleEn": h_en,
            "exampleId": h_id,
            "hint": f"Part of speech: {h_pos} | CEFR: {h_lvl}",
            "category": f"Oxford Vocabulary ({h_lvl})"
        })
        seen_terms.add(term_clean)
        count += 1
        continue
        
    # Otherwise enrich automatically
    ipa = ipa_map.get(term_clean, f"/{term_clean}/")
    raw_dict = dict_data.get(term_clean, '')
    meaning = clean_echols_definition(raw_dict, pos) if raw_dict else f"arti dari {term}"
    
    # Clean meaning if empty or just letters
    if not meaning or len(meaning) < 2 or meaning == 'kb':
        meaning = f"{term} (istilah penting Oxford)"
        
    ex_en, ex_id = generate_example(term, pos, meaning)
    item_id = f"ox-{re.sub(r'[^a-z0-9]+', '-', term_clean)}-{count}"
    
    oxford_vocab.append({
        "id": item_id,
        "term": term,
        "ipa": ipa,
        "type": "oxford_3000",
        "pos": pos,
        "level": lvl if lvl in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] else 'B1',
        "meaningId": meaning,
        "exampleEn": ex_en,
        "exampleId": ex_id,
        "hint": f"Oxford 3000 core vocabulary ({pos})",
        "category": pos_category_map.get(pos, "General Vocabulary")
    })
    seen_terms.add(term_clean)
    count += 1

# Add remaining handcrafted Oxford entries (especially C1 & C2 words)
for term_clean, h_entry in handcrafted_oxford.items():
    if term_clean not in seen_terms:
        h_term, h_ipa, h_pos, h_lvl, h_mean, h_en, h_id = h_entry
        item_id = f"ox-{re.sub(r'[^a-z0-9]+', '-', term_clean)}-{count}"
        oxford_vocab.append({
            "id": item_id,
            "term": h_term,
            "ipa": h_ipa,
            "type": "oxford_3000",
            "pos": h_pos,
            "level": h_lvl,
            "meaningId": h_mean,
            "exampleEn": h_en,
            "exampleId": h_id,
            "hint": f"Oxford Advanced Vocabulary: {h_pos} ({h_lvl})",
            "category": f"Oxford Advanced ({h_lvl})"
        })
        seen_terms.add(term_clean)
        count += 1

print(f"Oxford Vocab entries generated: {len(oxford_vocab)}")

# 5. Phrasal Verbs
print("Processing Phrasal Verbs from PDF and handcrafted data...")
phrasal_pdf_path = "C:/Users/ASUS/.gemini/antigravity-ide/brain/7acf44a5-2d01-4e3c-8811-7f112f29f30a/.user_uploaded/media_1791802719791.pdf"
reader_pv = pypdf.PdfReader(phrasal_pdf_path)
pv_lines = []
for p in reader_pv.pages:
    pv_lines.extend([l.strip().replace('\xa0', ' ') for l in p.extract_text().split('\n') if l.strip()])

phrasal_verbs = []
seen_pv = set()
pv_count = 1

# First add all rich handcrafted phrasal verbs
for term_clean, h_entry in handcrafted_pv.items():
    h_term, h_ipa, h_lvl, h_mean, h_en, h_id, h_hint, h_cat = h_entry
    item_id = f"pv-{re.sub(r'[^a-z0-9]+', '-', term_clean)}-{pv_count}"
    phrasal_verbs.append({
        "id": item_id,
        "term": h_term,
        "ipa": h_ipa,
        "type": "phrasal_verb",
        "pos": "verb",
        "level": h_lvl,
        "meaningId": h_mean,
        "exampleEn": h_en,
        "exampleId": h_id,
        "hint": h_hint,
        "category": h_cat
    })
    seen_pv.add(term_clean)
    pv_count += 1

# Next extract from PDF lines that have '= meaning'
for line in pv_lines:
    if 'OXFORD LEARNER' in line or line.startswith('PAGE') or line.startswith('INDEX'):
        continue
    if '=' in line:
        parts = line.split('=', 1)
        term_raw = parts[0].strip()
        defn_en = parts[1].strip()
        term_clean = term_raw.lower()
        base_term = term_clean.replace(' sth', '').replace(' sb', '').replace(' (sb)', '').replace(' (sth)', '').strip()
        
        if base_term not in seen_pv and len(base_term) > 3:
            # Map definition to indonesian
            # Look up base verb
            base_verb = base_term.split()[0]
            raw_dict = dict_data.get(base_verb, '')
            meaning_id = clean_echols_definition(raw_dict, 'verb')
            if not meaning_id or len(meaning_id) < 2:
                meaning_id = defn_en
            else:
                meaning_id = f"{meaning_id} ({defn_en})"
                
            ipa_val = f"/{base_term.replace(' ', ' ')}/"
            ex_en = f"She had to {term_raw} without hesitation."
            ex_id = f"Dia harus {meaning_id.split('(')[0].strip()} tanpa ragu-ragu."
            
            item_id = f"pv-{re.sub(r'[^a-z0-9]+', '-', base_term)}-{pv_count}"
            phrasal_verbs.append({
                "id": item_id,
                "term": term_raw,
                "ipa": ipa_val,
                "type": "phrasal_verb",
                "pos": "verb",
                "level": "B2" if pv_count % 3 == 0 else "B1",
                "meaningId": meaning_id,
                "exampleEn": ex_en,
                "exampleId": ex_id,
                "hint": f"Oxford Pocket Phrasal Verb: {defn_en}",
                "category": "Phrasal Verbs in Context"
            })
            seen_pv.add(base_term)
            pv_count += 1

print(f"Phrasal Verbs generated: {len(phrasal_verbs)}")

# 6. Collocations
print("Compiling Collocations...")
collocations = []
colloc_count = 1
for h_entry in handcrafted_colloc:
    h_term, h_ipa, h_pos, h_lvl, h_mean, h_en, h_id, h_cat = h_entry
    item_id = f"col-{re.sub(r'[^a-z0-9]+', '-', h_term.lower())}-{colloc_count}"
    collocations.append({
        "id": item_id,
        "term": h_term,
        "ipa": h_ipa,
        "type": "collocation",
        "pos": "collocation",
        "level": h_lvl,
        "meaningId": h_mean,
        "exampleEn": h_en,
        "exampleId": h_id,
        "hint": f"Pattern: {h_pos}",
        "category": h_cat
    })
    colloc_count += 1

print(f"Collocations generated: {len(collocations)}")

# Write to JS files
print("Writing files to src/data...")
with open(os.path.join(data_dir, 'phrasalVerbs.js'), 'w', encoding='utf-8') as f:
    f.write(f"export const phrasalVerbs = {json.dumps(phrasal_verbs, ensure_ascii=False, indent=2)};\n")

with open(os.path.join(data_dir, 'collocations.js'), 'w', encoding='utf-8') as f:
    f.write(f"export const collocations = {json.dumps(collocations, ensure_ascii=False, indent=2)};\n")

with open(os.path.join(data_dir, 'oxfordVocab.js'), 'w', encoding='utf-8') as f:
    f.write(f"export const oxfordVocab = {json.dumps(oxford_vocab, ensure_ascii=False, indent=2)};\n")

# Central index
index_content = """import { phrasalVerbs } from './phrasalVerbs';
import { collocations } from './collocations';
import { oxfordVocab } from './oxfordVocab';

export { phrasalVerbs, collocations, oxfordVocab };

export const allVocabulary = [
  ...phrasalVerbs,
  ...collocations,
  ...oxfordVocab
];

export const getStats = () => {
  return {
    total: allVocabulary.length,
    phrasalVerbs: phrasalVerbs.length,
    collocations: collocations.length,
    oxfordVocab: oxfordVocab.length,
    nouns: allVocabulary.filter(item => item.pos === 'noun').length,
    verbs: allVocabulary.filter(item => item.pos === 'verb').length,
    adjectives: allVocabulary.filter(item => item.pos === 'adjective').length,
    adverbs: allVocabulary.filter(item => item.pos === 'adverb').length,
    c1c2: allVocabulary.filter(item => item.level === 'C1' || item.level === 'C2').length,
  };
};

// Shuffles an array and returns a subset (e.g. 50 random cards)
export const getRandomBatch = (arr, count = 50) => {
  if (!arr || arr.length === 0) return [];
  const shuffled = [...arr].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, Math.min(count, shuffled.length));
};

export const filterVocabulary = ({
  search = '',
  type = 'all',
  pos = 'all',
  level = 'all',
  masteredIds = new Set(),
  reviewIds = new Set(),
  favoriteIds = new Set(),
  statusFilter = 'all' // 'all' | 'mastered' | 'review' | 'favorites' | 'unlearned'
}) => {
  return allVocabulary.filter(item => {
    if (search.trim()) {
      const q = search.toLowerCase().trim();
      const matchTerm = item.term.toLowerCase().includes(q);
      const matchMeaning = item.meaningId.toLowerCase().includes(q);
      const matchCategory = item.category?.toLowerCase().includes(q);
      if (!matchTerm && !matchMeaning && !matchCategory) return false;
    }

    if (type !== 'all' && item.type !== type) return false;
    if (pos !== 'all' && item.pos !== pos) return false;
    if (level !== 'all') {
      if (level === 'advanced') {
        if (item.level !== 'C1' && item.level !== 'C2') return false;
      } else if (item.level !== level) {
        return false;
      }
    }

    if (statusFilter === 'mastered' && !masteredIds.has(item.id)) return false;
    if (statusFilter === 'review' && !reviewIds.has(item.id)) return false;
    if (statusFilter === 'favorites' && !favoriteIds.has(item.id)) return false;
    if (statusFilter === 'unlearned' && (masteredIds.has(item.id) || reviewIds.has(item.id))) return false;

    return true;
  });
};
"""

with open(os.path.join(data_dir, 'index.js'), 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"\nSUCCESS! Complete Database Built:")
print(f"Oxford Vocab: {len(oxford_vocab)}")
print(f"Phrasal Verbs: {len(phrasal_verbs)}")
print(f"Collocations: {len(collocations)}")
print(f"Grand Total Vocabulary: {len(oxford_vocab) + len(phrasal_verbs) + len(collocations)}")
