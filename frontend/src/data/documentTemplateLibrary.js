/**
 * Document Template Library
 *
 * This file contains all available document templates and access levels:
 * - Free: Available to all users without login
 * - Registered: Requires a user account but no premium subscription
 * - Premium: Requires a premium subscription
 */

// Document Templates Array
export const documentTemplates = [
  // Employment Law Templates
  {
    id: 'employment-termination-notice',
    name: 'Employment Termination Notice',
    category: 'Employment Law',
    subcategory: 'Termination',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/employment/termination-notice.html',
    description:
      'A formal notice to terminate employment relationship, specifying the termination date and conditions.',
    estimatedCompletionTime: '15-20 min',
    difficulty: 'easy',
    tags: ['termination', 'employment', 'notice'],
    icon: 'WorkOff',
    popularity: 85,
    featured: true,
  },
  {
    id: 'employment-offer-letter',
    name: 'Employment Offer Letter',
    category: 'Employment Law',
    subcategory: 'Hiring',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/employment/offer-letter.html',
    description:
      'A formal job offer document outlining position details, compensation, and terms of employment.',
    estimatedCompletionTime: '20-30 min',
    difficulty: 'medium',
    tags: ['offer', 'employment', 'hiring'],
    icon: 'Work',
    popularity: 92,
    featured: false,
  },
  {
    id: 'non-disclosure-agreement',
    name: 'Non-Disclosure Agreement (NDA)',
    category: 'Employment Law',
    subcategory: 'Confidentiality',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/employment/nda.html',
    description:
      'Protects confidential information shared between parties during business or employment relationships.',
    estimatedCompletionTime: '25-35 min',
    difficulty: 'medium',
    tags: ['confidentiality', 'NDA', 'business', 'protection'],
    icon: 'Security',
    popularity: 88,
    featured: true,
  },

  // Housing Law Templates
  {
    id: 'residential-lease-agreement',
    name: 'Residential Lease Agreement',
    category: 'Housing Law',
    subcategory: 'Rental',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/housing/residential-lease.html',
    description:
      'Standard lease agreement for residential properties, outlining terms, rent, and tenant responsibilities.',
    estimatedCompletionTime: '30-45 min',
    difficulty: 'medium',
    tags: ['lease', 'rental', 'housing', 'tenant'],
    icon: 'Home',
    popularity: 96,
    featured: true,
  },
  {
    id: 'eviction-notice',
    name: 'Eviction Notice',
    category: 'Housing Law',
    subcategory: 'Eviction',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/housing/eviction-notice.html',
    description:
      'Formal notice to tenant of eviction proceedings due to lease violations or other reasons.',
    estimatedCompletionTime: '15-25 min',
    difficulty: 'medium',
    tags: ['eviction', 'notice', 'landlord', 'tenant'],
    icon: 'NoMeetingRoom',
    popularity: 82,
    featured: false,
  },
  {
    id: 'security-deposit-dispute',
    name: 'Security Deposit Dispute Letter',
    category: 'Housing Law',
    subcategory: 'Dispute',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/housing/deposit-dispute.html',
    description:
      'Letter to landlord disputing security deposit withholding, requesting itemization or return.',
    estimatedCompletionTime: '15-20 min',
    difficulty: 'easy',
    tags: ['deposit', 'dispute', 'tenant', 'landlord'],
    icon: 'AttachMoney',
    popularity: 78,
    featured: false,
  },

  // Family Law Templates
  {
    id: 'child-custody-agreement',
    name: 'Child Custody Agreement',
    category: 'Family Law',
    subcategory: 'Custody',
    accessLevel: 'registered',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/family/custody-agreement.html',
    description:
      'Detailed agreement outlining custody arrangements, visitation schedules, and parental responsibilities.',
    estimatedCompletionTime: '45-60 min',
    difficulty: 'complex',
    tags: ['custody', 'family', 'children', 'divorce', 'parenting'],
    icon: 'People',
    popularity: 89,
    featured: true,
  },
  {
    id: 'divorce-settlement',
    name: 'Divorce Settlement Agreement',
    category: 'Family Law',
    subcategory: 'Divorce',
    accessLevel: 'premium',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/family/divorce-settlement.html',
    description:
      'Comprehensive agreement covering asset division, support, and other terms of divorce settlement.',
    estimatedCompletionTime: '60-90 min',
    difficulty: 'complex',
    tags: ['divorce', 'settlement', 'family', 'assets', 'separation'],
    icon: 'SplitScreen',
    popularity: 85,
    featured: false,
  },

  // Debt & Consumer Law Templates
  {
    id: 'debt-validation-letter',
    name: 'Debt Validation Letter',
    category: 'Debt & Consumer Law',
    subcategory: 'Debt',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/consumer/debt-validation.html',
    description: 'Letter requesting debt collector to validate and provide proof of alleged debt.',
    estimatedCompletionTime: '10-15 min',
    difficulty: 'easy',
    tags: ['debt', 'collection', 'validation', 'consumer'],
    icon: 'MoneyOff',
    popularity: 91,
    featured: false,
  },
  {
    id: 'credit-dispute-letter',
    name: 'Credit Report Dispute Letter',
    category: 'Debt & Consumer Law',
    subcategory: 'Credit',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/consumer/credit-dispute.html',
    description: 'Letter to credit bureaus disputing inaccurate information on your credit report.',
    estimatedCompletionTime: '15-25 min',
    difficulty: 'medium',
    tags: ['credit', 'dispute', 'report', 'correction'],
    icon: 'CreditCard',
    popularity: 87,
    featured: false,
  },

  // New templates to be implemented
  {
    id: 'power-of-attorney',
    name: 'Power of Attorney',
    category: 'Family Law',
    subcategory: 'Estate Planning',
    accessLevel: 'registered',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/family/power-of-attorney.html',
    description:
      'Legal document designating someone to make decisions on your behalf if you become unable to do so.',
    estimatedCompletionTime: '30-45 min',
    difficulty: 'complex',
    tags: ['power of attorney', 'legal authority', 'estate planning'],
    icon: 'Assignment',
    popularity: 80,
    featured: false,
  },
  {
    id: 'will-testament',
    name: 'Last Will and Testament',
    category: 'Family Law',
    subcategory: 'Estate Planning',
    accessLevel: 'premium',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/family/will-testament.html',
    description:
      'Document specifying how your assets should be distributed after your death and naming guardians for minor children.',
    estimatedCompletionTime: '45-60 min',
    difficulty: 'complex',
    tags: ['will', 'testament', 'estate', 'inheritance', 'guardian'],
    icon: 'MenuBook',
    popularity: 83,
    featured: true,
  },

  // New templates - Immigration Law
  {
    id: 'daca-renewal-cover-letter',
    name: 'DACA Renewal Cover Letter',
    category: 'Immigration Law',
    subcategory: 'DACA',
    accessLevel: 'free',
    jurisdictions: ['US'],
    templatePath: '/templates/immigration/daca-renewal-letter.html',
    description:
      'Cover letter to accompany DACA (Deferred Action for Childhood Arrivals) renewal application.',
    estimatedCompletionTime: '20-30 min',
    difficulty: 'medium',
    tags: ['DACA', 'immigration', 'renewal', 'cover letter'],
    icon: 'NoteAdd',
    popularity: 88,
    featured: true,
    isNew: true,
  },
  {
    id: 'fee-waiver-request',
    name: 'Immigration Fee Waiver Request',
    category: 'Immigration Law',
    subcategory: 'Fee Waiver',
    accessLevel: 'free',
    jurisdictions: ['US'],
    templatePath: '/templates/immigration/fee-waiver-request.html',
    description: 'Request for waiver of immigration application fees based on financial hardship.',
    estimatedCompletionTime: '30-40 min',
    difficulty: 'medium',
    tags: ['immigration', 'fee waiver', 'financial hardship'],
    icon: 'AttachMoney',
    popularity: 84,
    featured: false,
    isNew: true,
  },

  // Civil Rights Templates
  {
    id: 'police-misconduct-complaint',
    name: 'Police Misconduct Complaint',
    category: 'Civil Rights',
    subcategory: 'Police Accountability',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/civil-rights/police-misconduct.html',
    description:
      'Formal complaint regarding alleged police misconduct or excessive force incidents.',
    estimatedCompletionTime: '40-50 min',
    difficulty: 'complex',
    tags: ['police', 'misconduct', 'civil rights', 'complaint'],
    icon: 'Gavel',
    popularity: 79,
    featured: true,
    isNew: true,
  },
  {
    id: 'discrimination-complaint',
    name: 'Discrimination Complaint Letter',
    category: 'Civil Rights',
    subcategory: 'Discrimination',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/civil-rights/discrimination-complaint.html',
    description:
      'Letter to file a formal complaint about discrimination in employment, housing, or public accommodations.',
    estimatedCompletionTime: '30-45 min',
    difficulty: 'medium',
    tags: ['discrimination', 'civil rights', 'complaint', 'equality'],
    icon: 'Balance',
    popularity: 86,
    featured: false,
    isNew: true,
  },

  // Small Business Templates
  {
    id: 'llc-operating-agreement',
    name: 'LLC Operating Agreement',
    category: 'Business Law',
    subcategory: 'Formation',
    accessLevel: 'registered',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/business/llc-operating-agreement.html',
    description:
      'Foundational document outlining ownership, management structure, and operating procedures for Limited Liability Companies.',
    estimatedCompletionTime: '60-90 min',
    difficulty: 'complex',
    tags: ['LLC', 'business', 'operating agreement', 'formation'],
    icon: 'Business',
    popularity: 92,
    featured: true,
    isNew: true,
  },
  {
    id: 'independent-contractor-agreement',
    name: 'Independent Contractor Agreement',
    category: 'Business Law',
    subcategory: 'Contracts',
    accessLevel: 'registered',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/business/contractor-agreement.html',
    description:
      'Contract defining the relationship between a business and an independent contractor, including scope of work and payment terms.',
    estimatedCompletionTime: '30-40 min',
    difficulty: 'medium',
    tags: ['contractor', 'business', 'agreement', 'freelance'],
    icon: 'Description',
    popularity: 89,
    featured: false,
    isNew: true,
  },

  // Accessibility Rights Templates
  {
    id: 'ada-accommodation-request',
    name: 'ADA Accommodation Request',
    category: 'Disability Rights',
    subcategory: 'Accommodations',
    accessLevel: 'free',
    jurisdictions: ['US'],
    templatePath: '/templates/disability/ada-accommodation.html',
    description:
      'Formal request for reasonable accommodations under the Americans with Disabilities Act in workplace or educational settings.',
    estimatedCompletionTime: '20-30 min',
    difficulty: 'medium',
    tags: ['ADA', 'disability', 'accommodation', 'accessibility'],
    icon: 'Accessibility',
    popularity: 83,
    featured: false,
    isNew: true,
  },

  // Education Law Templates
  {
    id: 'iep-meeting-request',
    name: 'IEP Meeting Request Letter',
    category: 'Education Law',
    subcategory: 'Special Education',
    accessLevel: 'free',
    jurisdictions: ['US'],
    templatePath: '/templates/education/iep-meeting-request.html',
    description:
      'Letter requesting an Individualized Education Program meeting to discuss accommodations for a student with disabilities.',
    estimatedCompletionTime: '15-20 min',
    difficulty: 'easy',
    tags: ['IEP', 'education', 'disability', 'special education'],
    icon: 'School',
    popularity: 77,
    featured: false,
    isNew: true,
  },

  // Healthcare Templates
  {
    id: 'medical-debt-negotiation',
    name: 'Medical Debt Negotiation Letter',
    category: 'Healthcare Law',
    subcategory: 'Medical Debt',
    accessLevel: 'free',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/healthcare/medical-debt-negotiation.html',
    description:
      'Letter to healthcare providers or collection agencies to negotiate payment terms for medical debt.',
    estimatedCompletionTime: '20-30 min',
    difficulty: 'medium',
    tags: ['medical debt', 'negotiation', 'healthcare', 'payment plan'],
    icon: 'LocalHospital',
    popularity: 90,
    featured: false,
    isNew: true,
  },
  {
    id: 'advance-healthcare-directive',
    name: 'Advance Healthcare Directive',
    category: 'Healthcare Law',
    subcategory: 'End of Life',
    accessLevel: 'premium',
    jurisdictions: ['US', 'General'],
    templatePath: '/templates/healthcare/advance-directive.html',
    description:
      'Document specifying your healthcare preferences and designating someone to make medical decisions if you cannot.',
    estimatedCompletionTime: '45-60 min',
    difficulty: 'complex',
    tags: ['healthcare', 'directive', 'living will', 'medical power of attorney'],
    icon: 'HealthAndSafety',
    popularity: 81,
    featured: true,
    isNew: true,
  },
];

/**
 * Get a document template by ID
 * @param {string} id - The template ID
 * @returns {Object|null} - The template object or null if not found
 */
export const getTemplateById = id => {
  return documentTemplates.find(template => template.id === id) || null;
};

/**
 * Get all templates in a specific category
 * @param {string} category - The category name
 * @returns {Array} - Array of templates in the category
 */
export const getTemplatesByCategory = category => {
  return documentTemplates.filter(template => template.category === category);
};

/**
 * Get templates by access level
 * @param {string} accessLevel - 'free', 'registered', or 'premium'
 * @returns {Array} - Array of templates with the specified access level
 */
export const getTemplatesByAccessLevel = accessLevel => {
  return documentTemplates.filter(template => template.accessLevel === accessLevel);
};

/**
 * Get all featured templates
 * @returns {Array} - Array of featured templates
 */
export const getFeaturedTemplates = () => {
  return documentTemplates.filter(template => template.featured);
};

/**
 * Get the most popular templates
 * @param {number} limit - Number of templates to return
 * @returns {Array} - Array of popular templates sorted by popularity
 */
export const getPopularTemplates = (limit = 5) => {
  return [...documentTemplates].sort((a, b) => b.popularity - a.popularity).slice(0, limit);
};

/**
 * Get all template categories
 * @returns {Array} - Array of unique template categories
 */
export const getAllTemplateCategories = () => {
  const categories = new Set(documentTemplates.map(template => template.category));
  return Array.from(categories);
};

/**
 * Search templates by keyword
 * @param {string} keyword - The search keyword
 * @returns {Array} - Array of templates matching the keyword
 */
export const searchTemplates = keyword => {
  const term = keyword.toLowerCase();
  return documentTemplates.filter(
    template =>
      template.name.toLowerCase().includes(term) ||
      template.description.toLowerCase().includes(term) ||
      (template.tags && template.tags.some(tag => tag.toLowerCase().includes(term)))
  );
};

export default documentTemplates;
