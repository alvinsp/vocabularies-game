// Web Speech API Pronunciation Utility with Accent & Speed controls

class SpeechAssistant {
  constructor() {
    this.voiceLang = 'en-US'; // default 'en-US' or 'en-GB'
    this.rate = 0.95; // slightly relaxed for clear learner listening
    this.pitch = 1.0;
  }

  setAccent(accent) {
    this.voiceLang = accent; // 'en-US' or 'en-GB'
  }

  setRate(rate) {
    this.rate = rate; // 0.8 to 1.2
  }

  getVoice() {
    if (!('speechSynthesis' in window)) return null;
    const voices = window.speechSynthesis.getVoices();
    // Prioritize natural English voices matching selected accent
    const match = voices.find(v => v.lang.replace('_', '-').toLowerCase().startsWith(this.voiceLang.toLowerCase()));
    if (match) return match;
    const fallback = voices.find(v => v.lang.startsWith('en'));
    return fallback || voices[0] || null;
  }

  speak(text, onEnd) {
    if (!('speechSynthesis' in window)) {
      console.warn('Speech synthesis not supported in this browser.');
      return;
    }

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    if (!text || !text.trim()) return;

    // Clean brackets or indicators like "(on sth)" or "sb/sth" for smoother audio
    const cleanText = text
      .replace(/\(sb\/sth\)/g, 'someone or something')
      .replace(/sb\/sth/g, 'someone or something')
      .replace(/\(sb\)/g, 'someone')
      .replace(/sb\b/g, 'someone')
      .replace(/\(sth\)/g, 'something')
      .replace(/sth\b/g, 'something')
      .replace(/[()]/g, '');

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = this.voiceLang;
    utterance.rate = this.rate;
    utterance.pitch = this.pitch;

    const voice = this.getVoice();
    if (voice) {
      utterance.voice = voice;
    }

    if (onEnd) {
      utterance.onend = onEnd;
      utterance.onerror = onEnd;
    }

    window.speechSynthesis.speak(utterance);
  }

  stop() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }
}

export const speechAssistant = new SpeechAssistant();
