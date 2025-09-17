import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import enTranslation from './translations/en.json';
import esTranslation from './translations/es.json';
import ptTranslation from './translations/pt.json';
import frTranslation from './translations/fr.json';
import zhTranslation from './translations/zh.json';
import arTranslation from './translations/ar.json';

// Initialize i18next for internationalization (only if not already initialized)
if (!i18n.isInitialized) {
  i18n
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
      resources: {
        en: {
          translation: enTranslation
        },
        es: {
          translation: esTranslation
        },
        pt: {
          translation: ptTranslation
        },
        fr: {
          translation: frTranslation
        },
        zh: {
          translation: zhTranslation
        },
        ar: {
          translation: arTranslation
        }
      },
      fallbackLng: 'en',
      debug: true, // Enable debug to see translation loading
      
      // User's language preference from local storage
      detection: {
        order: ['localStorage', 'navigator'],
        lookupLocalStorage: 'preferredLanguage',
      },
      
      interpolation: {
        escapeValue: false, // React already escapes values
      },
      
      // Enable returnObjects to access nested translation objects
      returnObjects: true,
      
      react: {
        useSuspense: false,
      }
    });
}

export default i18n;
