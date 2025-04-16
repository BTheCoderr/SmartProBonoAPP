import { Box, Accordion, AccordionSummary, AccordionDetails, Typography } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const ContractGuide = () => {
  const guides = [
    {
      title: 'Understanding Contracts',
      content:
        'A contract is a legally binding agreement between two or more parties. It defines the rights and obligations of each party.',
      tips: [
        'Always read the entire contract',
        'Understand all terms before signing',
        'Keep copies of all signed documents',
      ],
    },
    {
      title: 'Contract Elements',
      content:
        'Every valid contract must have certain essential elements to be legally enforceable.',
      tips: [
        'Ensure clear offer and acceptance',
        'Verify consideration exists',
        'Check legal capacity of parties',
      ],
    },
  ];

  return (
    <Box sx={{ mt: 3 }}>
      {guides.map((guide, index) => (
        <Accordion key={index}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="h6">{guide.title}</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography paragraph>{guide.content}</Typography>
            <Typography variant="subtitle1">Key Tips:</Typography>
            <ul>
              {guide.tips.map((tip, i) => (
                <li key={i}>
                  <Typography>{tip}</Typography>
                </li>
              ))}
            </ul>
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );
};

export default ContractGuide;
