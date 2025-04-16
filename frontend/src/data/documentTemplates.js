/**
 * Document templates data
 * Contains predefined document templates for the application
 */

export const documentTemplates = [
  {
    id: 'rental-agreement',
    name: 'Rental Agreement',
    category: 'Housing',
    description: 'Standard residential rental/lease agreement template',
    icon: 'home',
    popularity: 4.9,
    downloadCount: 12500,
    lastUpdated: '2023-09-15',
    sections: [
      'Parties',
      'Property',
      'Term',
      'Rent',
      'Security Deposit',
      'Utilities',
      'Maintenance',
      'Rules',
      'Signatures'
    ],
    tags: ['housing', 'rental', 'lease', 'residential', 'property']
  },
  {
    id: 'power-of-attorney',
    name: 'Power of Attorney',
    category: 'Legal',
    description: 'General power of attorney document that grants legal authority to act for another person',
    icon: 'gavel',
    popularity: 4.7,
    downloadCount: 8900,
    lastUpdated: '2023-10-22',
    sections: [
      'Principal',
      'Agent',
      'Powers Granted',
      'Duration',
      'Revocation',
      'Signatures',
      'Notary'
    ],
    tags: ['legal', 'power of attorney', 'representation', 'authorization']
  },
  {
    id: 'demand-letter',
    name: 'Demand Letter',
    category: 'Disputes',
    description: 'Formal letter demanding payment, action, or rectification from another party',
    icon: 'mail',
    popularity: 4.5,
    downloadCount: 7300,
    lastUpdated: '2023-11-05',
    sections: [
      'Sender Information',
      'Recipient Information',
      'Demand Details',
      'Timeline',
      'Legal Consequences',
      'Settlement Options',
      'Closing'
    ],
    tags: ['disputes', 'demand', 'payment', 'debt', 'collection']
  },
  {
    id: 'non-disclosure',
    name: 'Non-Disclosure Agreement',
    category: 'Business',
    description: 'Confidentiality agreement to protect sensitive information',
    icon: 'security',
    popularity: 4.8,
    downloadCount: 10200,
    lastUpdated: '2023-09-30',
    sections: [
      'Parties',
      'Definition of Confidential Information',
      'Exclusions',
      'Obligations',
      'Term',
      'Remedies',
      'Signatures'
    ],
    tags: ['business', 'confidentiality', 'NDA', 'privacy', 'contract']
  },
  {
    id: 'will-testament',
    name: 'Last Will & Testament',
    category: 'Estate',
    description: 'Legal document that expresses how personal property should be distributed',
    icon: 'description',
    popularity: 4.6,
    downloadCount: 6800,
    lastUpdated: '2023-10-10',
    sections: [
      'Personal Information',
      'Executor Appointment',
      'Guardianship',
      'Asset Distribution',
      'Specific Bequests',
      'Signatures',
      'Witnesses',
      'Notary'
    ],
    tags: ['estate', 'will', 'testament', 'inheritance', 'property']
  }
];

export default documentTemplates; 