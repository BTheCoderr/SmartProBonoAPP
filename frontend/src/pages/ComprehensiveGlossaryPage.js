import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  TextField,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  InputAdornment,
  Chip,
  Paper,
  Badge
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Search as SearchIcon,
  Gavel as GavelIcon,
  Business as BusinessIcon,
  FamilyRestroom as FamilyIcon,
  Security as SecurityIcon,
  LocalHospital as MedicalIcon,
  Flight as ImmigrationIcon,
  Person as PersonIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';
// import { useTranslation } from 'react-i18next';

const ComprehensiveGlossaryPage = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const legalTerms = [
    {
      category: 'General Legal Terms',
      icon: <GavelIcon />,
      color: 'primary',
      terms: [
        { term: 'Affidavit', definition: 'A written statement made under oath, used as evidence in court proceedings.' },
        { term: 'Appeal', definition: 'A request to a higher court to review and change the decision of a lower court.' },
        { term: 'Arraignment', definition: 'A court proceeding where the defendant is formally charged and enters a plea.' },
        { term: 'Bail', definition: 'Money or property given to the court to ensure a defendant appears for trial.' },
        { term: 'Burden of Proof', definition: 'The obligation to prove allegations in a legal proceeding.' },
        { term: 'Contempt of Court', definition: 'Disrespectful or disobedient behavior toward a court of law.' },
        { term: 'Deposition', definition: 'Out-of-court testimony given under oath for discovery purposes.' },
        { term: 'Discovery', definition: 'The pre-trial process where parties exchange information and evidence.' },
        { term: 'Due Process', definition: 'Fair treatment through the normal judicial system.' },
        { term: 'Evidence', definition: 'Information presented in court to prove or disprove facts.' },
        { term: 'Habeas Corpus', definition: 'A writ requiring a person under arrest to be brought before a judge.' },
        { term: 'Injunction', definition: 'A court order requiring a party to do or refrain from doing something.' },
        { term: 'Jurisdiction', definition: 'The authority of a court to hear and decide cases.' },
        { term: 'Liability', definition: 'Legal responsibility for one\'s actions or omissions.' },
        { term: 'Litigation', definition: 'The process of taking legal action through the courts.' },
        { term: 'Motion', definition: 'A formal request made to a court for a specific ruling or order.' },
        { term: 'Plea', definition: 'A defendant\'s formal answer to criminal charges.' },
        { term: 'Precedent', definition: 'A legal decision that serves as a rule for future similar cases.' },
        { term: 'Pro Se', definition: 'Representing oneself in court without an attorney.' },
        { term: 'Subpoena', definition: 'A writ ordering a person to attend court as a witness.' },
        { term: 'Verdict', definition: 'The decision reached by a jury or judge in a legal proceeding.' },
        { term: 'Writ', definition: 'A formal written order issued by a court.' },
        { term: 'Statute of Limitations', definition: 'A law that sets the maximum time after an event within which legal proceedings may be initiated.' },
        { term: 'Settlement', definition: 'An agreement reached between parties to resolve a legal dispute without going to trial.' },
        { term: 'Damages', definition: 'Monetary compensation awarded to a party who has suffered loss or injury.' },
        { term: 'Tort', definition: 'A wrongful act or infringement of a right leading to civil legal liability.' }
      ]
    },
    {
      category: 'Criminal Law',
      icon: <SecurityIcon />,
      color: 'error',
      terms: [
        { term: 'Arrest', definition: 'The act of taking someone into custody by legal authority.' },
        { term: 'Bail Bond', definition: 'A financial guarantee that a defendant will appear in court.' },
        { term: 'Felony', definition: 'A serious crime typically punishable by imprisonment for more than one year.' },
        { term: 'Misdemeanor', definition: 'A minor crime typically punishable by fine or imprisonment for less than one year.' },
        { term: 'Probable Cause', definition: 'Reasonable grounds for making a search, pressing a charge, or making an arrest.' },
        { term: 'Search Warrant', definition: 'A court order authorizing law enforcement to search a specific location.' },
        { term: 'Miranda Rights', definition: 'Rights that must be read to a suspect before interrogation.' },
        { term: 'Plea Bargain', definition: 'An agreement between prosecutor and defendant to plead guilty to a lesser charge.' },
        { term: 'Probation', definition: 'A period of supervision over an offender instead of imprisonment.' },
        { term: 'Parole', definition: 'Early release from prison under supervision.' },
        { term: 'DUI/DWI', definition: 'Driving under the influence or driving while intoxicated.' },
        { term: 'Assault', definition: 'An intentional act that causes another person to fear imminent physical harm.' },
        { term: 'Battery', definition: 'The actual physical contact that causes harm to another person.' },
        { term: 'Burglary', definition: 'The unlawful entry into a building with intent to commit a crime.' },
        { term: 'Theft', definition: 'The unlawful taking of another person\'s property.' },
        { term: 'Robbery', definition: 'Theft accomplished through force or threat of force.' },
        { term: 'Fraud', definition: 'Intentional deception to secure unfair or unlawful gain.' },
        { term: 'Embezzlement', definition: 'Theft or misappropriation of funds by a person entrusted with those funds.' },
        { term: 'Money Laundering', definition: 'The process of making illegally-gained proceeds appear legal.' },
        { term: 'Racketeering', definition: 'Engaging in organized criminal activity.' }
      ]
    },
    {
      category: 'Family Law',
      icon: <FamilyIcon />,
      color: 'success',
      terms: [
        { term: 'Divorce', definition: 'The legal dissolution of a marriage by a court.' },
        { term: 'Alimony', definition: 'Financial support paid by one spouse to another after divorce.' },
        { term: 'Child Support', definition: 'Financial support paid by a non-custodial parent for their child.' },
        { term: 'Custody', definition: 'The legal right to make decisions about a child\'s upbringing.' },
        { term: 'Visitation', definition: 'The right of a non-custodial parent to spend time with their child.' },
        { term: 'Prenuptial Agreement', definition: 'A contract made before marriage regarding property and support.' },
        { term: 'Annulment', definition: 'A legal procedure to declare a marriage null and void.' },
        { term: 'Legal Separation', definition: 'A court-ordered arrangement where spouses live apart but remain married.' },
        { term: 'Paternity', definition: 'The legal establishment of fatherhood.' },
        { term: 'Adoption', definition: 'The legal process of establishing a parent-child relationship.' },
        { term: 'Guardianship', definition: 'Legal responsibility for the care and management of another person.' },
        { term: 'Emancipation', definition: 'The legal process of freeing a minor from parental control.' },
        { term: 'Restraining Order', definition: 'A court order prohibiting contact between parties.' },
        { term: 'Domestic Violence', definition: 'Violence or abuse within a domestic relationship.' },
        { term: 'Mediation', definition: 'A process where a neutral third party helps resolve disputes.' },
        { term: 'Arbitration', definition: 'A process where a neutral third party makes a binding decision.' },
        { term: 'Community Property', definition: 'Property acquired during marriage that belongs to both spouses.' },
        { term: 'Separate Property', definition: 'Property owned by one spouse before marriage or acquired by gift or inheritance.' }
      ]
    },
    {
      category: 'Immigration Law',
      icon: <ImmigrationIcon />,
      color: 'info',
      terms: [
        { term: 'Green Card', definition: 'A document allowing a foreign national to live and work permanently in the US.' },
        { term: 'Naturalization', definition: 'The process of becoming a US citizen.' },
        { term: 'Deportation', definition: 'The removal of a foreign national from the US.' },
        { term: 'Asylum', definition: 'Protection granted to foreign nationals who fear persecution in their home country.' },
        { term: 'Refugee', definition: 'A person forced to flee their country due to persecution or war.' },
        { term: 'Visa', definition: 'A document allowing entry into a country for a specific purpose and duration.' },
        { term: 'Work Permit', definition: 'Authorization to work in the US for foreign nationals.' },
        { term: 'I-485', definition: 'Application to Register Permanent Residence or Adjust Status.' },
        { term: 'N-400', definition: 'Application for Naturalization.' },
        { term: 'I-130', definition: 'Petition for Alien Relative.' },
        { term: 'I-765', definition: 'Application for Employment Authorization.' },
        { term: 'I-94', definition: 'Arrival/Departure Record for foreign visitors.' },
        { term: 'DACA', definition: 'Deferred Action for Childhood Arrivals program.' },
        { term: 'TPS', definition: 'Temporary Protected Status for nationals of certain countries.' },
        { term: 'H-1B', definition: 'Temporary work visa for specialty occupations.' },
        { term: 'L-1', definition: 'Intracompany transfer visa for managers and executives.' },
        { term: 'F-1', definition: 'Student visa for academic studies.' },
        { term: 'B-1/B-2', definition: 'Visitor visas for business and tourism.' },
        { term: 'Waiver', definition: 'Forgiveness of certain grounds of inadmissibility.' },
        { term: 'Removal Proceedings', definition: 'Administrative process to determine if a person should be deported.' }
      ]
    },
    {
      category: 'Personal Injury Law',
      icon: <MedicalIcon />,
      color: 'warning',
      terms: [
        { term: 'Negligence', definition: 'Failure to exercise reasonable care resulting in harm to another.' },
        { term: 'Liability', definition: 'Legal responsibility for one\'s actions or omissions.' },
        { term: 'Damages', definition: 'Monetary compensation for losses suffered.' },
        { term: 'Compensatory Damages', definition: 'Money awarded to compensate for actual losses.' },
        { term: 'Punitive Damages', definition: 'Money awarded to punish the defendant for egregious conduct.' },
        { term: 'Pain and Suffering', definition: 'Non-economic damages for physical and emotional distress.' },
        { term: 'Medical Malpractice', definition: 'Negligence by a healthcare provider causing injury or death.' },
        { term: 'Product Liability', definition: 'Legal responsibility for injuries caused by defective products.' },
        { term: 'Premises Liability', definition: 'Legal responsibility for injuries occurring on someone\'s property.' },
        { term: 'Workers\' Compensation', definition: 'Benefits provided to employees injured on the job.' },
        { term: 'Wrongful Death', definition: 'A death caused by another\'s negligence or intentional act.' },
        { term: 'Settlement', definition: 'An agreement to resolve a legal dispute without going to trial.' },
        { term: 'Contingency Fee', definition: 'Attorney fee based on a percentage of the recovery.' },
        { term: 'Statute of Limitations', definition: 'Time limit for filing a personal injury lawsuit.' },
        { term: 'Comparative Negligence', definition: 'A system where fault is divided between parties.' },
        { term: 'Contributory Negligence', definition: 'A defense that the plaintiff\'s own negligence contributed to their injury.' },
        { term: 'Assumption of Risk', definition: 'A defense that the plaintiff voluntarily accepted the risk of injury.' },
        { term: 'Duty of Care', definition: 'Legal obligation to act reasonably to avoid harming others.' },
        { term: 'Breach of Duty', definition: 'Failure to meet the standard of care required by law.' },
        { term: 'Causation', definition: 'The connection between the defendant\'s actions and the plaintiff\'s injury.' }
      ]
    },
    {
      category: 'Business Law',
      icon: <BusinessIcon />,
      color: 'secondary',
      terms: [
        { term: 'Articles of Incorporation', definition: 'Legal documents filed to create a corporation.' },
        { term: 'Bylaws', definition: 'Rules and regulations for internal corporate governance.' },
        { term: 'Partnership', definition: 'A business structure where two or more people share ownership.' },
        { term: 'LLC', definition: 'Limited Liability Company - a hybrid business structure.' },
        { term: 'Corporation', definition: 'A legal entity separate from its owners with limited liability.' },
        { term: 'Sole Proprietorship', definition: 'A business owned and operated by one person.' },
        { term: 'Contract', definition: 'A legally binding agreement between parties.' },
        { term: 'Breach of Contract', definition: 'Failure to fulfill the terms of a contract.' },
        { term: 'Consideration', definition: 'Something of value exchanged between parties in a contract.' },
        { term: 'Capacity', definition: 'Legal ability to enter into a contract.' },
        { term: 'Duress', definition: 'Coercion that makes a contract voidable.' },
        { term: 'Fraud', definition: 'Intentional deception that makes a contract voidable.' },
        { term: 'Tort', definition: 'A wrongful act leading to civil legal liability.' },
        { term: 'Intellectual Property', definition: 'Legal rights to creations of the mind.' },
        { term: 'Copyright', definition: 'Legal protection for original works of authorship.' },
        { term: 'Trademark', definition: 'Legal protection for words, symbols, or designs identifying goods or services.' },
        { term: 'Patent', definition: 'Legal protection for inventions and processes.' },
        { term: 'Trade Secret', definition: 'Confidential business information that provides a competitive advantage.' },
        { term: 'Non-Disclosure Agreement', definition: 'A contract protecting confidential information.' },
        { term: 'Non-Compete Agreement', definition: 'A contract restricting competition after employment ends.' }
      ]
    },
    {
      category: 'Civil Rights Law',
      icon: <PersonIcon />,
      color: 'primary',
      terms: [
        { term: 'Discrimination', definition: 'Unfair treatment based on protected characteristics.' },
        { term: 'Equal Protection', definition: 'Constitutional guarantee of equal treatment under the law.' },
        { term: 'Due Process', definition: 'Constitutional guarantee of fair treatment in legal proceedings.' },
        { term: 'First Amendment', definition: 'Constitutional protection for freedom of speech, religion, and assembly.' },
        { term: 'Fourth Amendment', definition: 'Constitutional protection against unreasonable searches and seizures.' },
        { term: 'Fifth Amendment', definition: 'Constitutional protection against self-incrimination and double jeopardy.' },
        { term: 'Sixth Amendment', definition: 'Constitutional right to a speedy trial and legal counsel.' },
        { term: 'Eighth Amendment', definition: 'Constitutional protection against cruel and unusual punishment.' },
        { term: 'Fourteenth Amendment', definition: 'Constitutional guarantee of equal protection and due process.' },
        { term: 'Title VII', definition: 'Federal law prohibiting employment discrimination.' },
        { term: 'ADA', definition: 'Americans with Disabilities Act - prohibits discrimination against people with disabilities.' },
        { term: 'Fair Housing Act', definition: 'Federal law prohibiting housing discrimination.' },
        { term: 'Voting Rights Act', definition: 'Federal law protecting voting rights and prohibiting discrimination.' },
        { term: 'Civil Rights Act', definition: 'Federal law prohibiting discrimination in public accommodations.' },
        { term: 'Affirmative Action', definition: 'Policies designed to increase opportunities for underrepresented groups.' },
        { term: 'Harassment', definition: 'Unwelcome conduct based on protected characteristics.' },
        { term: 'Retaliation', definition: 'Adverse action taken against someone for engaging in protected activity.' },
        { term: 'Reasonable Accommodation', definition: 'Modifications to enable people with disabilities to perform essential functions.' },
        { term: 'Hostile Work Environment', definition: 'Workplace where harassment creates an intimidating or offensive atmosphere.' },
        { term: 'Quid Pro Quo', definition: 'Harassment where employment benefits are conditioned on sexual favors.' }
      ]
    }
  ];

  const filteredTerms = legalTerms.map(category => ({
    ...category,
    terms: category.terms.filter(term =>
      term.term.toLowerCase().includes(searchQuery.toLowerCase()) ||
      term.definition.toLowerCase().includes(searchQuery.toLowerCase())
    )
  })).filter(category => category.terms.length > 0);

  const totalTerms = legalTerms.reduce((sum, category) => sum + category.terms.length, 0);

  return (
    <PageLayout>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom>
            Legal Glossary
          </Typography>
          <Typography variant="h6" color="text.secondary" paragraph>
            Comprehensive definitions of legal terms and concepts
          </Typography>
          <Badge badgeContent={totalTerms} color="primary">
            <Chip label="Total Terms" color="primary" variant="outlined" />
          </Badge>
        </Box>

        <Paper sx={{ p: 3, mb: 4 }}>
          <TextField
            fullWidth
            placeholder="Search legal terms..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Paper>

        <Grid container spacing={3}>
          {filteredTerms.map((category, index) => (
            <Grid item xs={12} key={index}>
              <Accordion defaultExpanded={index === 0}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                    <Box sx={{ color: `${category.color}.main`, mr: 2 }}>
                      {category.icon}
                    </Box>
                    <Typography variant="h6" sx={{ flexGrow: 1 }}>
                      {category.category}
                    </Typography>
                    <Chip 
                      label={`${category.terms.length} terms`} 
                      color={category.color} 
                      size="small" 
                    />
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={2}>
                    {category.terms.map((term, termIndex) => (
                      <Grid item xs={12} sm={6} md={4} key={termIndex}>
                        <Card variant="outlined" sx={{ height: '100%' }}>
                          <CardContent>
                            <Typography variant="h6" gutterBottom color="primary">
                              {term.term}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {term.definition}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                </AccordionDetails>
              </Accordion>
            </Grid>
          ))}
        </Grid>

        {filteredTerms.length === 0 && searchQuery && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h6" color="text.secondary">
              No terms found matching "{searchQuery}"
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Try searching with different keywords
            </Typography>
          </Box>
        )}
      </Container>
    </PageLayout>
  );
};

export default ComprehensiveGlossaryPage;
