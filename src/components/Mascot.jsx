import React from 'react';

export default function Mascot({ mood = 'happy', message = '', size = 80 }) {
  // Moods: 'happy', 'celebrate', 'thinking', 'cheer', 'curious'
  return (
    <div className="mascot-container" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
      <div 
        className={`mascot-avatar mascot-${mood}`} 
        style={{ width: size, height: size, position: 'relative', flexShrink: 0 }}
      >
        <svg 
          viewBox="0 0 100 100" 
          width="100%" 
          height="100%" 
          className="mascot-svg"
        >
          {/* Shadow */}
          <ellipse cx="50" cy="94" rx="30" ry="6" fill="rgba(0,0,0,0.12)" />

          {/* Body - Soft Rounded Cute Owl / Penguin Buddy */}
          <ellipse cx="50" cy="52" rx="36" ry="38" fill="var(--mascot-body, #60A5FA)" />

          {/* Belly */}
          <ellipse cx="50" cy="58" rx="26" ry="26" fill="#FFFFFF" />

          {/* Cute Little Wings */}
          {mood === 'celebrate' || mood === 'cheer' ? (
            <>
              {/* Upraised wings */}
              <path d="M 16 46 Q 4 30 18 24 Q 28 36 24 50 Z" fill="var(--mascot-dark, #3B82F6)" />
              <path d="M 84 46 Q 96 30 82 24 Q 72 36 76 50 Z" fill="var(--mascot-dark, #3B82F6)" />
            </>
          ) : (
            <>
              {/* Resting wings */}
              <ellipse cx="18" cy="56" rx="8" ry="16" transform="rotate(18 18 56)" fill="var(--mascot-dark, #3B82F6)" />
              <ellipse cx="82" cy="56" rx="8" ry="16" transform="rotate(-18 82 56)" fill="var(--mascot-dark, #3B82F6)" />
            </>
          )}

          {/* Graduation / Scholar Cap */}
          <polygon points="50,12 80,22 50,30 20,22" fill="#1E293B" />
          <rect x="42" y="27" width="16" height="7" rx="3" fill="#334155" />
          <circle cx="50" cy="21" r="3" fill="#F59E0B" />
          <path d="M 50 21 Q 68 25 72 35" stroke="#F59E0B" strokeWidth="2.5" fill="none" />
          <circle cx="72" cy="35" r="3" fill="#F59E0B" />

          {/* Eyes & Blushing */}
          {mood === 'happy' || mood === 'celebrate' ? (
            <>
              {/* Happy curved eyes (^_^) */}
              <path d="M 34 46 Q 40 40 46 46" stroke="#1E293B" strokeWidth="3.5" strokeLinecap="round" fill="none" />
              <path d="M 54 46 Q 60 40 66 46" stroke="#1E293B" strokeWidth="3.5" strokeLinecap="round" fill="none" />
            </>
          ) : mood === 'thinking' ? (
            <>
              {/* Thinking eyes */}
              <circle cx="40" cy="45" r="4.5" fill="#1E293B" />
              <circle cx="60" cy="45" r="4.5" fill="#1E293B" />
              <circle cx="42" cy="43" r="1.5" fill="#FFFFFF" />
              <circle cx="62" cy="43" r="1.5" fill="#FFFFFF" />
            </>
          ) : (
            <>
              {/* Wide sparkle eyes */}
              <circle cx="40" cy="46" r="5" fill="#1E293B" />
              <circle cx="60" cy="46" r="5" fill="#1E293B" />
              <circle cx="38" cy="44" r="2" fill="#FFFFFF" />
              <circle cx="58" cy="44" r="2" fill="#FFFFFF" />
              <circle cx="42" cy="48" r="1" fill="#FFFFFF" />
              <circle cx="62" cy="48" r="1" fill="#FFFFFF" />
            </>
          )}

          {/* Rosy Cheeks */}
          <circle cx="28" cy="54" r="5" fill="#F472B6" opacity="0.65" />
          <circle cx="72" cy="54" r="5" fill="#F472B6" opacity="0.65" />

          {/* Little Cute Orange Beak */}
          <polygon points="46,50 54,50 50,57" fill="#F97316" rx="2" />

          {/* Cute Little Feet */}
          <ellipse cx="40" cy="88" rx="7" ry="4" fill="#F97316" />
          <ellipse cx="60" cy="88" rx="7" ry="4" fill="#F97316" />
        </svg>
      </div>

      {message && (
        <div className="mascot-bubble">
          <div className="mascot-bubble-tail"></div>
          <span className="mascot-text">{message}</span>
        </div>
      )}
    </div>
  );
}
