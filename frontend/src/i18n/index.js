import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

// Define supported languages
const supportedLanguages = [
  'en',
  'es',
  'fr',
  'de',
  'zh',
  'ar',
  'ru',
  'pt',
  'hi',
  'bn',
  'sw',
  'uk'
];

// Base translations for critical UI elements
const baseTranslations = {
  en: {
    translation: {
      "Loading": "Loading...",
      "Error": "Error",
      "Success": "Success",
      "Cancel": "Cancel",
      "Save": "Save",
      "Delete": "Delete",
      "Edit": "Edit",
      "Close": "Close",
      "Back": "Back",
      "Next": "Next",
      "Submit": "Submit",
      "Search": "Search",
      "Filter": "Filter",
      "Sort": "Sort",
      "Legal Chat": "Legal Chat",
      "Document Generator": "Document Generator",
      "Find Lawyer": "Find Lawyer",
      "Emergency Support": "Emergency Support",
      "Settings": "Settings",
      "Profile": "Profile",
      "Logout": "Logout",
      "Login": "Login",
      "Register": "Register",
      "Language": "Language",
      "Theme": "Theme",
      "Accessibility": "Accessibility",
      "High Contrast": "High Contrast",
      "Font Size": "Font Size",
      "Help": "Help",
      "Support": "Support",
      "Contact": "Contact",
      "About": "About",
      "Privacy": "Privacy",
      "Terms": "Terms"
    },
    common: {
      "loading": "Loading...",
      "submit": "Submit",
      "error": "Error",
      "success": "Success"
    },
    legalChat: {
      "title": "Legal Chat Assistant",
      "disclaimer": "This AI assistant provides general legal information. For specific legal advice, please consult with a qualified attorney.",
      "placeholder": "Type your legal question here...",
      "send": "Send Message",
      "thinking": "Assistant is thinking...",
      "error": "Failed to send message. Please try again."
    },
    feedback: {
      "title": "Feedback",
      "rating": "Rating",
      "comment": "Comment",
      "submit": "Submit Feedback",
      "thanks": "Thank you for your feedback!"
    },
    accessibility: {
      "options": "Accessibility Options",
      "screenReader": {
        "enable": "Enable screen reader optimizations",
        "description": "Optimize the interface for screen readers"
      },
      "contrast": {
        "high": "High contrast mode",
        "description": "Enhance visual contrast for better readability"
      },
      "textSize": {
        "title": "Text size",
        "small": "Small",
        "medium": "Medium",
        "large": "Large",
        "description": "Adjust text size for better readability"
      },
      "motion": {
        "reduce": "Reduce motion",
        "description": "Minimize animations and transitions"
      },
      "keyboard": {
        "enable": "Enhanced keyboard navigation",
        "description": "Improve keyboard-only navigation"
      }
    }
  }
};

// Initialize i18next
i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: baseTranslations,
    fallbackLng: 'en',
    supportedLngs: supportedLanguages,
    debug: process.env.NODE_ENV === 'development',
    interpolation: {
      escapeValue: false,
    },
    detection: {
      order: ['querystring', 'localStorage', 'navigator', 'htmlTag'],
      lookupQuerystring: 'lang',
      lookupLocalStorage: 'i18nextLng',
      caches: ['localStorage'],
    },
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
      addPath: '/locales/add/{{lng}}/{{ns}}',
      allowMultiLoading: true,
      crossDomain: true,
    },
    react: {
      useSuspense: true,
      bindI18n: 'languageChanged loaded',
      bindStore: 'added removed',
      nsMode: 'default'
    },
    returnObjects: true,
    returnEmptyString: false,
    returnNull: false,
    load: 'languageOnly',
    preload: ['en'],
    ns: ['translation', 'legal', 'documents', 'errors'],
    defaultNS: 'translation',
    fallbackNS: 'translation'
  });

// Language change handler with RTL support
i18n.on('languageChanged', (lng) => {
  document.documentElement.lang = lng;
  document.documentElement.dir = ['ar', 'he', 'fa'].includes(lng) ? 'rtl' : 'ltr';
  
  if (['ar', 'he', 'fa'].includes(lng)) {
    document.body.classList.add('rtl-layout');
  } else {
    document.body.classList.remove('rtl-layout');
  }
  
  // Load additional namespaces if needed
  const pageSpecificNamespaces = {
    '/legal-chat': ['legal'],
    '/documents': ['documents'],
    '/find-lawyer': ['legal'],
    '/emergency': ['legal']
  };
  
  const currentPath = window.location.pathname;
  const namespacesToLoad = pageSpecificNamespaces[currentPath] || [];
  
  namespacesToLoad.forEach(ns => {
    if (!i18n.hasResourceBundle(lng, ns)) {
      i18n.loadNamespaces(ns);
    }
  });
});

// Helper function to get browser language with region
export const getBrowserLanguage = () => {
  const browserLang = navigator.language || navigator.userLanguage;
  return supportedLanguages.find(lang => 
    browserLang.toLowerCase().startsWith(lang.toLowerCase())
  ) || 'en';
};

// Helper function to format dates according to locale
export const formatDate = (date, lng = i18n.language) => {
  return new Intl.DateTimeFormat(lng, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

export { i18n };
export default i18n;
