import React, { useState, useEffect, useMemo } from 'react';
import confetti from 'canvas-confetti';
import { 
  Volume2, 
  RotateCw, 
  ChevronLeft, 
  ChevronRight, 
  Shuffle, 
  Heart, 
  CheckCircle, 
  AlertCircle, 
  HelpCircle,
  Sparkles,
  BookMarked,
  Trophy,
  ArrowRight
} from 'lucide-react';
import { sounds } from '../utils/soundEffects';
import { speechAssistant } from '../utils/speechUtils';
import { allVocabulary } from '../data';
import Mascot from './Mascot';

export default function FlashcardGame({
  masteredIds,
  reviewIds,
  favoriteIds,
  onMarkMastered,
  onMarkReview,
  onToggleFavorite,
  onAddXP,
  accent
}) {
  const [activeFilter, setActiveFilter] = useState('all'); // 'all', 'phrasal_verb', 'collocation', 'oxford_3000', 'noun', 'verb', 'adjective', 'adverb'
  const [levelFilter, setLevelFilter] = useState('all'); // 'all', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'
  const [statusFilter, setStatusFilter] = useState('all'); // 'all', 'unlearned', 'review', 'mastered', 'favorites'

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [isSessionComplete, setIsSessionComplete] = useState(false);

  // 50-Card Batch Mode
  const [isBatchMode, setIsBatchMode] = useState(true);
  const [sessionKey, setSessionKey] = useState(0);

  // Base Filtered list
  const filteredList = useMemo(() => {
    return allVocabulary.filter((item) => {
      // Type or POS filter
      if (activeFilter === 'phrasal_verb' && item.type !== 'phrasal_verb') return false;
      if (activeFilter === 'collocation' && item.type !== 'collocation') return false;
      if (activeFilter === 'oxford_3000' && item.type !== 'oxford_3000') return false;
      if (activeFilter === 'noun' && item.pos !== 'noun') return false;
      if (activeFilter === 'verb' && item.pos !== 'verb') return false;
      if (activeFilter === 'adjective' && item.pos !== 'adjective') return false;
      if (activeFilter === 'adverb' && item.pos !== 'adverb') return false;

      // Level
      if (levelFilter !== 'all' && item.level !== levelFilter) return false;

      // Status
      if (statusFilter === 'mastered' && !masteredIds.has(item.id)) return false;
      if (statusFilter === 'review' && !reviewIds.has(item.id)) return false;
      if (statusFilter === 'favorites' && !favoriteIds.has(item.id)) return false;
      if (statusFilter === 'unlearned' && (masteredIds.has(item.id) || reviewIds.has(item.id))) return false;

      return true;
    });
  }, [activeFilter, levelFilter, statusFilter, masteredIds, reviewIds, favoriteIds]);

  // Active Deck: randomized 50 cards if in batch mode, or all filtered cards
  const activeDeck = useMemo(() => {
    if (filteredList.length === 0) return [];
    if (!isBatchMode) return filteredList;
    
    // Shuffled copy
    const shuffled = [...filteredList].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, Math.min(50, shuffled.length));
  }, [filteredList, isBatchMode, sessionKey]);

  // Current Card
  const currentCard = activeDeck[currentIndex] || null;

  // Reset index when filter or deck changes
  useEffect(() => {
    setCurrentIndex(0);
    setIsFlipped(false);
    setShowHint(false);
    setIsSessionComplete(false);
  }, [activeFilter, levelFilter, statusFilter, isBatchMode, sessionKey]);

  // Trigger new random 50 batch
  const handleNewRandomBatch = () => {
    sounds.playPop();
    setSessionKey(prev => prev + 1);
    setCurrentIndex(0);
    setIsFlipped(false);
    setShowHint(false);
    setIsSessionComplete(false);
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'Space') {
        e.preventDefault();
        flipCard();
      } else if (e.code === 'ArrowRight') {
        nextCard();
      } else if (e.code === 'ArrowLeft') {
        prevCard();
      } else if (e.code === 'ArrowUp' || e.code === 'ArrowDown') {
        e.preventDefault();
        setShowHint(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentIndex, activeDeck.length]);

  const flipCard = () => {
    sounds.playFlip();
    setIsFlipped(!isFlipped);
  };

  const nextCard = () => {
    if (currentIndex < activeDeck.length - 1) {
      sounds.playPop();
      setCurrentIndex(currentIndex + 1);
      setIsFlipped(false);
      setShowHint(false);
    } else if (activeDeck.length > 0 && currentIndex === activeDeck.length - 1) {
      // End of session!
      sounds.playFanfare();
      setIsSessionComplete(true);
      confetti({
        particleCount: 80,
        spread: 90,
        origin: { y: 0.6 }
      });
    }
  };

  const prevCard = () => {
    if (currentIndex > 0) {
      sounds.playPop();
      setCurrentIndex(currentIndex - 1);
      setIsFlipped(false);
      setShowHint(false);
    }
  };

  const playSpeech = (text, e) => {
    if (e) e.stopPropagation();
    setSpeaking(true);
    speechAssistant.setAccent(accent);
    speechAssistant.speak(text, () => setSpeaking(false));
  };

  const handleMastered = () => {
    if (!currentCard) return;
    sounds.playCorrect();
    onMarkMastered(currentCard.id);
    onAddXP(15);

    // Fire cute mini confetti
    confetti({
      particleCount: 35,
      spread: 60,
      origin: { y: 0.7 },
      colors: ['#34D399', '#60A5FA', '#F472B6']
    });

    if (currentIndex < activeDeck.length - 1) {
      setTimeout(() => nextCard(), 300);
    } else {
      setTimeout(() => {
        sounds.playFanfare();
        setIsSessionComplete(true);
      }, 400);
    }
  };

  const handleReview = () => {
    if (!currentCard) return;
    sounds.playWrong();
    onMarkReview(currentCard.id);
    onAddXP(5);
    if (currentIndex < activeDeck.length - 1) {
      setTimeout(() => nextCard(), 300);
    } else {
      setTimeout(() => {
        sounds.playFanfare();
        setIsSessionComplete(true);
      }, 400);
    }
  };

  const isFavorite = currentCard ? favoriteIds.has(currentCard.id) : false;

  return (
    <div className="flashcard-game-container">
      {/* Top Header & Mascot */}
      <div className="game-intro-card">
        <Mascot 
          mood={isSessionComplete ? "celebrate" : isFlipped ? "celebrate" : "happy"} 
          message={
            isSessionComplete
              ? "Luar biasa! Kamu menyelesaikan semua 50 kartu di sesi ini! 🎉"
              : activeDeck.length === 0 
                ? "Wah, belum ada kartu untuk filter ini! Coba pilih kategori lain ya."
                : isFlipped
                  ? "Pelajari contoh kalimatnya & dengarkan cara pengucapannya!"
                  : "Tebak arti kata ini sebelum membalik kartu! Semangat!"
          }
          size={72}
        />
      </div>

      {/* Filter Toolbar */}
      <div className="flashcard-filters">
        <div className="filter-group-row">
          <span className="filter-group-title">Kategori:</span>
          <div className="filter-pills">
            <button 
              className={`pill-btn ${activeFilter === 'all' ? 'active' : ''}`}
              onClick={() => setActiveFilter('all')}
            >
              Semua ({allVocabulary.length})
            </button>
            <button 
              className={`pill-btn ${activeFilter === 'phrasal_verb' ? 'active' : ''}`}
              onClick={() => setActiveFilter('phrasal_verb')}
            >
              Phrasal Verbs ⚡
            </button>
            <button 
              className={`pill-btn ${activeFilter === 'collocation' ? 'active' : ''}`}
              onClick={() => setActiveFilter('collocation')}
            >
              Collocations 🧩
            </button>
            <button 
              className={`pill-btn ${activeFilter === 'oxford_3000' ? 'active' : ''}`}
              onClick={() => setActiveFilter('oxford_3000')}
            >
              Oxford 3000 📚
            </button>
            <button 
              className={`pill-btn ${activeFilter === 'verb' ? 'active' : ''}`}
              onClick={() => setActiveFilter('verb')}
            >
              Verbs
            </button>
            <button 
              className={`pill-btn ${activeFilter === 'noun' ? 'active' : ''}`}
              onClick={() => setActiveFilter('noun')}
            >
              Nouns
            </button>
            <button 
              className={`pill-btn ${activeFilter === 'adjective' ? 'active' : ''}`}
              onClick={() => setActiveFilter('adjective')}
            >
              Adjectives
            </button>
            <button 
              className={`pill-btn ${activeFilter === 'adverb' ? 'active' : ''}`}
              onClick={() => setActiveFilter('adverb')}
            >
              Adverbs
            </button>
          </div>
        </div>

        <div className="filter-group-row secondary-filters">
          <div className="filter-sub-group">
            <span className="filter-group-title">Level CEFR:</span>
            <div className="filter-pills">
              {['all', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'].map(lvl => (
                <button 
                  key={lvl}
                  className={`pill-btn small ${levelFilter === lvl ? 'active' : ''}`}
                  onClick={() => setLevelFilter(lvl)}
                >
                  {lvl === 'all' ? 'Semua' : lvl}
                </button>
              ))}
            </div>
          </div>

          <div className="filter-sub-group">
            <span className="filter-group-title">Status:</span>
            <div className="filter-pills">
              <button 
                className={`pill-btn small ${statusFilter === 'all' ? 'active' : ''}`}
                onClick={() => setStatusFilter('all')}
              >
                Semua
              </button>
              <button 
                className={`pill-btn small ${statusFilter === 'unlearned' ? 'active' : ''}`}
                onClick={() => setStatusFilter('unlearned')}
              >
                Belum Dipelajari
              </button>
              <button 
                className={`pill-btn small ${statusFilter === 'review' ? 'active' : ''}`}
                onClick={() => setStatusFilter('review')}
              >
                Perlu Review ({reviewIds.size})
              </button>
              <button 
                className={`pill-btn small ${statusFilter === 'mastered' ? 'active' : ''}`}
                onClick={() => setStatusFilter('mastered')}
              >
                Sudah Paham ({masteredIds.size})
              </button>
              <button 
                className={`pill-btn small ${statusFilter === 'favorites' ? 'active' : ''}`}
                onClick={() => setStatusFilter('favorites')}
              >
                Favorit ❤️ ({favoriteIds.size})
              </button>
            </div>
          </div>
        </div>

        {/* 50-Card Batch Toolbar */}
        <div className="flashcard-session-toolbar">
          <div className="session-tag-wrap">
            <span className="session-badge">
              {isBatchMode ? '🎴 Sesi Belajar: 50 Kartu Acak' : `📚 Menampilkan Semua (${filteredList.length}) Kartu`}
            </span>
            <span className="session-sub">
              {isBatchMode ? 'Diacak otomatis setiap refresh untuk latihan harian' : 'Urutan lengkap sesuai filter'}
            </span>
          </div>

          <div className="session-buttons">
            <button 
              className="cute-primary-btn small-btn" 
              onClick={handleNewRandomBatch}
              title="Acak 50 kosakata baru sekarang"
            >
              <Shuffle size={16} />
              <span>Acak 50 Kartu Baru</span>
            </button>

            <button 
              className="pill-btn small" 
              onClick={() => setIsBatchMode(!isBatchMode)}
              title="Ganti antara mode 50 kartu acak atau semua kartu"
            >
              {isBatchMode ? `Lihat Semua (${filteredList.length})` : 'Mode 50 Kartu Acak'}
            </button>
          </div>
        </div>
      </div>

      {/* Main Flashcard Arena */}
      {activeDeck.length === 0 ? (
        <div className="empty-state-box">
          <BookMarked size={48} className="empty-icon" />
          <h3>Tidak ada kartu yang cocok</h3>
          <p>Coba ganti filter kategori atau status belajar Anda untuk melihat kartu lainnya.</p>
          <button 
            className="cute-primary-btn"
            onClick={() => {
              setActiveFilter('all');
              setLevelFilter('all');
              setStatusFilter('all');
            }}
          >
            Reset Semua Filter
          </button>
        </div>
      ) : isSessionComplete ? (
        /* Sesi Selesai Celebration Card */
        <div className="session-complete-card">
          <Trophy size={64} className="trophy-icon" />
          <h2>Hebat Sekali! Sesi Selesai 🎉</h2>
          <p>
            Kamu telah menuntaskan pembelajaran <strong>{activeDeck.length} kartu</strong> pada sesi ini.
            Penguasaan kosakata kamu semakin meningkat!
          </p>
          <div className="complete-action-buttons">
            <button className="cute-primary-btn" onClick={handleNewRandomBatch}>
              <Shuffle size={18} />
              <span>Mulai 50 Kartu Baru 🚀</span>
            </button>
            <button 
              className="cute-secondary-btn" 
              onClick={() => {
                setIsSessionComplete(false);
                setCurrentIndex(0);
              }}
            >
              <RotateCw size={18} />
              <span>Ulangi Sesi Ini</span>
            </button>
          </div>
        </div>
      ) : (
        <div className="flashcard-scene">
          {/* Progress Header with direct navigation arrows */}
          <div className="flashcard-progress-bar-wrap">
            <div className="progress-info">
              <div className="progress-counter-badge">
                <span className="progress-text">
                  Kartu <strong>{currentIndex + 1}</strong> dari <strong>{activeDeck.length}</strong>
                </span>
                {isBatchMode && <span className="batch-pill-indicator">Sesi 50 Acak</span>}
              </div>

              <div className="progress-quick-nav">
                <button 
                  className="quick-nav-btn"
                  onClick={prevCard}
                  disabled={currentIndex === 0}
                  title="Kartu Sebelumnya (Panah Kiri)"
                >
                  <ChevronLeft size={18} />
                </button>
                <button 
                  className="quick-nav-btn"
                  onClick={nextCard}
                  disabled={currentIndex === activeDeck.length - 1}
                  title="Kartu Berikutnya (Panah Kanan)"
                >
                  <ChevronRight size={18} />
                </button>
              </div>

              <span className="shortcut-tip">💡 Klik kartu / Spasi: Balik • ◄ / ►: Pindah kartu</span>
            </div>

            <div className="progress-track">
              <div 
                className="progress-fill" 
                style={{ width: `${((currentIndex + 1) / activeDeck.length) * 100}%` }}
              />
            </div>
          </div>

          {/* Flashcard Stage with Floating Lateral Navigation Arrows */}
          <div className="flashcard-stage-container">
            {/* FLOATING LEFT CHEVRON BUTTON */}
            <button 
              className="card-floating-nav-btn prev-floating-btn"
              onClick={prevCard}
              disabled={currentIndex === 0}
              title="Kartu Sebelumnya (Tekan Panah Kiri ◄)"
              aria-label="Previous card"
            >
              <ChevronLeft size={34} />
              <span className="nav-btn-sub">Prev</span>
            </button>

            {/* 3D Card Element */}
            <div 
              className={`flashcard-3d ${isFlipped ? 'flipped' : ''}`}
              onClick={flipCard}
              title="Klik untuk membalik kartu (atau tekan Spasi)"
            >
              {/* FRONT OF CARD */}
              <div className="flashcard-face flashcard-front">
                <div className="card-top-bar">
                  <div className="badge-group">
                    <span className={`badge-pill badge-${currentCard.type}`}>
                      {currentCard.type === 'phrasal_verb' ? 'Phrasal Verb ⚡' : currentCard.type === 'collocation' ? 'Collocation 🧩' : 'Oxford 📚'}
                    </span>
                    <span className="badge-pill badge-level">{currentCard.level}</span>
                    <span className="badge-pill badge-pos">{currentCard.pos}</span>
                  </div>

                  <div className="card-top-actions">
                    <button 
                      className={`icon-action-btn heart-btn ${isFavorite ? 'favorited' : ''}`}
                      onClick={(e) => {
                        e.stopPropagation();
                        sounds.playPop();
                        onToggleFavorite(currentCard.id);
                      }}
                      title="Simpan ke Favorit"
                    >
                      <Heart size={20} fill={isFavorite ? '#EF4444' : 'none'} color={isFavorite ? '#EF4444' : 'currentColor'} />
                    </button>
                  </div>
                </div>

                <div className="card-center-content">
                  <h2 className="card-term">{currentCard.term}</h2>
                  <div className="card-ipa-wrap">
                    <span className="card-ipa">{currentCard.ipa}</span>
                    <button 
                      className={`speak-btn ${speaking ? 'is-speaking' : ''}`}
                      onClick={(e) => playSpeech(currentCard.term, e)}
                      title={`Dengarkan pengucapan (${accent === 'en-US' ? 'US' : 'UK'})`}
                    >
                      <Volume2 size={22} />
                    </button>
                  </div>
                  <p className="card-category-tag">Topik: {currentCard.category}</p>

                  {showHint ? (
                    <div className="hint-bubble" onClick={(e) => e.stopPropagation()}>
                      <span className="hint-label">Petunjuk:</span> {currentCard.hint}
                    </div>
                  ) : (
                    <button 
                      className="hint-toggle-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        sounds.playPop();
                        setShowHint(true);
                      }}
                    >
                      <HelpCircle size={15} /> Butuh Petunjuk?
                    </button>
                  )}
                </div>

                <div className="card-bottom-prompt">
                  <RotateCw size={16} className="rotate-icon" />
                  <span>Klik kartu untuk membalik & lihat arti serta contoh</span>
                </div>
              </div>

              {/* BACK OF CARD */}
              <div className="flashcard-face flashcard-back">
                <div className="card-top-bar">
                  <div className="badge-group">
                    <span className="badge-pill badge-meaning-title">Arti & Makna (ID)</span>
                    <span className="badge-pill badge-level">{currentCard.level}</span>
                    <span className="badge-pill badge-pos">{currentCard.pos}</span>
                  </div>
                  <button 
                    className={`icon-action-btn heart-btn ${isFavorite ? 'favorited' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      sounds.playPop();
                      onToggleFavorite(currentCard.id);
                    }}
                  >
                    <Heart size={20} fill={isFavorite ? '#EF4444' : 'none'} color={isFavorite ? '#EF4444' : 'currentColor'} />
                  </button>
                </div>

                <div className="card-back-main">
                  <h3 className="card-indonesian-meaning">{currentCard.meaningId}</h3>
                  
                  <div className="example-section" onClick={(e) => e.stopPropagation()}>
                    <div className="example-header">
                      <span className="example-badge">Contoh Kalimat:</span>
                      <button 
                        className="speak-mini-btn"
                        onClick={(e) => playSpeech(currentCard.exampleEn, e)}
                        title="Dengarkan seluruh kalimat"
                      >
                        <Volume2 size={16} /> Dengarkan
                      </button>
                    </div>
                    <p className="example-en">"{currentCard.exampleEn}"</p>
                    <p className="example-id">Artinya: "{currentCard.exampleId}"</p>
                  </div>

                  <div className="note-box" onClick={(e) => e.stopPropagation()}>
                    <span className="note-title">💡 Tips Pemakaian:</span>
                    <span className="note-text">{currentCard.hint}</span>
                  </div>
                </div>

                <div className="card-bottom-prompt">
                  <RotateCw size={16} className="rotate-icon" />
                  <span>Klik untuk kembali ke depan</span>
                </div>
              </div>
            </div>

            {/* FLOATING RIGHT CHEVRON BUTTON */}
            <button 
              className="card-floating-nav-btn next-floating-btn"
              onClick={nextCard}
              disabled={currentIndex === activeDeck.length - 1}
              title="Kartu Berikutnya (Tekan Panah Kanan ►)"
              aria-label="Next card"
            >
              <ChevronRight size={34} />
              <span className="nav-btn-sub">Next</span>
            </button>
          </div>

          {/* Action Navigation Controls Below Card */}
          <div className="flashcard-controls">
            <button 
              className="nav-control-btn prev-btn" 
              onClick={prevCard}
              disabled={currentIndex === 0}
              title="Kembali ke kartu sebelumnya"
            >
              <ChevronLeft size={20} />
              <span>Sebelumnya</span>
            </button>

            <button 
              className="action-btn review-btn"
              onClick={handleReview}
              title="Tandai perlu diulang lagi nanti (+5 XP)"
            >
              <AlertCircle size={20} />
              <span>Perlu Review</span>
              <span className="xp-tag">+5 XP</span>
            </button>

            <button 
              className="action-btn master-btn"
              onClick={handleMastered}
              title="Tandai sudah hafal dan paham! (+15 XP)"
            >
              <CheckCircle size={20} />
              <span>Sudah Paham!</span>
              <span className="xp-tag">+15 XP</span>
            </button>

            <button 
              className="nav-control-btn next-btn" 
              onClick={nextCard}
              disabled={currentIndex === activeDeck.length - 1}
              title="Lanjut ke kartu berikutnya"
            >
              <span>Berikutnya</span>
              <ChevronRight size={20} />
            </button>
          </div>

          {/* Keyboard & Swipe Navigation Guide */}
          <div className="flashcard-nav-tip-footer">
            <span>⌨️ Pintasan Keyboard:</span>
            <span className="key-cap">◄ Panah Kiri</span> Sebelumnya
            <span className="key-cap">Spasi</span> Balik Kartu
            <span className="key-cap">Panah Kanan ►</span> Berikutnya
            <span className="key-cap">▲ / ▼</span> Petunjuk
          </div>
        </div>
      )}
    </div>
  );
}
