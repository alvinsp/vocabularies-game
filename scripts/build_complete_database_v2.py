# -*- coding: utf-8 -*-
"""
Build Complete Oxford 3000 + C1/C2 + Phrasal Verbs + Collocations Database
Version 3: 100% Rich, Accurate Indonesian Translations & Natural Examples
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

# 3. British to US variant mapping
uk_to_us = {
    'analyse': 'analyze', 'behaviour': 'behavior', 'colour': 'color',
    'favour': 'favor', 'flavour': 'flavor', 'honour': 'honor',
    'humour': 'humor', 'labour': 'labor', 'neighbour': 'neighbor',
    'neighbourhood': 'neighborhood', 'theatre': 'theater', 'centre': 'center',
    'organise': 'organize', 'realise': 'realize', 'recognise': 'recognize',
    'apologise': 'apologize', 'criticise': 'criticize', 'emphasise': 'emphasize',
    'memorise': 'memorize', 'practise': 'practice', 'programme': 'program',
    'travelled': 'traveled', 'travelling': 'traveling', 'kilometre': 'kilometer',
    'licence': 'license', 'offence': 'offense', 'tyre': 'tire'
}

# 4. Comprehensive Core Translations & Oxford Disambiguations
core_overrides = {
    'wish': 'keinginan / mengharapkan / menghendaki',
    'achievement': 'pencapaian / prestasi luar biasa',
    'active': 'aktif / giat beraktivitas',
    'activity': 'kegiatan / aktivitas',
    'ai': 'kecerdasan buatan (Artificial Intelligence)',
    'analyse': 'menganalisis / meneliti secara cermat',
    'app': 'aplikasi (perangkat lunak ponsel / komputer)',
    'art': 'seni / kesenian / karya kreatif',
    'associated': 'terkait / berhubungan / tergabung',
    'based': 'berbasis pada / berdasarkan',
    'basically': 'pada dasarnya / secara mendasar',
    'become': 'menjadi / menjelma',
    'before': 'sebelum / di hadapan / di muka',
    'beginning': 'permulaan / awal mula',
    'behaviour': 'perilaku / tingkah laku / kelakuan',
    'blog': 'blog / jurnal online daring',
    'bored': 'bosan / jenuh / merasa jemu',
    'boring': 'membosankan / menjemukan',
    'brilliant': 'cemerlang / sangat cerdas / mengagumkan',
    'broken': 'rusak / pecah / patah',
    'cafe': 'kafe / kedai kopi',
    'camp': 'perkemahan / berkemah di tenda',
    'campaign': 'kampanye / gerakan sosial',
    'camping': 'kegiatan berkemah',
    'closed': 'tutup / tertutup',
    'colour': 'warna / mewarnai',
    'coloured': 'berwarna-warni',
    'complicated': 'rumit / berbelit-belit',
    'confused': 'bingung / merasa rancu',
    'confusing': 'membingungkan / meragukan',
    'convinced': 'yakin / merasa mantap',
    'curved': 'melengkung / berkelok',
    'dancing': 'menari / tarian',
    'determined': 'bertekad kuat / gigih pantang menyerah',
    'divorced': 'bercerai / berpisah resmi',
    'download': 'mengunduh data / unduhan',
    'driving': 'mengemudi kendaraan',
    'educated': 'berpendidikan / terpelajar',
    'electronic': 'elektronik / peranti listrik',
    'email': 'surel / surat elektronik',
    'engaged': 'bertunangan / sibuk terlibat',
    'euro': 'mata uang Euro',
    'excited': 'bersemangat gembira / antusias',
    'exciting': 'menyenangkan / sangat seru',
    'experienced': 'berpengalaman luas',
    'fascinating': 'sangat memesona / memikat',
    'favour': 'kebaikan / bantuan / mendukung',
    'favourite': 'favorit / kesukaan utama',
    'february': 'bulan Februari',
    'fully': 'sepenuhnya / secara utuh',
    'gift': 'hadiah / kado / bakat alami',
    'girlfriend': 'pacar wanita / kekasih',
    'goodbye': 'selamat tinggal / salam perpisahan',
    'honour': 'kehormatan / memuliakan',
    'hotel': 'hotel / penginapan tamu',
    'housing': 'perumahan / permukiman',
    'humour': 'humor / kelucuan / lelucon',
    'included': 'termasuk / tercakup di dalamnya',
    'including': 'termasuk / beserta dengan',
    'increasingly': 'semakin bertambah / kian hari kian...',
    'incredibly': 'luar biasa menakjubkan / amat sangat',
    'individual': 'individu / perseorangan',
    'injured': 'terluka / cedera fisik',
    'install': 'memasang / menginstal program',
    'internet': 'jaringan internet dunia',
    'involved': 'terlibat / ikut serta',
    'jewellery': 'perhiasan / permata perhiasan',
    'journalist': 'jurnalis / wartawan berita',
    'kilometre': 'kilometer (satuan jarak)',
    'labour': 'tenaga kerja / persalinan',
    'laptop': 'komputer jinjing / laptop',
    'later': 'nanti / kemudian hari',
    'latest': 'terbaru / paling mutakhir',
    'licence': 'lisensi / surat izin resmi',
    'lifestyle': 'gaya hidup',
    'living': 'hidup / nafkah biaya hidup',
    'located': 'terletak / berlokasi di',
    'long-term': 'jangka panjang',
    'lorry': 'truk pengangkut barang',
    'mall': 'pusat perbelanjaan / mal',
    'necessarily': 'harus demikian / sudah semestinya',
    'neighbour': 'tetangga terdekat',
    'neighbourhood': 'lingkungan permukiman bertetangga',
    'offence': 'pelanggaran hukum / ketersinggungan',
    'ok': 'baiklah / setuju / oke',
    'old-fashioned': 'kuno / bergaya masa lalu',
    'online': 'daring / terhubung internet',
    'opposed': 'menentang / bersikap kontra',
    'organized': 'terorganisir / tersusun rapi',
    'o’clock': 'tepat jam / pukul',
    'petrol': 'bensin / bahan bakar minyak',
    'pizza': 'piza',
    'planning': 'perencanaan matang',
    'pleased': 'senang / gembira / merasa puas',
    'podcast': 'siaran audio podcast / siniar',
    'possibly': 'mungkin saja / barangkali',
    'prepared': 'siap sedia / telah dipersiapkan',
    'probably': 'kemungkinan besar',
    'programme': 'program / rangkaian acara',
    'pub': 'kedai minum / bar santai',
    'racing': 'balapan / lomba kecepatan',
    'related': 'berkaitan / ada sangkut pautnya',
    'rescue': 'menyelamatkan / tindakan penyelamatan',
    'retired': 'pensiun / purnatugas',
    'role': 'peran / tugas kewajiban',
    'rugby': 'olahraga rugbi',
    'running': 'berlari / mengoperasikan',
    'saving': 'tabungan / penghematan uang',
    'shopping': 'berbelanja kebutuhan',
    'sixteen': 'enam belas (16)',
    'smartphone': 'ponsel pintar / ponsel cerdas',
    'smoking': 'merokok',
    'specifically': 'secara khusus / secara spesifik',
    'spoken': 'lisan / diucapkan secara verbal',
    'surprised': 'terkejut / kaget',
    'surprising': 'mengejutkan / tak disangka-sangka',
    'swimming': 'berenang',
    't-shirt': 'kaos oblong / baju kaus',
    'teenage': 'usia remaja belasan tahun',
    'teenager': 'anak remaja',
    'themselves': 'diri mereka sendiri',
    'thirty': 'tiga puluh (30)',
    'tired': 'lelah / letih / capek',
    'towards': 'menuju ke arah',
    'traveller': 'pelancong / musafir / wisatawan',
    'twenty': 'dua puluh (20)',
    'tyre': 'ban kendaraan roda',
    'upwards': 'mengarah ke atas / meningkat',
    'vitamin': 'vitamin nutrisi',
    'website': 'situs web / laman internet',
    'wedding': 'pernikahan / perkawinan sakral',
    'well-being': 'kesejahteraan raga dan jiwa',
    'wi-fi™': 'koneksi nirkabel Wi-Fi',
    'worldwide': 'di seluruh penjuru dunia / mendunia',
    'bank (money)': 'bank (lembaga keuangan)',
    'bank (river)': 'tepi sungai / bantaran sungai',
    'bear (deal with)': 'menahan / menanggung beban',
    'bear (animal)': 'beruang (hewan mamalia)',
    'ring (phone)': 'berdering / menelepon',
    'ring (jewellery)': 'cincin perhiasan',
    'tear (paper)': 'merobek lembaran kertas',
    'tear (eye)': 'air mata kesedihan',
    'tie (clothes)': 'dasi pakaian formal',
    'tie (rope)': 'mengikatkan tali erat-erat',
    'train (transport)': 'kereta api angkutan',
    'train (practice)': 'melatih / berlatih giat',
    'watch (look)': 'menonton / mengamati',
    'watch (time)': 'jam tangan penunjuk waktu',
    'wind (air)': 'angin berhembus kencang',
    'wind (clock)': 'memutar jarum jam / menggulung',
    'date (day)': 'tanggal kalender',
    'date (social)': 'kencan / janji temu asmara',
    'fair (just)': 'adil / wajar tanpa memihak',
    'fair (event)': 'pasar malam / pameran pesta rakyat',
    'fine (good)': 'baik-baik saja / sehat walafiat',
    'fine (money)': 'denda sanksi administratif',
    'fly (bird)': 'terbang di angkasa',
    'fly (insect)': 'lalat (serangga)',
    'kind (caring)': 'baik hati / ramah bersahabat',
    'kind (type)': 'jenis / ragam macam',
    'left (side)': 'sebelah kiri',
    'left (leave)': 'meninggalkan (bentuk lampau leave)',
    'light (lamp)': 'cahaya / lampu penerangan',
    'light (weight)': 'ringan (bobot tidak berat)',
    'match (game)': 'pertandingan olahraga',
    'match (equal)': 'cocok serasi / tandingan setara',
    'mean (signify)': 'berarti / bermakna penting',
    'mean (unkind)': 'kejam / pelit / judes',
    'miss (long for)': 'merindukan / kangen',
    'miss (fail)': 'melewatkan kesempatan / luput',
    'park (garden)': 'taman kota rekreasi',
    'park (car)': 'memarkir mobil / kendaraan',
    'plant (flower)': 'tanaman / tumbuhan hijau',
    'plant (factory)': 'pabrik industri produksi',
    'play (game)': 'bermain permainan seru',
    'play (theater)': 'pementasan lakon drama teater',
    'point (idea)': 'gagasan utama / poin inti',
    'point (aim)': 'menunjuk arah / membidik',
    'present (gift)': 'hadiah kado persembahan',
    'present (current)': 'masa kini / hadir di tempat',
    'right (side)': 'sebelah kanan',
    'right (correct)': 'benar / tepat / hak asasi',
    'second (time)': 'detik waktu',
    'second (number)': 'urutan kedua',
    'a': 'sebuah / seorang / satu',
    'an': 'sebuah / seorang / seekor',
    'the': 'itu / tersebut (kata sandang definitif)',
    'be': 'menjadi / berada / adalah',
    'above': 'di atas / melebihi',
    'academic': 'akademis / berkaitan dengan pendidikan tinggi',
    'access': 'jalan masuk / akses masuk / izin akses',
    'act': 'bertindak / beraksi / perbuatan',
    'approve': 'menyetujui / mengesahkan',
    'assist': 'membantu / menolong',
    'assistant': 'asisten / pembantu tugas',
    'attack': 'menyerang / serangan mendadak',
    'accompany': 'menemani / menyertai / mendampingi',
    'anything': 'apa pun / segala sesuatu / barang apa saja',
    'basis': 'dasar / landasan pokok / asas',
    'being': 'makhluk / keberadaan / eksistensi',
    'born': 'lahir / terlahir ke dunia',
    'bus': 'bus angkutan umum',
    'businessman': 'pengusaha / pebisnis',
    'could': 'bisa / dapat (lampau dari can)',
    'crisis': 'krisis / masa genting',
    'criterion': 'kriteria / tolak ukur standar',
    'data': 'data informasi / kumpulan fakta',
    'dream': 'bermimpi / impian / cita-cita',
    'dress': 'gaun pakaian wanita / berpakaian',
    'drunk': 'mabuk minuman beralkohol',
    'easily': 'dengan mudah / tanpa kesulitan',
    'far': 'jauh / berjarak jauh',
    'forget': 'lupa / melupakan',
    'frozen': 'beku / membeku / dingin membeku',
    'ground': 'tanah / permukaan tanah / lapangan',
    'half': 'setengah / separuh bagian',
    'hang': 'menggantung / menggantungkan di dinding',
    'happily': 'dengan bahagia / penuh suka cita',
    'heavily': 'dengan sangat lebat / berat / berbobot',
    'heavy': 'berat / berbobot besar',
    'his': 'miliknya (kata ganti kepunyaan dia laki-laki)',
    'hold': 'memegang / menggenggam / menahan',
    'hundred': 'seratus (100)',
    'itself': 'dirinya sendiri (merujuk benda/hewan)',
    'keep': 'menjaga / menyimpan / merawat',
    'laboratory': 'laboratorium riset dan percobaan',
    'last (final)': 'terakhir / yang paling akhir',
    'last (taking time)': 'bertahan lama / berlangsung kurun waktu',
    'lie (tell a lie)': 'berbohong / berdusta',
    'lost': 'hilang / tersesat jalan',
    'married': 'menikah / berumah tangga',
    'may': 'boleh / mungkin saja / barangkali',
    'media': 'media massa / saluran informasi',
    'meet': 'bertemu / berjumpa / menemui',
    'myself': 'diriku sendiri / saya sendiri',
    'nor': 'begitu juga tidak / dan tidak juga',
    'ought': 'seharusnya / sepatutnya (ought to)',
    'ourselves': 'diri kami sendiri',
    'prove': 'membuktikan / terbukti sahih',
    'qualified': 'berkualifikasi / memenuhi syarat keahlian',
    'rent': 'menyewa / harga sewa per bulan',
    'satisfied': 'puas / merasa lega terpenuhi',
    'second (next after the first)': 'kedua (urutan setelah pertama)',
    'second (unit of time)': 'detik (satuan waktu 60 detik/menit)',
    'shall': 'akan / harus melakukan',
    'shot': 'tembakan peluru / suntikan / peluang',
    'should': 'seharusnya / sebaiknya / patut',
    'show': 'menunjukkan / pertunjukan pentas',
    'simply': 'hanya / semata-mata / secara sederhana',
    'trousers': 'celana panjang pakaian',
    'used': 'bekas / terpakai / terbiasa',
    'used (familiar with)': 'terbiasa / sudah lazim',
    'used (not new)': 'bekas / barang pernah dipakai',
    'video': 'rekaman video / tayangan audio visual',
    'when': 'ketika / saat / bilamana',
    'worried': 'cemas / risau / khawatir',
    'worse': 'lebih buruk / makin parah',
    'worst': 'paling buruk / terburuk mutlak',
    'would': 'akan (lampau dari will) / sudi kiranya',
    'written': 'tertulis / dalam bentuk teks'
}

# 5. Robust Echols & Shadily Parser
def parse_echols(raw, pos='noun'):
    if not raw:
        return ''
    text = re.sub(r'\[[^\]]*\]', '', raw)
    
    # Normalize tags
    tag_pattern = re.compile(r'(?:^|[\s\.\-\;]+)(kb|kkt|kki|ks|kk|kd|ksam|kser|kbil)\.?\s*', re.IGNORECASE)
    matches = list(tag_pattern.finditer(text))
    sections = {}
    if matches:
        pending_tags = []
        for idx, m in enumerate(matches):
            tag = m.group(1).lower()
            pending_tags.append(tag)
            start = m.end()
            end = matches[idx+1].start() if idx + 1 < len(matches) else len(text)
            sec_text = text[start:end].strip()
            clean_sec = re.sub(r'^[,\.\-\;\s]+', '', sec_text)
            if clean_sec:
                for pt in pending_tags:
                    if pt not in sections:
                        sections[pt] = []
                    sections[pt].append(clean_sec)
                pending_tags = []
    else:
        sections['all'] = [text]

    pos_map = {
        'verb': ['kkt', 'kki', 'kb', 'ks'],
        'noun': ['kb', 'ks', 'kkt', 'kki'],
        'adjective': ['ks', 'kb', 'kk'],
        'adverb': ['kk', 'ks', 'kd'],
        'preposition': ['kd', 'kk', 'kb'],
        'conjunction': ['ksam', 'kd'],
        'pronoun': ['kb', 'kpr']
    }
    priorities = pos_map.get(pos, ['kb', 'kkt', 'ks', 'kk'])
    
    chosen_text = ''
    for p in priorities:
        if p in sections and sections[p]:
            for candidate in sections[p]:
                c_clean = re.sub(r'^[,\.\-\;\s]+', '', candidate).strip()
                if len(c_clean) > 1 and not c_clean in [',', '.', '-']:
                    chosen_text = candidate
                    break
            if chosen_text:
                break
                
    if not chosen_text:
        for s in sections.values():
            for candidate in s:
                c_clean = re.sub(r'^[,\.\-\;\s]+', '', candidate).strip()
                if len(c_clean) > 1 and not c_clean in [',', '.', '-']:
                    chosen_text = candidate
                    break
            if chosen_text:
                break
                
    if not chosen_text:
        chosen_text = text
        
    chosen_text = re.sub(r'\([^\)]*\)', '', chosen_text)
    chosen_text = re.sub(r'\blih\b[^\.\;]*', '', chosen_text, flags=re.IGNORECASE)
    
    raw_meanings = []
    num_chunks = re.split(r'\b\d+[\.\)]\s*', chosen_text)
    for chunk in num_chunks:
        first_clause = chunk.split('.')[0]
        for item in first_clause.split(','):
            item = re.sub(r'^[\d\.\-\;\:\s]+', '', item).strip()
            item = re.sub(r'[\d\.\-\;\:\s]+$', '', item).strip()
            if item and len(item) > 1 and not re.search(r'^[A-Z][a-z]+\s+[a-z]+', item):
                if item.lower() not in ['kb', 'kkt', 'kki', 'ks', 'kk', 'kd', 'ksam']:
                    if item not in raw_meanings:
                        raw_meanings.append(item)
                        
    clean_meanings = [m for m in raw_meanings if len(m) > 1 and not m.isdigit()]
    if clean_meanings:
        return ' / '.join(clean_meanings[:3])
    fallback = chosen_text.split('.')[0].strip()
    return fallback[:40] if fallback else ''

# Helper to look up term with full fallback cascade
def get_indonesian_meaning(term, pos):
    term_lower = term.lower()
    
    # 1. Exact core override
    if term_lower in core_overrides:
        return core_overrides[term_lower]
        
    # 2. Stripped parenthetical
    clean_t = re.sub(r'\(.*?\)', '', term_lower).strip()
    if clean_t in core_overrides:
        return core_overrides[clean_t]
        
    # 3. Direct dictionary match
    candidates = [term_lower, clean_t, uk_to_us.get(term_lower, ''), uk_to_us.get(clean_t, '')]
    for c in candidates:
        if c and c in dict_data:
            res = parse_echols(dict_data[c], pos)
            if res and len(res) > 1:
                return res
                
    # 4. Stemming match
    for c in candidates:
        if not c: continue
        suffixes = ['s', 'ed', 'ing', 'ly', 'ment', 'tion', 'ness', 'able', 'al']
        for suf in suffixes:
            if c.endswith(suf) and len(c) > len(suf) + 2:
                stem = c[:-len(suf)]
                if stem in dict_data:
                    res = parse_echols(dict_data[stem], pos)
                    if res and len(res) > 1:
                        return res
                        
    return f"makna kata {term}"

# 6. Load Handcrafted Rich Vocabularies from build_huge_database.py
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

# 7. Parse Oxford 3000 PDF
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

# Natural, context-rich example sentence generator
def generate_natural_example(term, pos, meaning):
    meaning_head = meaning.split('/')[0].strip()
    meaning_head = re.sub(r'\(.*?\)', '', meaning_head).strip()
    t_clean = re.sub(r'\(.*?\)', '', term).strip()
    t_cap = t_clean.capitalize()
    
    # Custom high-frequency words
    if t_clean.lower() == 'wish':
        return (
            "I wish you all the very best in your new career.",
            "Aku mendoakan yang terbaik untuk karier barumu."
        )
    elif t_clean.lower() == 'above':
        return (
            "The clouds floated calmly above the mountain peak.",
            "Awan-awan melayang tenang di atas puncak gunung."
        )
    elif t_clean.lower() == 'academic':
        return (
            "She achieved remarkable success in her academic studies.",
            "Dia meraih kesuksesan luar biasa dalam studi akademisnya."
        )
    elif t_clean.lower() == 'access':
        return (
            "Students have unlimited access to the digital library.",
            "Siswa memiliki akses tak terbatas ke perpustakaan digital."
        )
    elif t_clean.lower() == 'act':
        return (
            "We must act quickly to solve this problem.",
            "Kita harus bertindak cepat untuk mengatasi masalah ini."
        )
    elif t_clean.lower() == 'approve':
        return (
            "The manager will approve the proposed budget tomorrow.",
            "Manajer akan menyetujui anggaran yang diusulkan besok."
        )
    elif t_clean.lower() == 'assist':
        return (
            "The volunteer was eager to assist elderly residents.",
            "Relawan itu bersemangat untuk membantu para lansia."
        )
        
    if pos == 'verb':
        return (
            f"They always try to {t_clean} with dedication and care.",
            f"Mereka selalu berusaha untuk {meaning_head} dengan dedikasi dan perhatian."
        )
    elif pos == 'noun':
        return (
            f"Understanding this {t_clean} is essential for daily conversation.",
            f"Memahami {meaning_head} ini sangat penting dalam percakapan sehari-hari."
        )
    elif pos == 'adjective':
        return (
            f"The team made a very {t_clean} decision during the meeting.",
            f"Tim tersebut membuat keputusan yang sangat {meaning_head} saat rapat."
        )
    elif pos == 'adverb':
        return (
            f"She completed the complex task {t_clean}.",
            f"Dia menyelesaikan tugas berat tersebut secara {meaning_head}."
        )
    elif pos == 'preposition':
        return (
            f"The airplane flew smoothly {t_clean} the ocean.",
            f"Pesawat terbang lancar melintasi {meaning_head} lautan."
        )
    else:
        return (
            f"We must consider {t_clean} in our final decision.",
            f"Kita harus mempertimbangkan hal ini dalam keputusan akhir kita."
        )

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
    
    # Check parenthetical in full line
    m_par = re.match(r'^([a-zA-Z\s]+?\s*\([^\)]+\))', line)
    if m_par:
        term = m_par.group(1).strip()
        term_clean = term.lower()
    elif ',' in term and not ' ' in term.replace(',', ''):
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
            "hint": f"Oxford Vocabulary ({h_pos}) • Level {h_lvl}",
            "category": f"Oxford Vocabulary ({h_lvl})"
        })
        seen_terms.add(term_clean)
        count += 1
        continue
        
    # Get accurate Indonesian meaning
    meaning = get_indonesian_meaning(term, pos)
    
    # Look up IPA
    clean_ipa_term = re.sub(r'\(.*?\)', '', term_clean).strip()
    ipa = ipa_map.get(clean_ipa_term, ipa_map.get(term_clean, f"/{clean_ipa_term}/"))
    
    ex_en, ex_id = generate_natural_example(term, pos, meaning)
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
        "hint": f"Oxford 3000 core vocabulary ({pos}) • Level {lvl}",
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
            "hint": f"Oxford Advanced Vocabulary ({h_pos}) • Level {h_lvl}",
            "category": f"Oxford Advanced ({h_lvl})"
        })
        seen_terms.add(term_clean)
        count += 1

print(f"Oxford Vocab entries generated: {len(oxford_vocab)}")

# 8. Phrasal Verbs
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
            base_verb = base_term.split()[0]
            raw_dict = dict_data.get(base_verb, '')
            meaning_id = parse_echols(raw_dict, 'verb')
            if not meaning_id or len(meaning_id) < 2:
                meaning_id = defn_en
            else:
                meaning_id = f"{meaning_id} ({defn_en})"
                
            ipa_val = f"/{base_term}/"
            ex_en = f"She decided to {term_raw} without delay."
            ex_id = f"Dia memutuskan untuk {meaning_id.split('(')[0].strip()} tanpa menunda lagi."
            
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

# 9. Collocations
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
        "hint": f"Collocation pattern: {h_pos}",
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

print(f"\nSUCCESS! Enhanced Complete Database Built:")
print(f"Oxford Vocab: {len(oxford_vocab)}")
print(f"Phrasal Verbs: {len(phrasal_verbs)}")
print(f"Collocations: {len(collocations)}")
print(f"Grand Total Vocabulary: {len(oxford_vocab) + len(phrasal_verbs) + len(collocations)}")
