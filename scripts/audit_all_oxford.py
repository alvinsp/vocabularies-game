import json
import re

with open('src/data/oxfordVocab.js', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'\{\s*"id":\s*"([^"]+)",\s*"term":\s*"([^"]+)"(?:,\s*"ipa":\s*"[^"]*")?(?:,\s*"type":\s*"[^"]*")?(?:,\s*"pos":\s*"[^"]*")?(?:,\s*"level":\s*"[^"]*")?,\s*"meaningId":\s*"([^"]+)"'
matches = re.findall(pattern, content)

imperfect = []
for mid, term, meaning in matches:
    issues = []
    # 1. Unbalanced parentheses
    if meaning.count('(') != meaning.count(')'):
        issues.append('unbalanced parentheses')
    # 2. Number inside (unless term is a number word)
    num_words = {'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 
                 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 
                 'eighteen', 'nineteen', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 
                 'eighty', 'ninety', 'hundred', 'thousand', 'million', 'billion', 'zero', 'mile', 'kilo', 'kilometre', 'century'}
    if re.search(r'\b\d+\b', meaning) and term.lower() not in num_words:
        issues.append('has number digit')
    # 3. Contains raw English dictionary markers
    if re.search(r'\b(to\s+[a-z]|Inf|sb|sth|kk|kb|ks|kd|am|kg|kn|kki|kkt|transitive|intransitive|etc)\b', meaning, re.I):
        issues.append('dictionary marker/raw english')
    # 4. Leading or trailing punctuation like ) or ( or / or ;
    if re.search(r'^[^\w\s(]|[\)\]\/\;\,]$', meaning.strip()):
        issues.append('odd trailing/leading punctuation')
    # 5. Multiple spaces
    if '  ' in meaning:
        issues.append('double spaces')
    # 6. Starts with lower case English preposition or article
    if re.search(r'^(to|of|in|for|on|with|at|by|from|up|about|into|over|after|a|an|the)\b', meaning):
        issues.append('starts with english word')
        
    if issues:
        imperfect.append((mid, term, meaning, issues))

print(f"Total Oxford entries checked: {len(matches)}")
print(f"Total imperfect entries: {len(imperfect)}")
for mid, term, meaning, issues in imperfect:
    print(f"[{mid}] {term} -> \"{meaning}\" | Issues: {', '.join(issues)}")
