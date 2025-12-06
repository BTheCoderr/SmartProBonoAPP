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
      debug: false, // Disable debug to reduce console noise
      
      // Suppress missing key warnings in production
      missingKeyHandler: (lng, ns, key) => {
        // Only log missing keys in development
        if (process.env.NODE_ENV === 'development') {
          console.warn(`Missing translation key: ${key}`);
        }
        return key; // Return key as fallback
      },
      
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
