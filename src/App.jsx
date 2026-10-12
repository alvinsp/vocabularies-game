import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import FlashcardGame from './components/FlashcardGame';
import SentenceScrambleGame from './components/SentenceScrambleGame';
import QuizGame from './components/QuizGame';
import MatchPairsGame from './components/MatchPairsGame';
import DictionaryExplorer from './components/DictionaryExplorer';
import { 
  getStoredXP, 
  addXP, 
  getStreakData, 
  getMasteredIds, 
  getReviewIds, 
  getFavoriteIds, 
  toggleFavoriteId, 
  markAsMastered, 
  markForReview,
  getStoredTheme,
  saveStoredTheme,
  getStoredAccent,
  saveStoredAccent
} from './utils/storage';
import { sounds } from './utils/soundEffects';
import { getStats } from './data';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('flashcard');
  const [xp, setXp] = useState(getStoredXP());
  const [streakData, setStreakData] = useState({ streak: 1, isNewDay: false });
  const [masteredIds, setMasteredIds] = useState(getMasteredIds());
  const [reviewIds, setReviewIds] = useState(getReviewIds());
  const [favoriteIds, setFavoriteIds] = useState(getFavoriteIds());
  const [theme, setTheme] = useState(getStoredTheme());
  const [accent, setAccent] = useState(getStoredAccent());
  const [muted, setMuted] = useState(sounds.muted);
  const [streakToast, setStreakToast] = useState(false);

  const stats = getStats();

  useEffect(() => {
    // Check and update streak
    const data = getStreakData();
    setStreakData(data);
    if (data.isNewDay) {
      setStreakToast(true);
      setTimeout(() => setStreakToast(false), 5000);
    }
  }, []);

  // Update theme on root
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    saveStoredTheme(theme);
  }, [theme]);

  // Update accent
  useEffect(() => {
    saveStoredAccent(accent);
  }, [accent]);

  const handleAddXP = (amount) => {
    const updated = addXP(amount);
    setXp(updated);
  };

  const handleMarkMastered = (id) => {
    markAsMastered(id);
    setMasteredIds(getMasteredIds());
    setReviewIds(getReviewIds());
  };

  const handleMarkReview = (id) => {
    markForReview(id);
    setMasteredIds(getMasteredIds());
    setReviewIds(getReviewIds());
  };

  const handleToggleFavorite = (id) => {
    toggleFavoriteId(id);
    setFavoriteIds(getFavoriteIds());
  };

  return (
    <div className={`app-container theme-${theme}`}>
      {/* Toast Notification for Daily Streak */}
      {streakToast && (
        <div className="streak-toast-card animate-slide-down">
          <span className="toast-emoji">🔥</span>
          <div className="toast-content">
            <strong>Streak Belajar Aktif! Hari ke-{streakData.streak}</strong>
            <p>Hebat! Konsistensi belajar harian adalah kunci utama fasih bahasa Inggris.</p>
          </div>
          <button className="toast-close-btn" onClick={() => setStreakToast(false)}>✕</button>
        </div>
      )}

      {/* Main Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        xp={xp}
        streak={streakData.streak}
        accent={accent}
        setAccent={setAccent}
        theme={theme}
        setTheme={setTheme}
        muted={muted}
        setMuted={setMuted}
        stats={stats}
      />

      {/* Main Content Arena */}
      <main className="main-content-area">
        {activeTab === 'flashcard' && (
          <FlashcardGame
            masteredIds={masteredIds}
            reviewIds={reviewIds}
            favoriteIds={favoriteIds}
            onMarkMastered={handleMarkMastered}
            onMarkReview={handleMarkReview}
            onToggleFavorite={handleToggleFavorite}
            onAddXP={handleAddXP}
            accent={accent}
          />
        )}

        {activeTab === 'scramble' && (
          <SentenceScrambleGame
            onAddXP={handleAddXP}
            accent={accent}
          />
        )}

        {activeTab === 'quiz' && (
          <QuizGame
            onAddXP={handleAddXP}
            accent={accent}
          />
        )}

        {activeTab === 'match' && (
          <MatchPairsGame
            onAddXP={handleAddXP}
            accent={accent}
          />
        )}

        {activeTab === 'dictionary' && (
          <DictionaryExplorer
            masteredIds={masteredIds}
            reviewIds={reviewIds}
            favoriteIds={favoriteIds}
            onMarkMastered={handleMarkMastered}
            onMarkReview={handleMarkReview}
            onToggleFavorite={handleToggleFavorite}
            accent={accent}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <span className="footer-logo">🦉 VocabPintar</span>
            <p>Aplikasi Pembelajaran Oxford Phrasal Verbs, Collocations, & Oxford 3000 Vocabulary.</p>
          </div>

          <div className="footer-stats-badges">
            <span className="footer-pill">⚡ 123 Phrasal Verbs</span>
            <span className="footer-pill">🧩 56 Collocations</span>
            <span className="footer-pill">📚 68 Oxford Vocabularies</span>
            <span className="footer-pill">🎯 {masteredIds.size} Dikuasai</span>
          </div>

          <div className="footer-bottom">
            <span>Dirancang khusus untuk pembelajar tingkat intermediate & advanced. Siap deploy di Vercel! 🚀</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
