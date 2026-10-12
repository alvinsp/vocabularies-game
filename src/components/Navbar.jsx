import React from 'react';
import { 
  Sparkles, 
  Flame, 
  Volume2, 
  VolumeX, 
  Layers, 
  Puzzle, 
  CheckCircle2, 
  Zap, 
  BookOpen, 
  Palette 
} from 'lucide-react';
import { sounds } from '../utils/soundEffects';

export default function Navbar({
  activeTab,
  setActiveTab,
  xp,
  streak,
  accent,
  setAccent,
  theme,
  setTheme,
  muted,
  setMuted,
  stats
}) {
  const getLevel = (pts) => {
    if (pts < 100) return { lvl: 1, title: 'Pemula 🐣', next: 100 };
    if (pts < 300) return { lvl: 2, title: 'Penjelajah 🌿', next: 300 };
    if (pts < 600) return { lvl: 3, title: 'Phrasal Hero 🦊', next: 600 };
    if (pts < 1000) return { lvl: 4, title: 'Collocation Wizard 🧙‍♂️', next: 1000 };
    return { lvl: 5, title: 'Oxford Master 👑', next: 2000 };
  };

  const currentLevel = getLevel(xp);

  const toggleSound = () => {
    const nextMuted = sounds.toggleMute();
    setMuted(nextMuted);
    if (!nextMuted) {
      sounds.playPop();
    }
  };

  const navItems = [
    { id: 'flashcard', label: 'Flashcard 3D', icon: Layers },
    { id: 'scramble', label: 'Susun Kata', icon: Puzzle },
    { id: 'quiz', label: 'Kuis Pilihan', icon: CheckCircle2 },
    { id: 'match', label: 'Pasangan Cepat', icon: Zap },
    { id: 'dictionary', label: 'Kamus & Koleksi', icon: BookOpen },
  ];

  const themes = [
    { id: 'mint', name: 'Matcha Mint 🍵' },
    { id: 'pink', name: 'Sakura Pastel 🌸' },
    { id: 'ocean', name: 'Ocean Sky 🌊' },
    { id: 'peach', name: 'Sunset Peach 🌅' }
  ];

  return (
    <header className="navbar-wrapper">
      <div className="navbar-top">
        {/* Brand */}
        <div className="navbar-brand" onClick={() => setActiveTab('flashcard')}>
          <div className="brand-logo-badge">
            <span className="brand-emoji">🦉</span>
          </div>
          <div className="brand-titles">
            <h1 className="brand-title">VocabPintar</h1>
            <span className="brand-subtitle">Oxford Phrasal, Collocations & 3000 Words</span>
          </div>
        </div>

        {/* Gamification Badges */}
        <div className="navbar-stats">
          <div className="stat-pill streak-pill" title="Streak Belajar Harian">
            <Flame className="stat-icon flame-icon" size={18} />
            <span className="stat-value">{streak}</span>
            <span className="stat-label">Hari</span>
          </div>

          <div className="stat-pill xp-pill" title="Total Poin Pengalaman (XP)">
            <Sparkles className="stat-icon star-icon" size={18} />
            <span className="stat-value">{xp}</span>
            <span className="stat-label">XP</span>
          </div>

          <div className="stat-pill level-pill" title="Level Pembelajar Anda">
            <span className="level-badge">{currentLevel.title}</span>
          </div>
        </div>

        {/* Global Controls: Accent, Audio, Theme */}
        <div className="navbar-controls">
          {/* Accent Switcher */}
          <button 
            className="control-btn accent-btn"
            onClick={() => {
              const next = accent === 'en-US' ? 'en-GB' : 'en-US';
              setAccent(next);
              sounds.playPop();
            }}
            title={`Aksen Pengucapan: ${accent === 'en-US' ? 'American English' : 'British Oxford'}`}
          >
            <span className="flag-icon">{accent === 'en-US' ? '🇺🇸 US' : '🇬🇧 UK'}</span>
          </button>

          {/* Sound Mute Toggle */}
          <button 
            className={`control-btn sound-btn ${muted ? 'is-muted' : ''}`}
            onClick={toggleSound}
            title={muted ? 'Aktifkan Efek Suara' : 'Bisukan Suara'}
          >
            {muted ? <VolumeX size={18} /> : <Volume2 size={18} />}
          </button>

          {/* Theme Dropdown / Quick Toggle */}
          <div className="theme-selector-container">
            <button 
              className="control-btn theme-btn"
              onClick={() => {
                const curIdx = themes.findIndex(t => t.id === theme);
                const nextTheme = themes[(curIdx + 1) % themes.length].id;
                setTheme(nextTheme);
                sounds.playPop();
              }}
              title="Ganti Tema Warna Lucu"
            >
              <Palette size={18} />
              <span className="theme-name-tag">{themes.find(t => t.id === theme)?.name.split(' ')[0]}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Tabs navigation */}
      <nav className="navbar-tabs">
        <div className="tabs-container">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                id={`tab-btn-${item.id}`}
                className={`tab-btn ${isActive ? 'active' : ''}`}
                onClick={() => {
                  sounds.playPop();
                  setActiveTab(item.id);
                }}
              >
                <Icon size={18} className="tab-icon" />
                <span className="tab-label">{item.label}</span>
                {isActive && <span className="tab-indicator" />}
              </button>
            );
          })}
        </div>
      </nav>
    </header>
  );
}
