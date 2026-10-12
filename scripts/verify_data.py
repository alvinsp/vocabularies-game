import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/oxfordVocab.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'export const oxfordVocab = '
if text.startswith(prefix):
    json_text = text[len(prefix):].rstrip(';\n')
else:
    json_text = text

data = json.loads(json_text)
print(f"Total Oxford items: {len(data)}")

fallbacks = [item for item in data if 'istilah penting' in item.get('meaningId', '') or 'makna kata' in item.get('meaningId', '')]
print(f"Total fallbacks: {len(fallbacks)}")
if fallbacks:
    print("Sample fallbacks:", [f['term'] for f in fallbacks[:10]])

wishes = [item for item in data if item['term'].lower() == 'wish']
for w in wishes:
    print("Found wish:")
    print("  Term:", w['term'])
    print("  POS:", w['pos'])
    print("  Level:", w['level'])
    print("  IPA:", w['ipa'])
    print("  Meaning ID:", w['meaningId'])
    print("  Example EN:", w['exampleEn'])
    print("  Example ID:", w['exampleId'])
