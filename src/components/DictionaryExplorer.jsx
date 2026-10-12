import React, { useState, useMemo } from 'react';
import { 
  Search, 
  Volume2, 
  Heart, 
  CheckCircle, 
  AlertCircle, 
  Filter, 
  Sparkles,
  BookOpen,
  ArrowUpDown
} from 'lucide-react';
import { sounds } from '../utils/soundEffects';
import { speechAssistant } from '../utils/speechUtils';
import { allVocabulary } from '../data';

export default function DictionaryExplorer({
  masteredIds,
  reviewIds,
  favoriteIds,
  onMarkMastered,
  onMarkReview,
  onToggleFavorite,
  accent
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedType, setSelectedType] = useState('all'); // 'all', 'phrasal_verb', 'collocation', 'oxford_3000'
  const [selectedPos, setSelectedPos] = useState('all'); // 'all', 'verb', 'noun', 'adjective', 'adverb'
  const [selectedLevel, setSelectedLevel] = useState('all'); // 'all', 'A1', 'A2', 'B1', 'B2'
  const [statusFilter, setStatusFilter] = useState('all'); // 'all', 'favorites', 'mastered', 'review'
  const [sortBy, setSortBy] = useState('term-asc'); // 'term-asc', 'term-desc', 'level'

  const filteredVocabulary = useMemo(() => {
    let list = allVocabulary.filter((item) => {
      // Search
      if (searchTerm.trim()) {
        const q = searchTerm.toLowerCase().trim();
        const matchTerm = item.term.toLowerCase().includes(q);
        const matchMeaning = item.meaningId.toLowerCase().includes(q);
        const matchCategory = item.category?.toLowerCase().includes(q);
        const matchExample = item.exampleEn?.toLowerCase().includes(q);
        if (!matchTerm && !matchMeaning && !matchCategory && !matchExample) return false;
      }

      // Type
      if (selectedType !== 'all' && item.type !== selectedType) return false;

      // POS
      if (selectedPos !== 'all' && item.pos !== selectedPos) return false;

      // Level
      if (selectedLevel !== 'all' && item.level !== selectedLevel) return false;

      // Status
      if (statusFilter === 'favorites' && !favoriteIds.has(item.id)) return false;
      if (statusFilter === 'mastered' && !masteredIds.has(item.id)) return false;
      if (statusFilter === 'review' && !reviewIds.has(item.id)) return false;

      return true;
    });

    // Sorting
    list.sort((a, b) => {
      if (sortBy === 'term-asc') return a.term.localeCompare(b.term);
      if (sortBy === 'term-desc') return b.term.localeCompare(a.term);
      if (sortBy === 'level') return a.level.localeCompare(b.level);
      return 0;
    });

    return list;
  }, [searchTerm, selectedType, selectedPos, selectedLevel, statusFilter, sortBy, favoriteIds, masteredIds, reviewIds]);

  const playSpeech = (text) => {
    speechAssistant.setAccent(accent);
    speechAssistant.speak(text);
  };

  return (
    <div className="dictionary-explorer-container">
      {/* Search & Stats Header */}
      <div className="dictionary-header-box">
        <div className="dict-title-section">
          <h2>Kamus Pintar & Koleksi Kosakata 📖</h2>
          <p>Cari dan pelajari kata, phrasal verbs, serta collocations lengkap dengan contoh dan audio native.</p>
        </div>

        {/* Big Search Input */}
        <div className="search-bar-wrap">
          <Search size={22} className="search-icon" />
          <input
            type="text"
            className="search-input"
            placeholder="Cari kata bahasa Inggris, arti bahasa Indonesia, topik..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {searchTerm && (
            <button className="clear-search-btn" onClick={() => setSearchTerm('')}>
              ×
            </button>
          )}
        </div>
      </div>

      {/* Filter Tabs & Selectors */}
      <div className="dict-filters-panel">
        {/* Main Type Tabs */}
        <div className="dict-type-tabs">
          <button 
            className={`dict-tab ${selectedType === 'all' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setSelectedType('all'); }}
          >
            Semua ({allVocabulary.length})
          </button>
          <button 
            className={`dict-tab ${selectedType === 'phrasal_verb' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setSelectedType('phrasal_verb'); }}
          >
            Phrasal Verbs ⚡ (123)
          </button>
          <button 
            className={`dict-tab ${selectedType === 'collocation' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setSelectedType('collocation'); }}
          >
            Collocations 🧩 (56)
          </button>
          <button 
            className={`dict-tab ${selectedType === 'oxford_3000' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setSelectedType('oxford_3000'); }}
          >
            Oxford 3000 📚 (68)
          </button>
        </div>

        {/* Dropdowns Row */}
        <div className="dict-sub-filters-row">
          <div className="filter-select-group">
            <span className="select-label">Jenis Kata (POS):</span>
            <select 
              className="dict-select"
              value={selectedPos}
              onChange={(e) => setSelectedPos(e.target.value)}
            >
              <option value="all">Semua Jenis</option>
              <option value="verb">Verbs (Kata Kerja)</option>
              <option value="noun">Nouns (Kata Benda)</option>
              <option value="adjective">Adjectives (Kata Sifat)</option>
              <option value="adverb">Adverbs (Kata Keterangan)</option>
              <option value="idiom">Idioms</option>
            </select>
          </div>

          <div className="filter-select-group">
            <span className="select-label">Level CEFR:</span>
            <select 
              className="dict-select"
              value={selectedLevel}
              onChange={(e) => setSelectedLevel(e.target.value)}
            >
              <option value="all">Semua Level</option>
              <option value="A1">A1 (Beginner)</option>
              <option value="A2">A2 (Elementary)</option>
              <option value="B1">B1 (Intermediate)</option>
              <option value="B2">B2 (Upper-Intermediate)</option>
            </select>
          </div>

          <div className="filter-select-group">
            <span className="select-label">Status Anda:</span>
            <select 
              className="dict-select"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">Semua Status</option>
              <option value="favorites">Favorit Saya ❤️ ({favoriteIds.size})</option>
              <option value="mastered">Sudah Dikuasai 🎯 ({masteredIds.size})</option>
              <option value="review">Perlu Diulang 🔄 ({reviewIds.size})</option>
            </select>
          </div>

          <div className="filter-select-group">
            <span className="select-label">Urutan:</span>
            <select 
              className="dict-select"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="term-asc">A ➔ Z</option>
              <option value="term-desc">Z ➔ A</option>
              <option value="level">Level CEFR</option>
            </select>
          </div>
        </div>
      </div>

      {/* Vocabulary Results Grid */}
      <div className="dict-results-container">
        <div className="results-count-bar">
          <span>Menampilkan <strong>{filteredVocabulary.length}</strong> kosakata</span>
        </div>

        {filteredVocabulary.length === 0 ? (
          <div className="empty-state-box">
            <BookOpen size={48} className="empty-icon" />
            <h3>Kosakata tidak ditemukan</h3>
            <p>Tidak ada entri yang cocok dengan kriteria pencarian "{searchTerm}".</p>
            <button 
              className="cute-primary-btn"
              onClick={() => {
                setSearchTerm('');
                setSelectedType('all');
                setSelectedPos('all');
                setSelectedLevel('all');
                setStatusFilter('all');
              }}
            >
              Hapus Semua Filter
            </button>
          </div>
        ) : (
          <div className="dict-items-grid">
            {filteredVocabulary.map((item) => {
              const isFav = favoriteIds.has(item.id);
              const isMaster = masteredIds.has(item.id);
              const isRev = reviewIds.has(item.id);

              return (
                <div key={item.id} className="dict-item-card">
                  {/* Card Top Pill Bar */}
                  <div className="dict-card-top">
                    <div className="badge-group">
                      <span className={`badge-pill badge-${item.type}`}>
                        {item.type === 'phrasal_verb' ? 'Phrasal Verb' : item.type === 'collocation' ? 'Collocation' : 'Oxford 3000'}
                      </span>
                      <span className="badge-pill badge-level">{item.level}</span>
                      <span className="badge-pill badge-pos">{item.pos}</span>
                    </div>

                    <button 
                      className={`icon-action-btn heart-btn ${isFav ? 'favorited' : ''}`}
                      onClick={() => {
                        sounds.playPop();
                        onToggleFavorite(item.id);
                      }}
                      title="Simpan ke favorit"
                    >
                      <Heart size={18} fill={isFav ? '#EF4444' : 'none'} color={isFav ? '#EF4444' : 'currentColor'} />
                    </button>
                  </div>

                  {/* Term & IPA */}
                  <div className="dict-term-row">
                    <h3 className="dict-term">{item.term}</h3>
                    <button 
                      className="speak-mini-btn"
                      onClick={() => playSpeech(item.term)}
                      title="Dengarkan pengucapan kata"
                    >
                      <Volume2 size={18} />
                    </button>
                  </div>

                  <span className="dict-ipa">{item.ipa}</span>
                  <p className="dict-meaning">{item.meaningId}</p>

                  {/* Example sentence with translation */}
                  <div className="dict-example-box">
                    <div className="example-header">
                      <span className="example-badge">Contoh:</span>
                      <button 
                        className="speak-mini-btn"
                        onClick={() => playSpeech(item.exampleEn)}
                        title="Dengarkan kalimat lengkap"
                      >
                        <Volume2 size={14} /> Dengarkan
                      </button>
                    </div>
                    <p className="dict-example-en">"{item.exampleEn}"</p>
                    <p className="dict-example-id">"{item.exampleId}"</p>
                  </div>

                  {/* Hint / Topic */}
                  {item.category && (
                    <div className="dict-category-footer">
                      <span className="category-tag">📂 {item.category}</span>
                      {item.hint && <span className="hint-tag" title={item.hint}>💡 {item.hint}</span>}
                    </div>
                  )}

                  {/* Quick Mastery Actions */}
                  <div className="dict-card-actions">
                    <button 
                      className={`dict-action-btn ${isRev ? 'active-review' : ''}`}
                      onClick={() => {
                        sounds.playPop();
                        onMarkReview(item.id);
                      }}
                      title="Perlu diulang"
                    >
                      <AlertCircle size={15} />
                      <span>{isRev ? 'Perlu Review' : 'Tandai Review'}</span>
                    </button>

                    <button 
                      className={`dict-action-btn ${isMaster ? 'active-master' : ''}`}
                      onClick={() => {
                        sounds.playCorrect();
                        onMarkMastered(item.id);
                      }}
                      title="Sudah paham"
                    >
                      <CheckCircle size={15} />
                      <span>{isMaster ? 'Sudah Paham' : 'Tandai Paham'}</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
