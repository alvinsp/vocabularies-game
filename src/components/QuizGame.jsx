import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { 
  Volume2, 
  Check, 
  X, 
  ArrowRight, 
  Sparkles, 
  Flame, 
  HelpCircle,
  Award
} from 'lucide-react';
import { sounds } from '../utils/soundEffects';
import { speechAssistant } from '../utils/speechUtils';
import { allVocabulary, phrasalVerbs, collocations, oxfordVocab } from '../data';
import Mascot from './Mascot';

export default function QuizGame({ onAddXP, accent }) {
  const [quizMode, setQuizMode] = useState('definition'); // 'definition', 'reverse', 'fill_blank'
  const [categoryFilter, setCategoryFilter] = useState('all'); // 'all', 'phrasal_verb', 'collocation', 'oxford_3000'
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [combo, setCombo] = useState(0);
  const [score, setScore] = useState(0);

  // Generate question
  const generateQuestion = () => {
    let pool = allVocabulary;
    if (categoryFilter === 'phrasal_verb') pool = phrasalVerbs;
    else if (categoryFilter === 'collocation') pool = collocations;
    else if (categoryFilter === 'oxford_3000') pool = oxfordVocab;

    if (pool.length < 4) pool = allVocabulary;

    // Pick target
    const target = pool[Math.floor(Math.random() * pool.length)];

    // Pick 3 distractors
    const otherItems = pool.filter(item => item.id !== target.id);
    const shuffledOthers = [...otherItems].sort(() => 0.5 - Math.random());
    const distractors = shuffledOthers.slice(0, 3);

    let options = [];
    let promptTitle = '';
    let promptSubtitle = '';
    let correctAnswer = '';

    if (quizMode === 'definition') {
      // English -> Indonesian
      promptTitle = target.term;
      promptSubtitle = `Pilih arti bahasa Indonesia yang paling tepat:`;
      correctAnswer = target.meaningId;
      options = [
        { text: target.meaningId, isCorrect: true, item: target },
        ...distractors.map(d => ({ text: d.meaningId, isCorrect: false, item: d }))
      ];
    } else if (quizMode === 'reverse') {
      // Indonesian -> English
      promptTitle = target.meaningId;
      promptSubtitle = `Pilih istilah bahasa Inggris yang sesuai:`;
      correctAnswer = target.term;
      options = [
        { text: target.term, isCorrect: true, item: target },
        ...distractors.map(d => ({ text: d.term, isCorrect: false, item: d }))
      ];
    } else {
      // Fill in the blank (e.g., Collocation / Phrasal verb missing key particle or verb)
      const words = target.term.split(/\s+/);
      if (words.length > 1) {
        // Hide first word (often the verb or adj) or particle
        const hideIdx = 0;
        const missingWord = words[hideIdx];
        const blankedTerm = words.map((w, i) => i === hideIdx ? '_____' : w).join(' ');
        
        promptTitle = blankedTerm;
        promptSubtitle = `Lengkapi kata yang rumpang untuk frasa "${target.meaningId}":`;
        correctAnswer = missingWord;

        // Distractor words
        const dummyWords = ['make', 'take', 'do', 'pay', 'get', 'put', 'break', 'catch', 'run', 'set', 'turn', 'hold', 'keep', 'bring', 'come', 'go']
          .filter(w => w.toLowerCase() !== missingWord.toLowerCase())
          .sort(() => 0.5 - Math.random())
          .slice(0, 3);

        options = [
          { text: missingWord, isCorrect: true, item: target },
          ...dummyWords.map(dw => ({ text: dw, isCorrect: false, item: target }))
        ];
      } else {
        // Fallback to definition
        promptTitle = target.term;
        promptSubtitle = `Pilih arti bahasa Indonesia:`;
        correctAnswer = target.meaningId;
        options = [
          { text: target.meaningId, isCorrect: true, item: target },
          ...distractors.map(d => ({ text: d.meaningId, isCorrect: false, item: d }))
        ];
      }
    }

    // Shuffle options
    options.sort(() => 0.5 - Math.random());

    setCurrentQuestion({
      target,
      promptTitle,
      promptSubtitle,
      correctAnswer,
      options
    });

    setSelectedOption(null);
    setIsAnswered(false);
  };

  useEffect(() => {
    generateQuestion();
  }, [quizMode, categoryFilter]);

  const handleSelectOption = (opt) => {
    if (isAnswered) return;
    setSelectedOption(opt);
    setIsAnswered(true);

    if (opt.isCorrect) {
      sounds.playCorrect();
      const newCombo = combo + 1;
      setCombo(newCombo);
      const earnedXP = 15 + Math.min(newCombo * 3, 15);
      setScore(prev => prev + earnedXP);
      onAddXP(earnedXP);

      // Play audio of target term
      speechAssistant.setAccent(accent);
      speechAssistant.speak(currentQuestion.target.term);

      if (newCombo % 3 === 0) {
        confetti({
          particleCount: 40,
          spread: 60,
          origin: { y: 0.7 },
          colors: ['#34D399', '#60A5FA', '#F472B6']
        });
      }
    } else {
      sounds.playWrong();
      setCombo(0);
    }
  };

  const playSpeech = (text) => {
    speechAssistant.setAccent(accent);
    speechAssistant.speak(text);
  };

  if (!currentQuestion) return null;

  return (
    <div className="quiz-game-container">
      {/* Header & Mascot */}
      <div className="game-top-header">
        <Mascot 
          mood={isAnswered ? (selectedOption?.isCorrect ? 'celebrate' : 'thinking') : (combo > 2 ? 'cheer' : 'happy')}
          message={
            isAnswered 
              ? (selectedOption?.isCorrect ? `Hebat, jawabanmu benar! (+15 XP)` : `Jangan patah semangat, perhatikan penjelasannya ya!`)
              : `Pilih satu dari 4 opsi jawaban di bawah ini.`
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
            <span>Skor Kuis: {score}</span>
          </div>
        </div>
      </div>

      {/* Mode & Category Bar */}
      <div className="quiz-settings-bar">
        <div className="setting-sub-group">
          <span className="setting-title">Mode Kuis:</span>
          <div className="filter-pills">
            <button 
              className={`pill-btn ${quizMode === 'definition' ? 'active' : ''}`}
              onClick={() => { sounds.playPop(); setQuizMode('definition'); }}
            >
              English ➔ Arti (ID)
            </button>
            <button 
              className={`pill-btn ${quizMode === 'reverse' ? 'active' : ''}`}
              onClick={() => { sounds.playPop(); setQuizMode('reverse'); }}
            >
              Arti (ID) ➔ English
            </button>
            <button 
              className={`pill-btn ${quizMode === 'fill_blank' ? 'active' : ''}`}
              onClick={() => { sounds.playPop(); setQuizMode('fill_blank'); }}
            >
              Lengkapi Frasa 🧩
            </button>
          </div>
        </div>

        <div className="setting-sub-group">
          <span className="setting-title">Kategori:</span>
          <div className="filter-pills">
            <button 
              className={`pill-btn small ${categoryFilter === 'all' ? 'active' : ''}`}
              onClick={() => { sounds.playPop(); setCategoryFilter('all'); }}
            >
              Semua
            </button>
            <button 
              className={`pill-btn small ${categoryFilter === 'phrasal_verb' ? 'active' : ''}`}
              onClick={() => { sounds.playPop(); setCategoryFilter('phrasal_verb'); }}
            >
              Phrasal Verbs ⚡
            </button>
            <button 
              className={`pill-btn small ${categoryFilter === 'collocation' ? 'active' : ''}`}
              onClick={() => { sounds.playPop(); setCategoryFilter('collocation'); }}
            >
              Collocations 🧩
            </button>
            <button 
              className={`pill-btn small ${categoryFilter === 'oxford_3000' ? 'active' : ''}`}
              onClick={() => { sounds.playPop(); setCategoryFilter('oxford_3000'); }}
            >
              Oxford 3000 📚
            </button>
          </div>
        </div>
      </div>

      {/* Question Card */}
      <div className="quiz-question-card">
        <div className="question-header">
          <div className="badge-group">
            <span className={`badge-pill badge-${currentQuestion.target.type}`}>
              {currentQuestion.target.type === 'phrasal_verb' ? 'Phrasal Verb' : currentQuestion.target.type === 'collocation' ? 'Collocation' : 'Oxford 3000'}
            </span>
            <span className="badge-pill badge-level">{currentQuestion.target.level}</span>
            <span className="badge-pill badge-pos">{currentQuestion.target.pos}</span>
          </div>
        </div>

        <p className="question-sub-prompt">{currentQuestion.promptSubtitle}</p>
        <div className="question-title-wrap">
          <h2 className="question-main-term">{currentQuestion.promptTitle}</h2>
          {quizMode !== 'reverse' && (
            <button 
              className="speak-mini-btn"
              onClick={() => playSpeech(currentQuestion.target.term)}
              title="Dengarkan pengucapan"
            >
              <Volume2 size={20} />
            </button>
          )}
        </div>

        {/* Options Grid */}
        <div className="quiz-options-grid">
          {currentQuestion.options.map((opt, idx) => {
            const letter = ['A', 'B', 'C', 'D'][idx];
            let stateClass = '';
            if (isAnswered) {
              if (opt.isCorrect) stateClass = 'is-correct';
              else if (selectedOption === opt) stateClass = 'is-wrong';
              else stateClass = 'is-disabled';
            }

            return (
              <button
                key={`opt-${idx}`}
                className={`quiz-option-btn ${stateClass}`}
                onClick={() => handleSelectOption(opt)}
                disabled={isAnswered}
              >
                <span className="option-letter">{letter}</span>
                <span className="option-text">{opt.text}</span>
                {isAnswered && opt.isCorrect && <Check size={20} className="status-check-icon" />}
                {isAnswered && !opt.isCorrect && selectedOption === opt && <X size={20} className="status-x-icon" />}
              </button>
            );
          })}
        </div>

        {/* Explanation & Context on Answer */}
        {isAnswered && (
          <div className="quiz-explanation-box">
            <div className="explanation-header">
              <span className="exp-title">💡 Pembahasan Lengkap:</span>
              <button 
                className="speak-mini-btn"
                onClick={() => playSpeech(currentQuestion.target.exampleEn)}
              >
                <Volume2 size={16} /> Dengarkan Contoh
              </button>
            </div>

            <div className="exp-details">
              <p><strong>{currentQuestion.target.term}</strong> {currentQuestion.target.ipa} : {currentQuestion.target.meaningId}</p>
              <p className="example-en-quote">"{currentQuestion.target.exampleEn}"</p>
              <p className="example-id-quote">Artinya: "{currentQuestion.target.exampleId}"</p>
              {currentQuestion.target.hint && (
                <p className="tip-snippet">Tips: {currentQuestion.target.hint}</p>
              )}
            </div>

            <button 
              className="cute-primary-btn next-quiz-btn"
              onClick={() => { sounds.playPop(); generateQuestion(); }}
            >
              <span>Soal Berikutnya</span>
              <ArrowRight size={20} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
