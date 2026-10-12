import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { 
  Sparkles, 
  RotateCcw, 
  Trophy, 
  Clock, 
  Volume2, 
  CheckCircle2, 
  Zap,
  ArrowRight
} from 'lucide-react';
import { sounds } from '../utils/soundEffects';
import { speechAssistant } from '../utils/speechUtils';
import { allVocabulary, phrasalVerbs, collocations, oxfordVocab } from '../data';
import Mascot from './Mascot';

export default function MatchPairsGame({ onAddXP, accent }) {
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [cards, setCards] = useState([]); // array of { id, pairId, text, type: 'en' | 'id', matched: false, rawItem }
  const [selectedCards, setSelectedCards] = useState([]);
  const [matchedCount, setMatchedCount] = useState(0);
  const [moves, setMoves] = useState(0);
  const [seconds, setSeconds] = useState(0);
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const [isGameComplete, setIsGameComplete] = useState(false);

  // Initialize new round with 6 pairs (12 cards)
  const startNewRound = () => {
    let pool = allVocabulary;
    if (categoryFilter === 'phrasal_verb') pool = phrasalVerbs;
    else if (categoryFilter === 'collocation') pool = collocations;
    else if (categoryFilter === 'oxford_3000') pool = oxfordVocab;

    // Pick 6 random items
    const shuffled = [...pool].sort(() => 0.5 - Math.random());
    const selectedItems = shuffled.slice(0, 6);

    const generatedCards = [];
    selectedItems.forEach((item, idx) => {
      // English card
      generatedCards.push({
        id: `card-en-${item.id}-${idx}`,
        pairId: item.id,
        text: item.term,
        lang: 'en',
        matched: false,
        rawItem: item
      });
      // Indonesian meaning card
      generatedCards.push({
        id: `card-id-${item.id}-${idx}`,
        pairId: item.id,
        text: item.meaningId,
        lang: 'id',
        matched: false,
        rawItem: item
      });
    });

    // Shuffle cards
    generatedCards.sort(() => 0.5 - Math.random());

    setCards(generatedCards);
    setSelectedCards([]);
    setMatchedCount(0);
    setMoves(0);
    setSeconds(0);
    setIsTimerRunning(true);
    setIsGameComplete(false);
  };

  useEffect(() => {
    startNewRound();
  }, [categoryFilter]);

  // Timer
  useEffect(() => {
    let interval = null;
    if (isTimerRunning && !isGameComplete) {
      interval = setInterval(() => {
        setSeconds(prev => prev + 1);
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isTimerRunning, isGameComplete]);

  // Handle Card Click
  const handleCardClick = (card) => {
    if (card.matched || selectedCards.find(c => c.id === card.id) || selectedCards.length >= 2) {
      return;
    }

    sounds.playPop();

    // If English card, pronounce it
    if (card.lang === 'en') {
      speechAssistant.setAccent(accent);
      speechAssistant.speak(card.text);
    }

    const nextSelected = [...selectedCards, card];
    setSelectedCards(nextSelected);

    if (nextSelected.length === 2) {
      setMoves(prev => prev + 1);
      const [cardA, cardB] = nextSelected;

      if (cardA.pairId === cardB.pairId && cardA.lang !== cardB.lang) {
        // MATCH!
        sounds.playCorrect();
        setCards(prev => prev.map(c => 
          c.pairId === cardA.pairId ? { ...c, matched: true } : c
        ));
        setSelectedCards([]);
        const newMatched = matchedCount + 1;
        setMatchedCount(newMatched);
        onAddXP(10);

        if (newMatched === 6) {
          // VICTORY!
          setIsGameComplete(true);
          setIsTimerRunning(false);
          sounds.playFanfare();
          onAddXP(30); // bonus victory XP
          confetti({
            particleCount: 80,
            spread: 90,
            origin: { y: 0.5 },
            colors: ['#F59E0B', '#10B981', '#6366F1', '#EC4899']
          });
        }
      } else {
        // MISMATCH
        sounds.playWrong();
        setTimeout(() => {
          setSelectedCards([]);
        }, 850);
      }
    }
  };

  const formatTime = (secs) => {
    const mins = Math.floor(secs / 60);
    const rem = secs % 60;
    return `${mins}:${rem < 10 ? '0' : ''}${rem}`;
  };

  return (
    <div className="match-game-container">
      {/* Top Header & Mascot */}
      <div className="game-top-header">
        <Mascot 
          mood={isGameComplete ? 'celebrate' : (matchedCount > 3 ? 'cheer' : 'happy')}
          message={
            isGameComplete
              ? `Luar biasa! Kamu menyelesaikan semua pasangan dalam ${formatTime(seconds)} dan ${moves} langkah!`
              : `Klik 1 kartu bahasa Inggris dan pasangkan dengan artinya dalam bahasa Indonesia!`
          }
          size={72}
        />

        <div className="game-stats-pill-group">
          <div className="stat-pill timer-pill">
            <Clock size={18} />
            <span>{formatTime(seconds)}</span>
          </div>
          <div className="stat-pill moves-pill">
            <Zap size={18} />
            <span>{moves} Langkah</span>
          </div>
          <div className="stat-pill match-progress-pill">
            <CheckCircle2 size={18} />
            <span>{matchedCount} / 6 Pasang</span>
          </div>
        </div>
      </div>

      {/* Category selector */}
      <div className="category-tabs-bar">
        <span className="category-tabs-title">Materi:</span>
        <div className="category-pill-list">
          <button 
            className={`cat-pill-btn ${categoryFilter === 'all' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setCategoryFilter('all'); }}
          >
            Semua Materi
          </button>
          <button 
            className={`cat-pill-btn ${categoryFilter === 'phrasal_verb' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setCategoryFilter('phrasal_verb'); }}
          >
            Phrasal Verbs ⚡
          </button>
          <button 
            className={`cat-pill-btn ${categoryFilter === 'collocation' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setCategoryFilter('collocation'); }}
          >
            Collocations 🧩
          </button>
          <button 
            className={`cat-pill-btn ${categoryFilter === 'oxford_3000' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setCategoryFilter('oxford_3000'); }}
          >
            Oxford 3000 📚
          </button>
        </div>
      </div>

      {/* Matching Grid */}
      <div className="match-board-card">
        {isGameComplete ? (
          <div className="match-victory-screen">
            <div className="trophy-badge animate-bounce">
              <Trophy size={64} className="trophy-icon" />
            </div>
            <h2>Selamat! Semua Pasangan Cocok! 🎉</h2>
            <p className="victory-stats-summary">
              Waktu: <strong>{formatTime(seconds)}</strong> | Total Langkah: <strong>{moves}</strong>
            </p>
            <div className="victory-xp-tag">
              <Sparkles size={20} />
              <span>Total +90 XP Berhasil Dikumpulkan!</span>
            </div>

            <button 
              className="cute-primary-btn play-again-btn"
              onClick={() => { sounds.playPop(); startNewRound(); }}
            >
              <span>Main Babak Baru</span>
              <ArrowRight size={20} />
            </button>
          </div>
        ) : (
          <div className="match-cards-grid">
            {cards.map((card) => {
              const isSelected = selectedCards.some(c => c.id === card.id);
              const isWrong = selectedCards.length === 2 && isSelected && selectedCards[0].pairId !== selectedCards[1].pairId;
              
              let cardClass = `match-card-tile card-${card.lang}`;
              if (card.matched) cardClass += ' is-matched';
              if (isSelected) cardClass += ' is-selected';
              if (isWrong) cardClass += ' is-wrong-shake';

              return (
                <button
                  key={card.id}
                  className={cardClass}
                  onClick={() => handleCardClick(card)}
                  disabled={card.matched}
                >
                  <span className="card-lang-tag">
                    {card.lang === 'en' ? '🇬🇧 EN' : '🇮🇩 ID'}
                  </span>
                  <span className="card-tile-text">{card.text}</span>
                  {card.matched && <CheckCircle2 size={18} className="matched-check" />}
                </button>
              );
            })}
          </div>
        )}

        {/* Footer Reset */}
        {!isGameComplete && (
          <div className="match-footer-actions">
            <button 
              className="rack-btn reset-btn"
              onClick={() => { sounds.playPop(); startNewRound(); }}
            >
              <RotateCcw size={16} /> Acak Ulang Babak Ini
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
