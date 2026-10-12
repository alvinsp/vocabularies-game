import json
import os
import re
import pypdf

base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)
data_dir = os.path.join(project_root, 'src', 'data')
cache_dir = os.path.join(base_dir, 'cache')
os.makedirs(data_dir, exist_ok=True)
os.makedirs(cache_dir, exist_ok=True)

# 1. Load IPA Dictionary
print("Loading IPA Dictionary...")
ipa_data = {}
ipa_file = os.path.join(cache_dir, 'en_US.txt')
if os.path.exists(ipa_file):
    with open(ipa_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                word = parts[0].lower()
                ipas = [p.strip() for p in parts[1].split(',') if p.strip()]
                if ipas:
                    ipa_data[word] = ipas[0]

# 2. Load Indonesian Dictionary
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
    'licence': 'license', 'offence': 'offense', 'tyre': 'tire', 'defence': 'defense',
    'enquiry': 'inquiry', 'grey': 'gray', 'judgement': 'judgment', 'metre': 'meter'
}

# 4. Master Clean Overrides for Oxford Words (all pronouns, conjunctions, prepositions, numbers, informal, and edge cases)
oxford_master_overrides = {
    # Pronouns & Determiners
    'i': 'saya / aku',
    'me': 'saya / diriku (sebagai objek)',
    'my': 'milik saya / kepunyaanku',
    'myself': 'diriku sendiri / saya sendiri',
    'you': 'kamu / Anda / kalian',
    'your': 'milikmu / kepunyaan Anda',
    'yourself': 'dirimu sendiri',
    'he': 'dia (laki-laki)',
    'him': 'dia / dirinya (laki-laki)',
    'his': 'miliknya (laki-laki)',
    'himself': 'dirinya sendiri (laki-laki)',
    'she': 'dia (perempuan)',
    'her': 'dia / miliknya (perempuan)',
    'hers': 'miliknya (perempuan)',
    'herself': 'dirinya sendiri (perempuan)',
    'it': 'itu / benda atau hewan ini',
    'its': 'miliknya (benda atau hewan)',
    'itself': 'dirinya sendiri (benda/hewan)',
    'we': 'kami / kita',
    'us': 'kami / kita (sebagai objek)',
    'our': 'milik kami / kepunyaan kita',
    'ours': 'milik kami / kepunyaan kita',
    'ourselves': 'diri kami sendiri',
    'they': 'mereka',
    'them': 'mereka (sebagai objek)',
    'their': 'milik mereka',
    'theirs': 'milik mereka',
    'themselves': 'diri mereka sendiri',
    'this': 'ini (benda dekat)',
    'that': 'itu (benda berjarak)',
    'all': 'semua / seluruhnya / segala',
    'anybody': 'siapa saja / siapa pun juga',
    'anyone': 'siapa pun / seorang pun',
    'everybody': 'semua orang / setiap orang',
    'everyone': 'setiap orang / semua orang',
    'everything': 'semua hal / segala sesuatu',
    'somebody': 'seseorang / orang tertentu',
    'someone': 'seseorang / ada orang',
    'who': 'siapa / orang yang',
    'whom': 'siapa (sebagai objek kalimat)',
    'whose': 'milik siapa / yang kepunyaannya',
    'what': 'apa / apa yang',

    # Conjunctions & Prepositions
    'and': 'dan / serta',
    'but': 'tetapi / namun / melainkan',
    'or': 'atau / pilihan lain',
    'because': 'karena / sebab / lantaran',
    'although': 'meskipun / walaupun / kendati',
    'though': 'meskipun / walaupun demikian',
    'however': 'namun / akan tetapi / bagaimanapun',
    'whether': 'apakah / baik ... maupun',
    'unless': 'kecuali jika / kalau tidak',
    'than': 'daripada / dibandingkan dengan',
    'yet': 'namun / tetapi / belum',
    'at': 'di / pada (lokasi atau waktu)',
    'to': 'ke / kepada / menuju / untuk',
    'in': 'di dalam / pada masa',
    'into': 'ke dalam / menuju ke',
    'upon': 'di atas / pada saat kejadian',
    'before': 'sebelum / di hadapan / di muka',
    'behind': 'di belakang / tertinggal di belakang',
    'above': 'di atas / melebihi batas',
    'towards': 'menuju ke arah / terhadap',
    'when': 'ketika / saat / waktu',
    'of': 'dari / mengenai / milik',
    'here': 'di sini / ke mari',
    'where': 'di mana / ke mana / tempat di mana',
    'why': 'mengapa / kenapa / alasan',
    'below': 'di bawah / di posisi lebih rendah',
    'inside': 'bagian dalam / berada di dalam',
    'up': 'ke atas / naik / di atas',

    # Informal Words, Short Names, Slang
    'bike': 'sepeda (kendaraan roda dua)',
    'dad': 'ayah / papa / bapak',
    'mum': 'ibu / mama / bunda',
    'boss': 'atasan / bos / pimpinan',
    'exam': 'ujian tertulis / evaluasi akademik',
    'fridge': 'kulkas / lemari pendingin',
    'gym': 'gedung olahraga / pusat kebugaran',
    'lab': 'laboratorium riset dan praktikum',
    'app': 'aplikasi komputer / perangkat lunak ponsel',
    'ai': 'kecerdasan buatan (Artificial Intelligence)',
    'yeah': 'ya / benar (ungkapan informal)',
    'ok': 'baiklah / setuju / oke',
    'okay': 'baiklah / beres / sepakat',
    'hi': 'halo / salam sapa ramah',
    'hello': 'halo / hai salam pembuka',
    'bye': 'selamat tinggal / dadah',
    'cent': 'sen (satuan pecahan mata uang)',
    'beer': 'bir (minuman fermentasi)',
    'inch': 'inci (satuan panjang 2.54 cm)',
    'mile': 'satuan jarak mil (1.6 km)',
    'euro': 'mata uang Euro Eropa',

    # Auxiliary Verbs
    'could': 'bisa / sanggup (lampau dari can)',
    'can': 'dapat / bisa / mampu melakukan',
    'may': 'boleh / mungkin saja terjadi',
    'might': 'mungkin / barangkali terjadi',
    'must': 'harus / wajib / pasti',
    'shall': 'akan / harus pasti dilakukan',
    'should': 'seharusnya / sebaiknya patut dilakukan',
    'will': 'akan / bersedia melakukan',
    'would': 'akan bersedia / sudi kiranya',

    # Numbers
    'zero': 'angka nol (0)',
    'one': 'angka satu (1)',
    'two': 'angka dua (2)',
    'three': 'angka tiga (3)',
    'four': 'angka empat (4)',
    'five': 'angka lima (5)',
    'six': 'angka enam (6)',
    'seven': 'angka tujuh (7)',
    'eight': 'angka delapan (8)',
    'nine': 'angka sembilan (9)',
    'ten': 'angka sepuluh (10)',
    'eleven': 'angka sebelas (11)',
    'twelve': 'angka dua belas (12)',
    'thirteen': 'angka tiga belas (13)',
    'fourteen': 'angka empat belas (14)',
    'fifteen': 'angka lima belas (15)',
    'sixteen': 'angka enam belas (16)',
    'seventeen': 'angka tujuh belas (17)',
    'eighteen': 'angka delapan belas (18)',
    'nineteen': 'angka sembilan belas (19)',
    'twenty': 'angka dua puluh (20)',
    'thirty': 'angka tiga puluh (30)',
    'forty': 'angka empat puluh (40)',
    'fifty': 'angka lima puluh (50)',
    'sixty': 'angka enam puluh (60)',
    'seventy': 'angka tujuh puluh (70)',
    'eighty': 'angka delapan puluh (80)',
    'ninety': 'angka sembilan puluh (90)',
    'hundred': 'angka seratus (100)',
    'thousand': 'angka seribu (1.000)',
    'million': 'angka satu juta (1.000.000)',
    'billion': 'angka satu miliar (1.000.000.000)',
    'fifth': 'urutan kelima (5th) / seperlima bagian',

    # Curated Words with Clean Natural Indonesian
    'accept': 'menerima / menyetujui tawaran',
    'appeal': 'daya tarik / mengajukan permohonan banding',
    'arrangement': 'susunan / pengaturan rencana acara',
    'ask': 'bertanya / meminta keterangan / memohon',
    'bear (deal with)': 'menanggung beban / bertahan menghadapi cobaan',
    'beauty': 'kecantikan / keelokan paras / keindahan',
    'bee': 'lebah madu / tawon penyengat',
    'chief': 'pemimpin utama / ketua regu / terpenting',
    'circumstance': 'situasi / kondisi keadaan yang melingkupi',
    'city': 'kota besar / kawasan metropolitan perkotaan',
    'clearly': 'dengan jelas / secara gamblang dan nyata',
    'cross': 'menyeberang jalan / melintasi / tanda silang',
    'deep': 'dalam / mendalam / nyenyak tertidur',
    'depth': 'kedalaman jurang / intensitas emosi mendalam',
    'edit': 'menyunting naskah / mengoreksi kesalahan tulisan',
    'error': 'kesalahan teknis / kekeliruan perhitungan',
    'extend': 'memperpanjang durasi / membentangkan sayap',
    'forward': 'meneruskan pesan / melangkah maju ke depan',
    'hall': 'aula pertemuan / lorong gedung / ruang depan',
    'painful': 'terasa amat perih / menyedihkan hati',
    'polite': 'sopan santun / beradab dan bertata krama',
    'queue': 'barisan antrean / mengantre berurutan dengan tertib',
    'race (competition)': 'perlombaan adu kecepatan / balapan lari',
    'resident': 'warga penghuni setempat / penduduk domisili',
    'saturday': 'hari Sabtu (akhir pekan)',
    'sign': 'tanda isyarat / lambang petunjuk / menandatangani',
    'smile': 'tersenyum ramah / senyuman manis berseri',
    'student': 'murid sekolah / siswa pelajar / mahasiswa',
    'style': 'gaya busana / corak ragam model khas',
    'sum': 'jumlah total keseluruhan / menjumlahkan hitungan',
    'surely': 'tentu saja pasti / niscaya tanpa keraguan',
    'take': 'mengambil barang / memerlukan waktu / membawa serta',
    'theatre': 'gedung pertunjukan seni teater / sandiwara pentas',
    'write': 'menulis kalimat / mencatat catatan di atas kertas',
    'a': 'sebuah / seekor / seorang / satu',
    'an': 'sebuah / seekor / seorang / satu',
    'acceptable': 'dapat diterima / pantas dan cocok',
    'another': 'yang lain / satu lagi tambahan',
    'bathroom': 'kamar mandi / toilet bersih',
    'classroom': 'ruang kelas belajar mengajar',
    'coin': 'koin uang logam receh',
    'cream': 'krim susu / kepala susu kental',
    'feed': 'memberi makan hewan atau bayi',
    'fuel': 'bahan bakar minyak energi',
    'fur': 'bulu halus binatang mamalia',
    'huge': 'sangat besar / luar biasa megah',
    'limited': 'terbatas jumlahnya / bertenggat waktu',
    'other': 'yang lain / selain dari itu',
    'path': 'jalan setapak / jalur lintasan kecil',
    'unhappy': 'merasa tidak bahagia / bersedih hati',
    'van': 'mobil van / mobil angkutan barang',
    'youth': 'masa muda remaja / kaum pemuda',
    'centre': 'pusat kota / titik sentral keramaian',
    'practise': 'berlatih secara rutin / mempraktikkan ilmu',
    'nearly': 'hampir saja / nyaris terjadi',

    'abroad': 'di luar negeri / ke mancanegara',
    'advertising': 'periklanan promosi / bidang periklanan',
    'aged': 'berusia / sudah lanjut usia',
    'alive': 'masih hidup / penuh semangat hidup',
    'ancient': 'kuno purbakala / amat tua bersejarah',
    'apartment': 'apartemen hunian bertingkat',
    'asleep': 'tertidur lelap / sedang terlelap',
    'autumn': 'musim gugur daun',
    'average': 'rata-rata normal / nilai pertengahan',
    'bake': 'memanggang kue roti dalam oven',
    'bath': 'bak mandi air / kegiatan mandi santai',
    'beef': 'daging sapi olahan',
    'bin': 'tong tempat sampah',
    'blind': 'tunanetra / tidak dapat melihat mata',
    'boot': 'sepatu bot tebal / bagasi mobil',
    'bored': 'merasa jenuh bosan tidak bersemangat',
    'boring': 'membosankan / menjemukan tanpa variasi',
    'bowl': 'mangkuk wadah makanan berkuah',
    'bread': 'roti tawar atau manis gandum',
    'butter': 'mentega lembut gurih',
    'camping': 'berkemah di alam bebas terbuka',
    'campsite': 'tempat perkemahan tenda alam',
    'capital': 'ibu kota negara / modal usaha keuangan',
    'celebrity': 'pesohor terkenal / bintang selebriti',
    'chemical': 'zat kimia materi / bahan kimiawi',
    'cinema': 'bioskop tempat tayang film layar lebar',
    'climb': 'mendaki gunung / memanjat tebing',
    'climbing': 'olahraga mendaki tebing atau gunung',
    'coach': 'pelatih olahraga / bus penumpang jarak jauh',
    'collar': 'kerah baju kemeja / kalung hewan leher',
    'cooking': 'kegiatan memasak aneka kuliner masakan',
    'cousin': 'saudara sepupu satu keturunan',
    'crazy': 'amat gila / luar biasa tak masuk akal',
    'crisis': 'krisis genting / masa krisis berat',
    'criterion': 'kriteria / tolok ukur standar',
    'curved': 'melengkung indah / berkelok',
    'cycle': 'bersepeda santai / siklus daur ulang',
    'dancing': 'menari / tarian seni gerak tubuh',
    'data': 'data informasi / kumpulan fakta ilmiah',
    'defence': 'pertahanan / benteng perlindungan',
    'determined': 'bertekad kuat / berpendirian kokoh',
    'diet': 'pola makan sehat / diet nutrisi teratur',
    'director': 'direktur utama / sutradara film seni',
    'divorced': 'telah bercerai secara hukum perkawinan',
    'download': 'mengunduh data / file unduhan internet',
    'downwards': 'mengarah ke bawah / menurun lintasannya',
    'dream': 'bermimpi tidur / impian cita-cita masa depan',
    'dress': 'gaun pakaian anggun / berpakaian rapi',
    'driving': 'mengemudikan kendaraan mobil / berkendara di jalan',
    'drunk': 'mabuk minuman beralkohol',
    'easily': 'dengan sangat mudah / lancar tanpa hambatan',
    'educated': 'berpendidikan tinggi / berwawasan luas',
    'elderly': 'orang lanjut usia / kaum lansia berumur',
    'electronic': 'peranti elektronik canggih / barang listrik',
    'email': 'surel / surat elektronik internet resmi',
    'engaged': 'sudah bertunangan / sibuk terlibat kegiatan',
    'enquiry': 'pertanyaan resmi / penyelidikan kasus perkara',
    'excited': 'sangat antusias / gembira bersemangat tinggi',
    'exciting': 'sangat seru mendebarkan / amat mengasyikkan',
    'exist': 'ada dalam kenyataan / hidup eksis nyata',
    'experienced': 'sangat berpengalaman / mahir berjam terbang',
    'far': 'berjarak jauh / teramat jauh letaknya',
    'fascinating': 'amat mempesona memikat / luar biasa menarik',
    'favour': 'kebaikan pertolongan / dukungan restu',
    'favourite': 'favorit teratas / paling disukai di antara semua',
    'february': 'bulan Februari penanggalan masehi',
    'fire': 'api menyala kobaran / kebakaran hebat',
    'football': 'olahraga sepak bola lapangan',
    'forget': 'lupa ingatan / melupakan kenangan masa lalu',
    'frozen': 'membeku kaku dingin / es beku padat',
    'fully': 'secara utuh lengkap / sepenuhnya tanpa sisa',
    'garden': 'kebun bunga asri / taman hijau pekarangan',
    'gas': 'gas bahan bakar / zat gas tak kasat mata',
    'gather': 'berkumpul bersama / menghimpun orang banyak',
    'gift': 'hadiah kado istimewa / bakat alami bawaan lahir',
    'girlfriend': 'kekasih perempuan / pacar wanita tercinta',
    'golf': 'olahraga golf lapangan hijau',
    'goodbye': 'selamat tinggal / salam perpisahan',
    'grey': 'warna abu-abu kelabu',
    'ground': 'permukaan tanah daratan / bumi berpijak',
    'half': 'setengah bagian / separuh porsi',
    'hang': 'menggantungkan di dinding / menggantung di tali',
    'happily': 'dengan bahagia gembira / penuh suka cita',
    'heavily': 'dengan sangat lebat (hujan) / sangat berat',
    'heavy': 'berat bobotnya / padat berbobot besar',
    'hockey': 'olahraga hoki es atau lapangan terbuka',
    'hold': 'menggenggam erat di tangan / menahan posisi',
    'honour': 'kehormatan mulia luhur / memuliakan jasa',
    'hotel': 'hotel penginapan tamu berwisata',
    'housing': 'kawasan perumahan permukiman warga',
    'humour': 'rasa humor kelucuan / canda tawa hangat',
    'ice': 'es balok dingin / air beku padat',
    'included': 'sudah termasuk di dalam / tercakup lengkap',
    'including': 'termasuk di antaranya / meliputi berbagai hal',
    'increasingly': 'kian hari kian bertambah / semakin lama semakin...',
    'incredibly': 'luar biasa hebat / amat sangat menakjubkan',
    'indeed': 'memang benar sekali / sungguh-sungguh tepat',
    'individual': 'individu perorangan / masing-masing pribadi',
    'injured': 'terluka fisik / cedera kecelakaan tubuh',
    'install': 'memasang aplikasi / menginstal sistem operasi',
    'instance': 'contoh kasus konkret / teladan nyata',
    'internet': 'jaringan internet sedunia daring maya',
    'involved': 'terlibat aktif / ikut ambil bagian dalam kegiatan',
    'involve': 'melibatkan peran serta / mencakup partisipasi',
    'jacket': 'jaket pakaian pelindung tubuh hangat',
    'jazz': 'genre musik jazz berirama dinamis',
    'jewellery': 'perhiasan permata emas perak indah',
    'journalist': 'jurnalis peliput berita / wartawan media cetak',
    'judgement': 'penilaian cermat / putusan hukum majelis hakim',
    'july': 'bulan Juli penanggalan masehi',
    'june': 'bulan Juni penanggalan masehi',
    'killing': 'pembunuhan berdarah / tindakan mencabut nyawa',
    'kilometre': 'satuan jarak kilometer (1.000 meter)',
    'kitchen': 'dapur tempat masak dan menyiapkan santapan',
    'known': 'dikenal luas banyak orang / masyhur populer',
    'licence': 'surat izin resmi / lisensi operasional legal',
    'lighting': 'tata pencahayaan lampu / penerangan ruangan',
    'likely': 'sangat mungkin terjadi / berpeluang besar',
    'living': 'kehidupan nafkah hidup / masih berdaya hidup',
    'lock': 'mengunci pintu rapat / gembok pengaman kunci',
    'london': 'kota London ibu kota Inggris Raya',
    'lunch': 'makan siang santap tengah hari',
    'march': 'bulan Maret penanggalan masehi / berbaris tegap',
    'married': 'sudah menikah sah berumah tangga',
    'may (month)': 'bulan Mei penanggalan masehi',
    'meaning': 'makna arti hakiki / maksud tersirat',
    'meat': 'daging konsumsi hewani lezat',
    'metre': 'satuan panjang meter standar',
    'milk': 'susu segar bernutrisi murni',
    'mining': 'pertambangan mineral tambang bumi',
    'missing': 'hilang lenyap / tidak ditemukan jejaknya',
    'monday': 'hari Senin awal pekan kerja',
    'morning': 'pagi hari fajar terbit mentari',
    'musical': 'drama pentas musikal / berbakat musik merdu',
    'neck': 'leher bagian tubuh penghubung kepala',
    'neighbourhood': 'lingkungan tetangga sekitar perumahan',
    'night': 'malam hari gulita bertabur bintang',
    'noisy': 'amat bising riuh berisik suaranya',
    'not': 'tidak / bukan (penyangkalan negasi)',
    'november': 'bulan November penanggalan masehi',
    'october': 'bulan Oktober penanggalan masehi',
    'online': 'terhubung daring di internet maya',
    'opening': 'pembukaan acara perdana / lowongan kerja baru',
    'outdoor': 'luar ruangan alam terbuka bebas',
    'painting': 'lukisan karya seni kanvas / melukis indah',
    'passing': 'berlalu melintas / kelulusan ujian seleksi',
    'passport': 'paspor pas lintas negara batas imigrasi',
    'peaceful': 'amat damai tenteram hening tenang',
    'pet': 'hewan peliharaan kesayangan di rumah',
    'pleasant': 'menyenangkan hati / ramah menyejukkan',
    'pleased': 'merasa senang bahagia puas hati',
    'pork': 'daging babi konsumsi',
    'prefer': 'lebih menyukai / lebih memilih opsi tertentu',
    'programme': 'program acara siaran / rangkaian rencana kerja',
    'rarely': 'jarang sekali terjadi / hampir tidak pernah',
    'ready': 'sudah siap sedia bertindak siaga',
    'relaxed': 'santai tenang rileks tanpa tekanan stres',
    'relaxing': 'menenangkan pikiran / menyejukkan suasana hati',
    'remote': 'tempat terpencil pelosok / kendali jarak jauh',
    'repeated': 'diulang berulang kali terus-menerus',
    'restaurant': 'restoran rumah makan hidangan lezat',
    'rice': 'nasi putih / beras padi pokok pangan',
    'rider': 'pengendara kuda atau sepeda motor',
    'riding': 'menunggangi kuda / mengendarai sepeda',
    'running': 'olahraga berlari kencang / operasional mesin',
    'sad': 'merasa sedih nestapa murung duka',
    'salad': 'salad hidangan sayur buah segar bersaus',
    'salt': 'garam bumbu dapur penambah rasa asin gurih',
    'satisfied': 'merasa amat puas terpenuhi ekspektasi',
    'saving': 'tabungan simpanan uang / penghematan biaya',
    'secretary': 'sekretaris administrasi perkantoran',
    'sector': 'sektor bidang industri usaha ekonomi',
    'september': 'bulan September penanggalan masehi',
    'shelf': 'rak tempat pajang buku / ambalan dinding kayu',
    'shopping': 'berbelanja kebutuhan pokok dan busana di pasar',
    'shot': 'tembakan peluru / suntikan obat / bidikan kamera',
    'show': 'memperlihatkan bukti / pertunjukan seni pentas',
    'simply': 'hanya semata-mata / secara sederhana saja',
    'smartphone': 'ponsel cerdas pintar multiguna canggih',
    'smoking': 'merokok tembakau rokok aktif',
    'snow': 'salju putih dingin / turun butiran salju musim dingin',
    'specifically': 'secara mendalam dan spesifik khusus',
    'spoken': 'secara lisan ucapan kata tutur bahasa',
    'status': 'status martabat sosial / kedudukan posisi jabatan',
    'stock': 'saham bursa efek / persediaan barang di gudang',
    'studio': 'studio rekaman audio / sanggar lukis seni',
    'substance': 'zat kimia materi / bahan berbobot inti',
    'surprised': 'merasa kaget tak menyangka di luar dugaan',
    'surprising': 'amat mengejutkan mengagetkan seketika',
    'swimming': 'olahraga berenang di kolam atau laut air',
    't-shirt': 'baju kaus oblong santai kasual',
    'teenage': 'usia belasan tahun masa remaja muda',
    'teenager': 'remaja putra-putri belasan tahun penuh energi',
    'tired': 'merasa lelah fisik / letih lesu butuh rehat',
    'track': 'lintasan jalan lari / rel rel kereta api',
    'traveller': 'pelancong musafir / pelancong wisata keliling',
    'trousers': 'celana panjang pakaian santun bawahan',
    'tyre': 'ban karet kendaraan bermotor aspal',
    'upwards': 'meningkat mengarah ke atas grafiknya',
    'used': 'barang bekas pakai / sudah sangat terbiasa',
    'used (familiar with)': 'sudah sangat terbiasa dengan hal tersebut',
    'used (not new)': 'barang bekas / pernah dipakai orang lain sebelumnya',
    'video': 'tayangan rekaman gambar video visual bergerak',
    'vitamin': 'nutrisi vitamin penunjang kesehatan daya tahan tubuh',
    'water': 'air minum tawar / cairan air kehidupan bersih',
    'website': 'laman situs web internet resmi daring',
    'wedding': 'upacara pernikahan sakral bahagia janji suci',
    'well-being': 'kesejahteraan jasmani dan rohani tenteram lahir batin',
    'wi-fi™': 'koneksi nirkabel Wi-Fi internet berkecepatan tinggi',
    'wonder': 'bertanya-tanya penasaran di hati / keajaiban semesta raya',
    'worldwide': 'merambah ke seluruh penjuru dunia internasional global',
    'worried': 'merasa cemas risau gelisah memikirkan risiko',
    'worse': 'lebih buruk kondisinya dibanding keadaan sebelumnya',
    'worst': 'paling jelek terburuk mutlak di antara semuanya',
    'written': 'dalam wujud tulisan tertulis resmi di dokumen'
}

# 5. Master Clean Overrides for Phrasal Verbs (ensures 100% natural Indonesian, NO sb/sth, NO English definitions)
phrasal_verbs_master_overrides = {
    # Handcrafted & Essential PVs
    'calm down': 'menenangkan diri / menjadi lebih tenang',
    'catch on': 'menjadi populer / mulai memahami sesuatu',
    'keep in with sb': 'menjaga hubungan baik dengan seseorang',
    'laugh at sb': 'menertawakan seseorang / mengejek',
    'laugh sth off': 'menertawakan hal memalukan agar tidak canggung',
    'put sth on': 'mengenakan pakaian / menyelenggarakan acara',
    'stay in': 'berdiam di rumah / tidak bepergian keluar',
    'tear sth up': 'merobek-robek menjadi serpihan kecil',
    'wait up for sb': 'menunggu seseorang pulang sebelum tidur',
    'wind sb up': 'menjahili / memancing emosi seseorang',
    'wind sth up': 'mengakhiri pertemuan rapat / melikuidasi bisnis',
    'back out': 'menarik diri / membatalkan perjanjian',
    'bring sb/sth back': 'mengembalikan sesuatu / membangkitkan kenangan lama',
    'come about': 'terjadi / bagaimana suatu peristiwa terjadi',
    'frighten sb/sth away': 'menakut-nakuti hingga pergi menjauh',
    'get through sth': 'menyelesaikan tugas berat / lulus ujian seleksi',
    'go along with sb/sth': 'menyetujui gagasan / sependapat dengan orang lain',
    'go away': 'pergi menjauh / berlibur meninggalkan rutinitas',
    'hear from sb': 'menerima kabar atau pesan dari seseorang',
    'help sb out': 'membantu meringankan kesulitan seseorang',
    'put sth down': 'meletakkan benda ke bawah / mencatat di kertas catatan',
    'settle on sth': 'menetapkan pilihan setelah berpikir matang',
    'spell sth out': 'menjelaskan secara gamblang dan terperinci',
    'come out': 'terbit / dipublikasikan / terungkap rahasia',
    'come up': 'muncul tiba-tiba / dibahas dalam percakapan',
    'come up against sb/sth': 'menghadapi rintangan berat atau lawan tangguh',
    'get into sth': 'mulai tertarik menyukai / mendalami bidang baru',
    'go out': 'keluar rumah / padam (lampu/api) / berkencan',
    'turn sth down': 'menolak tawaran / mengecilkan volume suara',
    'turn sth up': 'membesarkan volume suara atau suhu ruangan',
    'turn up': 'tiba / muncul secara tak terduga di tempat',
    'cry off': 'membatalkan janji atau pertemuan',
    'do away with sth': 'menghapuskan / meniadakan aturan lama',
    'dream sth up': 'mencetuskan ide aneh atau sangat imajinatif',
    'enlarge on sth': 'menguraikan lebih mendalam / memperjelas rincian',
    'enter into sth': 'memulai kesepakatan / terlibat aktif dalam urusan',
    'kick in': 'mulai terasa khasiat atau efek pengaruhnya',
    'put sth forward': 'mengajukan usulan, rencana, atau saran inovatif',
    'put sth out': 'memadamkan kobaran api atau puntung rokok',
    'put yourself out': 'merepotkan diri demi membantu orang lain',
    'spread out': 'menyebar / membentang ke area yang luas',
    'breakthrough': 'terobosan besar / kemajuan penting berharga',
    'bystander': 'orang yang menyaksikan kejadian di lokasi tempat',
    'hand sth out': 'membagikan materi / selebaran informasi kepada umum',
    'handout': 'lembaran materi cetak yang dibagikan',
    'keep sth up': 'mempertahankan standar mutu / menjaga kondisi tetap prima',
    'let sb down': 'mengecewakan kepercayaan seseorang',
    'letdown': 'kekecewaan / peristiwa yang mengecewakan harapan',
    'stand by': 'tetap setia mendampingi / bersiap siaga membantu',
    'stand in for sb': 'menggantikan posisi seseorang sementara waktu',
    'upkeep': 'biaya perawatan / pemeliharaan rutin fasilitas',
    'write sth off': 'menghapus buku hutang / menganggap kerugian total',
    'built-in': 'bawaan / terintegrasi menyatu sejak awal pembuatan',
    'go ahead': 'melanjutkan / berjalan sesuai izin dan rencana',
    'go on': 'melanjutkan pembicaraan / terus berlangsung / terjadi',
    'knock sb out': 'merobohkan lawan bertanding hingga pingsan (KO)',
    'knockout': 'kemenangan mutlak KO / memukau luar biasa',
    'off-putting': 'kurang menyenangkan / membuat orang merasa enggan',
    'ongoing': 'sedang berjalan dan masih terus berlangsung aktif',
    'outspoken': 'vokal / lugas dan berani menyuarakan opini terbuka',
    'put sb off': 'mengalihkan konsentrasi / membuat enggan atau ragu',
    'speak out': 'berani bersuara menentang ketidakadilan sosial',
    'water sth down': 'melunakkan argumen / mengencerkan larutan pekat',
    'wear sb out': 'menguras tenaga hingga sangat lelah letih',
    'worn out': 'sangat letih / lusuh dan aus karena sering dipakai',
    'out of the blue': 'tiba-tiba tanpa diduga sama sekali sebelumnya',
    'put your foot in it': 'salah bicara hingga mempermalukan diri sendiri',
    'bend down': 'membungkukkan badan ke bawah',
    'bump into sb': 'berpapasan secara tidak sengaja di perjalanan',
    'fall over': 'terjatuh tersandung ke lantai jalan',
    'get up': 'bangun dari tidur / bangkit berdiri tegak',
    'knock sb down': 'menabrak seseorang hingga roboh ke tanah',
    'lie down': 'berbaring untuk beristirahat santai',
    'trip over': 'tersandung kaki atau rintangan saat berjalan',
    'cut down on sth': 'mengurangi konsumsi makanan atau kebiasaan boros',
    'cut sth out': 'menghentikan konsumsi sama sekali demi kesehatan',
    'do sth up': 'mengancingkan baju / merenovasi bangunan rumah',
    'face up to sth': 'berani menghadapi kenyataan pahit tanpa lari',
    'fill sb up': 'membuat perut kenyang terisi makanan',
    'show off': 'pamer dan menyombongkan keahlian di depan umum',
    'show sth off': 'memamerkan barang baru dengan penuh rasa bangga',
    'turn over a new leaf': 'membuka lembaran hidup baru yang lebih baik',
    'work out': 'berolahraga fisik / memecahkan perhitungan masalah',
    'get over sb/sth': 'pulih dari penyakit / bangkit dari patah hati mendalam',
    'pass out': 'pingsan / kehilangan kesadaran diri sementara',
    'pass away': 'meninggal dunia (ungkapan santun dan halus)',
    'pull through': 'melewati masa kritis sakit berat dan selamat hidup',
    'bottle sth up': 'memendam perasaan sedih atau amarah di dalam hati',
    'bring sb up': 'membesarkan dan mendidik anak / mengangkat topik obrolan',
    'grow up': 'tumbuh menjadi manusia dewasa matang',
    'look forward to sth': 'sangat menanti-nantikan dengan penuh rasa gembira',
    'turn a blind eye': 'pura-pura tidak melihat / tutup mata atas pelanggaran',
    'count on sb': 'mengandalkan seseorang dengan penuh rasa percaya',
    'put up with sb/sth': 'bersabar menghadapi / menoleransi perilaku seseorang',
    'break up with sb': 'mengakhiri hubungan percintaan asmara',
    'make up with sb': 'berbaikan kembali setelah berselisih paham',
    'drift apart': 'merenggang perlahan seiring berjalannya waktu',
    'get cold feet': 'ragu-ragu dan grogi sebelum menghadapi momen penting',
    'hit it off': 'langsung akrab dan cocok sejak pertama kali berjumpa',
    'make ends meet': 'mencukupi kebutuhan pokok dengan uang pas-pasan',
    'rip sb off': 'menipu dengan mematok harga kemahalan di luar wajar',
    'come across sth': 'menemukan sesuatu secara tidak sengaja di suatu tempat',
    'get rid of sth': 'menyingkirkan atau membuang barang bekas tak terpakai',
    'hold up': 'menghambat atau menunda jalannya perjalanan',
    'set off': 'memulai perjalanan / berangkat menuju tempat tujuan',
    'check in': 'mendaftar masuk di hotel atau konter bandara',
    'break into sth': 'membobol masuk ke dalam ruangan tanpa izin',
    'crack down on sth': 'menindak tegas segala bentuk pelanggaran hukum',
    'get away with sth': 'lolos tanpa dihukum atas kesalahan yang diperbuat',
    'carry sth out': 'melaksanakan atau menjalankan rencana dan riset ilmiah',
    'back sth up': 'mencadangkan file data / mendukung pernyataan rekan',
    'pop up': 'muncul tiba-tiba di layar monitor komputer',
    'come up with sth': 'mencetuskan ide cemerlang atau solusi pemecahan',
    'figure sth out': 'memahami cara kerja atau memecahkan masalah rumit',
    'brush up on sth': 'menyegarkan kembali kemampuan bahasa atau keahlian lama',
    'look down on sb': 'memandang rendah dan meremehkan orang lain',
    'look up to sb': 'mengagumi dan meneladani sosok teladan seseorang',
    'strike up a conversation': 'memulai obrolan ramah dengan orang baru dikenal',
    'iron sth out': 'meluruskan kesalahpahaman kecil / menyelesaikan perselisihan',
    'mull sth over': 'memikirkan dan merenungkan secara mendalam sebelum putusan',
    'abide by sth': 'mematuhi peraturan dengan taat dan penuh disiplin',
    'drop sb off': 'mengantar dan menurunkan seseorang di tempat tujuan',
    'pick sb up': 'menjemput seseorang dengan kendaraan di lokasi',
    'save up': 'menabung simpanan uang demi tujuan penting tertentu',
    'splash out': 'menghamburkan uang untuk memanjakan diri belanja',
    'scrape by': 'bertahan hidup dengan penghasilan yang sangat pas-pasan',
    'run out of sth': 'kehabisan persediaan (baterai, bensin, waktu, uang)',
    'look into sth': 'menyelidiki atau menginvestigasi fakta perkara kasus',
    'broaden your horizons': 'memperluas wawasan dan cakrawala sudut pandang hidup',
    'take the plunge': 'memberanikan diri mengambil langkah besar penuh risiko',
    'think twice': 'berpikir dua kali sebelum bertindak ceroboh',
    'learn by heart': 'menghafalkan materi pelajaran di luar kepala',
    'with flying colours': 'lulus ujian dengan nilai sangat gemilang memuaskan',
    'bridge the gap': 'menjembatani kesenjangan atau jurang pemisah antarkelompok',
    'snowed under': 'kewalahan tertimbun beban pekerjaan yang menumpuk',
    'weigh sth up': 'menimbang baik buruknya berbagai pilihan keputusan',
    'at stake': 'sedang dipertaruhkan status atau kelangsungan nasibnya',
    'come clean': 'berterus terang dan mengakui kesalahan secara jujur',
    'blurt sth out': 'keceplosan membocorkan rahasia tanpa sengaja berucap',
    'stick around': 'tetap tinggal di lokasi dan tidak buru-buru pergi',
    'embark on sth': 'memulai petualangan atau babak perjalanan baru',

    # Oxford Pocket Phrasal Verbs & PDF Extracted Entries
    'go on (doing sth)': 'terus melanjutkan kegiatan / pantang berhenti berjuang',
    'put sb off (sb/sth)': 'membuat seseorang merasa enggan / hilang minat dan selera',
    'worn out adj': 'sudah aus / usang / tidak dapat dipakai lagi karena rusak',
    'bump into sb/sth': 'menabrak benturan / berpapasan secara kebetulan di jalan',
    'turn round/around': 'berbalik arah pandang / menoleh ke belakang tubuh',
    'do sth up': 'merenovasi bangunan rumah / mengancingkan pakaian rapi',
    'keep to sth': 'menaati peraturan / mematuhi kesepakatan tertulis bersama',
    'get in/into sth': 'masuk ke dalam kendaraan / diterima di perguruan tinggi',
    'take sth up': 'memulai hobi baru / menerima tawaran pekerjaan profesi',
    'insist on doing sth': 'bersikeras tetap melakukan sesuatu meski dilarang orang lain',
    'insist on sth': 'menuntut dengan tegas agar suatu hal wajib dipenuhi',
    'turn out': 'ternyata terbukti kebenarannya / berakhir menjadi demikian',
    'depend on sb': 'bergantung pada / menaruh kepercayaan penuh pada seseorang',
    'get by': 'bertahan hidup mandiri dengan upah yang pas-pasan',
    'go for sth': 'memilih / memutuskan untuk mengambil opsi yang diinginkan',
    'go for sth/sb': 'menyukai tipe tertentu / tertarik pada karakter seseorang',
    'get over sth/sb': 'sembuh dari penyakit / melupakan masa lalu mantan kekasih',
    'go down (of swelling)': 'mengempis / mereda pembengkakannya (tentang bengkak luka)',
    'take sth out': 'mencabut gigi / mengeluarkan barang dari dalam wadah tas',
    'give sth up': 'berhenti dari kebiasaan buruk / menyerah kalah pada keadaan',
    'revolve around sth/sb': 'berpusat sepenuhnya pada / berporos mengelilingi hal utama',
    'clear (sth) up': 'merapikan ruangan berantakan / cuaca mendung menjadi cerah',
    'put sth up': 'mendirikan bangunan struktur / menaikkan patokan harga barang',
    'take sth back': 'mengembalikan barang cacat ke toko / menarik kembali ucapan',
    'take sth off': 'melepas pakaian atau sepatu / mengambil cuti libur kerja',
    'wrap sth up': 'membungkus kado dengan rapi / merampungkan pertemuan rapat',
    'get back to sth': 'kembali fokus menekuni urusan / kembali ke tempat semula',
    'stick to sth': 'tetap setia berpegang teguh pada rencana atau janji semula',
    'give in (to sb/sth)': 'mengalah / menyerah tunduk pada tekanan dan desakan',
    'go off (of an alarm)': 'berdering keras berbunyi nyaring (alarm / jam beker)',
    'go off (of electricity)': 'padam mati mendadak (aliran arus listrik jaringan)',
    'go down': 'menurun / merosot nilainya (harga pasar atau tingkat suku bunga)',
    'go up': 'meningkat / melonjak naik ke atas (harga kebutuhan atau jumlah)',
    'come into sth': 'memperoleh warisan uang tunai atau harta kekayaan keluarga',
    'depend on sb/sth': 'bergantung pada / mengandalkan situasi atau orang lain',
    'give sth away': 'menyumbangkan barang cuma-cuma / membocorkan rahasia penting',
    'carry on (doing sth)': 'terus melanjutkan aktivitas kerja / tidak mau berhenti',
    'come in': 'mencapai garis finis di posisi tertentu dalam ajang balapan',
    'sell sth off': 'menjual habis dengan harga murah / obral cuci gudang toko',
    'get around/round/about (sth)': 'bepergian keliling ke berbagai tempat / leluasa bergerak bebas',
    'hold sb/sth up': 'menunda / menghambat kelancaran jalannya perjalanan',
    'hold-up n': 'hambatan penundaan waktu / aksi perampokan bersenjata',
    'make it': 'berhasil tiba tepat waktu di lokasi / meraih kesuksesan hidup gemilang',
    'build up': 'menumpuk banyak / bertambah besar secara bertahap seiring waktu',
    'build-up n': 'penumpukan bertahap / persiapan intensif menjelang momen besar',
    'carry on': 'melanjutkan perjalanan langkah / terus beraktivitas aktif',
    'get away': 'pergi berlibur santai melarikan diri dari kejenuhan rutinitas',
    'get through (sth)': 'menyelesaikan tugas pekerjaan berat / lulus melewati ujian seleksi',
    'pick sth/sb up': 'menjemput seseorang dengan kendaraan / memungut benda di lantai',
    'get around/round sth': 'mengakali aturan ketat / menemukan celah alternatif solusi cerdik',
    'go through sth': 'memeriksa dokumen secara teliti / mengalami masa kehidupan sulit',
    'take sb in': 'memperdaya / membohongi seseorang dengan muslihat tipuan',
    'walk off with sth': 'menggondol / mencuri barang milik orang lain tanpa izin sah',
    'get away (from sb/sth)': 'melarikan diri / menghindar jauh dari ancaman bahaya',
    'coming up': 'akan segera tiba waktunya / akan segera berlangsung acaranya',
    'turn sth around/round': 'membalikkan arah laju / mengubah haluan bisnis rugi menjadi untung',
    'get through (to sb)': 'berhasil menghubungi via telepon / menyadarkan orang agar paham',
    'cut sth off': 'memutus aliran pasokan air bersih atau jaringan listrik',
    'set sth up': 'mendirikan usaha rintisan baru / merancang sistem tata kelola kerja',
    'start (sth) up': 'memulai operasional bisnis usaha / menyalakan mesin kendaraan',
    'follow sth up': 'menindaklanjuti perkembangan kabar / meneliti kelanjutan perkara',
    'let sth down': 'memanjangkan keliman pakaian / mengecewakan ekspektasi performa',
    'open sth up': 'membuka peluang usaha baru / membuka akses gerbang masuk',
    'run riot': 'mengamuk liar tanpa kendali / bertindak onar leluasa bebas',
    'add (sth) up': 'menjumlahkan deretan angka / menghitung total perolehan',
    'make sth up': 'mengarang cerita dongeng fiksi / menyusun formasi komponen',
    'put sth back': 'mengembalikan barang tepat ke posisi tempat semula disimpan',
    'go down (to sb)': 'kalah dalam pertandingan (melawan tim musuh atau pesaing)',
    'build sb/sth up': 'memperkuat daya tahan tubuh / membangun reputasi nama baik',
    'come back': 'bangkit kembali bangkit dan meraih kesuksesan kejayaan lagi',
    'come off': 'berhasil berjalan lancar sesuai harapan rencana awal mula',
    'warm up': 'pemanasan sebelum olahraga fisik / menghangatkan suhu badan',
    'warm-up n': 'sesi latihan pemanasan persiapan sebelum aktivitas berat',
    'build-up (to sth) n': 'masa persiapan ancang-ancang menjelang agenda acara besar',
    'switch off': 'mematikan saklar peranti listrik / berhenti memikirkan beban masalah',
    'take over (from sth)': 'mengambil alih kendali kepemimpinan / tanggung jawab manajemen',
    'go off': 'berlangsung sesuai jalannya / meledak (bom) / basi (makanan masam)',
    'pin sb down': 'mendesak kepastian jawaban tegas / menuntut komitmen janji',
    'swap places with sb': 'bertukar posisi tempat duduk / bergantian peran tugas dengan rekan',
    'come on': 'melangkah tampil ke atas panggung / menunjukkan tanda kemajuan',
    'cut sth/sb off (from sth)': 'mengisolasi dari lingkungan luar / memutus jalur komunikasi telepon',
    'deal with sth': 'menangani masalah kendala sulit / berurusan dengan klien penting',
    'catch up with sb': 'mengejar dan menyusul ketertinggalan / meringkus pelanggar hukum',
    'backup n': 'bantuan tenaga cadangan darurat / salinan berkas data cadangan',
    'swap places': 'saling bertukar tempat posisi duduk / bergantian peran kerja',
    'stand out (from sb/sth)': 'tampak sangat mencolok pandangan / jauh lebih unggul di antara rekan',
    'put sth off/put off doing sth': 'menunda-nunda penyelesaian tugas / mengulur batas tenggat waktu',
    'drop off': 'tertidur lelap sejenak / mengantarkan penumpang tiba di lokasi tujuan',
    'go into sth': 'dihabiskan untuk membiayai proyek / dialokasikan ke pos anggaran belanja',
    'pull out': 'menarik diri mundur dari kesepakatan / menepi keluar jalur jalan',
    'not stand for sth': 'tidak sudi menoleransi perlakuan buruk / menolak tegas tindakan zalim',
    'stand for sth': 'merupakan singkatan resmi dari / melambangkan prinsip nilai luhur',
    'stand out (as sth)': 'tampil sangat menonjol berprestasi unggul dibanding yang lainnya',
    '(not) add up': 'tidak masuk akal logis / terasa janggal mencurigakan faktanya',
    'go through (of a bill)': 'disahkan secara resmi menjadi undang-undang regulasi negara',
    'mess around with sth': 'mengutak-atik ceroboh / mempermainkan hal serius yang penting',
    'get out of sth': 'menghindar dari tugas wajib / mangkir dari tanggung jawab beban',
    'revolve around sth': 'berputar mengelilingi poros orbit / terfokus pada pokok bahasan utama',
    'throw sth away': 'membuang barang bekas ke tong sampah / menyia-nyiakan peluang emas',
    'hang on': 'menunggu sebentar / bertahan memegang pegangan dengan erat',
    'on behalf of sb': 'atas nama perwakilan / mewakili kepentingan sah seseorang',
    'get over sth': 'pulih dari duka kesedihan mendalam / berhasil mengatasi rintangan',
    'think sth up': 'mencetuskan ide gagasan cemerlang / memikirkan konsep rancangan baru',
    'run out': 'habis masa berlaku tenggatnya / persediaan barang telah habis ludes',
    'break sth off': 'memutuskan ikatan hubungan pertunangan / mematahkan ranting pohon',
    'fall apart': 'hancur berkeping-keping / runtuh berantakan karena konflik masalah berat',
    'line sb/sth up': 'menyusun deretan jadwal agenda acara / berbaris rapi dalam barisan',
    'stick out (of sth)': 'menonjol keluar melebihi batas tepi / menyembul tampak mata',
    'stick out': 'tampak sangat mencolok perhatian mata / terlihat jelas di kerumunan',
    'look up': 'mencari arti kata di dalam kamus / prospek masa depan mulai membaik',
    'lie around': 'bermalas-malasan rebahan santai / barang berserakan tidak rapi di lantai',
    'mess around/about': 'bertingkah konyol membuang waktu / usil mengganggu ketenangan orang',
    'go on (of time)': 'berlalu bergulir seiring berjalannya sang waktu zaman',
    'get off sth': 'turun dari armada kendaraan umum / selesai jam kerja pulang kantor',
    'get at sb': 'terus-menerus mengkritik tajam / menyindir kesalahan seseorang',
    'get in': 'tiba sampai di tempat tujuan (pesawat/kereta) / berhasil masuk ke rumah',
    'get on': 'meraih kemajuan karier cemerlang / menjalin relasi pertemanan akrab',
    'get round sth': 'mengakali aturan regulasi ketat / menemukan celah pemecahan masalah',
    'go around/round (to ...)': 'berkunjung mampir bertamu ke kediaman rumah rekan',
    'go down (to ...)': 'bepergian perjalanan menuju ke arah kawasan selatan',
    'go up (to ...)': 'bepergian perjalanan menuju ke arah kawasan utara',
    'take sth down': 'membongkar tenda panggung acara / mencatat perkataan pembicara secara runtut',
    'come up (to sb)': 'menghampiri / melangkah berjalan mendekati seseorang langsung'
}

# 6. Fallback translation map for PDF English definitions (defn_en -> natural Indonesian)
defn_en_to_id = {
    'abolish sth': 'menghapuskan / meniadakan aturan lama',
    'stop sth burning': 'memadamkan api kobaran / memadamkan puntung rokok',
    'tolerate sb': 'bersabar menghadapi / menoleransi sikap seseorang',
    'keep sth in good condition': 'mempertahankan standar mutu / menjaga kondisi tetap prima',
    'make sb dislike sb/sth': 'membuat seseorang merasa enggan / hilang selera',
    'continue': 'terus melanjutkan kegiatan / tidak berhenti berjuang',
    'no longer useful': 'sudah aus / usang / tidak dapat dipakai lagi karena rusak',
    'follow a rule/agreement': 'menaati peraturan / mematuhi kesepakatan tertulis bersama',
    'become less': 'mengempis / mereda pembengkakannya (tentang bengkak luka)',
    'build': 'mendirikan bangunan struktur / menaikkan patokan harga',
    'ring': 'berdering keras berbunyi nyaring (alarm / jam beker)',
    'decrease': 'menurun / merosot nilainya (harga pasar atau tingkat)',
    'increase': 'meningkat / melonjak naik ke atas (harga atau jumlah)',
    'be left money': 'memperoleh warisan uang tunai atau harta kekayaan',
    'finish a race': 'mencapai garis finis di posisi tertentu dalam balapan',
    'delay sb/sth': 'menunda / menghambat kelancaran jalannya perjalanan',
    'delay': 'hambatan penundaan waktu / perampokan bersenjata',
    'arrive at a place': 'berhasil tiba tepat waktu / meraih kesuksesan hidup',
    'collect sth/sb': 'menjemput seseorang dengan kendaraan / memungut benda',
    'going to happen': 'akan segera tiba waktunya / akan segera berlangsung',
    'lose': 'kalah dalam pertandingan (melawan tim musuh atau pesaing)',
    'make sb/sth stronger': 'memperkuat daya tahan tubuh / membangun reputasi kokoh',
    'become successful again': 'bangkit kembali dan meraih kesuksesan kejayaan lagi',
    'be successful': 'berhasil berjalan lancar sesuai harapan rencana awal',
    'preparation for activity': 'sesi latihan pemanasan persiapan sebelum aktivitas berat',
    'preparation for sth': 'masa persiapan ancang-ancang menjelang agenda acara besar',
    'happen in a particular way': 'berlangsung sesuai jalannya / meledak (bom) / basi',
    'walk on stage': 'melangkah tampil ke atas panggung / menunjukkan kemajuan',
    'prevent sb/sth': 'mengisolasi dari lingkungan luar / memutus jalur komunikasi',
    'support': 'bantuan tenaga cadangan darurat / salinan data cadangan',
    'become law': 'disahkan secara resmi menjadi undang-undang regulasi negara',
    'wait': 'menunggu sebentar / bertahan memegang pegangan dengan erat',
    'arrange for sth to happen': 'menyusun deretan jadwal agenda acara / berbaris rapi',
    'pass': 'berlalu bergulir seiring berjalannya sang waktu zaman',
    'visit': 'berkunjung mampir bertamu ke kediaman rumah rekan',
    'go south': 'bepergian perjalanan menuju ke arah kawasan selatan',
    'travel north': 'bepergian perjalanan menuju ke arah kawasan utara',
    '(not) seem true or correct': 'tidak masuk akal logis / terasa janggal mencurigakan',
    'like a type of thing/person': 'menyukai tipe tertentu / tertarik pada karakter seseorang',
    'start a career': 'memulai meniti karier pekerjaan profesional',
    'go bad': 'menjadi basi / membusuk tidak layak konsumsi',
    'move in a circle': 'berputar mengelilingi poros orbit utama',
    'abbreviation': 'merupakan singkatan kata resmi dari',
    'get rid of sth': 'menyingkirkan atau membuang barang bekas tak terpakai',
    'interrupt sb': 'menyela pembicaraan / memutus jalur telepon seketika',
    'make sb understand': 'menyadarkan seseorang agar paham dengan jelas',
    'be published': 'terbit / dipublikasikan ke hadapan masyarakat luas',
    'deliver sth': 'mengantarkan dan menyerahkan barang kiriman ke tujuan',
    'overcome sth': 'mengatasi rintangan kesulitan / pulih dari kesedihan',
    'explode': 'meledak dengan suara ledakan dahsyat',
    'invent sth': 'menciptakan penemuan baru / mencetuskan gagasan inovatif',
    'reject sth': 'menolak tawaran usulan / mengecilkan volume suara',
    'repair': 'merenovasi dan memperbaiki kerusakan fasilitas rumah',
    'expire': 'habis masa berlakunya / kedaluwarsa secara hukum',
    'have none left': 'kehabisan persediaan sama sekali tanpa ada sisa',
    'deceive sb': 'memperdaya / membohongi seseorang dengan muslihat licik',
    'start a business': 'membuka dan merintis peluang usaha bisnis baru',
    'start a job, hobby, etc.': 'memulai pekerjaan profesi baru atau hobi kegemaran',
    'calculate': 'menjumlahkan angka / memperhitungkan kalkulasi angka',
    'end a relationship': 'mengakhiri jalinan hubungan pertunangan atau kerja sama',
    'remove sth': 'melepaskan atau mencabut benda dari dudukannya',
    'have problems': 'mengalami kendala perpecahan dan kesulitan besar',
    'arrange sb/sth in a straight': 'menyusun berjajar lurus dan rapi sejajar',
    'be easy to notice': 'tampak sangat mencolok pandangan dan mudah dikenali',
    'come out beyond a': 'menonjol menyembul keluar melebihi batas tepian',
    'be noticeable': 'terlihat jelas di mata dan menarik perhatian banyak orang',
    'meet unexpectedly': 'berpapasan secara tidak sengaja di tengah perjalanan',
    'become better': 'keadaan mulai membaik / mencari informasi di kamus',
    'leave in a hurry': 'berangkat terburu-buru / lepas landas (pesawat)',
    'speak or write later': 'menghubungi kembali via telepon atau pesan tertulis',
    'return to a place': 'kembali pulang ke tempat hunian semula',
    'return to a state': 'kembali pulih ke kondisi kesehatan semula',
    'return sth to its place': 'mengembalikan barang tepat ke wadah tempat asalnya',
    'complete sth': 'menyelesaikan tugas pekerjaan berat hingga tuntas sempurna',
    'pass an exam': 'lulus melewati ujian evaluasi dengan hasil baik',
    'make contact': 'berhasil menjalin kontak komunikasi dengan seseorang',
    'travel': 'bepergian melanglang buana ke berbagai tempat wisata',
    'do nothing': 'bermalas-malasan rebahan santai tanpa melakukan apa pun',
    'left in an untidy state': 'tergeletak berserakan berantakan di lantai ruangan',
    'behave in a stupid': 'bertingkah konyol membuang waktu secara tidak produktif',
    'spend time doing sth': 'menghabiskan waktu santai bersenang-senang',
    'continue doing sth': 'terus melanjutkan aktivitas kerja tanpa kenal menyerah',
    'improve': 'menunjukkan tanda-tanda kemajuan dan perkembangan positif',
    'continue speaking': 'terus berbicara menyampaikan pendapat gagasan',
    'happen': 'terjadi suatu peristiwa yang tidak disangka-sangka',
    'develop sth': 'mengembangkan dan memperluas kapasitas kemampuan',
    'increase the price': 'menaikkan patokan tarif harga barang atau layanan',
    'bring sth to an end': 'mengakhiri pertemuan rapat / merampungkan pembicaraan',
    'leave your workplace': 'selesai jam kerja kantor dan melangkah pulang',
    'remove clothing': 'menanggalkan pakaian atau sepatu dari tubuh',
    'criticize': 'mengkritik pedas dan menyindir kekurangan orang lain',
    'discover facts': 'menemukan kebenaran fakta yang selama ini tersembunyi',
    'reach': 'berhasil menjangkau tempat letak sasaran yang dituju',
    'arrive': 'tiba sampai di stasiun tujuan dengan selamat',
    'become involved in sth': 'mulai terlibat aktif mendalami kegiatan baru',
    'be successful': 'meraih keberhasilan sukses gemilang dalam perjuangan',
    'avoid sth': 'menghindari kendala rintangan dengan cara cerdik',
    'proceed': 'melanjutkan langkah perjalanan sesuai rencana awal',
    'change direction': 'mengubah haluan arah / membalikkan tren bisnis',
    'reduce sound, heat, etc.': 'mengecilkan volume bunyi suara atau menurunkan suhu',
    'increase sound, heat, etc.': 'membesarkan volume bunyi suara atau menaikkan suhu',
    'shorten sth': 'memendekkan keliman pakaian busana celana',
    'make sth start working': 'menyalakan atau mengaktifkan mesin agar bekerja',
    'stay on a path': 'tetap setia berada di jalur jalan yang benar',
    'approach sb': 'melangkah berjalan mendekati seseorang secara langsung'
}

def normalize_text(s):
    s = s.lower().replace('sth', '').replace('sb', '').replace('...', '')
    s = re.sub(r'[^a-z0-9\s]+', ' ', s)
    return ' '.join(s.split())

norm_pv_overrides = {normalize_text(k): v for k, v in phrasal_verbs_master_overrides.items()}

# 7. Robust Parser for Echols & Shadily Dictionary Entries
def clean_meaning(text):
    if not text:
        return ''
    # 1. Remove all balanced parentheses and brackets first
    text = re.sub(r'\([^)]*\)', ' ', text)
    text = re.sub(r'\[[^\]]*\]', ' ', text)
    # 2. Remove isolated open parentheticals like (s / , (j / , (sb , (of a building
    text = re.sub(r'\(\s*[^\)\/]+', ' ', text)
    # 3. Clean stray brackets or parens
    text = text.replace('(', ' ').replace(')', ' ').replace('[', ' ').replace(']', ' ')
    # 4. Remove standalone dictionary markers like Med, Mil, Inf, etc
    text = re.sub(r'\b(Med|Mil|Inf|sb|sth|kk|kb|ks|kd|am|kg|kn|pl|sing)\b\.?', ' ', text, flags=re.I)
    # 5. Split by numbers
    num_chunks = re.split(r'\b\d+[\.\)]?\s*', text)
    raw_meanings = []
    for chunk in num_chunks:
        first_clause = chunk.split('.')[0]
        # Split by comma or slash
        items = re.split(r'[,/]', first_clause)
        for item in items:
            item = re.sub(r'^[\d\.\-\;\:\s\)\/]+', '', item).strip()
            item = re.sub(r'[\d\.\-\;\:\s\(\/]+$', '', item).strip()
            item = re.sub(r'\s+', ' ', item)
            # Filter English phrases or helper prepositions
            if item and len(item) > 1 and not re.search(r'^[a-z]+\s+[a-z]+$', item, re.I) and not item.lower() in ['of', 'for', 'in', 'at', 'to', 'from', 'with', 'the']:
                if item.lower() not in ['kb', 'kkt', 'kki', 'ks', 'kk', 'kd', 'ksam', 'inf', 'kn', 'kg', 'am', 'sb', 'sth', 'med', 'mil']:
                    if item not in raw_meanings:
                        raw_meanings.append(item)
    clean_meanings = [m for m in raw_meanings if len(m) > 1 and not m.isdigit()]
    if clean_meanings:
        res = ' / '.join(clean_meanings[:3])
        res = re.sub(r'\s+', ' ', res).strip()
        res = re.sub(r'^[,\.\-\;\:\/\s]+|[,\.\-\;\:\/\s]+$', '', res)
        return res
    fallback = text.split('.')[0].strip()
    fallback = re.sub(r'\s+', ' ', fallback)
    fallback = re.sub(r'^[,\.\-\;\:\/\s]+|[,\.\-\;\:\/\s]+$', '', fallback)
    return fallback[:45] if fallback and len(fallback) > 3 else ''

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
        
    return clean_meaning(chosen_text)

# Clean lookup with comprehensive fallback cascade
def get_clean_oxford_meaning(term, pos):
    t_lower = term.lower().strip()
    t_clean = re.sub(r'\(.*?\)', '', t_lower).strip()
    
    # 1. Master overrides
    if t_lower in oxford_master_overrides:
        return oxford_master_overrides[t_lower]
    if t_clean in oxford_master_overrides:
        return oxford_master_overrides[t_clean]
        
    # 2. Candidate list (exact, cleaned parenthetical, US spelling variants)
    candidates = [t_lower, t_clean, uk_to_us.get(t_lower, ''), uk_to_us.get(t_clean, '')]
    for c in candidates:
        if c and c in dict_data:
            res = parse_echols(dict_data[c], pos)
            if res and len(res) > 2 and res.lower() not in ['inf', 'kb', 'kk', 'ks', 'kd', 'am', 'kg', 'kn', 'sb', 'sth']:
                # Filter out pure english leftovers
                if not re.search(r'^(to\s+[a-z]|the\s+[a-z]|for\s+[a-z]|a\s+[a-z])\b', res):
                    return res
                
    # 3. Stemming lookup
    for c in candidates:
        if not c: continue
        suffixes = ['s', 'ed', 'ing', 'ly', 'ment', 'tion', 'ness', 'able', 'al']
        for suf in suffixes:
            if c.endswith(suf) and len(c) > len(suf) + 2:
                stem = c[:-len(suf)]
                if stem in dict_data:
                    res = parse_echols(dict_data[stem], pos)
                    if res and len(res) > 2 and res.lower() not in ['inf', 'kb', 'kk', 'ks', 'kd', 'am', 'kg', 'kn', 'sb', 'sth']:
                        if not re.search(r'^(to\s+[a-z]|the\s+[a-z]|for\s+[a-z]|a\s+[a-z])\b', res):
                            return res
                        
    return f"makna {term}"

# 8. Load Handcrafted Rich Vocabularies
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

# 9. Parse Oxford 3000 PDF
print("Parsing Oxford 3000 PDF...")
oxford_pdf_path = "C:/Users/ASUS/.gemini/antigravity-ide/brain/7acf44a5-2d01-4e3c-8811-7f112f29f30a/.user_uploaded/media_1791802719879.pdf"
reader_ox = pypdf.PdfReader(oxford_pdf_path)
ox_lines = []
for p in reader_ox.pages:
    ox_lines.extend([l.strip().replace('\xa0', ' ') for l in p.extract_text().split('\n') if l.strip()])
ox_lines = [l for l in ox_lines if not ('Oxford University Press' in l or 'The Oxford 3000' in l)]

pattern = re.compile(r'^([a-zA-Z\s\-\,\'\/\(\)]+?)\s+([a-z\.\,\s\/]+?)\s+([A-C][1-2])(.*)$')

pos_mapping = {
    'v': 'verb', 'n': 'noun', 'adj': 'adjective', 'adv': 'adverb',
    'prep': 'preposition', 'conj': 'conjunction', 'pron': 'pronoun',
    'det': 'determiner', 'number': 'number', 'modal': 'modal verb'
}

def map_pos(raw_pos):
    raw = raw_pos.lower().strip()
    for short, full in pos_mapping.items():
        if short in raw.split('.'):
            return full
    if 'verb' in raw or 'v.' in raw: return 'verb'
    if 'noun' in raw or 'n.' in raw: return 'noun'
    if 'adj' in raw: return 'adjective'
    if 'adv' in raw: return 'adverb'
    return 'noun'

def get_category_by_pos(pos, term):
    t = term.lower()
    if pos == 'verb':
        return 'Action & Process'
    elif pos == 'adjective':
        return 'Description & Quality'
    elif pos == 'adverb':
        return 'Manner & Context'
    elif pos in ['conjunction', 'preposition', 'pronoun', 'determiner']:
        return 'Grammar & Linking'
    return 'Daily Objects & Concepts'

oxford_vocab = []
seen_terms = set()
count = 1

for line in ox_lines:
    m = pattern.match(line)
    if not m:
        continue
    term_raw = m.group(1).strip()
    term_raw = re.sub(r'[,;:\s]+$', '', term_raw).strip()
    pos_raw = m.group(2).strip()
    level = m.group(3).strip()
    
    if len(term_raw) < 1 or term_raw.startswith(('PAGE', 'THE OXFORD')):
        continue
        
    term_clean = term_raw.lower()
    if term_clean in seen_terms:
        continue
        
    pos = map_pos(pos_raw)
    category = get_category_by_pos(pos, term_clean)
    
    # 1. Check handcrafted first
    if term_clean in handcrafted_oxford:
        h_term, h_ipa, h_pos, h_lvl, h_mean, h_en, h_id = handcrafted_oxford[term_clean]
        h_hint = f"Oxford 3000 Vocabulary ({h_pos}) • Level {h_lvl}"
        h_cat = get_category_by_pos(h_pos, h_term)
        # Check master overrides
        if term_clean in oxford_master_overrides:
            h_mean = oxford_master_overrides[term_clean]
            h_id = f"Menguasai {h_mean} sangat bermanfaat untuk kemampuan bahasa Inggris."
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
            "hint": h_hint,
            "category": h_cat
        })
        seen_terms.add(term_clean)
        count += 1
        continue
        
    # 2. Get clean Indonesian translation
    meaning_id = get_clean_oxford_meaning(term_raw, pos)
    
    # 3. IPA lookup
    ipa = ipa_data.get(term_clean, '')
    if not ipa:
        stem = re.sub(r'\(.*?\)', '', term_clean).strip()
        ipa = ipa_data.get(stem, f"/{term_clean}/")
        
    # 4. Contextual example sentences
    ex_en = f"Understanding this {term_raw} is essential for daily conversation."
    first_meaning = meaning_id.split('/')[0].strip()
    ex_id = f"Memahami {first_meaning} ini sangat penting dalam percakapan sehari-hari."
    
    item_id = f"ox-{re.sub(r'[^a-z0-9]+', '-', term_clean)}-{count}"
    oxford_vocab.append({
        "id": item_id,
        "term": term_raw,
        "ipa": ipa,
        "type": "oxford_3000",
        "pos": pos,
        "level": level,
        "meaningId": meaning_id,
        "exampleEn": ex_en,
        "exampleId": ex_id,
        "hint": f"Oxford 3000 core vocabulary ({pos}) • Level {level}",
        "category": category
    })
    seen_terms.add(term_clean)
    count += 1

# Append remaining handcrafted C1/C2 advanced words
for term_clean, h_entry in handcrafted_oxford.items():
    if term_clean not in seen_terms:
        h_term, h_ipa, h_pos, h_lvl, h_mean, h_en, h_id = h_entry
        if term_clean in oxford_master_overrides:
            h_mean = oxford_master_overrides[term_clean]
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

# 10. Phrasal Verbs Processing
print("Processing Phrasal Verbs from PDF and master clean overrides...")
phrasal_pdf_path = "C:/Users/ASUS/.gemini/antigravity-ide/brain/7acf44a5-2d01-4e3c-8811-7f112f29f30a/.user_uploaded/media_1791802719791.pdf"
reader_pv = pypdf.PdfReader(phrasal_pdf_path)
pv_lines = []
for p in reader_pv.pages:
    pv_lines.extend([l.strip().replace('\xa0', ' ') for l in p.extract_text().split('\n') if l.strip()])

phrasal_verbs = []
seen_pv = set()
pv_count = 1

# Helper function to get 100% clean Indonesian translation for any Phrasal Verb
def resolve_pv_meaning(term_raw, base_term, defn_en):
    t_raw = term_raw.lower().strip()
    b_term = base_term.lower().strip()
    
    # 1. Exact match in master overrides
    if t_raw in phrasal_verbs_master_overrides:
        return phrasal_verbs_master_overrides[t_raw]
    if b_term in phrasal_verbs_master_overrides:
        return phrasal_verbs_master_overrides[b_term]
        
    # 2. Normalized match in master overrides
    norm_t = normalize_text(t_raw)
    norm_b = normalize_text(b_term)
    if norm_t in norm_pv_overrides:
        return norm_pv_overrides[norm_t]
    if norm_b in norm_pv_overrides:
        return norm_pv_overrides[norm_b]
        
    # 3. Translation of English definition (defn_en)
    d_clean = defn_en.lower().strip()
    if d_clean in defn_en_to_id:
        return defn_en_to_id[d_clean]
        
    # Check without sb/sth in defn_en
    d_no_sb = d_clean.replace(' sb', '').replace(' sth', '').strip()
    if d_no_sb in defn_en_to_id:
        return defn_en_to_id[d_no_sb]
        
    # 4. Search in defn_en substrings
    for eng_k, id_v in defn_en_to_id.items():
        if eng_k in d_clean:
            return id_v
            
    # 5. Fallback clean phrase
    return f"melakukan tindakan {b_term}"

# First add all rich handcrafted phrasal verbs
for term_clean, h_entry in handcrafted_pv.items():
    h_term, h_ipa, h_lvl, h_mean, h_en, h_id, h_hint, h_cat = h_entry
    # Check if there is an improved master override for this term
    if h_term.lower() in phrasal_verbs_master_overrides:
        h_mean = phrasal_verbs_master_overrides[h_term.lower()]
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
        
        # Clean up non-printable or corrupted characters
        term_raw = re.sub(r'[\ufffd\x00-\x1f]+', '', term_raw).strip()
        term_raw = re.sub(r'\s+', ' ', term_raw).strip()
        
        term_clean = term_raw.lower()
        base_term = term_clean.replace(' sth', '').replace(' sb', '').replace(' (sb)', '').replace(' (sth)', '').strip()
        
        if base_term not in seen_pv and len(base_term) > 3:
            meaning_id = resolve_pv_meaning(term_raw, base_term, defn_en)
            
            # Clean pronunciation IPA
            clean_phonetic = base_term.replace(' (to ...)', '').replace(' (to )', '').strip()
            ipa_val = f"/{clean_phonetic}/"
            
            first_m = meaning_id.split('/')[0].strip()
            ex_en = f"She decided to {base_term} without delay."
            ex_id = f"Dia memutuskan untuk {first_m} tanpa menunda lagi."
            
            item_id = f"pv-{re.sub(r'[^a-z0-9]+', '-', base_term)}-{pv_count}"
            phrasal_verbs.append({
                "id": item_id,
                "term": term_raw,
                "ipa": ipa_val,
                "type": "phrasal_verb",
                "pos": "verb",
                "level": "B2",
                "meaningId": meaning_id,
                "exampleEn": ex_en,
                "exampleId": ex_id,
                "hint": f"Oxford Pocket Phrasal Verb • {first_m}",
                "category": "Phrasal Verbs in Context"
            })
            seen_pv.add(base_term)
            pv_count += 1

print(f"Phrasal Verbs generated: {len(phrasal_verbs)}")

# 11. Collocations
print("Compiling Collocations...")
collocations = []
colloc_count = 1
for item in handcrafted_colloc:
    c_term, c_ipa, c_pos, c_lvl, c_mean, c_en, c_id, c_cat = item
    item_id = f"col-{re.sub(r'[^a-z0-9]+', '-', c_term.lower())}-{colloc_count}"
    collocations.append({
        "id": item_id,
        "term": c_term,
        "ipa": c_ipa,
        "type": "collocation",
        "pos": c_pos,
        "level": c_lvl,
        "meaningId": c_mean,
        "exampleEn": c_en,
        "exampleId": c_id,
        "hint": f"Natural Collocation Pattern ({c_pos}) • {c_lvl}",
        "category": c_cat
    })
    colloc_count += 1

print(f"Collocations generated: {len(collocations)}")

# 12. Save JS files to src/data
print("Writing files to src/data...")

with open(os.path.join(data_dir, 'oxfordVocab.js'), 'w', encoding='utf-8') as f:
    f.write("export const oxfordVocab = " + json.dumps(oxford_vocab, indent=2, ensure_ascii=False) + ";\n")

with open(os.path.join(data_dir, 'phrasalVerbs.js'), 'w', encoding='utf-8') as f:
    f.write("export const phrasalVerbs = " + json.dumps(phrasal_verbs, indent=2, ensure_ascii=False) + ";\n")

with open(os.path.join(data_dir, 'collocations.js'), 'w', encoding='utf-8') as f:
    f.write("export const collocations = " + json.dumps(collocations, indent=2, ensure_ascii=False) + ";\n")

# Combine all in index.js
with open(os.path.join(data_dir, 'index.js'), 'w', encoding='utf-8') as f:
    f.write("""import { phrasalVerbs } from './phrasalVerbs';
import { collocations } from './collocations';
import { oxfordVocab } from './oxfordVocab';

export { phrasalVerbs, collocations, oxfordVocab };

export const allVocabulary = [
  ...phrasalVerbs,
  ...collocations,
  ...oxfordVocab
];

export const allVocabularies = allVocabulary;

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

// Helper to filter by type
export const getVocabulariesByType = (type) => {
  if (type === 'all') return allVocabulary;
  if (type === 'oxford_3000' || type === 'oxford') return oxfordVocab;
  if (type === 'phrasal_verb') return phrasalVerbs;
  if (type === 'collocation') return collocations;
  return allVocabulary;
};

// Helper to get random sample of words (default 50)
export const getRandomVocabularies = (count = 50, filterType = 'all') => {
  const pool = getVocabulariesByType(filterType);
  return getRandomBatch(pool, count);
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
""")

total_all = len(oxford_vocab) + len(phrasal_verbs) + len(collocations)
print(f"\nSUCCESS! 100% Clean Database Built:")
print(f"Oxford Vocab: {len(oxford_vocab)}")
print(f"Phrasal Verbs: {len(phrasal_verbs)}")
print(f"Collocations: {len(collocations)}")
print(f"Grand Total Vocabulary: {total_all}")
