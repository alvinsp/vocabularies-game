// LocalStorage persistence for user learning progress, streaks, XP, and settings

const STORAGE_KEYS = {
  XP: 'vocab_app_xp',
  STREAK: 'vocab_app_streak',
  LAST_LOGIN: 'vocab_app_last_date',
  MASTERED: 'vocab_app_mastered_ids',
  REVIEW: 'vocab_app_review_ids',
  FAVORITES: 'vocab_app_favorite_ids',
  THEME: 'vocab_app_theme',
  ACCENT: 'vocab_app_accent',
  MUTED: 'vocab_app_muted',
};

export const getStoredXP = () => {
  return parseInt(localStorage.getItem(STORAGE_KEYS.XP) || '0', 10);
};

export const addXP = (amount) => {
  const current = getStoredXP();
  const next = current + amount;
  localStorage.setItem(STORAGE_KEYS.XP, next.toString());
  return next;
};

export const getStreakData = () => {
  const streak = parseInt(localStorage.getItem(STORAGE_KEYS.STREAK) || '1', 10);
  const lastDate = localStorage.getItem(STORAGE_KEYS.LAST_LOGIN);
  const today = new Date().toISOString().slice(0, 10);

  if (!lastDate) {
    localStorage.setItem(STORAGE_KEYS.LAST_LOGIN, today);
    localStorage.setItem(STORAGE_KEYS.STREAK, '1');
    return { streak: 1, isNewDay: true };
  }

  const last = new Date(lastDate);
  const cur = new Date(today);
  const diffDays = Math.floor((cur - last) / (1000 * 60 * 60 * 24));

  if (diffDays === 1) {
    // Consecutive day streak increment!
    const newStreak = streak + 1;
    localStorage.setItem(STORAGE_KEYS.STREAK, newStreak.toString());
    localStorage.setItem(STORAGE_KEYS.LAST_LOGIN, today);
    return { streak: newStreak, isNewDay: true };
  } else if (diffDays > 1) {
    // Reset streak if gap > 1
    localStorage.setItem(STORAGE_KEYS.STREAK, '1');
    localStorage.setItem(STORAGE_KEYS.LAST_LOGIN, today);
    return { streak: 1, isNewDay: true };
  }

  return { streak, isNewDay: false };
};

export const getStoredSet = (key) => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? new Set(JSON.parse(raw)) : new Set();
  } catch {
    return new Set();
  }
};

export const saveStoredSet = (key, setObj) => {
  localStorage.setItem(key, JSON.stringify(Array.from(setObj)));
};

export const getMasteredIds = () => getStoredSet(STORAGE_KEYS.MASTERED);
export const getReviewIds = () => getStoredSet(STORAGE_KEYS.REVIEW);
export const getFavoriteIds = () => getStoredSet(STORAGE_KEYS.FAVORITES);

export const toggleFavoriteId = (id) => {
  const favs = getFavoriteIds();
  if (favs.has(id)) {
    favs.delete(id);
  } else {
    favs.add(id);
  }
  saveStoredSet(STORAGE_KEYS.FAVORITES, favs);
  return favs.has(id);
};

export const markAsMastered = (id) => {
  const mastered = getMasteredIds();
  const review = getReviewIds();
  mastered.add(id);
  review.delete(id);
  saveStoredSet(STORAGE_KEYS.MASTERED, mastered);
  saveStoredSet(STORAGE_KEYS.REVIEW, review);
};

export const markForReview = (id) => {
  const mastered = getMasteredIds();
  const review = getReviewIds();
  review.add(id);
  mastered.delete(id);
  saveStoredSet(STORAGE_KEYS.MASTERED, mastered);
  saveStoredSet(STORAGE_KEYS.REVIEW, review);
};

export const getStoredTheme = () => {
  return localStorage.getItem(STORAGE_KEYS.THEME) || 'mint';
};

export const saveStoredTheme = (theme) => {
  localStorage.setItem(STORAGE_KEYS.THEME, theme);
};

export const getStoredAccent = () => {
  return localStorage.getItem(STORAGE_KEYS.ACCENT) || 'en-US';
};

export const saveStoredAccent = (accent) => {
  localStorage.setItem(STORAGE_KEYS.ACCENT, accent);
};
