import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { 
  Volume2, 
  RotateCcw, 
  Check, 
  ArrowRight, 
  Sparkles, 
  Lightbulb, 
  Flame, 
  HelpCircle,
  Undo2
} from 'lucide-react';
import { sounds } from '../utils/soundEffects';
import { speechAssistant } from '../utils/speechUtils';
import { allVocabulary } from '../data';
import Mascot from './Mascot';

// Helper to cleanly tokenize a sentence while keeping punctuation attached or readable
const tokenizeSentence = (sentence) => {
  if (!sentence) return [];
  // Clean quotes or clean punctuation
  return sentence.trim().split(/\s+/);
};

export default function SentenceScrambleGame({ onAddXP, accent }) {
  const [selectedCategory, setSelectedCategory] = useState('all'); // 'all', 'phrasal_verb', 'collocation', 'oxford_3000'
  const [currentItem, setCurrentItem] = useState(null);
  const [scrambledWords, setScrambledWords] = useState([]); // array of { id, text, used }
  const [userWords, setUserWords] = useState([]); // array of { id, text }
  const [isAnswered, setIsAnswered] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [combo, setCombo] = useState(0);
  const [score, setScore] = useState(0);

  // Filter pool based on selected category
  const getPool = () => {
    let pool = allVocabulary.filter(item => item.exampleEn && item.exampleEn.split(/\s+/).length >= 4);
    if (selectedCategory !== 'all') {
      pool = pool.filter(item => item.type === selectedCategory);
    }
    return pool;
  };

  // Pick new question
  const pickNewQuestion = () => {
    const pool = getPool();
    if (pool.length === 0) return;
    const randomItem = pool[Math.floor(Math.random() * pool.length)];
    setCurrentItem(randomItem);

    const originalTokens = tokenizeSentence(randomItem.exampleEn);
    // Create token objects with unique ids
    const tokens = originalTokens.map((word, idx) => ({
      id: `${word}-${idx}-${Math.random()}`,
      text: word,
      originalIndex: idx,
      used: false
    }));

    // Shuffle tokens (ensuring not identical to original order)
    let shuffled = [...tokens];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }

    setScrambledWords(shuffled);
    setUserWords([]);
    setIsAnswered(false);
    setIsCorrect(false);
    setShowHint(false);
  };

  useEffect(() => {
    pickNewQuestion();
  }, [selectedCategory]);

  // Click word from bank to add to sentence
  const handleSelectWord = (wordObj) => {
    if (isAnswered) return;
    sounds.playPop();

    // Mark as used in scrambled
    setScrambledWords(prev =>
      prev.map(w => w.id === wordObj.id ? { ...w, used: true } : w)
    );

    // Add to user sentence
    setUserWords(prev => [...prev, wordObj]);
  };

  // Click word in user sentence to return it to bank
  const handleRemoveWord = (wordObj) => {
    if (isAnswered) return;
    sounds.playPop();

    setUserWords(prev => prev.filter(w => w.id !== wordObj.id));
    setScrambledWords(prev =>
      prev.map(w => w.id === wordObj.id ? { ...w, used: false } : w)
    );
  };

  // Reset words in rack
  const handleResetRack = () => {
    sounds.playPop();
    setUserWords([]);
    setScrambledWords(prev => prev.map(w => ({ ...w, used: false })));
  };

  // Undo last word
  const handleUndo = () => {
    if (userWords.length === 0 || isAnswered) return;
    sounds.playPop();
    const lastWord = userWords[userWords.length - 1];
    setUserWords(prev => prev.slice(0, -1));
    setScrambledWords(prev =>
      prev.map(w => w.id === lastWord.id ? { ...w, used: false } : w)
    );
  };

  // Check Answer
  const handleCheckAnswer = () => {
    if (userWords.length === 0) return;

    const userSentence = userWords.map(w => w.text).join(' ').trim();
    const originalSentence = currentItem.exampleEn.trim();

    // Clean comparison: strip trailing periods and normalize spaces
    const normalize = str => str.replace(/[.,!?;:"'“”]/g, '').toLowerCase().trim();

    const correct = normalize(userSentence) === normalize(originalSentence);

    setIsAnswered(true);
    setIsCorrect(correct);

    if (correct) {
      sounds.playCorrect();
      const newCombo = combo + 1;
      setCombo(newCombo);
      const earnedXP = 20 + Math.min(newCombo * 5, 20);
      setScore(prev => prev + earnedXP);
      onAddXP(earnedXP);

      // Play audio of complete sentence
      speechAssistant.setAccent(accent);
      speechAssistant.speak(originalSentence);

      // Confetti burst
      confetti({
        particleCount: 50,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#10B981', '#60A5FA', '#F59E0B']
      });
    } else {
      sounds.playWrong();
      setCombo(0);
    }
  };

  const playSpeech = (text) => {
    speechAssistant.setAccent(accent);
    speechAssistant.speak(text);
  };

  if (!currentItem) return null;

  return (
    <div className="scramble-game-container">
      {/* Header Info & Mascot */}
      <div className="game-top-header">
        <Mascot 
          mood={isAnswered ? (isCorrect ? 'celebrate' : 'thinking') : (combo > 2 ? 'cheer' : 'happy')}
          message={
            isAnswered 
              ? (isCorrect 
                  ? `Luar biasa benar! Kamu dapat ${combo > 1 ? `+${20 + Math.min(combo * 5, 20)} XP (Combo x${combo})!` : '+20 XP!'}` 
                  : "Hampir tepat! Coba lihat susunan kalimat aslinya ya.")
              : "Susun kata-kata acak di bawah ini menjadi kalimat bahasa Inggris yang padu!"
          }
          size={72}
        />

        <div className="game-stats-pill-group">
          {combo > 1 && (
            <div className="stat-pill combo-pill animate-bounce">
              <Flame size={18} className="flame-icon" />
              <span>Combo x{combo}</span>
            </div>
          )}
          <div className="stat-pill score-pill">
            <Sparkles size={18} />
            <span>Skor Game: {score}</span>
          </div>
        </div>
      </div>

      {/* Category selector */}
      <div className="category-tabs-bar">
        <span className="category-tabs-title">Materi:</span>
        <div className="category-pill-list">
          <button 
            className={`cat-pill-btn ${selectedCategory === 'all' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setSelectedCategory('all'); }}
          >
            Semua Materi
          </button>
          <button 
            className={`cat-pill-btn ${selectedCategory === 'phrasal_verb' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setSelectedCategory('phrasal_verb'); }}
          >
            Phrasal Verbs ⚡
          </button>
          <button 
            className={`cat-pill-btn ${selectedCategory === 'collocation' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setSelectedCategory('collocation'); }}
          >
            Collocations 🧩
          </button>
          <button 
            className={`cat-pill-btn ${selectedCategory === 'oxford_3000' ? 'active' : ''}`}
            onClick={() => { sounds.playPop(); setSelectedCategory('oxford_3000'); }}
          >
            Oxford 3000 📚
          </button>
        </div>
      </div>

      {/* Main Game Card */}
      <div className="scramble-board-card">
        {/* Target Term Clue */}
        <div className="target-term-banner">
          <div className="target-tags">
            <span className={`badge-pill badge-${currentItem.type}`}>
              {currentItem.type === 'phrasal_verb' ? 'Phrasal Verb' : currentItem.type === 'collocation' ? 'Collocation' : 'Oxford 3000'}
            </span>
            <span className="badge-pill badge-level">{currentItem.level}</span>
          </div>

          <div className="target-phrase-info">
            <span className="target-label">Kata Kunci:</span>
            <strong className="target-word">{currentItem.term}</strong>
            <span className="target-ipa">{currentItem.ipa}</span>
            <button 
              className="speak-mini-btn"
              onClick={() => playSpeech(currentItem.term)}
              title="Dengarkan kata kunci"
            >
              <Volume2 size={16} />
            </button>
          </div>
        </div>

        {/* Translation Prompt (Challenge Goal) */}
        <div className="translation-challenge-box">
          <span className="challenge-guide">Susun kalimat untuk arti bahasa Indonesia berikut:</span>
          <p className="indonesian-sentence-prompt">"{currentItem.exampleId}"</p>
          <div className="meaning-snippet">
            <span>Arti kata "{currentItem.term}": <strong>{currentItem.meaningId}</strong></span>
          </div>
        </div>

        {/* Answer Construction Area */}
        <div className={`answer-rack ${userWords.length === 0 ? 'is-empty' : ''} ${isAnswered ? (isCorrect ? 'is-correct' : 'is-wrong') : ''}`}>
          {userWords.length === 0 ? (
            <span className="rack-placeholder">Klik kata-kata acak di bawah untuk menyusun kalimat di sini...</span>
          ) : (
            <div className="user-tokens-list">
              {userWords.map((token, idx) => (
                <button
                  key={`user-${token.id}-${idx}`}
                  className="word-token user-token"
                  onClick={() => handleRemoveWord(token)}
                  disabled={isAnswered}
                  title="Klik untuk kembalikan kata ini"
                >
                  {token.text}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Answer Action Bar (Undo, Reset) */}
        {!isAnswered && (
          <div className="rack-actions-bar">
            <button 
              className="rack-btn undo-btn"
              onClick={handleUndo}
              disabled={userWords.length === 0}
            >
              <Undo2 size={16} /> Hapus Terakhir
            </button>

            <button 
              className="rack-btn reset-btn"
              onClick={handleResetRack}
              disabled={userWords.length === 0}
            >
              <RotateCcw size={16} /> Reset Susunan
            </button>
          </div>
        )}

        {/* Scrambled Word Bank */}
        <div className="scrambled-bank-section">
          <span className="bank-label">Pilihan Kata Acak:</span>
          <div className="word-tokens-grid">
            {scrambledWords.map((token) => (
              <button
                key={`scramble-${token.id}`}
                className={`word-token bank-token ${token.used ? 'is-used' : ''}`}
                onClick={() => handleSelectWord(token)}
                disabled={token.used || isAnswered}
              >
                {token.text}
              </button>
            ))}
          </div>
        </div>

        {/* Hint Box */}
        {showHint ? (
          <div className="hint-card">
            <Lightbulb size={18} className="hint-icon" />
            <span><strong>Petunjuk:</strong> Kata pertama diawali huruf kapital. Kata kunci "{currentItem.term}" ada di dalam kalimat ini.</span>
          </div>
        ) : (
          !isAnswered && (
            <button 
              className="hint-pill-btn"
              onClick={() => { sounds.playPop(); setShowHint(true); }}
            >
              <HelpCircle size={15} /> Butuh Bantuan Petunjuk?
            </button>
          )
        )}

        {/* Feedback on Answer */}
        {isAnswered && (
          <div className={`answer-feedback-card ${isCorrect ? 'correct-card' : 'wrong-card'}`}>
            <div className="feedback-status-row">
              {isCorrect ? (
                <>
                  <div className="status-badge success">
                    <Check size={18} /> Jawaban Anda Tepat Sekali!
                  </div>
                  <span className="xp-earned-badge">+20 XP Ditambahkan</span>
                </>
              ) : (
                <div className="status-badge error">
                  Belum tepat, susunan yang benar adalah:
                </div>
              )}
            </div>

            <div className="correct-sentence-reveal">
              <p className="full-en-sentence">"{currentItem.exampleEn}"</p>
              <button 
                className="listen-full-btn"
                onClick={() => playSpeech(currentItem.exampleEn)}
                title="Dengarkan pengucapan kalimat lengkap"
              >
                <Volume2 size={18} /> Dengarkan Suara Native
              </button>
            </div>
          </div>
        )}

        {/* Bottom Game Controls */}
        <div className="scramble-controls">
          {!isAnswered ? (
            <button
              className="cute-primary-btn check-answer-btn"
              onClick={handleCheckAnswer}
              disabled={userWords.length === 0}
            >
              <Check size={20} />
              Cek Jawaban Saya
            </button>
          ) : (
            <button
              className="cute-primary-btn next-question-btn"
              onClick={() => { sounds.playPop(); pickNewQuestion(); }}
            >
              <span>Soal Berikutnya</span>
              <ArrowRight size={20} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
