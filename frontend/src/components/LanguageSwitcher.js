import React, { useState } from 'react';
import { 
  Button, 
  Menu, 
  MenuItem, 
  IconButton, 
  Tooltip, 
  Box, 
  Typography,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import TranslateIcon from '@mui/icons-material/Translate';
import CheckIcon from '@mui/icons-material/Check';
import FlagIcon from '@mui/icons-material/Flag';
import LanguageIcon from '@mui/icons-material/Language';

const languages = [
  { code: 'en', label: 'English', flag: '🇺🇸' },
  { code: 'es', label: 'Español', flag: '🇪🇸' },
  { code: 'pt', label: 'Português', flag: '🇧🇷' }
];

const LanguageSwitcher = ({ variant = 'icon' }) => {
  const { i18n, t } = useTranslation();
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const changeLanguage = (languageCode) => {
    i18n.changeLanguage(languageCode);
    localStorage.setItem('preferredLanguage', languageCode);
    handleClose();
  };

  const getCurrentLanguageLabel = () => {
    const current = languages.find(lang => lang.code === i18n.language);
    return current ? current.label : 'English';
  };

  const getCurrentLanguageFlag = () => {
    const current = languages.find(lang => lang.code === i18n.language);
    return current ? current.flag : '🇺🇸';
  };

  if (variant === 'icon') {
    return (
      <>
        <Tooltip title={t('common.changeLanguage')}>
          <IconButton
            onClick={handleClick}
            color="inherit"
            aria-controls={open ? 'language-menu' : undefined}
            aria-haspopup="true"
            aria-expanded={open ? 'true' : undefined}
          >
            <TranslateIcon />
          </IconButton>
        </Tooltip>
        <Menu
          id="language-menu"
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          MenuListProps={{
            'aria-labelledby': 'language-button',
          }}
        >
          {languages.map((language) => (
            <MenuItem 
              key={language.code}
              onClick={() => changeLanguage(language.code)}
              selected={i18n.language === language.code}
            >
              <ListItemIcon sx={{ fontSize: '1.2rem' }}>
                {language.flag}
              </ListItemIcon>
              <ListItemText>{language.label}</ListItemText>
              {i18n.language === language.code && <CheckIcon fontSize="small" />}
            </MenuItem>
          ))}
        </Menu>
      </>
    );
  }

  if (variant === 'button') {
    return (
      <>
        <Button
          onClick={handleClick}
          startIcon={<LanguageIcon />}
          endIcon={<Typography component="span" sx={{ mx: 1 }}>{getCurrentLanguageFlag()}</Typography>}
        >
          {getCurrentLanguageLabel()}
        </Button>
        <Menu
          id="language-menu"
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          MenuListProps={{
            'aria-labelledby': 'language-button',
          }}
        >
          {languages.map((language) => (
            <MenuItem 
              key={language.code}
              onClick={() => changeLanguage(language.code)}
              selected={i18n.language === language.code}
            >
              <ListItemIcon sx={{ fontSize: '1.2rem' }}>
                {language.flag}
              </ListItemIcon>
              <ListItemText>{language.label}</ListItemText>
              {i18n.language === language.code && <CheckIcon fontSize="small" />}
            </MenuItem>
          ))}
        </Menu>
      </>
    );
  }

  return (
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
      {languages.map((language) => (
        <Button
          key={language.code}
          onClick={() => changeLanguage(language.code)}
          variant={i18n.language === language.code ? 'contained' : 'outlined'}
          size="small"
          sx={{ mx: 0.5 }}
        >
          <Box component="span" sx={{ mr: 1 }}>{language.flag}</Box>
          {language.code.toUpperCase()}
        </Button>
      ))}
    </Box>
  );
};

export default LanguageSwitcher; 