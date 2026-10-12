# 🦉 VocabPintar - Game Belajar Phrasal Verbs, Collocations & Oxford 3000

Aplikasi web interaktif dan menyenangkan untuk pembelajar Bahasa Inggris tingkat **Upper-Intermediate & Advanced (CEFR B1 - B2)**. Dirancang khusus untuk memperkuat penguasaan **Phrasal Verbs**, **Collocations**, dan **Oxford 3000 Vocabulary (Noun, Verb, Adjective, Adverb)** melalui game gamifikasi yang lucu dan edukatif.

Siap dideploy langsung ke **Vercel** dengan konfigurasi SPA routing otomatis! 🚀

---

## ✨ Fitur Unggulan

### 1. 🗂️ Flashcard 3D Interaktif
- Animasi membalik kartu 3D yang halus.
- **Audio Pengucapan Native** menggunakan Web Speech API dengan opsi aksen **US (American) 🇺🇸** dan **UK (British Oxford) 🇬🇧**.
- Panduan fonetik **IPA (International Phonetic Alphabet)**.
- Arti bahasa Indonesia & contoh kalimat nyata lengkap dengan terjemahannya (contoh: *"go: I go to school"*).
- Penanda status belajar: **Sudah Paham (+15 XP)** & **Perlu Review (+5 XP)**.
- Filter kategori lengkap: Phrasal Verbs, Collocations, Oxford 3000, Nouns, Verbs, Adjectives, Adverbs, serta level CEFR (A1, A2, B1, B2).

### 2. 🧩 Susunan Kata (Sentence Scramble)
- Game menyusun kata acak menjadi kalimat utuh yang tepat berdasarkan makna bahasa Indonesia yang diminta.
- Menempatkan phrasal verb atau kolokasi dalam konteks kalimat nyata.
- Animasi interaktif, tombol undo kata, dan cek jawaban seketika.
- Audio pembacaan kalimat lengkap secara otomatis saat jawaban benar!
- Pengganda skor **Combo Streak (x2, x3, dst.)** & ledakan confetti.

### 3. 🎯 Kuis Pilihan Ganda & Collocation Builder
- **Mode 1**: English ➔ Arti Bahasa Indonesia.
- **Mode 2**: Arti Bahasa Indonesia ➔ Istilah English.
- **Mode 3**: *Lengkapi Frasa (Fill in the Blank)* untuk melatih pasangan kata kolokasi & partikel phrasal verb.
- Pembahasan lengkap dengan quote contoh kalimat dan tips pemakaian.

### 4. ⚡ Pasangan Cepat (Speed Match Pairs)
- Grid kartu interaktif untuk menjodohkan kosakata bahasa Inggris dan artinya secepat mungkin.
- Penghitung waktu (timer), jumlah langkah, efek suara pop, dan perayaan kemenangan dengan trofi dan confetti.

### 5. 📖 Kamus Pintar & Koleksi Kosakata
- Pencarian seketika (*real-time search*) berdasarkan kata, arti Indonesia, atau topik.
- Tab filter: **123 Phrasal Verbs**, **56 Collocations**, dan **68 Oxford Vocabularies**.
- Filter status: *Favorit Saya ❤️*, *Sudah Dikuasai 🎯*, dan *Perlu Diulang 🔄*.
- Audio speaker pada setiap kata dan contoh kalimat.

### 6. 🎮 Gamifikasi & Desain Lucu
- **Maskot Pintar**: Burung hantu cerdas dengan ekspresi adaptif (tersenyum, berpikir, bersorak, dan merayakan keberhasilan).
- **Streak Harian (🔥)**: Melacak konsistensi belajar harian yang tersimpan di `localStorage`.
- **Leveling & XP**: Kumpulkan poin XP untuk naik level dari *Pemula 🐣* hingga *Oxford Master 👑*.
- **Efek Suara Sintetis (Web Audio API)**: Suara chime kemenangan, boing, dan pop tanpa ketergantungan file eksternal.
- **4 Pilihan Tema Pastel**:
  - 🍵 Matcha Mint (Hijau segar & tenang)
  - 🌸 Sakura Pastel (Merah muda manis)
  - 🌊 Ocean Sky (Biru langit sejuk)
  - 🌅 Sunset Peach (Oranye hangat)

---

## 📚 Sumber Materi Kosakata

1. **Oxford Learner's Pocket Phrasal Verbs and Idioms Wordlist**:
   - Mencakup berbagai kategori kehidupan: *Body, Health, Feelings, Family, Friends, Romantic Relationships, Everyday Life, Food, Cooking, Home, Clothes, Sleep, Money, Transport, Law & Order, Technology, Media, Leisure, Sport, Dramatic Events, Study, Work, Business, Politics, Concepts, dan Particles*.
2. **Essential High-Yield Collocations**:
   - *Verb + Noun* (e.g., pay attention, make an effort, take advantage, bear in mind, raise awareness, pose a threat, break a habit).
   - *Adjective + Noun* (e.g., heavy rain, golden opportunity, fierce competition, profound effect, wide variety).
   - *Adverb + Adjective* (e.g., deeply concerned, highly recommended, bitterly disappointed, strictly forbidden, painfully obvious).
   - *Verb + Preposition / Adverb* (e.g., strictly adhere to, strongly recommend, apologize profusely, cope with, stem from).
3. **The Oxford 3000™**:
   - Kosakata esensial A1 hingga B2 yang diklasifikasikan berdasarkan Part of Speech: **Noun (Kata Benda)**, **Verb (Kata Kerja)**, **Adjective (Kata Sifat)**, dan **Adverb (Kata Keterangan)**.

---

## 🛠️ Menjalankan di Lokal (Local Development)

Pastikan Node.js (v18+) sudah terpasang di komputer Anda:

```bash
# 1. Clone repository
git clone https://github.com/alvinsp/vocabularies-game.git
cd vocabularies-game

# 2. Install dependensi
npm install

# 3. Jalankan development server
npm run dev
```

Buka peramban di `http://localhost:5173`.

---

## 🚀 Cara Deploy ke Vercel

1. Buka [Vercel](https://vercel.com/) dan login menggunakan akun GitHub Anda.
2. Klik tombol **"Add New..."** lalu pilih **"Project"**.
3. Pilih repository **`alvinsp/vocabularies-game`**.
4. Pengaturan build Vite akan terdeteksi otomatis:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Klik **"Deploy"**! Dalam 1 menit website Anda sudah aktif secara online.

---

## 📦 Lisensi

Dibuat dengan ❤️ untuk membantu pembelajar bahasa Inggris meningkatkan kefasihan kosakata, phrasal verbs, dan kolokasi.
