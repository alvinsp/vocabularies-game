import re
import sys

def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match full object entries
    pattern = r'\{\s*"id":\s*"([^"]+)",\s*"term":\s*"([^"]+)"(?:,\s*"ipa":\s*"[^"]*")?(?:,\s*"type":\s*"[^"]*")?(?:,\s*"pos":\s*"[^"]*")?(?:,\s*"level":\s*"[^"]*")?,\s*"meaningId":\s*"([^"]+)"'
    matches = re.findall(pattern, content)
    
    suspicious = []
    bad_patterns = [
        (r'^(kb|kk|ks|kd|am|kg|kn|Inf|sb|sth|kki|kkt)\b', "abbreviation prefix"),
        (r'\b(sb|sth)\b', "contains sb or sth"),
        (r'\b(kk|kb|ks|kd|am|kg|kn)\b', "contains grammatical abbreviation"),
        (r'istilah penting', "istilah penting placeholder"),
        (r'makna kata', "makna kata placeholder"),
        (r'^[a-z]{1,2}$', "1-2 letter meaning"),
        (r'\(abolish', "English parenthetical"),
        (r'\(tolerate', "English parenthetical"),
        (r'\(defeat', "English parenthetical"),
        (r'\.\.\.[a-z]', "dots between characters in meaning"),
    ]
    for mid, term, meaning in matches:
        if re.search(r'\.\.\.[a-z]', term):
            suspicious.append((mid, term, meaning, "dots between characters in term"))
            continue
        for p, desc in bad_patterns:
            if re.search(p, meaning, re.I):
                suspicious.append((mid, term, meaning, desc))
                break
    return len(matches), suspicious

total_all = 0
suspicious_all = 0
for f in ['src/data/phrasalVerbs.js', 'src/data/oxfordVocab.js', 'src/data/collocations.js']:
    total, bad = check_file(f)
    total_all += total
    suspicious_all += len(bad)
    print(f"\n=== {f}: {total} entries, {len(bad)} suspicious ===")
    for mid, term, meaning, desc in bad:
        print(f"   [{mid}] {term} -> \"{meaning}\" ({desc})")

print(f"\nAudit complete: Total {total_all} words, {suspicious_all} suspicious entries found.")
