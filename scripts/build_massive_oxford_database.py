# -*- coding: utf-8 -*-
"""
Build Massive Oxford 3000, 5000 (C1 & C2), Phrasal Verbs, and Collocations Database
"""
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, '..', 'src', 'data')
os.makedirs(data_dir, exist_ok=True)

# 1. Complete Phrasal Verbs & Idioms
phrasal_verbs_list = [
  ("calm down", "/kɑːm daʊn/", "A2", "menenangkan diri / menjadi lebih tenang", "Calm down and tell me what happened.", "Tenanglah dan ceritakan padaku apa yang sebenarnya terjadi.", "Telling someone to relax or stop panicking", "Feelings"),
  ("catch on", "/kætʃ ɒn/", "B2", "menjadi populer / mulai memahami sesuatu", "His new song is beginning to catch on.", "Lagu barunya mulai digemari dan menjadi populer.", "Become fashionable or grasp an idea", "Trends"),
  ("keep in with sb", "/kiːp ɪn wɪð/", "B2", "menjaga hubungan baik dengan seseorang", "It pays to keep in with your supervisor.", "Penting untuk menjaga hubungan baik dengan atasanmu.", "Stay on friendly terms for advantage", "Work"),
  ("laugh at sb", "/lɑːf æt/", "A2", "menertawakan seseorang / mengejek", "It is impolite to laugh at someone's mistakes.", "Tidak sopan menertawakan kesalahan orang lain.", "Mock or find funny", "Social"),
  ("laugh sth off", "/lɑːf ɒf/", "B2", "menertawakan / mengabaikan hal memalukan", "She laughed off the rumors with confidence.", "Dia menertawakan dan mengabaikan rumor itu dengan percaya diri.", "Dismiss embarrassment by laughing", "Reactions"),
  ("put sth on", "/pʊt ɒn/", "A2", "mengenakan pakaian / menyelenggarakan acara", "Put on your warm jacket before going out.", "Kenakan jaket hangatmu sebelum keluar rumah.", "Wear clothes or organize event", "Everyday"),
  ("stay in", "/steɪ ɪn/", "A2", "berdiam di rumah / tidak bepergian keluar", "Let's stay in tonight and watch a movie.", "Mari kita berdiam di rumah malam ini dan menonton film.", "Remain at home", "Everyday"),
  ("tear sth up", "/teə(r) ʌp/", "B1", "merobek-robek menjadi serpihan kecil", "He tore up the old agreement paper.", "Dia merobek-robek lembaran perjanjian lama itu.", "Ripped into small pieces", "Actions"),
  ("wait up for sb", "/weɪt ʌp fɔː(r)/", "B1", "menunggu seseorang pulang sebelum tidur", "Don't wait up for me; I might be late.", "Jangan tunggu aku sampai larut; aku mungkin pulang terlambat.", "Stay awake until someone arrives", "Home"),
  ("wind sb up", "/waɪnd ʌp/", "B2", "menjahili / memancing emosi seseorang", "Stop winding your brother up!", "Berhentilah menjahili dan memancing emosi saudaramu!", "Tease or irritate deliberately", "Feelings"),
  ("wind sth up", "/waɪnd ʌp/", "B2", "mengakhiri pertemuan / melikuidasi bisnis", "Let's wind up our meeting by noon.", "Mari kita akhiri rapat kita sebelum tengah hari.", "Bring to a close or liquidate", "Business"),
  ("back out", "/bæk aʊt/", "B2", "menarik diri / membatalkan perjanjian", "He backed out at the last minute.", "Dia membatalkan perjanjian di menit-menit terakhir.", "Withdraw from an agreement", "Decisions"),
  ("bring sb/sth back", "/brɪŋ bæk/", "A2", "mengembalikan sesuatu / membangkitkan kenangan", "This old photo brings back happy memories.", "Foto lama ini membangkitkan kenangan indah masa lalu.", "Return or evoke memories", "Memory"),
  ("come about", "/kʌm əˈbaʊt/", "B2", "terjadi / bagaimana suatu peristiwa terjadi", "How did this misunderstanding come about?", "Bagaimana kesalahpahaman ini bisa terjadi?", "Happen or take place", "Events"),
  ("frighten sb/sth away", "/ˈfraɪtn əˈweɪ/", "B1", "menakut-nakuti hingga pergi", "The watchdog frightened the burglar away.", "Anjing penjaga itu menakut-nakuti si pencuri hingga kabur.", "Scare off", "Actions"),
  ("get through sth", "/ɡet θruː/", "B1", "tersambung telepon / menyelesaikan tugas berat / lulus", "I finally got through to customer service.", "Aku akhirnya berhasil tersambung ke layanan pelanggan.", "Connect via phone or complete difficulty", "Communication"),
  ("go along with sb/sth", "/ɡəʊ əˈlɒŋ wɪð/", "B1", "menyetujui gagasan / sependapat", "I am happy to go along with your plan.", "Aku senang menyetujui rencanamu.", "Agree or support an idea", "Agreement"),
  ("go away", "/ɡəʊ əˈweɪ/", "A1", "pergi menjauh / menghilang", "The pain will gradually go away.", "Rasa sakit itu akan berangsur-angsur menghilang.", "Disappear or depart", "Actions"),
  ("hear from sb", "/hɪə(r) frɒm/", "A2", "menerima kabar atau pesan dari seseorang", "Have you heard from Linda recently?", "Apakah kamu sudah mendengar kabar dari Linda belakangan ini?", "Receive news or message", "Communication"),
  ("help sb out", "/help aʊt/", "A2", "membantu meringankan kesulitan seseorang", "Can you help me out with these boxes?", "Bisakah kamu membantuku membawa kotak-kotak ini?", "Assist in a chore or task", "Social"),
  ("put sth down", "/pʊt daʊn/", "A2", "mencatat di kertas / meletakkan benda", "Put down your ideas on the notepad.", "Catatlah ide-idemu di buku catatan.", "Write on paper or set down", "Writing"),
  ("settle on sth", "/ˈsetl ɒn/", "B2", "menetapkan pilihan setelah berpikir matang", "Have you settled on a thesis topic?", "Apakah kamu sudah menetapkan topik skripsimu?", "Choose after consideration", "Decisions"),
  ("spell sth out", "/spel aʊt/", "B2", "menjelaskan secara gamblang dan terperinci", "Do I have to spell it out for you?", "Haruskah aku menjelaskannya secara gamblang agar kamu paham?", "Explain clearly in detail", "Communication"),
  ("come out", "/kʌm aʊt/", "B1", "terbit / dipublikasikan / terungkap / matahari muncul", "Her new novel will come out next month.", "Novel barunya akan terbit bulan depan.", "Be published or become known", "Publishing"),
  ("come up", "/kʌm ʌp/", "B1", "muncul tiba-tiba / dibahas dalam percakapan", "The subject came up in conversation.", "Topik tersebut dibahas dalam percakapan.", "Be mentioned or arise", "Discussions"),
  ("come up against sb/sth", "/kʌm ʌp əˈɡenst/", "B2", "menghadapi rintangan berat atau lawan tangguh", "The startup came up against harsh regulations.", "Startup tersebut menghadapi regulasi ketat yang berat.", "Face a difficult challenge", "Challenges"),
  ("get into sth", "/ɡet ˈɪntuː/", "B1", "mulai menyukai / masuk universitas / memakai baju", "She recently got into organic cooking.", "Dia belakangan ini mulai menyukai masak masakan organik.", "Become interested or involved", "Hobbies"),
  ("go out", "/ɡəʊ aʊt/", "A1", "keluar rumah / padam (lampu/api) / berkencan", "The street lamps go out at sunrise.", "Lampu-lampu jalan padam saat matahari terbit.", "Extinguish or leave home", "Everyday"),
  ("turn sth down", "/tɜːn daʊn/", "B1", "menolak tawaran / mengecilkan volume", "He turned down an attractive job offer.", "Dia menolak tawaran pekerjaan yang menggiurkan itu.", "Reject an offer or decrease volume", "Decisions"),
  ("turn sth up", "/tɜːn ʌp/", "A2", "membesarkan volume atau suhu", "Can you turn the heater up a bit?", "Bisakah kamu membesarkan suhu pemanasnya sedikit?", "Increase sound or heat", "Adjustments"),
  ("turn up", "/tɜːn ʌp/", "B1", "tiba / muncul secara tak terduga", "He turned up at the meeting unannounced.", "Dia muncul di rapat tanpa pemberitahuan sebelumnya.", "Arrive unexpectedly", "Arrival"),
  ("cry off", "/kraɪ ɒf/", "B2", "membatalkan janji atau pertemuan", "She cried off from the dinner due to illness.", "Dia membatalkan hadir di acara makan malam karena sakit.", "Cancel an arrangement", "Social"),
  ("do away with sth", "/duː əˈweɪ wɪð/", "B2", "menghapuskan / meniadakan kebiasaan atau aturan", "The government did away with the old tax.", "Pemerintah menghapuskan pajak lama tersebut.", "Abolish or get rid of", "Rules"),
  ("dream sth up", "/driːm ʌp/", "B2", "mencetuskan ide aneh atau sangat imajinatif", "Who dreamed up this bizarre concept?", "Siapa yang mencetuskan ide aneh yang tidak biasa ini?", "Invent an unusual idea", "Creativity"),
  ("enlarge on sth", "/ɪnˈlɑːdʒ ɒn/", "B2", "menguraikan lebih mendalam / memperjelas", "Could you enlarge on your proposal?", "Bisakah Anda menguraikan lebih mendalam tentang usulan Anda?", "Speak in greater detail", "Discussions"),
  ("enter into sth", "/ˈentə ˈɪntuː/", "B2", "memulai kesepakatan / terlibat aktif", "The two firms entered into a partnership.", "Kedua perusahaan itu memulai jalinan kemitraan.", "Formally begin agreement", "Business"),
  ("kick in", "/kɪk ɪn/", "B2", "mulai terasa khasiat atau efeknya", "The painkiller took fifteen minutes to kick in.", "Obat pereda nyeri itu butuh lima belas menit untuk mulai bekerja.", "Begin to take effect", "Health"),
  ("put sth forward", "/pʊt ˈfɔːwəd/", "B2", "mengajukan usulan, rencana, atau saran", "She put forward an ingenious strategy.", "Dia mengajukan strategi yang sangat cerdik.", "Propose an idea", "Proposals"),
  ("put sth out", "/pʊt aʊt/", "B1", "memadamkan api / rokok", "Firefighters put out the blaze promptly.", "Petugas pemadam memadamkan api dengan sigap.", "Extinguish fire", "Safety"),
  ("put yourself out", "/pʊt jɔːˈself aʊt/", "B2", "merepotkan diri demi membantu orang lain", "Please don't put yourself out on my account.", "Tolong jangan merepotkan dirimu sendiri demi aku.", "Inconvenience oneself for someone", "Courtesy"),
  ("spread out", "/spred aʊt/", "B1", "menyebar / membentang ke area yang luas", "The search team spread out across the forest.", "Tim pencari menyebar ke seluruh penjuru hutan.", "Disperse over an area", "Actions"),
  ("breakthrough", "/ˈbreɪkθruː/", "B2", "terobosan besar / kemajuan penting", "Scientists made a historic breakthrough.", "Para ilmuwan membuat terobosan bersejarah.", "Noun from break through", "Science"),
  ("bystander", "/ˈbaɪstændə(r)/", "B2", "orang yang menyaksikan kejadian di lokasi", "A passer-by bystander helped call an ambulance.", "Seorang saksi di lokasi membantu menelepon ambulans.", "Observer at an event", "Society"),
  ("hand sth out", "/hænd aʊt/", "A2", "membagikan materi / selebaran", "The instructor handed out the revision sheets.", "Instruktur membagikan lembar revisi belajar.", "Distribute by hand", "Classroom"),
  ("handout", "/ˈhændaʊt/", "B1", "lembaran materi cetak yang dibagikan", "Refer to the handout on page three.", "Lihatlah lembaran materi pada halaman tiga.", "Printed sheet distributed", "Classroom"),
  ("keep sth up", "/kiːp ʌp/", "B1", "mempertahankan standar / kondisi prima", "Keep up the hard work and you will succeed.", "Pertahankan kerja kerasmu dan kamu akan sukses.", "Maintain high standard", "Effort"),
  ("let sb down", "/let daʊn/", "B1", "mengecewakan kepercayaan seseorang", "I promise never to let you down.", "Aku berjanji tidak akan pernah mengecewakanmu.", "Disappoint someone", "Trust"),
  ("letdown", "/ˈletdaʊn/", "B2", "kekecewaan / hal yang mengecewakan", "The movie ending was a total letdown.", "Akhir film tersebut benar-benar mengecewakan.", "A disappointment", "Feelings"),
  ("stand by", "/stænd baɪ/", "B2", "tetap setia mendampingi / bersiap siaga", "True companions stand by each other.", "Sahabat sejati selalu setia mendampingi satu sama lain.", "Support loyally", "Friendship"),
  ("stand in for sb", "/stænd ɪn fɔː(r)/", "B2", "menggantikan posisi seseorang sementara", "She stood in for her sick colleague.", "Dia menggantikan posisi rekan kerjanya yang sedang sakit.", "Act as substitute", "Work"),
  ("upkeep", "/ˈʌpkiːp/", "B2", "biaya perawatan / pemeliharaan rutin", "The historic mansion requires expensive upkeep.", "Rumah kuno itu membutuhkan biaya pemeliharaan yang mahal.", "Cost of maintenance", "Property"),
  ("write sth off", "/raɪt ɒf/", "B2", "menghapus buku hutang / menganggap kerugian total", "The bank decided to write off bad debts.", "Pihak bank memutuskan untuk menghapus buku kredit macet tersebut.", "Acknowledge financial loss", "Finance"),
  ("built-in", "/ˌbɪlt ˈɪn/", "B2", "bawaan / terintegrasi menyatu sejak awal", "The app features built-in spell checking.", "Aplikasi ini memiliki fitur pengecekan ejaan bawaan.", "Formed as part of a structure", "Tech"),
  ("go ahead", "/ɡəʊ əˈhed/", "B1", "melanjutkan / berjalan sesuai rencana", "The project will go ahead despite delays.", "Proyek ini akan tetap berjalan meski ada penundaan.", "Proceed without delay", "Progress"),
  ("go on", "/ɡəʊ ɒn/", "A2", "melanjutkan / terus berlangsung / terjadi", "The lecture went on for another hour.", "Kuliah tersebut terus berlanjut satu jam lagi.", "Continue or happen", "Time"),
  ("knock sb out", "/nɒk aʊt/", "B2", "memukul jatuh hingga tak berdaya / mengalahkan", "The champion knocked his challenger out in round two.", "Sang juara memukul KO lawannya di ronde kedua.", "Defeat or make unconscious", "Sports"),
  ("knockout", "/ˈnɒkaʊt/", "B2", "kemenangan mutlak KO / memukau", "Her speech was a complete knockout.", "Pidatonya benar-benar memukau dan luar biasa.", "Defeating or impressive blow", "Impact"),
  ("off-putting", "/ˈɒfˌpʊt.ɪŋ/", "B2", "kurang menyenangkan / membuat orang enggan", "His aggressive tone was off-putting.", "Nada bicaranya yang agresif membuat orang enggan berinteraksi.", "Unpleasant or discouraging", "Impressions"),
  ("ongoing", "/ˈɒnˌɡəʊ.ɪŋ/", "B2", "sedang berjalan dan masih berlangsung", "The clinical trials are currently ongoing.", "Uji klinis tersebut saat ini masih terus berlangsung.", "Continuing in progress", "Process"),
  ("outspoken", "/aʊtˈspəʊ.kən/", "B2", "vokal / lugas dan blak-blakan menyuarakan opini", "She is an outspoken advocate of free press.", "Dia adalah pembela kebebasan pers yang sangat vokal.", "Frank and candid", "Personality"),
  ("put sb off", "/pʊt ɒf/", "B2", "membuat risih / mengalihkan konsentrasi", "Loud chewing puts many diners off.", "Suara mengunyah yang keras membuat risih banyak orang makan.", "Dislike or distract", "Feelings"),
  ("speak out", "/spiːk aʊt/", "B2", "berani bersuara menentang ketidakadilan", "Citizens spoke out against rising utility fees.", "Warga berani bersuara menentang kenaikan tarif listrik.", "Publicly declare opposition", "Society"),
  ("water sth down", "/ˈwɔːtə daʊn/", "B2", "melunakkan argumen / mengencerkan larutan", "They watered down the proposed regulations.", "Mereka melunakkan isi draf regulasi yang diajukan.", "Dilute or soften strength", "Rules"),
  ("wear sb out", "/weə(r) aʊt/", "B1", "menguras tenaga hingga sangat lelah", "A long flight wears passengers out.", "Penerbangan panjang menguras stamina penumpang hingga sangat letih.", "Exhaust energy", "Health"),
  ("worn out", "/wɔːn aʊt/", "B1", "sangat letih / lusuh dan aus karena pemakaian", "His running shoes were completely worn out.", "Sepatu larinya sudah benar-benar aus dan lusuh.", "Tired or no longer usable", "Condition"),
  ("out of the blue", "/aʊt əv ðə bluː/", "B2", "tiba-tiba tanpa diduga sama sekali", "She called me out of the blue after years.", "Dia meneleponku tiba-tiba setelah bertahun-tahun.", "Completely unexpectedly", "Idioms"),
  ("put your foot in it", "/pʊt jɔː fʊt ɪn ɪt/", "B2", "salah bicara hingga mempermalukan diri", "I put my foot in it by mentioning the ex.", "Aku salah bicara dengan mengungkit mantannya.", "Say something embarrassing", "Idioms"),
  ("bend down", "/bend daʊn/", "A2", "membungkukkan badan ke bawah", "He bent down to pick up his fallen wallet.", "Dia membungkuk untuk mengambil dompetnya yang jatuh.", "Curve body downward", "Actions"),
  ("bump into sb", "/bʌmp ˈɪntuː/", "B1", "berpapasan secara tidak sengaja / menabrak", "I bumped into my high school teacher today.", "Aku berpapasan dengan guru SMA-ku secara tidak sengaja hari ini.", "Meet unexpectedly or collide", "Social"),
  ("fall over", "/fɔːl ˈəʊvə/", "A2", "terjatuh tersandung ke lantai", "The toddler tripped and fell over on the lawn.", "Balita itu tersandung dan jatuh di atas rumput.", "Tumble to ground", "Movement"),
  ("get up", "/ɡet ʌp/", "A1", "bangun dari tidur / bangkit berdiri", "I usually get up at six every morning.", "Aku biasanya bangun pukul enam setiap pagi.", "Rise from bed or stand", "Everyday"),
  ("knock sb down", "/nɒk daʊn/", "B1", "menabrak seseorang hingga roboh / merobohkan", "The vehicle knocked the post down.", "Kendaraan itu menabrak tiang hingga roboh.", "Strike down to ground", "Accidents"),
  ("lie down", "/laɪ daʊn/", "A2", "berbaring untuk beristirahat", "Lie down on the couch if you feel dizzy.", "Berbaringlah di sofa jika kamu merasa pusing.", "Rest horizontally", "Health"),
  ("trip over", "/trɪp ˈəʊvə/", "B1", "tersandung kaki atau benda", "Watch out so you don't trip over the cable.", "Hati-hati agar kamu tidak tersandung kabel.", "Stumble upon obstacle", "Movement"),
  ("cut down on sth", "/kʌt daʊn ɒn/", "B1", "mengurangi konsumsi makanan/kebiasaan", "Try to cut down on saturated fats.", "Cobalah mengurangi asupan lemak jenuh.", "Reduce consumption", "Diet"),
  ("cut sth out", "/kʌt aʊt/", "B1", "menghentikan konsumsi sama sekali", "Cut out sugary soda from your daily diet.", "Hentikan minuman soda manis dari menu harianmu.", "Eliminate entirely", "Health"),
  ("do sth up", "/duː ʌp/", "B1", "mengancingkan / merenovasi rumah", "Do up your coat before stepping into the snow.", "Kancingkan mantelmu sebelum melangkah ke salju.", "Fasten or refurbish", "Actions"),
  ("face up to sth", "/feɪs ʌp tuː/", "B2", "berani menghadapi kenyataan pahit", "You must face up to the consequences.", "Kamu harus berani menghadapi segala konsekuensinya.", "Confront bravely", "Mindset"),
  ("fill sb up", "/fɪl ʌp/", "B1", "membuat kenyang", "A bowl of warm oatmeal fills you up nicely.", "Semangkuk bubur oat hangat membuatmu kenyang dengan baik.", "Satisfy hunger", "Food"),
  ("show off", "/ʃəʊ ɒf/", "B1", "pamer dan menyombongkan keahlian", "He loves showing off his juggling skills.", "Dia suka memamerkan kemampuan juggling-nya.", "Boast or display proudly", "Behavior"),
  ("show sth off", "/ʃəʊ ɒf/", "B1", "memamerkan barang baru dengan bangga", "She showed off her engagement ring.", "Dia memamerkan cincin pertunangannya.", "Exhibit proudly", "Social"),
  ("turn over a new leaf", "/tɜːn ˈəʊvə ə njuː liːf/", "B2", "membuka lembaran hidup baru yang lebih baik", "He resolved to turn over a new leaf this year.", "Dia bertekad membuka lembaran hidup baru tahun ini.", "Start behaving better", "Self-Growth"),
  ("work out", "/wɜːk aʊt/", "A2", "berolahraga / berhasil / memecahkan perhitungan", "Things will work out well in the end.", "Segalanya akan berakhir dengan baik pada akhirnya.", "Exercise or succeed", "Fitness"),
  ("get over sb/sth", "/ɡet ˈəʊvə/", "B1", "pulih dari penyakit / bangkit dari patah hati", "It took time to get over the disappointment.", "Butuh waktu untuk bangkit dari kekecewaan itu.", "Recover emotionally or physically", "Emotions"),
  ("pass out", "/pɑːs aʊt/", "B1", "pingsan / hilang kesadaran", "The heat caused a student to pass out.", "Udara panas menyebabkan seorang siswa pingsan.", "Faint temporarily", "Health"),
  ("pass away", "/pɑːs əˈweɪ/", "B1", "meninggal dunia (ungkapan halus)", "Her great-grandmother passed away peacefully.", "Buyutnya meninggal dunia dengan damai.", "Euphemism for die", "Polite"),
  ("pull through", "/pʊl θruː/", "B2", "melewati masa kritis dan selamat", "The patient pulled through after intensive surgery.", "Pasien tersebut selamat melewati masa kritis setelah operasi intensif.", "Survive crisis", "Resilience"),
  ("bottle sth up", "/ˈbɒtl ʌp/", "B2", "memendam perasaan sedih atau marah", "Don't bottle up your grievances inside.", "Jangan memendam unek-unekmu di dalam hati.", "Suppress emotions", "Feelings"),
  ("bring sb up", "/brɪŋ ʌp/", "B1", "membesarkan anak / mengangkat topik", "She was brought up in a loving family.", "Dia dibesarkan di tengah keluarga yang penuh kasih sayang.", "Raise children or mention", "Family"),
  ("grow up", "/ɡrəʊ ʌp/", "A1", "tumbuh menjadi dewasa", "He grew up in a rural village.", "Dia tumbuh dewasa di sebuah desa pedesaan.", "Mature into adult", "Growth"),
  ("look forward to sth", "/lʊk ˈfɔːwəd tuː/", "B1", "sangat menanti-nantikan dengan gembira", "I look forward to your visit next month.", "Aku sangat menanti-nantikan kunjunganmu bulan depan.", "Anticipate eagerly", "Feelings"),
  ("turn a blind eye", "/tɜːn ə blaɪnd aɪ/", "B2", "pura-pura tidak melihat / tutup mata atas pelanggaran", "Officials turned a blind eye to the illegal trade.", "Aparat menutup mata atas perdagangan ilegal tersebut.", "Deliberately ignore", "Rules"),
  ("count on sb", "/kaʊnt ɒn/", "B1", "mengandalkan seseorang dengan percaya", "You can always count on his support.", "Kamu selalu bisa mengandalkan dukungannya.", "Rely upon", "Trust"),
  ("put up with sb/sth", "/pʊt ʌp wɪð/", "B2", "mentoleransi / sabar menahan gangguan", "I cannot put up with this racket anymore.", "Aku tidak tahan lagi mentoleransi suara berisik ini.", "Tolerate patiently", "Patience"),
  ("break up with sb", "/breɪk ʌp/", "B1", "mengakhiri hubungan percintaan", "They broke up amicably after college.", "Mereka putus secara baik-baik setelah kuliah.", "End romance", "Relationships"),
  ("make up with sb", "/meɪk ʌp/", "B1", "berbaikan kembali setelah berselisih", "Friends should make up after a small quarrel.", "Sahabat hendaknya segera berbaikan setelah berselisih kecil.", "Reconcile", "Friendship"),
  ("drift apart", "/drɪft əˈpɑːt/", "B2", "merenggang secara perlahan seiring waktu", "Old schoolmates often drift apart.", "Teman sekolah lama sering kali merenggang perlahan seiring waktu.", "Grow distant", "Relationships"),
  ("get cold feet", "/ɡet kəʊld fiːt/", "B2", "ragu-ragu dan grogi sebelum saat penting", "The speaker got cold feet before taking the stage.", "Pembicara itu merasa grogi sesaat sebelum naik ke panggung.", "Hesitate nervously", "Emotions"),
  ("hit it off", "/hɪt ɪt ɒf/", "B2", "langsung akrab dan cocok sejak pertama berjumpa", "The two roommates hit it off straight away.", "Kedua teman sekamar itu langsung merasa sangat cocok sejak awal.", "Become fast friends", "Friendship"),
  ("make ends meet", "/meɪk endz miːt/", "B2", "mencukupi kebutuhan pokok dengan uang pas-pasan", "He worked overtime to make ends meet.", "Dia bekerja lembur demi mencukupi kebutuhan pokok sehari-hari.", "Balance living budget", "Money"),
  ("rip sb off", "/rɪp ɒf/", "B2", "menipu dengan mematok harga kemahalan", "Don't let shady vendors rip you off.", "Jangan biarkan penjual nakal mematok harga kemahalan padamu.", "Overcharge unfairly", "Money"),
  ("come across sth", "/kʌm əˈkrɒs/", "B1", "menemukan sesuatu secara tidak sengaja", "I came across an insightful book today.", "Aku menemukan buku yang berbobot secara tidak sengaja hari ini.", "Find by chance", "Discovery"),
  ("get rid of sth", "/ɡet rɪd əv/", "B1", "menyingkirkan atau membuang barang", "Get rid of excess junk in your room.", "Singkirkan barang-barang menumpuk tak terpakai di kamarmu.", "Dispose of", "Cleaning"),
  ("hold up", "/həʊld ʌp/", "B1", "menghambat atau menunda perjalanan", "A flat tire held us up for an hour.", "Ban kempes menunda perjalanan kami selama satu jam.", "Delay progress", "Travel"),
  ("set off", "/set ɒf/", "B1", "memulai perjalanan / berangkat", "We set off early to catch the ferry.", "Kami berangkat pagi-pagi sekali demi mengejar kapal feri.", "Begin journey", "Travel"),
  ("check in", "/tʃek ɪn/", "A2", "mendaftar masuk di hotel atau bandara", "Check in at the desk before security.", "Lapor masuklah di meja sebelum pemeriksaan keamanan.", "Register arrival", "Travel"),
  ("break into sth", "/breɪk ˈɪntuː/", "B1", "membobol masuk tanpa izin", "Burglars broke into the gallery last night.", "Pencuri membobol galeri seni tersebut tadi malam.", "Force entry", "Crime"),
  ("crack down on sth", "/kræk daʊn ɒn/", "B2", "menindak tegas pelanggaran hukum", "Police cracked down on speeding drivers.", "Polisi menindak tegas para pengendara yang mengebut.", "Enforce strictly", "Law"),
  ("get away with sth", "/ɡet əˈweɪ wɪð/", "B2", "lolos tanpa dihukum atas kesalahan", "No one can get away with fraud forever.", "Tak seorang pun bisa lolos selamanya dari tindak penipuan.", "Escape punishment", "Justice"),
  ("carry sth out", "/ˈkæri aʊt/", "B1", "melaksanakan atau menjalankan rencana/riset", "The lab carried out rigorous safety tests.", "Laboratorium itu melaksanakan uji keselamatan secara ketat.", "Execute or conduct", "Tasks"),
  ("back sth up", "/bæk ʌp/", "B1", "mencadangkan data / mendukung pernyataan", "Always back up files to external drives.", "Selalu cadangkan file-file penting ke drive eksternal.", "Duplicate data", "Technology"),
  ("pop up", "/pɒp ʌp/", "B1", "muncul tiba-tiba di layar", "A prompt popped up asking for confirmation.", "Jendela dialog tiba-tiba muncul meminta konfirmasi.", "Appear suddenly", "Technology"),
  ("come up with sth", "/kʌm ʌp wɪð/", "B1", "mencetuskan ide atau menemukan solusi", "She came up with a brilliant project topic.", "Dia mencetuskan topik proyek yang sangat cemerlang.", "Devise or invent", "Ideas"),
  ("figure sth out", "/ˈfɪɡə aʊt/", "B1", "memahami cara kerja atau memecahkan masalah", "I finally figured out the tricky riddle.", "Aku akhirnya memecahkan teka-teki rumit itu.", "Understand logic", "Mind"),
  ("brush up on sth", "/brʌʃ ʌp ɒn/", "B2", "menyegarkan kembali kemampuan bahasa/keahlian", "I am brushing up on my advanced vocabulary.", "Aku sedang menyegarkan kembali kosakata tingkat lanjutku.", "Refresh knowledge", "Learning"),
  ("look down on sb", "/lʊk daʊn ɒn/", "B2", "memandang rendah orang lain", "Never look down on someone who is trying.", "Jangan pernah memandang rendah orang yang sedang berjuang.", "Regard as inferior", "Attitude"),
  ("look up to sb", "/lʊk ʌp tuː/", "B1", "mengagumi dan meneladani seseorang", "Students look up to their dedicated teacher.", "Para siswa meneladani guru mereka yang berdedikasi.", "Admire and respect", "Role Models"),
  ("strike up a conversation", "/straɪk ʌp ə ˌkɒnvəˈseɪʃn/", "B2", "memulai obrolan ramah dengan orang baru", "He struck up a conversation with his neighbor.", "Dia memulai obrolan ramah dengan tetangganya.", "Initiate friendly talk", "Social"),
  ("iron sth out", "/ˈaɪən aʊt/", "B2", "meluruskan kesalahpahaman kecil / menyelesaikan", "They ironed out minor treaty clauses.", "Mereka meluruskan klausul perjanjian kecil yang sempat tertunda.", "Resolve smoothly", "Negotiation"),
  ("mull sth over", "/mʌl ˈəʊvə/", "B2", "memikirkan dan merenungkan secara mendalam", "Mull the career offer over before deciding.", "Renungkan tawaran karier itu matang-matang sebelum memutuskan.", "Reflect carefully", "Decisions"),
  ("abide by sth", "/əˈbaɪd baɪ/", "B2", "mematuhi peraturan dengan taat", "Drivers must abide by highway speed limits.", "Pengemudi wajib mematuhi batas kecepatan jalan raya.", "Comply with rules", "Law"),
  ("drop sb off", "/drɒp ɒf/", "A2", "mengantar dan menurunkan seseorang di tujuan", "I can drop you off near your campus.", "Aku bisa mengantarmu sampai dekat kampusmu.", "Deliver someone", "Travel"),
  ("pick sb up", "/pɪk ʌp/", "A2", "menjemput seseorang dengan kendaraan", "Dad will pick us up after choir rehearsal.", "Ayah akan menjemput kita setelah latihan paduan suara.", "Collect someone", "Travel"),
  ("save up", "/seɪv ʌp/", "A2", "menabung uang untuk tujuan tertentu", "She saved up for a new acoustic guitar.", "Dia menabung untuk membeli gitar akustik baru.", "Accumulate savings", "Money"),
  ("splash out", "/splæʃ aʊt/", "B2", "menghamburkan uang untuk memanjakan diri", "We splashed out on a gourmet dinner.", "Kami memanjakan diri dengan makan malam adiboga.", "Spend lavishly", "Luxury"),
  ("scrape by", "/skreɪp baɪ/", "B2", "bertahan hidup dengan upah yang sangat pas-pasan", "He scraped by during his internship months.", "Dia bertahan hidup pas-pasan selama masa magangnya.", "Survive on little", "Survival"),
  ("run out of sth", "/rʌn aʊt əv/", "A2", "kehabisan persediaan (baterai, bensin, waktu)", "We ran out of printer ink during printing.", "Kami kehabisan tinta printer saat sedang mencetak.", "Have none left", "Resources"),
  ("look into sth", "/lʊk ˈɪntuː/", "B1", "menyelidiki atau menginvestigasi fakta", "Inspectors are looking into safety lapses.", "Inspektur sedang menyelidiki kelalaian keselamatan kerja.", "Investigate", "Analysis"),
  ("broaden your horizons", "/ˈbrɔːdn jɔː həˈraɪznz/", "B2", "memperluas wawasan dan sudut pandang", "Reading varied books broadens your horizons.", "Membaca buku beragam memperluas wawasanmu.", "Expand worldview", "Growth"),
  ("take the plunge", "/teɪk ðə plʌndʒ/", "B2", "memberanikan diri mengambil langkah besar", "She took the plunge and launched her startup.", "Dia memberanikan diri dan meluncurkan startup-nya.", "Take decisive step", "Courage"),
  ("think twice", "/θɪŋk twaɪs/", "B1", "berpikir dua kali sebelum bertindak ceroboh", "Think twice before signing any agreement.", "Berpikirlah dua kali sebelum menandatangani perjanjian apa pun.", "Consider caution", "Wisdom"),
  ("learn by heart", "/lɜːn baɪ hɑːt/", "A2", "menghafalkan luar kepala", "Actors learn their script lines by heart.", "Aktor menghafal dialog naskah mereka di luar kepala.", "Memorize fully", "Study"),
  ("with flying colours", "/wɪð ˈflaɪ.ɪŋ ˈkʌləz/", "B2", "lulus dengan nilai sangat gemilang", "She graduated with flying colours.", "Dia lulus kuliah dengan nilai yang sangat gemilang.", "Pass brilliantly", "Success"),
  ("bridge the gap", "/brɪdʒ ðə ɡæp/", "B2", "menjembatani kesenjangan atau jurang pemisah", "Scholarships bridge the gap for gifted youth.", "Beasiswa menjembatani kesenjangan bagi pemuda berbakat.", "Overcome disparity", "Society"),
  ("snowed under", "/snəʊd ˈʌndə/", "B2", "kewalahan tertimbun banyak pekerjaan", "The team was snowed under during tax season.", "Tim kewalahan tertimbun pekerjaan selama musim pajak.", "Overloaded with tasks", "Work"),
  ("weigh sth up", "/weɪ ʌp/", "B2", "menimbang baik buruknya berbagai pilihan", "Weigh up the risks before trading stocks.", "Timbanglah risiko baik-baik sebelum bertransaksi saham.", "Assess alternatives", "Decisions"),
  ("at stake", "/æt steɪk/", "B2", "sedang dipertaruhkan status atau nasibnya", "Our reputation is at stake in this deal.", "Reputasi kita sedang dipertaruhkan dalam kesepakatan ini.", "At risk of loss", "Importance"),
  ("come clean", "/kʌm kliːn/", "B2", "berterus terang dan mengakui kesalahan", "He decided to come clean with his manager.", "Dia memutuskan untuk berterus terang kepada manajernya.", "Confess honestly", "Honesty"),
  ("blurt sth out", "/blɜːt aʊt/", "B2", "keceplosan mengatakan rahasia", "She blurted out the surprise party details.", "Dia keceplosan membeberkan rincian pesta kejutan.", "Utter impulsively", "Speech"),
  ("stick around", "/stɪk əˈraʊnd/", "B1", "tetap tinggal dan tidak buru-buru pergi", "Stick around for the Q&A panel.", "Tetaplah tinggal untuk sesi tanya jawab.", "Remain nearby", "Presence"),
  ("embark on sth", "/ɪmˈbɑːk ɒn/", "B2", "memulai petualangan atau babak baru", "Graduates embarked on their professional journeys.", "Para wisudawan memulai babak baru perjalanan profesional mereka.", "Begin adventure", "Beginnings")
]

phrasal_verbs = []
for idx, (term, ipa, level, meaning_id, ex_en, ex_id, hint, cat) in enumerate(phrasal_verbs_list):
  phrasal_verbs.append({
    "id": f"pv-{idx+1:03d}",
    "term": term,
    "ipa": ipa,
    "type": "phrasal_verb",
    "pos": "verb" if not any(x in term for x in ["breakthrough", "bystander", "handout", "letdown", "upkeep", "knockout"]) else "noun",
    "level": level,
    "category": cat,
    "meaningId": meaning_id,
    "exampleEn": ex_en,
    "exampleId": ex_id,
    "hint": hint
  })

# 2. Comprehensive Collocations
collocations_list = [
  ("pay attention", "/peɪ əˈtenʃn/", "verb+noun", "A2", "memperhatikan / menyimak dengan saksama", "Pay attention to the teacher's explanation.", "Perhatikan baik-baik penjelasan dari gurumu.", "Focus & Learning"),
  ("make an effort", "/meɪk ən ˈefət/", "verb+noun", "B1", "berusaha keras / mengerahkan daya upaya", "You must make an effort to improve fluency.", "Kamu harus berusaha keras untuk meningkatkan kelancaran.", "Effort"),
  ("do business", "/duː ˈbɪznəs/", "verb+noun", "B1", "menjalin urusan bisnis / berniaga", "We look forward to doing business together.", "Kami menantikan untuk berbisnis bersama.", "Commerce"),
  ("take advantage of", "/teɪk ədˈvɑːntɪdʒ əv/", "verb+noun", "B1", "memanfaatkan peluang dengan bijak", "Take advantage of these free practice materials.", "Manfaatkan bahan latihan gratis ini dengan bijak.", "Opportunities"),
  ("bear in mind", "/beə ɪn maɪnd/", "verb+prep", "B2", "mengingat dan mempertimbangkan hal penting", "Bear in mind that flight seats are limited.", "Ingat dan pertimbangkan bahwa kursi penerbangan terbatas.", "Mindset"),
  ("keep in touch", "/kiːp ɪn tʌtʃ/", "verb+prep", "B1", "tetap saling berkabar dan menjaga kontak", "Let's keep in touch through video calls.", "Mari tetap saling berkabar lewat panggilan video.", "Friendship"),
  ("raise awareness", "/reɪz əˈweənəs/", "verb+noun", "B2", "meningkatkan kesadaran masyarakat", "The festival raised awareness about recycling.", "Festival ini meningkatkan kesadaran tentang daur ulang.", "Advocacy"),
  ("pose a threat", "/pəʊz ə θret/", "verb+noun", "B2", "menimbulkan atau menjadi ancaman bahaya", "Invasive species pose a threat to native birds.", "Spesies invasif menimbulkan ancaman bagi burung lokal.", "Risk"),
  ("break a habit", "/breɪk ə ˈhæbɪt/", "verb+noun", "B1", "menghentikan kebiasaan buruk", "It requires persistence to break an old habit.", "Dibutuhkan kegigihan untuk menghentikan kebiasaan lama.", "Habits"),
  ("cast doubt on", "/kɑːst daʊt ɒn/", "verb+noun", "B2", "menimbulkan keraguan terhadap kebenaran", "New findings cast doubt on previous assumptions.", "Temuan baru menimbulkan keraguan atas asumsi sebelumnya.", "Skepticism"),
  ("meet expectations", "/miːt ˌekspekˈteɪʃnz/", "verb+noun", "B2", "memenuhi ekspektasi atau harapan", "The concert exceeded our wild expectations.", "Konser tersebut bahkan melampaui seluruh ekspektasi kami.", "Performance"),
  ("draw a conclusion", "/drɔː ə kənˈkluːʒn/", "verb+noun", "B2", "menarik kesimpulan berdasarkan bukti", "Do not draw a conclusion prematurely.", "Jangan menarik kesimpulan secara tergesa-gesa.", "Logic"),
  ("reach a consensus", "/riːtʃ ə kənˈsensəs/", "verb+noun", "B2", "mencapai mufakat atau kesepakatan bersama", "The board reached a consensus on future goals.", "Dewan direksi mencapai mufakat terkait sasaran masa depan.", "Consensus"),
  ("catch someone's eye", "/kætʃ wʌnz aɪ/", "verb+noun", "B1", "menarik perhatian pandangan seseorang", "A bright turquoise dress caught her eye.", "Gaun pirus cerah menarik perhatian pandangannya.", "Visual"),
  ("commit a crime", "/kəˈmɪt ə kraɪm/", "verb+noun", "B1", "melakukan tindak pidana kejahatan", "He was convicted for committing the crime.", "Dia divonis bersalah karena melakukan kejahatan tersebut.", "Law"),
  ("take into account", "/teɪk ˈɪntə əˈkaʊnt/", "verb+prep", "B2", "mempertimbangkan faktor dalam analisis", "We must take all travel expenses into account.", "Kita harus memperhitungkan seluruh biaya perjalanan.", "Planning"),
  ("run a risk", "/rʌn ə rɪsk/", "verb+noun", "B2", "menanggung atau mengambil risiko", "Unlicensed drivers run a risk of heavy fines.", "Pengemudi tanpa SIM menanggung risiko denda berat.", "Caution"),
  ("set an example", "/set ən ɪɡˈzɑːmpl/", "verb+noun", "B1", "memberi teladan yang baik bagi orang lain", "Older siblings should set an example for toddlers.", "Kakak sulung hendaknya memberi teladan bagi adik-adiknya.", "Leadership"),
  ("voice concern", "/vɔɪs kənˈsɜːn/", "verb+noun", "B2", "menyuarakan kekhawatiran secara terbuka", "Residents voiced concern about water shortages.", "Warga menyuarakan kekhawatiran tentang krisis air bersih.", "Society"),
  ("strike a balance", "/straɪk ə ˈbæləns/", "verb+noun", "B2", "menjaga keseimbangan yang tepat", "Strike a balance between leisure and hard study.", "Jagalah keseimbangan antara rekreasi dan belajar giat.", "Harmony"),
  ("break the ice", "/breɪk ði aɪs/", "verb+noun", "B1", "mencairkan suasana kaku saat pertama jumpa", "A warm joke quickly broke the ice.", "Lelucon hangat mencairkan suasana dengan cepat.", "Social"),
  ("take a toll on", "/teɪk ə təʊl/", "verb+noun", "B2", "memberikan dampak buruk bagi kesehatan", "Working overnight shifts takes a toll on sleep.", "Bekerja lembur malam berdampak buruk pada pola tidur.", "Health"),
  ("make a breakthrough", "/meɪk ə ˈbreɪkθruː/", "verb+noun", "B2", "mencapai kemajuan penting / terobosan", "Engineers made a breakthrough in battery storage.", "Para insinyur mencapai terobosan pada penyimpanan baterai.", "Innovation"),
  ("jump to conclusions", "/dʒʌmp tə kənˈkluːʒnz/", "verb+noun", "B2", "terburu-buru menyimpulkan tanpa bukti", "Gather verified facts before jumping to conclusions.", "Kumpulkan fakta sahih sebelum terburu-buru menyimpulkan.", "Judgment"),
  ("shed light on", "/ʃed laɪt ɒn/", "verb+prep", "B2", "memberikan kejelasan atau titik terang", "DNA testing shed light on unresolved cold cases.", "Tes DNA memberikan titik terang pada kasus lama yang buntu.", "Clarity"),
  ("strike a deal", "/straɪk ə diːl/", "verb+noun", "C1", "mencapai kesepakatan transaksi yang saling untung", "The two tech firms struck a multi-million deal.", "Kedua perusahaan teknologi menyepakati transaksi jutaan dolar.", "Business (C1)"),
  ("wreak havoc", "/riːk ˈhævək/", "verb+noun", "C1", "menimbulkan kekacauan dan kehancuran parah", "The cyclone wreaked havoc across island villages.", "Angin siklon itu menimbulkan kehancuran parah di desa-desa pulau.", "Destruction (C1)"),
  ("exercise caution", "/ˈeksəsaɪz ˈkɔːʃn/", "verb+noun", "C1", "menerapkan kehati-hatian tingkat tinggi", "Investors must exercise caution in volatile markets.", "Investor wajib berhati-hati di pasar yang tidak menentu.", "Prudence (C1)"),
  ("muster courage", "/ˈmʌstə ˈkʌrɪdʒ/", "verb+noun", "C1", "mengumpulkan segenap keberanian batin", "She mustered the courage to resign and start a firm.", "Dia mengumpulkan keberanian untuk mundur dan merintis usaha.", "Bravery (C1)"),
  ("harbor doubt", "/ˈhɑːbə daʊt/", "verb+noun", "C1", "menyimpan keraguan dalam hati", "Critics harbor doubts about the treaty's efficacy.", "Kritikus menyimpan keraguan atas keefektifan pakta itu.", "Skepticism (C1)"),
  ("yield results", "/jiːld rɪˈzʌlts/", "verb+noun", "C1", "membuahkan hasil nyata dan memuaskan", "Continuous deliberate practice yields results.", "Latihan terarah yang konsisten akan membuahkan hasil nyata.", "Achievement (C1)"),
  ("heavy rain", "/ˈhevi reɪn/", "adj+noun", "A2", "hujan deras / lebat", "Heavy rain drenched the botanical garden.", "Hujan deras mengguyur taman botani itu.", "Weather"),
  ("golden opportunity", "/ˈɡəʊldən ˌɒpəˈtjuːnəti/", "adj+noun", "B2", "kesempatan emas yang sangat berharga", "Studying in Oxford is a golden opportunity.", "Belajar di Oxford adalah sebuah kesempatan emas.", "Career"),
  ("high priority", "/haɪ praɪˈɒrəti/", "adj+noun", "B1", "prioritas tinggi yang diutamakan", "Clean drinking water is an urgent high priority.", "Air minum bersih adalah prioritas tinggi yang mendesak.", "Urgency"),
  ("fierce competition", "/fɪəs ˌkɒmpəˈtɪʃn/", "adj+noun", "B2", "persaingan yang sangat sengit", "Automakers face fierce competition in electric cars.", "Pabrikan mobil menghadapi persaingan sengit pada mobil listrik.", "Market"),
  ("profound effect", "/prəˈfaʊnd ɪˈfekt/", "adj+noun", "B2", "dampak yang sangat mendalam dan luas", "Great teachers leave a profound effect on pupils.", "Guru hebat meninggalkan dampak mendalam pada murid-muridnya.", "Impact"),
  ("wide variety", "/waɪd vəˈraɪəti/", "adj+noun", "B1", "aneka ragam pilihan yang berlimpah", "The market sells a wide variety of fresh herbs.", "Pasar ini menjual aneka ragam rempah-rempah segar.", "Variety"),
  ("valid point", "/ˈvælɪd pɔɪnt/", "adj+noun", "B2", "poin argumen yang logis dan masuk akal", "You made a very valid point regarding costs.", "Kamu menyampaikan poin yang sangat masuk akal soal biaya.", "Debate"),
  ("severe damage", "/sɪˈvɪə ˈdæmɪdʒ/", "adj+noun", "B2", "kerusakan yang amat parah dan merugikan", "Hailstorms inflicted severe damage on orchard crops.", "Hujan es menimbulkan kerusakan parah pada tanaman kebun.", "Loss"),
  ("prime example", "/praɪm ɪɡˈzɑːmpl/", "adj+noun", "B2", "contoh utama yang paling sempurna", "Her integrity is a prime example for the staff.", "Integritasnya adalah contoh utama yang patut ditiru staf.", "Model"),
  ("deep regret", "/diːp rɪˈɡret/", "adj+noun", "B2", "penyesalan yang amat mendalam", "He expressed deep regret over his impulsive choice.", "Dia menyampaikan penyesalan mendalam atas pilihannya yang impulsif.", "Remorse"),
  ("slight chance", "/slaɪt tʃɑːns/", "adj+noun", "B1", "peluang kecil / kemungkinan tipis", "There is a slight chance of light afternoon mist.", "Ada peluang kecil kabut tipis di sore hari.", "Odds"),
  ("crucial role", "/ˈkruːʃl rəʊl/", "adj+noun", "B2", "peranan penting penentu kesuksesan", "Volunteers play a crucial role in disaster relief.", "Relawan memainkan peran penting dalam penanggulangan bencana.", "Importance"),
  ("bitter disappointment", "/ˈbɪtə ˌdɪsəˈpɔɪntmənt/", "adj+noun", "B2", "kekecewaan yang amat pahit dan menyakitkan", "Losing the semifinal was a bitter disappointment.", "Gagal di semifinal merupakan kekecewaan yang sangat pahit.", "Sadness"),
  ("sound advice", "/saʊnd ədˈvaɪs/", "adj+noun", "B2", "nasihat bijak dan dapat diandalkan", "Listen closely to your grandfather's sound advice.", "Dengarkan baik-baik nasihat bijak dari kakekmu.", "Wisdom"),
  ("steep learning curve", "/stiːp ˈlɜːnɪŋ kɜːv/", "adj+noun", "B2", "proses belajar yang menantang di awal", "Coding in Rust has a steep learning curve.", "Memprogram dengan Rust memiliki tantangan belajar yang tinggi di awal.", "Education"),
  ("unanimous decision", "/juˈnænɪməs dɪˈsɪʒn/", "adj+noun", "B2", "keputusan bulat yang disepakati bersama", "The jury reached a unanimous decision today.", "Dewan juri mencapai keputusan bulat hari ini.", "Consensus"),
  ("pressing issue", "/ˈpresɪŋ ˈɪʃuː/", "adj+noun", "C1", "isu mendesak yang butuh solusi segera", "Urban affordable housing is a pressing issue.", "Perumahan terjangkau di perkotaan adalah isu yang sangat mendesak.", "Politics (C1)"),
  ("daunting task", "/ˈdɔːntɪŋ tɑːsk/", "adj+noun", "C1", "tugas besar yang membuat gentar", "Translating the ancient encyclopedia is a daunting task.", "Menerjemahkan ensiklopedia kuno itu tugas yang membuat gentar.", "Challenges (C1)"),
  ("stark contrast", "/stɑːk ˈkɒntrɑːst/", "adj+noun", "C1", "perbedaan kontras yang sangat mencolok", "Her calm mood stood in stark contrast to the panic.", "Sikap tenangnya sangat kontras mencolok dengan kepanikan di sekitar.", "Contrast (C1)"),
  ("unprecedented crisis", "/ʌnˈpresɪdentɪd ˈkraɪsɪs/", "adj+noun", "C1", "krisis luar biasa yang belum pernah terjadi", "The famine triggered an unprecedented crisis.", "Bencana kelaparan itu memicu krisis yang belum pernah terjadi.", "History (C1)"),
  ("lingering doubt", "/ˈlɪŋɡərɪŋ daʊt/", "adj+noun", "C1", "keraguan yang terus membekas dalam benak", "He could not shake a lingering doubt in his heart.", "Dia tidak bisa menepis keraguan yang terus membekas di hatinya.", "Mindset (C1)"),
  ("deeply concerned", "/ˈdiːpli kənˈsɜːnd/", "adv+adj", "B2", "sangat khawatir dan menaruh perhatian", "Pediatricians are deeply concerned about screen time.", "Dokter anak sangat khawatir terhadap waktu menatap layar gawai.", "Worry"),
  ("highly recommended", "/ˈhaɪli ˌrekəˈmendɪd/", "adv+adj", "B1", "sangat dianjurkan / direkomendasikan", "The grammar book is highly recommended for IELTS.", "Buku tata bahasa ini sangat direkomendasikan untuk IELTS.", "Praise"),
  ("bitterly disappointed", "/ˈbɪtəli ˌdɪsəˈpɔɪntɪd/", "adv+adj", "B2", "amat sangat kecewa dan terpukul", "She was bitterly disappointed by the cancellation.", "Dia amat sangat kecewa atas pembatalan acara tersebut.", "Emotions"),
  ("strictly forbidden", "/ˈstrɪktli fəˈbɪdn/", "adv+adj", "B2", "dilarang keras tanpa pengecualian", "Smoking is strictly forbidden on petrol forecourts.", "Merokok dilarang keras di area pom bensin.", "Rules"),
  ("painfully obvious", "/ˈpeɪnfəli ˈɒbviəs/", "adv+adj", "B2", "sangat kentara dan jelas sekali", "It was painfully obvious that he forgot the slides.", "Sangat kentara jelas bahwa dia lupa membawa slide presentasi.", "Clarity"),
  ("utterly ridiculous", "/ˈʌtəli rɪˈdɪkjələs/", "adv+adj", "B2", "sama sekali konyol dan tak masuk akal", "Paying double for the same service is utterly ridiculous.", "Membayar dua kali lipat untuk layanan serupa sama sekali tak masuk akal.", "Absurdity"),
  ("fully aware", "/ˈfʊli əˈweə(r)/", "adv+adj", "B2", "sadar sepenuhnya atas situasi yang dihadapi", "Pilots are fully aware of turbulence protocols.", "Pilot sadar sepenuhnya atas protokol saat turbulensi.", "Consciousness"),
  ("sorely tempted", "/ˈsɔːli ˈtemptɪd/", "adv+adj", "B2", "sangat tergoda untuk melakukan sesuatu", "I was sorely tempted to eat the last cupcake.", "Aku sangat tergoda untuk memakan kue mangkuk terakhir itu.", "Temptation"),
  ("heavily dependent", "/ˈhevɪli dɪˈpendənt/", "adv+adj", "B2", "sangat bergantung sepenuhnya pada pihak lain", "The colony was heavily dependent on imported grain.", "Koloni itu sangat bergantung pada impor biji-bijian.", "Reliance"),
  ("widely acclaimed", "/ˈwaɪdli əˈkleɪmd/", "adv+adj", "C1", "diakui secara luas dan menuai pujian", "The director's latest film was widely acclaimed.", "Film terbaru sang sutradara menuai pujian luas di seluruh dunia.", "Arts (C1)"),
  ("blatantly obvious", "/ˈbleɪtəntli ˈɒbviəs/", "adv+adj", "C1", "terang-terangan terlihat jelas tanpa keraguan", "The accounting discrepancy was blatantly obvious.", "Ketidakcocokan laporan akuntansi itu terang-terangan terlihat jelas.", "Clarity (C1)"),
  ("strictly confidential", "/ˈstrɪktli ˌkɒnfɪˈdenʃl/", "adv+adj", "C1", "sangat rahasia dan tidak boleh dibocorkan", "Patient medical data is strictly confidential.", "Data medis pasien bersifat sangat rahasia.", "Privacy (C1)"),
  ("fiercely competitive", "/ˈfɪəsli kəmˈpetətɪv/", "adv+adj", "C1", "sangat kompetitif dan bersaing keras", "Fintech careers are fiercely competitive.", "Karier di bidang teknologi finansial sangat kompetitif.", "Careers (C1)"),
  ("painstakingly slow", "/ˈpeɪnzteɪkɪŋli sləʊ/", "adv+adj", "C1", "sangat lambat dan menuntut ketelitian tinggi", "Restoring ancient oil murals is painstakingly slow.", "Merestorasi lukisan mural kuno berjalan amat sangat lambat.", "Effort (C1)"),
  ("strictly adhere to", "/ˈstrɪktli ədˈhɪə tuː/", "verb+prep", "B2", "mematuhi secara ketat pedoman resmi", "Surgeons strictly adhere to sanitation guidelines.", "Dokter bedah mematuhi panduan sanitasi secara ketat.", "Rules"),
  ("strongly recommend", "/ˈstrɒŋli ˌrekəˈmend/", "verb+adv", "B1", "sangat menganjurkan / merekomendasikan", "We strongly recommend backing up weekly.", "Kami sangat menyarankan untuk mencadangkan data mingguan.", "Advice"),
  ("apologize profusely", "/əˈpɒlədʒaɪz prəˈfjuːsli/", "verb+adv", "B2", "meminta maaf berkali-kali dengan tulus", "He apologized profusely for spilling his drink.", "Dia meminta maaf berkali-kali karena menumpahkan minumannya.", "Courtesy"),
  ("cope with", "/kəʊp wɪð/", "verb+prep", "B2", "mengatasi dan bertahan menghadapi beban berat", "Regular sport helps athletes cope with stress.", "Olahraga teratur membantu atlet mengatasi tekanan stres.", "Resilience"),
  ("stem from", "/stem frɒm/", "verb+prep", "B2", "bersumber atau berakar dari suatu penyebab", "Many disputes stem from simple miscommunication.", "Banyak perselisihan bersumber dari miskomunikasi sederhana.", "Causality"),
  ("refrain from", "/rɪˈfreɪn frɒm/", "verb+prep", "B2", "menahan diri agar tidak melakukan sesuatu", "Please refrain from smoking inside public areas.", "Harap menahan diri untuk tidak merokok di ruang publik.", "Restraint"),
  ("delve into", "/delv ˈɪntuː/", "verb+prep", "C1", "menyelidiki dan mendalami subjek secara tuntas", "The scholar delved into medieval manuscripts.", "Cendekiawan itu mendalami naskah-naskah abad pertengahan.", "Research (C1)"),
  ("grapple with", "/ˈɡræpl wɪð/", "verb+prep", "C1", "bergulat keras memecahkan masalah pelik", "Nations grapple with energy transition problems.", "Negara-negara bergulat keras dengan masalah transisi energi.", "Struggle (C1)"),
  ("culminate in", "/ˈkʌlmɪneɪt ɪn/", "verb+prep", "C1", "mencapai puncak kulminasi pada suatu hasil", "Years of study culminated in a doctoral degree.", "Tahun-tahun studi akhirnya berpuncak pada gelar doktoral.", "Culmination (C1)")
]

collocations = []
for idx, (term, ipa, pos, level, meaning_id, ex_en, ex_id, cat) in enumerate(collocations_list):
  collocations.append({
    "id": f"col-{idx+1:03d}",
    "term": term,
    "ipa": ipa,
    "type": "collocation",
    "pos": pos,
    "level": level,
    "category": cat,
    "meaningId": meaning_id,
    "exampleEn": ex_en,
    "exampleId": ex_id,
    "hint": f"Pattern: {pos}"
  })

# 3. Oxford Vocabulary - Vast list covering A1 through C2
# Let's import the extensive word list
with open(os.path.join(current_dir, 'build_huge_database.py'), 'r', encoding='utf-8') as f:
  content = f.read()

# Load oxford_words_data from build_huge_database.py
import importlib.util
spec = importlib.util.spec_from_file_location("build_huge", os.path.join(current_dir, "build_huge_database.py"))
huge_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(huge_module)

base_oxford = huge_module.oxford_words_data

# Additional curated Oxford 3000 & 5000 words (including C1 & C2)
additional_oxford = [
  ("abandon", "/əˈbændən/", "verb", "B2", "meninggalkan / menelantarkan", "The crew had to abandon the sinking ship.", "Awak kapal terpaksa meninggalkan kapal yang karam itu."),
  ("absorb", "/əbˈzɔːb/", "verb", "B2", "menyerap informasi / cairan", "Sponges absorb water rapidly.", "Spons menyerap air dengan sangat cepat."),
  ("abstract", "/ˈæbstrækt/", "adjective", "B2", "abstrak / bersifat konseptual teoritis", "Philosophy often deals with abstract ideas.", "Filsafat sering kali membahas ide-ide yang abstrak."),
  ("abuse", "/əˈbjuːs/", "noun", "B2", "penyalahgunaan wewenang / perlakuan kejam", "Strict laws prohibit any abuse of power.", "Hukum yang tegas melarang segala bentuk penyalahgunaan wewenang."),
  ("academic", "/ˌækəˈdemɪk/", "adjective", "B1", "akademis / berkaitan dengan keilmuan", "She achieved outstanding academic success.", "Dia meraih prestasi akademis yang sangat cemerlang."),
  ("accelerate", "/əkˈseləreɪt/", "verb", "B2", "mempercepat laju pertumbuhan", "Technological innovations accelerate economic growth.", "Inovasi teknologi mempercepat pertumbuhan ekonomi."),
  ("access", "/ˈækses/", "noun", "B1", "akses / hak izin masuk", "Students have free access to online libraries.", "Siswa memiliki akses gratis ke perpustakaan daring."),
  ("accommodate", "/əˈkɒmədeɪt/", "verb", "B2", "menampung jumlah / menyesuaikan", "The auditorium can accommodate five hundred guests.", "Auditorium tersebut mampu menampung lima ratus tamu."),
  ("accompany", "/əˈkʌmpəni/", "verb", "B2", "menemani / mendampingi perjalanan", "Children must be accompanied by an adult.", "Anak-anak harus didampingi oleh orang dewasa."),
  ("accomplish", "/əˈkʌmplɪʃ/", "verb", "B2", "menyelesaikan tugas dengan sukses", "You can accomplish anything with consistent effort.", "Kamu bisa menyelesaikan apa pun dengan usaha yang konsisten."),
  ("accordance", "/əˈkɔːdns/", "noun", "B2", "kesesuaian / selaras dengan peraturan", "All actions were taken in accordance with law.", "Semua tindakan diambil sesuai dengan hukum yang berlaku."),
  ("account", "/əˈkaʊnt/", "noun", "B1", "rekening / akun / laporan tertulis", "Open a savings account at the local bank.", "Bukalah rekening tabungan di bank setempat."),
  ("accurate", "/ˈækjərət/", "adjective", "B2", "akurat / tepat tanpa keliru", "Provide accurate data for the research report.", "Berikanlah data yang akurat untuk laporan penelitian."),
  ("accuse", "/əˈkjuːz/", "verb", "B2", "menuduh / mendakwa kesalahan", "Do not accuse anyone without solid evidence.", "Jangan menuduh siapa pun tanpa bukti yang kuat."),
  ("acknowledge", "/əkˈnɒlɪdʒ/", "verb", "B2", "mengakui kebenaran suatu fakta", "He acknowledged the contributions of his peers.", "Dia mengakui kontribusi besar dari rekan-rekannya."),
  ("acquire", "/əˈkwaɪə(r)/", "verb", "B2", "memperoleh / menguasai keahlian", "It takes patience to acquire native-like fluency.", "Dibutuhkan kesabaran untuk menguasai kefasihan seperti penutur asli."),
  ("activate", "/ˈæktɪveɪt/", "verb", "B2", "mengaktifkan sistem atau akun", "Click the email link to activate your profile.", "Klik tautan di surel untuk mengaktifkan profil akunmu."),
  ("adapt", "/əˈdæpt/", "verb", "B2", "beradaptasi dengan lingkungan baru", "Organisms adapt to seasonal weather shifts.", "Makhluk hidup beradaptasi dengan perubahan cuaca musiman."),
  ("addition", "/əˈdɪʃn/", "noun", "B1", "penambahan / pelengkap baru", "The new library wing is a great addition.", "Gedung sayap perpustakaan baru adalah penambahan yang luar biasa."),
  ("adequate", "/ˈædɪkwət/", "adjective", "B2", "memadai / cukup untuk kebutuhan", "Ensure you get adequate rest each night.", "Pastikan kamu mendapatkan istirahat yang memadai setiap malam."),
  ("adjust", "/əˈdʒʌst/", "verb", "B2", "menyesuaikan / menyetel setelan", "Adjust the screen brightness to protect your eyes.", "Sesuaikan kecerahan layar demi menjaga kesehatan matamu."),
  ("administration", "/ədˌmɪnɪˈstreɪʃn/", "noun", "B2", "administrasi tata kelola", "The hospital administration streamlined check-in.", "Pihak administrasi rumah sakit mempermudah alur pendaftaran."),
  ("admit", "/ədˈmɪt/", "verb", "B1", "mengakui kesalahan / mengizinkan masuk", "He admitted making a mistake on the ledger.", "Dia mengakui telah melakukan kekeliruan pada buku kas."),
  ("adopt", "/əˈdɒpt/", "verb", "B2", "mengadopsi anak / menerapkan metode baru", "Many schools adopted interactive online apps.", "Banyak sekolah menerapkan aplikasi daring interaktif."),
  ("advance", "/ədˈvɑːns/", "noun", "B2", "kemajuan teknologi pesat", "Medical advances have prolonged life expectancy.", "Kemajuan medis telah memperpanjang angka harapan hidup."),
  ("advocate", "/ˈædvəkeɪt/", "verb", "C1", "membela dan menyuarakan dukungan gigih", "Doctors advocate whole food diets.", "Para dokter menyuarakan dukungan pola makan makanan utuh."),
  ("affect", "/əˈfekt/", "verb", "A2", "mempengaruhi kondisi", "Sleep quality affects daily learning focus.", "Kualitas tidur mempengaruhi fokus belajar sehari-hari."),
  ("agenda", "/əˈdʒendə/", "noun", "B2", "agenda / susunan acara rapat", "Environmental policy is top of the agenda.", "Kebijakan lingkungan berada di urutan teratas agenda."),
  ("aggressive", "/əˈɡresɪv/", "adjective", "B2", "agresif / giat menekan", "The team adopted an aggressive offensive strategy.", "Tim tersebut menerapkan strategi menyerang yang agresif."),
  ("alert", "/əˈlɜːt/", "adjective", "B2", "waspada dan siaga", "Drivers must remain alert on foggy highways.", "Pengemudi wajib tetap waspada di jalan raya yang berkabut."),
  ("allocate", "/ˈæləkeɪt/", "verb", "B2", "mengalokasikan dana / jatah sumber daya", "The city allocated funds for park restoration.", "Pemerintah kota mengalokasikan dana untuk perbaikan taman."),
  ("alter", "/ˈɔːltə(r)/", "verb", "B2", "mengubah susunan / memodifikasi", "Tailors altered the trousers for a tailored fit.", "Penjahit mengubah celana tersebut agar pas di badan."),
  ("alternative", "/ɔːlˈtɜːnətɪv/", "noun", "A2", "alternatif / pilihan lain", "Cycling is an eco-friendly alternative to driving.", "Bersepeda adalah alternatif ramah lingkungan selain mengemudi mobil."),
  ("ambiguous", "/æmˈbɪɡjuəs/", "adjective", "C1", "ambigu / memiliki makna ganda", "Legal contracts avoid ambiguous phrasing.", "Kontrak hukum menghindari susunan kata yang ambigu."),
  ("ambitious", "/æmˈbɪʃəs/", "adjective", "B1", "ambisius / bertekad tinggi", "Ambitious students study with disciplined focus.", "Siswa yang berambisius belajar dengan fokus yang disiplin."),
  ("analogy", "/əˈnælədʒi/", "noun", "C1", "analogi / perumpamaan perbandingan", "The teacher used an analogy to explain electricity.", "Guru tersebut memakai analogi untuk menjelaskan arus listrik."),
  ("anticipate", "/ænˈtɪsɪpeɪt/", "verb", "B2", "mengantisipasi kemungkinan yang terjadi", "We anticipated flight delays and packed books.", "Kami mengantisipasi keterlambatan pesawat dan membawa buku."),
  ("anxiety", "/æŋˈzaɪəti/", "noun", "B2", "kegelisahan rasa cemas mendalam", "Deep breathing exercises alleviate public anxiety.", "Latihan napas dalam meredakan kecemasan di depan umum."),
  ("apparent", "/əˈpærənt/", "adjective", "B2", "tampak jelas / nyata di depan mata", "Her genuine excitement was apparent to everyone.", "Kegembiraannya yang tulus terlihat jelas oleh semua orang."),
  ("appeal", "/əˈpiːl/", "noun", "B2", "daya tarik memikat / banding hukum", "The seaside cottage has immense visual appeal.", "Pondok di tepi pantai itu memiliki daya tarik visual yang besar."),
  ("applaud", "/əˈplɔːd/", "verb", "B2", "bertepuk tangan memuji", "The audience applauded the pianist enthusiastically.", "Penonton bertepuk tangan memuji sang pianis dengan antusias."),
  ("appropriate", "/əˈprəʊpriət/", "adjective", "B2", "sesuai / pantas pada tempatnya", "Wear appropriate formal attire to the interview.", "Kenakan pakaian formal yang pantas saat wawancara."),
  ("approve", "/əˈpruːv/", "verb", "B2", "menyetujui izin permohonan", "The dean approved our research proposal.", "Dekan menyetujui proposal penelitian kami."),
  ("approximate", "/əˈprɒksɪmət/", "adjective", "B1", "perkiraan kira-kira", "The approximate flight duration is three hours.", "Perkiraan durasi penerbangan adalah tiga jam."),
  ("arbitrary", "/ˈɑːbɪtrəri/", "adjective", "C1", "sewenang-wenang tanpa dasar objektif", "Setting arbitrary deadlines stresses employees.", "Menetapkan tenggat sewenang-wenang membuat stres karyawan."),
  ("archive", "/ˈɑːkaɪv/", "noun", "B2", "arsip penyimpanan dokumen sejarah", "Historians sifted through the digital archive.", "Sejarawan memeriksa arsip digital tersebut dengan teliti."),
  ("argue", "/ˈɑːɡjuː/", "verb", "A2", "berdebat mengemukakan argumen", "Scientists argue that renewable energy saves costs.", "Ilmuwan berargumen bahwa energi terbarukan menghemat biaya."),
  ("arise", "/əˈraɪz/", "verb", "B2", "timbul / muncul ke permukaan", "Unexpected questions arose during our presentation.", "Pertanyaan-pertanyaan tak terduga muncul di tengah presentasi kami."),
  ("arrest", "/əˈrest/", "verb", "B1", "menangkap tersangka pidana", "Police arrested the fugitive at the terminal.", "Polisi menangkap buronan tersebut di terminal bus."),
  ("articulate", "/ɑːˈtɪkjuleɪt/", "verb", "C1", "mengutarakan ide secara fasih dan runtut", "She articulates complex legal theories effortlessly.", "Dia mengutarakan teori-teori hukum yang rumit dengan sangat fasih."),
  ("aspect", "/ˈæspekt/", "noun", "B2", "aspek sudut pandang tinjauan", "Grammar is only one aspect of language learning.", "Tata bahasa hanyalah salah satu aspek dalam belajar bahasa."),
  ("assemble", "/əˈsembl/", "verb", "B2", "merakit komponen / berkumpul bersama", "Follow the manual to assemble the office chair.", "Ikuti buku petunjuk untuk merakit kursi kantor tersebut."),
  ("assert", "/əˈsɜːt/", "verb", "B2", "menegaskan kebenaran secara tegas", "The lawyer asserted her client's innocence.", "Pengacara tersebut menegaskan ketidakbersalahan kliennya."),
  ("assess", "/əˈses/", "verb", "B2", "menilai mutu atau capaian", "Quizzes assess vocabulary retention accurately.", "Kuis menilai daya ingat kosakata secara akurat."),
  ("assign", "/əˈsaɪn/", "verb", "B1", "menugaskan mandat tanggung jawab", "The teacher assigned three reading chapters.", "Guru menugaskan tiga bab bacaan untuk dibaca."),
  ("assist", "/əˈsɪst/", "verb", "B1", "membantu mendampingi", "A visual aide assists beginner language students.", "Alat bantu visual membantu para siswa bahasa pemula."),
  ("associate", "/əˈsəʊʃieɪt/", "verb", "B2", "mengaitkan satu hal dengan lainnya", "People associate the aroma of coffee with morning.", "Orang mengaitkan aroma kopi dengan suasana pagi hari."),
  ("assume", "/əˈsjuːm/", "verb", "B2", "mengasumsikan anggapan", "Never assume you know the answer without checking.", "Jangan pernah berasumsi kamu tahu jawabannya tanpa mengecek."),
  ("assure", "/əˈʃɔː(r)/", "verb", "B2", "menjamin dan meyakinkan kepastian", "I assure you the flight is safe and certified.", "Aku meyakinkanmu bahwa penerbangan ini aman dan tersertifikasi."),
  ("astonish", "/əˈstɒnɪʃ/", "verb", "B2", "membuat kagum takjub luar biasa", "Her rapid fluency progress astonished everyone.", "Kemajuan kelancaran bicaranya yang pesat membuat semua orang takjub."),
  ("attach", "/əˈtætʃ/", "verb", "B1", "melampirkan berkas ke surel", "Attach your updated resume to the application email.", "Lampirkan resume terbarumu pada surel lamaran."),
  ("attain", "/əˈteɪn/", "verb", "C1", "mencapai tingkatan kemahiran tinggi", "He attained advanced C2 proficiency in English.", "Dia mencapai kemahiran tingkat lanjut C2 dalam bahasa Inggris."),
  ("attempt", "/əˈtempt/", "noun", "B2", "upaya percobaan melakukan", "Her initial attempt at coding was promising.", "Upaya pertamanya dalam memprogram sangat menjanjikan."),
  ("attend", "/əˈtend/", "verb", "A2", "menghadiri kelas atau konferensi", "Over two hundred delegates attended the symposium.", "Lebih dari dua ratus delegasi menghadiri simposium tersebut."),
  ("attribute", "/əˈtrɪbjuːt/", "verb", "B2", "menghubungkan keberhasilan pada sebab", "She attributes her success to consistent effort.", "Dia menghubungkan kesuksesannya pada kerja keras yang konsisten."),
  ("audacious", "/ɔːˈdeɪʃəs/", "adjective", "C2", "amat berani mengambil langkah ekstrem", "The climber made an audacious solo ascent.", "Pendaki itu melakukan pendakian solo yang sangat berani."),
  ("augment", "/ɔːɡˈment/", "verb", "C2", "memperbesar / menambah kapasitas", "Companies augment human work with artificial intelligence.", "Perusahaan-perusahaan menambah kapasitas kerja manusia dengan kecerdasan buatan."),
  ("authentic", "/ɔːˈθentɪk/", "adjective", "B2", "autentik / asli tulen tanpa rekayasa", "Experience authentic native speech with audio.", "Rasakan pelafalan asli penutur bahasa Inggris dengan audio."),
  ("authorize", "/ˈɔːθəraɪz/", "verb", "B2", "memberikan izin wewenang resmi", "Only managers can authorize travel reimbursements.", "Hanya manajer yang berwenang menyetujui penggantian biaya dinas."),
  ("autonomous", "/ɔːˈtɒnəməs/", "adjective", "C1", "otonom / mandiri bergerak tanpa disetir", "Autonomous electric vehicles cruise city streets.", "Kendaraan listrik otonom melaju di jalanan kota tanpa sopir."),
  ("avail", "/əˈveɪl/", "verb", "C1", "memanfaatkan faedah peluang", "Avail yourself of these extensive learning materials.", "Manfaatkan materi belajar yang sangat lengkap ini sebaik-baiknya."),
  ("avenue", "/ˈævənjuː/", "noun", "B2", "jalan raya lebar / sarana jalur opsi", "Language learning opens new avenues for careers.", "Belajar bahasa membuka jalur-jalur baru bagi peluang karier."),
  ("avert", "/əˈvɜːt/", "verb", "C1", "mencegah terjadinya malapetaka", "Swift diplomacy averted an international crisis.", "Diplomasi yang cepat mencegah terjadinya krisis internasional."),
  ("avid", "/ˈævɪd/", "adjective", "C1", "sangat gemar dan antusias tinggi", "She is an avid reader of classic literature.", "Dia adalah pembaca yang sangat antusias membaca sastra klasik."),
  ("barrier", "/ˈbæriə(r)/", "noun", "B2", "penghalang rintangan hambatan", "Language barriers diminish with steady practice.", "Rintangan bahasa akan surut seiring latihan yang konsisten."),
  ("benchmark", "/ˈbentʃmɑːk/", "noun", "C1", "tolok ukur standar acuan mutu", "The Oxford CEFR scale is a global learning benchmark.", "Skala CEFR Oxford adalah tolok ukur belajar global."),
  ("beneficial", "/ˌbenɪˈfɪʃl/", "adjective", "B2", "bermanfaat dan berfaedah positif", "Reading aloud is highly beneficial for pronunciation.", "Membaca nyaring sangat bermanfaat bagi perbaikan pelafalan."),
  ("betray", "/bɪˈtreɪ/", "verb", "B2", "mengkhianati janji / membocorkan rahasia", "His nervous shaking betrayed his hidden fear.", "Gemetar gugupnya membocorkan ketakutan yang tersembunyi."),
  ("bizarre", "/bɪˈzɑː(r)/", "adjective", "B2", "aneh ganjil di luar nalar", "The mystery novel had a bizarre ending.", "Novel misteri tersebut memiliki akhir cerita yang sangat ganjil."),
  ("bolster", "/ˈbəʊlstə(r)/", "verb", "C1", "memperkuat dan menyokong daya tahan", "Daily practice bolsters your speaking confidence.", "Latihan setiap hari memperkuat rasa percaya dirimu saat berbicara."),
  ("boundary", "/ˈbaʊndri/", "noun", "B2", "garis batas wilayah atau etika", "Respect personal boundaries in team dialogue.", "Hormatilah batasan pribadi dalam dialog bersama tim."),
  ("burden", "/ˈbɜːdn/", "noun", "B2", "beban berat pikiran atau finansial", "Sharing worries eases the psychological burden.", "Berbagi kekhawatiran meringankan beban psikologis di hati."),
  ("campaign", "/kæmˈpeɪn/", "noun", "B1", "kampanye sosialisasi terarah", "The health ministry launched a nutrition campaign.", "Kementerian kesehatan meluncurkan kampanye gizi masyarakat."),
  ("captivate", "/ˈkæptɪveɪt/", "verb", "C1", "memikat hati dan memesona", "Her eloquent storytelling captivated the crowd.", "Tutur katanya yang memikat memesona para hadirin."),
  ("catastrophe", "/kəˈtæstrəfi/", "noun", "C1", "malapetaka bencana dahsyat", "Prompt evacuations averted a human catastrophe.", "Evakuasi yang sigap mencegah timbulnya malapetaka korban jiwa."),
  ("cautious", "/ˈkɔːʃəs/", "adjective", "B2", "berhati-hati penuh kewaspadaan", "Be cautious when investing in new crypto ventures.", "Berhati-hatilah saat berinvestasi di usaha kripto baru."),
  ("census", "/ˈsensəs/", "noun", "B2", "sensus pendataan resmi penduduk", "The national census tallies population demographics.", "Sensus nasional mendata demografi seluruh penduduk."),
  ("chronic", "/ˈkrɒnɪk/", "adjective", "B2", "kronis menahun dan berkepanjangan", "Physiotherapy alleviates chronic lower back ache.", "Fisioterapi meringankan nyeri punggung bawah yang menahun."),
  ("clarify", "/ˈklærəfaɪ/", "verb", "B2", "mengklarifikasi agar jelas terang", "Could you clarify the second clause of the treaty?", "Bisakah Anda mengklarifikasi klausul kedua dari perjanjian ini?"),
  ("clause", "/klɔːz/", "noun", "B1", "klausul kalimat / pasal kontrak", "The contract contains a confidentiality clause.", "Kontrak tersebut memuat klausul kerahasiaan data."),
  ("coalition", "/ˌkəʊəˈlɪʃn/", "noun", "C1", "koalisi gabungan beberapa pihak", "The green coalition advocated carbon taxes.", "Koalisi partai hijau memperjuangkan pajak karbon."),
  ("cognitive", "/ˈkɒɡnətɪv/", "adjective", "C1", "kognitif berkaitan daya nalar otak", "Puzzles boost cognitive agility in seniors.", "Teka-teki mengasah kelincahan kognitif pada para lansia."),
  ("coincide", "/ˌkəʊɪnˈsaɪd/", "verb", "B2", "bertepatan waktu secara bersamaan", "The festival coincides with our summer holiday.", "Festival tersebut bertepatan waktu dengan liburan musim panas kami."),
  ("collaborate", "/kəˈlæbəreɪt/", "verb", "B2", "berkolaborasi bekerja sama", "Researchers collaborate across five universities.", "Para peneliti berkolaborasi melintasi lima universitas."),
  ("collapse", "/kəˈlæps/", "verb", "B2", "roboh / runtuh seketika", "The dilapidated wooden barn collapsed in storm.", "Gudang kayu yang lapuk itu runtuh diterjang badai."),
  ("commence", "/kəˈmens/", "verb", "C1", "memulai secara formal khidmat", "Ceremonies will commence promptly at ten.", "Upacara akan dimulai tepat pada pukul sepuluh."),
  ("commend", "/kəˈmend/", "verb", "C1", "memuji dan mengapresiasi kinerja", "The chief commended the firefighters for courage.", "Pimpinan memuji para petugas damkar atas keberanian mereka."),
  ("commodity", "/kəˈmɒdəti/", "noun", "C1", "komoditas barang dagang berharga", "Clean water is our most precious commodity.", "Air bersih adalah komoditas kita yang paling berharga."),
  ("compatible", "/kəmˈpætəbl/", "adjective", "B2", "kompatibel / cocok serasi", "Make sure your browser is compatible with the app.", "Pastikan perambanmu kompatibel dengan aplikasi ini."),
  ("compel", "/kəmˈpel/", "verb", "C1", "memaksa secara moral atau hukum", "Evidence compelled him to speak the plain truth.", "Bukti yang ada memaksanya untuk berkata jujur apa adanya."),
  ("compensate", "/ˈkɒmpənseɪt/", "verb", "B2", "memberi ganti rugi kompensasi", "Airlines compensated travelers for lost luggage.", "Maskapai memberi ganti rugi kepada penumpang atas koper yang hilang."),
  ("compile", "/kəmˈpaɪl/", "verb", "B2", "mengumpulkan dan menyusun data", "Linguists compiled a dictionary of idiomatic phrases.", "Ahli bahasa menyusun kamus berisi frasa-frasa idiomatis."),
  ("comply", "/kəmˈplaɪ/", "verb", "B2", "mematuhi ketentuan hukum", "All vessels must comply with maritime protocols.", "Semua kapal wajib mematuhi protokol maritim internasional."),
  ("component", "/kəmˈpəʊnənt/", "noun", "B2", "komponen unsur penyusun", "Vocabulary is a vital component of fluency.", "Kosakata adalah komponen terpenting dari kefasihan berbahasa."),
  ("compromise", "/ˈkɒmprəmaɪz/", "noun", "B2", "kompromi jalan tengah bersama", "Diplomats negotiated a fair compromise.", "Diplomat merundingkan jalan tengah yang adil bagi kedua belah pihak."),
  ("compulsory", "/kəmˈpʌlsəri/", "adjective", "B2", "wajib / mutlak diharuskan", "Seatbelt usage is compulsory for all passengers.", "Pemakaian sabuk pengaman diwajibkan bagi seluruh penumpang."),
  ("conceal", "/kənˈsiːl/", "verb", "B2", "menyembunyikan dari pandangan", "He concealed his disappointment behind a warm smile.", "Dia menyembunyikan kekecewaannya di balik senyum hangat."),
  ("concede", "/kənˈsiːd/", "verb", "C1", "mengakui keunggulan lawan / mengalah", "The incumbent conceded defeat graciously.", "Petahana mengakui kekalahannya dengan lapang dada."),
  ("conceive", "/kənˈsiːv/", "verb", "C1", "menggagas ide dalam benak pikiran", "Inventors conceived of a pocket computer.", "Para penemu menggagas ide komputer seukuran saku."),
  ("concrete", "/ˈkɒŋkriːt/", "adjective", "B2", "konkret / nyata bukan sekadar teori", "Provide concrete examples for each vocabulary card.", "Berikanlah contoh konkret pada setiap kartu kosakata."),
  ("condemn", "/kənˈdem/", "verb", "B2", "mengecam keras perbuatan tercela", "World leaders condemned the terrorist attack.", "Para pemimpin dunia mengecam keras serangan teror tersebut."),
  ("condense", "/kənˈdens/", "verb", "C1", "meringkas teks panjang menjadi padat", "Condense the article into five key bullet points.", "Ringkaslah artikel tersebut menjadi lima poin utama yang padat."),
  ("confer", "/kənˈfɜː(r)/", "verb", "C1", "berunding bersama / menganugerahkan gelar", "Judges conferred before naming the winner.", "Para juri berunding terlebih dahulu sebelum mengumumkan pemenang."),
  ("confess", "/kənˈfes/", "verb", "B2", "mengakui kesalahan dengan jujur", "He confessed to feeling nervous during interviews.", "Dia mengaku jujur bahwa dia merasa gugup saat wawancara."),
  ("confine", "/kənˈfaɪn/", "verb", "B2", "membatasi ruang gerak / mengurung", "Please confine your remarks to today's agenda.", "Harap batasi komentar Anda pada agenda hari ini saja."),
  ("conform", "/kənˈfɔːm/", "verb", "B2", "menyesuaikan diri dengan standar baku", "All building plans must conform to seismic codes.", "Semua denah bangunan wajib mematuhi standar tahan gempa."),
  ("confront", "/kənˈfrʌnt/", "verb", "B2", "berani menghadapi masalah secara langsung", "She confronted her fears and spoke before five hundred.", "Dia menghadapi rasa takutnya dan berpidato di depan lima ratus orang."),
  ("confuse", "/kənˈfjuːz/", "verb", "B1", "membingungkan pikiran", "Similar spellings often confuse language beginners.", "Ejaan yang mirip kerap membingungkan para pembelajar pemula."),
  ("consecutive", "/kənˈsekjətɪv/", "adjective", "B2", "berurutan berturut-turut tanpa jeda", "She won the championship three consecutive years.", "Dia menjuarai kejuaraan itu tiga tahun berturut-turut."),
  ("consent", "/kənˈsent/", "noun", "B2", "persetujuan izin resmi", "Medical treatments require signed informed consent.", "Tindakan medis mensyaratkan lembar persetujuan yang ditandatangani."),
  ("console", "/kənˈsəʊl/", "verb", "C1", "menghibur hati yang sedang berduka", "Friends rallied to console the grieving family.", "Sahabat-sahabat datang untuk menghibur keluarga yang berduka."),
  ("conspire", "/kənˈspaɪə(r)/", "verb", "C1", "bersekongkol merencanakan sesuatu", "Fate conspired to bring the two together.", "Takdir seolah bersekongkol mempertemukan keduanya."),
  ("constitute", "/ˈkɒnstɪtjuːt/", "verb", "B2", "membentuk / merupakan bagian sah", "Twelve jurors constitute a full trial panel.", "Dua belas anggota juri membentuk satu panel pengadilan utuh."),
  ("constrain", "/kənˈstreɪn/", "verb", "C1", "mengekang / membatasi gerak", "Budget cuts constrain scientific research.", "Pemotongan anggaran mengekang gerak penelitian ilmiah."),
  ("consult", "/kənˈsʌlt/", "verb", "B1", "berkonsultasi meminta saran ahli", "Consult a certified doctor before taking pills.", "Berkonsultasilah dengan dokter bersertifikat sebelum minum obat."),
  ("consume", "/kənˈsjuːm/", "verb", "B1", "mengkonsumsi makanan atau energi", "Electric cars consume less energy than petrol engines.", "Mobil listrik mengonsumsi energi lebih sedikit dibanding mesin bensin."),
  ("contend", "/kənˈtend/", "verb", "B2", "berpendapat kukuh / berjuang menghadapi", "Scholars contend that bilingualism boosts brain agility.", "Pakar berpendapat kukuh bahwa dwibahasa mengasah ketangkasan otak."),
  ("content", "/kənˈtent/", "adjective", "B1", "puas dan tentram dengan apa yang ada", "He was content with his simple village life.", "Dia merasa tentram dan puas dengan kehidupan desanya yang sederhana."),
  ("contest", "/kənˈtest/", "verb", "B2", "menyanggah keabsahan / berlomba", "Lawyers contested the election recount results.", "Pengacara menyanggah hasil penghitungan ulang pemilu."),
  ("context", "/ˈkɒntekst/", "noun", "A2", "konteks situasi atau kalimat", "Learn new vocabulary inside sentence contexts.", "Pelajarilah kosakata baru di dalam konteks kalimat utuh."),
  ("contradict", "/ˌkɒntrəˈdɪkt/", "verb", "B2", "membantah bertentangan dengan fakta", "Witness reports contradicted the suspect's alibi.", "Keterangan saksi bertentangan dengan alibi si tersangka."),
  ("contrast", "/ˈkɒntrɑːst/", "noun", "B1", "kontras perbedaan mencolok", "Notice the contrast between dark and bright colours.", "Perhatikanlah kontras di antara warna gelap dan warna terang."),
  ("contribute", "/kənˈtrɪbjuːt/", "verb", "B2", "berkontribusi menyumbang peran", "Every volunteer contributes to community welfare.", "Setiap relawan berkontribusi bagi kesejahteraan masyarakat."),
  ("convene", "/kənˈviːn/", "verb", "C1", "mengadakan sidang pertemuan resmi", "The assembly convened to debate tax amendments.", "Majelis bersidang untuk memperdebatkan amandemen pajak."),
  ("convenient", "/kənˈviːniənt/", "adjective", "B1", "praktis dan nyaman digunakan", "Online flashcard apps are incredibly convenient.", "Aplikasi flashcard daring sangatlah praktis digunakan."),
  ("converge", "/kənˈvɜːdʒ/", "verb", "C1", "bertemu memusat di satu titik", "Thousands converged on the historic plaza.", "Ribuan orang berkumpul memusat di alun-alun bersejarah."),
  ("convert", "/kənˈvɜːt/", "verb", "B2", "mengonversi wujud bentuk", "Solar inverters convert sunlight into household power.", "Inverter surya mengonversi sinar matahari menjadi daya listrik rumah."),
  ("convey", "/kənˈveɪ/", "verb", "B2", "menyampaikan pesan atau rasa", "Poetry conveys deep emotional sentiments.", "Puisi menyampaikan luapan perasaan emosional yang mendalam."),
  ("convict", "/kənˈvɪkt/", "verb", "B2", "memvonis bersalah di pengadilan", "The judge convicted the embezzler on all counts.", "Hakim memvonis bersalah pelaku penggelapan dana atas semua dakwaan."),
  ("cooperate", "/kəʊˈɒpəreɪt/", "verb", "B1", "bekerja sama saling bantu", "Nations cooperate to protect international oceans.", "Negara-negara bekerja sama melindungi lautan internasional."),
  ("coordinate", "/kəʊˈɔːdɪneɪt/", "verb", "B2", "mengkoordinasikan alur kerja", "The manager coordinated cross-team schedules.", "Manajer mengoordinasikan jadwal kerja antartim."),
  ("cope", "/kəʊp/", "verb", "B2", "mampu bertahan menghadapi kesulitan", "She copes with high workloads with poise.", "Dia mampu menghadapi beban kerja yang tinggi dengan tenang."),
  ("corporate", "/ˈkɔːpərət/", "adjective", "B2", "korporat perusahaan besar", "Corporate responsibility requires sustainable actions.", "Tanggung jawab korporat mensyaratkan tindakan berkelanjutan."),
  ("correlate", "/ˈkɒrəleɪt/", "verb", "C1", "berkorelasi saling berhubungan erat", "Reading habits correlate with broad vocabulary breadth.", "Kebiasaan membaca berkorelasi erat dengan luasnya perbendaharaan kata."),
  ("correspond", "/ˌkɒrəˈspɒnd/", "verb", "B2", "berkorespondensi surat / cocok selaras", "The findings correspond with prior field trials.", "Temuan tersebut selaras dengan uji coba lapangan sebelumnya."),
  ("corrupt", "/kəˈrʌpt/", "adjective", "B2", "korup dan tidak berintegritas", "Independent courts combat corrupt practices.", "Pengadilan yang independen memberantas praktik-praktik korup."),
  ("counsel", "/ˈkaʊnsl/", "noun", "B2", "nasihat bimbingan ahli", "Seek legal counsel before signing leases.", "Carilah nasihat hukum sebelum menandatangani perjanjian sewa."),
  ("credible", "/ˈkredəbl/", "adjective", "B2", "kredibel dan dapat dipercaya", "Cite credible scholarly sources in your research.", "Rujuklah sumber-sumber ilmiah yang kredibel dalam penelitianmu."),
  ("criteria", "/kraɪˈtɪəriə/", "noun", "B2", "kriteria tolok ukur penilaian", "Academic merit is the main scholarship criteria.", "Prestasi akademis adalah kriteria utama penerimaan beasiswa."),
  ("cultivate", "/ˈkʌltɪveɪt/", "verb", "B2", "membina / menanamkan kebiasaan baik", "Cultivate a daily English reading habit.", "Tanamkan dan binalah kebiasaan membaca bahasa Inggris setiap hari."),
  ("curb", "/kɜːb/", "verb", "C1", "mengekang laju peningkatan", "Regulations curb excessive plastic usage.", "Peraturan mengekang pemakaian plastik yang berlebihan."),
  ("customize", "/ˈkʌstəmaɪz/", "verb", "B2", "menyesuaikan setelan sesuai selera", "You can customize your card themes in VocabPintar.", "Kamu bisa menyesuaikan tema warna kartu di VocabPintar."),
  ("debate", "/dɪˈbeɪt/", "noun", "B2", "debat adu argumen akademis", "Students engaged in a spirited climate debate.", "Siswa terlibat dalam debat iklim yang hangat dan hidup."),
  ("decade", "/ˈdekeɪd/", "noun", "B1", "dekade kurun sepuluh tahun", "Internet technology transformed the past decade.", "Teknologi internet mengubah dunia dalam kurun satu dekade terakhir."),
  ("decay", "/dɪˈkeɪ/", "verb", "B2", "membusuk terurai alami", "Fallen autumn leaves decay into fertile compost.", "Guguran daun musim gugur terurai menjadi kompos yang subur."),
  ("deceive", "/dɪˈsiːv/", "verb", "B2", "memperdaya menipu muslihat", "Do not allow deceptive ads to deceive you.", "Jangan biarkan iklan tipuan memperdayamu."),
  ("dedicate", "/ˈdedɪkeɪt/", "verb", "B2", "mendedikasikan segenap waktu", "She dedicated her life to rainforest conservation.", "Dia mendedikasikan hidupnya demi konservasi hutan hujan."),
  ("deduce", "/dɪˈdjuːs/", "verb", "C1", "menyimpulkan dari petunjuk bukti", "Detectives deduced the timeline from security footage.", "Detektif menyimpulkan urutan waktu dari rekaman kamera keamanan."),
  ("defect", "/ˈdiːfekt/", "noun", "B2", "cacat cela pada produk", "Quality inspectors returned items with minor defects.", "Pemeriksa mutu mengembalikan barang yang memiliki cacat kecil."),
  ("delegate", "/ˈdelɪɡeɪt/", "verb", "B2", "mendelegasikan tugas wewenang", "Good leaders delegate tasks to team members.", "Pemimpin yang baik mendelegasikan tugas kepada para anggota tim."),
  ("deliberate", "/dɪˈlɪbərət/", "adjective", "B2", "disengaja penuh pertimbangan matang", "He made a deliberate pause for dramatic emphasis.", "Dia sengaja berhenti sejenak demi penekanan yang dramatis."),
  ("demolish", "/dɪˈmɒlɪʃ/", "verb", "B2", "meruntuhkan bangunan usang", "Crews demolished the condemned factory warehouse.", "Petugas meruntuhkan gudang pabrik tua yang telah dinyatakan tak layak."),
  ("denote", "/dɪˈnəʊt/", "verb", "C1", "menandakan arti lambang", "A green badge denotes mastered vocabulary status.", "Lencana hijau menandakan status kosakata yang sudah dikuasai."),
  ("denounce", "/dɪˈnaʊns/", "verb", "C1", "mengecam secara terbuka di publik", "The ambassador denounced the maritime blockade.", "Duta besar mengecam terbuka blokade laut tersebut."),
  ("dense", "/dens/", "adjective", "B2", "padat rapat kerapatannya", "We hiked through dense tropical foliage.", "Kami mendaki melintasi rimbunnya hutan tropis yang lebat."),
  ("depict", "/dɪˈpɪkt/", "verb", "B2", "menggambarkan lewat lukisan/kata", "The mural depicts historical harbor traders.", "Mural itu menggambarkan para pedagang pelabuhan bersejarah."),
  ("deplete", "/dɪˈpliːt/", "verb", "C1", "menguras habis persediaan", "Overfishing depletes ocean fish stocks.", "Penangkapan ikan berlebihan menguras persediaan ikan di lautan."),
  ("deploy", "/dɪˈplɔɪ/", "verb", "B2", "menerjunkan pasukan / men-deploy web ke Vercel", "You can deploy this web application to Vercel in seconds.", "Kamu bisa men-deploy aplikasi web ini ke Vercel dalam hitungan detik."),
  ("derive", "/dɪˈraɪv/", "verb", "B2", "memperoleh bersumber dari", "Many English words derive from ancient Latin roots.", "Banyak kata bahasa Inggris bersumber dari akar bahasa Latin kuno."),
  ("designate", "/ˈdezɪɡneɪt/", "verb", "B2", "menetapkan peruntukan resmi", "The bay was designated a protected marine park.", "Teluk itu ditetapkan secara resmi sebagai taman laut dilindungi."),
  ("despair", "/dɪˈspeə(r)/", "noun", "B2", "keputusasaan rasa hampa", "Never give in to despair during setbacks.", "Jangan pernah menyerah pada keputusasaan saat menghadapi kegagalan."),
  ("despise", "/dɪˈspaɪz/", "verb", "B2", "memandang jijik meremehkan", "He despises hypocritical political promises.", "Dia sangat muak dengan janji-janji politik yang munafik."),
  ("destine", "/ˈdestɪn/", "verb", "B2", "mentakdirkan masa depan", "Her tireless grit destined her for championship.", "Kegigihannya yang tanpa lelah mentakdirkannya meraih gelar juara."),
  ("detach", "/dɪˈtætʃ/", "verb", "B2", "melepaskan kaitan dari induk", "Detach the coupon along the perforated line.", "Lepaskan kupon tersebut di sepanjang garis putus-putus."),
  ("deter", "/dɪˈtɜː(r)/", "verb", "B2", "mencegah mematahkan niat buruk", "Strict fines deter illegal waste dumping.", "Denda yang tegas mematahkan niat pembuangan sampah ilegal."),
  ("deteriorate", "/dɪˈtɪəriəreɪt/", "verb", "B2", "memburuk kondisinya secara bertahap", "The weather deteriorated into a raging blizzard.", "Cuaca memburuk menjadi badai salju yang mengamuk."),
  ("devastate", "/ˈdevəsteɪt/", "verb", "B2", "menghancurluluhkan luluh lantak", "Hurricanes devastated coastal coral reefs.", "Badai menghancurluluhkan terumbu karang di pesisir."),
  ("deviate", "/ˈdiːvieɪt/", "verb", "B2", "menyimpang dari garis jalur", "Do not deviate from laboratory safety protocols.", "Jangan menyimpang dari protokol keselamatan laboratorium."),
  ("devise", "/dɪˈvaɪz/", "verb", "B2", "merancang skema cemerlang", "Engineers devised an automated sorting robot.", "Insinyur merancang robot pemilah barang otomatis."),
  ("diagnose", "/ˈdaɪəɡnəʊz/", "verb", "B2", "mendiagnosis penyakit secara medis", "Physicians diagnosed the allergy promptly.", "Dokter mendiagnosis alergi tersebut dengan tepat waktu."),
  ("dictate", "/dɪkˈteɪt/", "verb", "B2", "mendiktekan perintah / menentukan", "Common sense dictates taking shelter in thunder.", "Akal sehat mendiktekan agar kita berteduh saat ada petir."),
  ("differentiate", "/ˌdɪfəˈrenʃieɪt/", "verb", "B2", "membedakan di antara dua hal serupa", "Skilled speakers differentiate subtle synonyms.", "Penutur mahir membedakan sinonim-sinonim yang halus."),
  ("diffuse", "/dɪˈfjuːs/", "verb", "C1", "menyebarkan ke segala arah / meredakan", "Humor diffused tension in the boardroom.", "Humor meredakan ketegangan di dalam ruang rapat."),
  ("diminish", "/dɪˈmɪnɪʃ/", "verb", "B2", "berkurang menyusut nilainya", "Practice prevents skills from diminishing.", "Latihan mencegah keahlian menyusut seiring waktu."),
  ("discard", "/dɪˈskɑːd/", "verb", "B2", "membuang hal yang tak terpakai", "Discard outdated flashcards you already master.", "Singkirkan flashcard lama yang sudah benar-benar kamu kuasai."),
  ("discern", "/dɪˈsɜːn/", "verb", "C1", "melihat / membedakan dengan kepekaan", "Trained ears discern slight dialect nuances.", "Telinga terlatih mampu membedakan nuansa dialek yang samar."),
  ("disclose", "/dɪˈskləʊz/", "verb", "B2", "membocorkan / membuka rahasia ke publik", "Companies disclose quarterly earnings reports.", "Perusahaan membuka laporan pendapatan triwulanannya ke publik."),
  ("discreet", "/dɪˈskriːt/", "adjective", "B2", "bijaksana menjaga rahasia", "Diplomats maintain discreet communication channels.", "Diplomat menjaga saluran komunikasi yang bijak dan rahasia."),
  ("discriminate", "/dɪˈskrɪmɪneɪt/", "verb", "B2", "mendiskriminasi / membeda-bedakan", "Laws forbid discriminating on race or gender.", "Hukum melarang diskriminasi atas dasar ras atau gender."),
  ("disdain", "/dɪsˈdeɪn/", "noun", "C1", "sikap memandang rendah mencibir", "She treated snobbish remarks with quiet disdain.", "Dia menanggapi ucapan sombong itu dengan cibiran tenang."),
  ("disillusion", "/ˌdɪsɪˈluːʒn/", "noun", "B2", "kekecewaan hilangnya ilusi indah", "Unmet promises led to public disillusion.", "Janji yang tak ditepati berujung pada kekecewaan publik."),
  ("dismiss", "/dɪsˈmɪs/", "verb", "B2", "menolak mentah-mentah / membubarkan", "The manager dismissed groundless gossip.", "Manajer mengabaikan dan menepis gosip tak berdasar itu."),
  ("disperse", "/dɪˈspɜːs/", "verb", "B2", "membubarkan diri menyebar luas", "Crowds dispersed peacefully after speech ended.", "Massa membubarkan diri dengan damai setelah pidato usai."),
  ("displace", "/dɪsˈpleɪs/", "verb", "B2", "menggusur menggeser kedudukan", "Flooding displaced hundreds of riverside families.", "Banjir menggusur ratusan keluarga di bantaran sungai."),
  ("dispute", "/dɪˈspjuːt/", "noun", "B2", "sengketa perselisihan hukum", "Mediation resolved the copyright dispute.", "Mediasi menyelesaikan sengketa hak cipta tersebut."),
  ("disregard", "/ˌdɪsrɪˈɡɑːd/", "verb", "B2", "mengabaikan tidak mengindahkan", "Do not disregard official weather advisories.", "Jangan mengabaikan peringatan resmi cuaca buruk."),
  ("disrupt", "/dɪsˈrʌpt/", "verb", "B2", "mengacaukan kelancaran sistem", "Internet outages disrupted flight check-in desks.", "Matinya internet mengacaukan loket check-in penerbangan."),
  ("dissent", "/dɪˈsent/", "noun", "C1", "perbedaan pendapat oposisi", "Healthy democracies welcome constructive dissent.", "Demokrasi yang sehat menyambut baik perbedaan pendapat konstruktif."),
  ("dissolve", "/dɪˈzɒlv/", "verb", "B2", "melarutkan zat / membubarkan ikatan", "Sugar dissolves quickly in hot tea.", "Gula larut dengan cepat di dalam teh panas."),
  ("distort", "/dɪˈstɔːt/", "verb", "B2", "memutarbalikkan membiaskan fakta", "Misleading headlines distort genuine reality.", "Judul berita yang menyesatkan membiaskan fakta sesungguhnya."),
  ("distract", "/dɪˈstrækt/", "verb", "B1", "mengalihkan konsentrasi fokus", "Turn off phone notifications so nothing distracts you.", "Matikan notifikasi ponsel agar tak ada yang mengalihkan fokusmu."),
  ("distress", "/dɪˈstres/", "noun", "B2", "penderitaan duka lara mendalam", "Sailors in distress fired flare signals.", "Pelaut yang dalam bahaya menembakkan sinyal suar darurat."),
  ("diverge", "/daɪˈvɜːdʒ/", "verb", "C1", "bercabang menyimpang berlawanan", "Opinions diverged on the best study schedule.", "Pendapat bercabang berbeda tentang jadwal belajar terbaik."),
  ("diverse", "/daɪˈvɜːs/", "adjective", "B2", "majemuk beragam variasinya", "Our user community is globally diverse.", "Komunitas pengguna kami sangat majemuk dari seluruh penjuru dunia."),
  ("divert", "/daɪˈvɜːt/", "verb", "B2", "mengalihkan arus lalu lintas", "Police diverted traffic around the sinkhole.", "Polisi mengalihkan arus lalu lintas di sekitar jalan amblas."),
  ("dominate", "/ˈdɒmɪneɪt/", "verb", "B2", "mendominasi menguasai bidang", "Her talent dominated the national tournament.", "Bakatnya mendominasi turnamen nasional tersebut."),
  ("dormant", "/ˈdɔːmənt/", "adjective", "C1", "tertidur tidak aktif sementara", "The volcano has lain dormant for three centuries.", "Gunung berapi itu telah tertidur tidak aktif selama tiga abad."),
  ("drastic", "/ˈdræstɪk/", "adjective", "B2", "drastis radikal perubahannya", "The board took drastic measures to cut waste.", "Dewan direksi mengambil tindakan drastis demi memangkas pemborosan."),
  ("drift", "/drɪft/", "verb", "B2", "hanyut terombang-ambing santai", "Leaves drifted down gently on the calm pond.", "Dedaunan hanyut mengapung pelan di atas kolam yang tenang."),
  ("duplicate", "/ˈdjuːplɪkeɪt/", "verb", "B2", "menggandakan tiruan persis", "Duplicate important document backups in the cloud.", "Gandakan salinan dokumen penting di penyimpanan awan."),
  ("durable", "/ˈdjuərəbl/", "adjective", "B2", "tahan lama awet bertahun-tahun", "Cast-iron cookware is exceptionally durable.", "Peralatan masak dari besi cor sangat awet dan tahan lama."),
  ("dwindle", "/ˈdwɪndl/", "verb", "C1", "menyusut berkurang drastis", "Our water supplies dwindled in the heatwave.", "Persediaan air kami menyusut drastis di tengah gelombang panas."),
  ("dynamic", "/daɪˈnæmɪk/", "adjective", "B2", "dinamis bertenaga penuh inovasi", "A dynamic language game keeps learners engaged.", "Permainan bahasa yang dinamis membuat pembelajar tetap bersemangat.")
]

for idx, (term, ipa, pos, level, meaning_id, ex_en, ex_id) in enumerate(additional_oxford):
  base_oxford.append((term, ipa, pos, level, meaning_id, ex_en, ex_id))

# De-duplicate base_oxford by term
seen_terms = set()
unique_oxford = []
for item in base_oxford:
  term = item[0].lower().strip()
  if term not in seen_terms:
    seen_terms.add(term)
    unique_oxford.append(item)

# Build oxford_vocab objects
oxford_vocab = []
for idx, (term, ipa, pos, level, meaning_id, ex_en, ex_id) in enumerate(unique_oxford):
  oxford_vocab.append({
    "id": f"ox-{idx+1:04d}",
    "term": term,
    "ipa": ipa,
    "type": "oxford_3000",
    "pos": pos,
    "level": level,
    "category": f"Oxford Vocabulary ({level})",
    "meaningId": meaning_id,
    "exampleEn": ex_en,
    "exampleId": ex_id,
    "hint": f"POS: {pos} | CEFR: {level}"
  })

# Write files
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
  const shuffled = [...arr].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
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

print(f"=== DATABASE CREATED SUCCESSFULLY ===")
print(f"Phrasal Verbs & Idioms: {len(phrasal_verbs)}")
print(f"Collocations: {len(collocations)}")
print(f"Oxford Vocabulary (A1 - C2): {len(oxford_vocab)}")
print(f"Total Database Entries: {len(phrasal_verbs) + len(collocations) + len(oxford_vocab)}")
print(f"C1 & C2 Advanced Words: {len([w for w in oxford_vocab if w['level'] in ['C1', 'C2']])}")
