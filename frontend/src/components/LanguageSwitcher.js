import React, { useState } from 'react';
import { 
  Button, 
  IconButton, 
  Tooltip, 
  Box, 
  Typography,
  Popover
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import CheckIcon from '@mui/icons-material/Check';
import LanguageIcon from '@mui/icons-material/Language';

const languages = [
  { code: 'en', label: 'English', flag: '🇺🇸' },
  { code: 'es', label: 'Español', flag: '🇪🇸' },
  { code: 'pt', label: 'Português', flag: '🇧🇷' },
  { code: 'fr', label: 'Français', flag: '🇫🇷' },
  { code: 'zh', label: '中文', flag: '🇨🇳' },
  { code: 'ar', label: 'العربية', flag: '🇸🇦' }
];

const LanguageSwitcher = ({ variant = 'icon' }) => {
  const { i18n, t } = useTranslation();
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setAnchorEl(event.currentTarget);
  };

  const handleClose = (event) => {
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
        <Tooltip title={`${t('common.changeLanguage', 'Change Language')} - ${getCurrentLanguageLabel()}`}>
          <IconButton
            onClick={handleClick}
            color="inherit"
            aria-controls={open ? 'language-menu' : undefined}
            aria-haspopup="true"
            aria-expanded={open ? 'true' : undefined}
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              minWidth: 40,
              minHeight: 40
            }}
          >
            <Typography component="span" sx={{ fontSize: '1.2rem', lineHeight: 1 }}>
              {getCurrentLanguageFlag()}
            </Typography>
            <Typography component="span" sx={{ fontSize: '0.6rem', lineHeight: 1, mt: 0.2 }}>
              {getCurrentLanguageLabel().substring(0, 2).toUpperCase()}
            </Typography>
          </IconButton>
        </Tooltip>
        <Popover
          id="language-menu"
          open={open}
          anchorEl={anchorEl}
          onClose={handleClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'left',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
          sx={{
            '& .MuiPaper-root': {
              zIndex: 9999,
              mt: 1,
              minWidth: 200
            }
          }}
        >
          <Box sx={{ p: 1 }}>
            {languages.map((language) => (
              <Box
                key={language.code}
                onClick={() => changeLanguage(language.code)}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  p: 1.5,
                  cursor: 'pointer',
                  borderRadius: 1,
                  '&:hover': {
                    bgcolor: 'action.hover'
                  },
                  bgcolor: i18n.language === language.code ? 'action.selected' : 'transparent'
                }}
              >
                <Typography sx={{ fontSize: '1.2rem', mr: 1.5 }}>
                  {language.flag}
                </Typography>
                <Typography sx={{ flexGrow: 1 }}>
                  {language.label}
                </Typography>
                {i18n.language === language.code && <CheckIcon fontSize="small" />}
              </Box>
            ))}
          </Box>
        </Popover>
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
        <Popover
          id="language-menu"
          open={open}
          anchorEl={anchorEl}
          onClose={handleClose}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'left',
          }}
          transformOrigin={{
            vertical: 'top',
            horizontal: 'left',
          }}
          sx={{
            '& .MuiPaper-root': {
              zIndex: 9999,
              mt: 1,
              minWidth: 200
            }
          }}
        >
          <Box sx={{ p: 1 }}>
            {languages.map((language) => (
              <Box
                key={language.code}
                onClick={() => changeLanguage(language.code)}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  p: 1.5,
                  cursor: 'pointer',
                  borderRadius: 1,
                  '&:hover': {
                    bgcolor: 'action.hover'
                  },
                  bgcolor: i18n.language === language.code ? 'action.selected' : 'transparent'
                }}
              >
                <Typography sx={{ fontSize: '1.2rem', mr: 1.5 }}>
                  {language.flag}
                </Typography>
                <Typography sx={{ flexGrow: 1 }}>
                  {language.label}
                </Typography>
                {i18n.language === language.code && <CheckIcon fontSize="small" />}
              </Box>
            ))}
          </Box>
        </Popover>
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