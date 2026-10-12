import { phrasalVerbs } from './phrasalVerbs';
import { collocations } from './collocations';
import { oxfordVocab } from './oxfordVocab';

export { phrasalVerbs, collocations, oxfordVocab };

export const allVocabulary = [
  ...phrasalVerbs,
  ...collocations,
  ...oxfordVocab
];

export const getStats = () => {
  return {
    total: allVocabulary.length,
    phrasalVerbs: phrasalVerbs.length,
    collocations: collocations.length,
    oxfordVocab: oxfordVocab.length,
    nouns: allVocabulary.filter(item => item.pos === 'noun').length,
    verbs: allVocabulary.filter(item => item.pos === 'verb').length,
    adjectives: allVocabulary.filter(item => item.pos === 'adjective').length,
    adverbs: allVocabulary.filter(item => item.pos === 'adverb').length,
  };
};

export const filterVocabulary = ({
  search = '',
  type = 'all',
  pos = 'all',
  level = 'all',
  masteredIds = new Set(),
  reviewIds = new Set(),
  favoriteIds = new Set(),
  statusFilter = 'all' // 'all' | 'mastered' | 'review' | 'favorites' | 'unlearned'
}) => {
  return allVocabulary.filter(item => {
    if (search.trim()) {
      const q = search.toLowerCase().trim();
      const matchTerm = item.term.toLowerCase().includes(q);
      const matchMeaning = item.meaningId.toLowerCase().includes(q);
      const matchCategory = item.category?.toLowerCase().includes(q);
      if (!matchTerm && !matchMeaning && !matchCategory) return false;
    }

    if (type !== 'all' && item.type !== type) return false;
    if (pos !== 'all' && item.pos !== pos) return false;
    if (level !== 'all' && item.level !== level) return false;

    if (statusFilter === 'mastered' && !masteredIds.has(item.id)) return false;
    if (statusFilter === 'review' && !reviewIds.has(item.id)) return false;
    if (statusFilter === 'favorites' && !favoriteIds.has(item.id)) return false;
    if (statusFilter === 'unlearned' && (masteredIds.has(item.id) || reviewIds.has(item.id))) return false;

    return true;
  });
};
