import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  TextField,
  Grid,
  List,
  ListItem,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  InputAdornment,
  Chip,
  Paper,
  Divider
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Search as SearchIcon,
  Gavel as GavelIcon,
  Business as BusinessIcon,
  FamilyRestroom as FamilyIcon,
  Security as SecurityIcon,
  Description as DescriptionIcon,
  AccountBalance as AccountBalanceIcon
} from '@mui/icons-material';
import PageLayout from '../components/PageLayout';

const GlossaryPage = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const legalTerms = [
    {
      category: 'General Legal Terms',
      icon: <GavelIcon />,
      color: 'primary',
      terms: [
        {
          term: 'Affidavit',
          definition: 'A written statement made under oath, used as evidence in court proceedings.'
        },
        {
          term: 'Appeal',
          definition: 'A request to a higher court to review and change the decision of a lower court.'
        },
        {
          term: 'Burden of Proof',
          definition: 'The obligation to prove one\'s assertion in a legal proceeding.'
        },
        {
          term: 'Due Process',
          definition: 'The legal requirement that the state must respect all legal rights owed to a person.'
        },
        {
          term: 'Injunction',
          definition: 'A court order requiring a person to do or cease doing a specific action.'
        },
        {
          term: 'Jurisdiction',
          definition: 'The authority of a court to hear and decide cases within a particular geographic area or over certain types of legal cases.'
        },
        {
          term: 'Liability',
          definition: 'Legal responsibility for one\'s actions or omissions that result in harm to another person.'
        },
        {
          term: 'Litigation',
          definition: 'The process of taking legal action through the court system.'
        },
        {
          term: 'Precedent',
          definition: 'A legal principle established in a previous case that is binding on or persuasive for a court when deciding subsequent cases with similar issues.'
        },
        {
          term: 'Statute of Limitations',
          definition: 'A law that sets the maximum time after an event within which legal proceedings may be initiated.'
        }
      ]
    },
    {
      category: 'Business Law',
      icon: <BusinessIcon />,
      color: 'secondary',
      terms: [
        {
          term: 'Articles of Incorporation',
          definition: 'Legal documents filed with a government body to legally document the creation of a corporation.'
        },
        {
          term: 'Bylaws',
          definition: 'Rules and regulations adopted by a corporation for its internal governance.'
        },
        {
          term: 'Intellectual Property',
          definition: 'Creations of the mind, such as inventions, literary and artistic works, designs, and symbols used in commerce.'
        },
        {
          term: 'Limited Liability Company (LLC)',
          definition: 'A business structure that combines the pass-through taxation of a partnership with the limited liability of a corporation.'
        },
        {
          term: 'Non-Disclosure Agreement (NDA)',
          definition: 'A legal contract that creates a confidential relationship between parties to protect sensitive information.'
        },
        {
          term: 'Partnership',
          definition: 'An arrangement where parties agree to cooperate to advance their mutual interests.'
        },
        {
          term: 'Trademark',
          definition: 'A recognizable sign, design, or expression which identifies products or services of a particular source.'
        }
      ]
    },
    {
      category: 'Family Law',
      icon: <FamilyIcon />,
      color: 'success',
      terms: [
        {
          term: 'Alimony',
          definition: 'Financial support paid by one spouse to another after divorce or separation.'
        },
        {
          term: 'Child Custody',
          definition: 'The legal and practical relationship between a parent and child, including the right to make decisions about the child\'s welfare.'
        },
        {
          term: 'Child Support',
          definition: 'Regular payments made by a non-custodial parent to help cover the costs of raising a child.'
        },
        {
          term: 'Divorce',
          definition: 'The legal dissolution of a marriage by a court or other competent body.'
        },
        {
          term: 'Prenuptial Agreement',
          definition: 'A written contract created by two people before they are married, outlining how assets will be divided in case of divorce.'
        },
        {
          term: 'Visitation Rights',
          definition: 'The right of a non-custodial parent to spend time with their child.'
        }
      ]
    },
    {
      category: 'Immigration Law',
      icon: <SecurityIcon />,
      color: 'warning',
      terms: [
        {
          term: 'Asylum',
          definition: 'Protection granted to foreign nationals who can demonstrate that they are unable or unwilling to return to their country of origin due to persecution.'
        },
        {
          term: 'Green Card',
          definition: 'A document that allows a foreign national to live and work permanently in the United States.'
        },
        {
          term: 'Naturalization',
          definition: 'The process by which a foreign national becomes a citizen of a country.'
        },
        {
          term: 'Refugee',
          definition: 'A person who has been forced to flee their country due to persecution, war, or violence.'
        },
        {
          term: 'Visa',
          definition: 'An official document that allows a person to enter, stay, or leave a country for a specific period.'
        },
        {
          term: 'Work Permit',
          definition: 'Official authorization that allows a foreign national to work in a country for a specific period.'
        }
      ]
    },
    {
      category: 'Document Terms',
      icon: <DescriptionIcon />,
      color: 'info',
      terms: [
        {
          term: 'Contract',
          definition: 'A legally binding agreement between two or more parties that creates mutual obligations.'
        },
        {
          term: 'Deed',
          definition: 'A legal document that transfers ownership of real property from one party to another.'
        },
        {
          term: 'Lease',
          definition: 'A contract outlining the terms under which one party agrees to rent property from another party.'
        },
        {
          term: 'Power of Attorney',
          definition: 'A legal document that gives one person the authority to act on behalf of another person in legal or financial matters.'
        },
        {
          term: 'Will',
          definition: 'A legal document that expresses a person\'s wishes as to how their property is to be distributed after their death.'
        }
      ]
    },
    {
      category: 'Court Terms',
      icon: <AccountBalanceIcon />,
      color: 'error',
      terms: [
        {
          term: 'Bench Trial',
          definition: 'A trial in which a judge, rather than a jury, decides the facts and applies the law.'
        },
        {
          term: 'Jury Trial',
          definition: 'A trial in which a jury decides the facts and applies the law as instructed by the judge.'
        },
        {
          term: 'Misdemeanor',
          definition: 'A criminal offense that is less serious than a felony and typically punishable by fines or imprisonment for less than one year.'
        },
        {
          term: 'Felony',
          definition: 'A serious criminal offense that is punishable by imprisonment for more than one year or by death.'
        },
        {
          term: 'Plea Bargain',
          definition: 'An agreement between a defendant and prosecutor in which the defendant pleads guilty to a lesser charge in exchange for a more lenient sentence.'
        },
        {
          term: 'Verdict',
          definition: 'The formal decision or finding made by a jury or judge in a legal proceeding.'
        }
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

  return (
    <PageLayout
      title="Legal Glossary"
      description="Comprehensive definitions of legal terms and concepts"
    >
      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* Search Section */}
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Search Legal Terms
          </Typography>
          <TextField
            fullWidth
            placeholder="Search for legal terms..."
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

        {/* Search Results */}
        {searchQuery && (
          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Search Results for "{searchQuery}"
            </Typography>
            {filteredTerms.length === 0 ? (
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="h6" gutterBottom>
                  No terms found
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Try different keywords or browse our categories below.
                </Typography>
              </Paper>
            ) : (
              <Grid container spacing={2}>
                {filteredTerms.map((category, categoryIndex) => (
                  <Grid item xs={12} key={categoryIndex}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {category.icon}
                          {category.category}
                        </Typography>
                        <List>
                          {category.terms.map((term, termIndex) => (
                            <ListItem key={termIndex} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                              <Typography variant="subtitle1" fontWeight="bold" color="primary">
                                {term.term}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                {term.definition}
                              </Typography>
                              {termIndex < category.terms.length - 1 && <Divider sx={{ width: '100%', mt: 1 }} />}
                            </ListItem>
                          ))}
                        </List>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
          </Box>
        )}

        {/* Category Browse */}
        {!searchQuery && (
          <Box>
            <Typography variant="h5" gutterBottom>
              Browse by Category
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Explore legal terms organized by practice area and topic.
            </Typography>

            {legalTerms.map((category, categoryIndex) => (
              <Accordion key={categoryIndex} sx={{ mb: 2 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    {category.icon}
                    <Typography variant="h6">
                      {category.category}
                    </Typography>
                    <Chip
                      label={`${category.terms.length} terms`}
                      size="small"
                      color={category.color}
                    />
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={2}>
                    {category.terms.map((term, termIndex) => (
                      <Grid item xs={12} sm={6} md={4} key={termIndex}>
                        <Card variant="outlined">
                          <CardContent>
                            <Typography variant="subtitle2" fontWeight="bold" color="primary" gutterBottom>
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
            ))}
          </Box>
        )}

        {/* Help Section */}
        <Paper sx={{ p: 3, mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Need More Help?
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            This glossary provides general definitions of legal terms. For specific legal advice, consult with a qualified attorney.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Chip
              label="Contact Legal Support"
              clickable
              color="primary"
              variant="outlined"
            />
            <Chip
              label="Schedule Consultation"
              clickable
              color="primary"
              variant="outlined"
            />
          </Box>
        </Paper>
      </Container>
    </PageLayout>
  );
};

export default GlossaryPage;

