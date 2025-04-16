import React, { useState } from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Box,
  Typography,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import CallIcon from '@mui/icons-material/Call';
import WarningIcon from '@mui/icons-material/Warning';
import PropTypes from 'prop-types';

const EmergencyLegalCallButton = ({ onClick }) => {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleConfirm = () => {
    setOpen(false);
    if (onClick) onClick();
  };

  return (
    <>
      <Button
        variant="contained"
        color="error"
        size="large"
        startIcon={<CallIcon />}
        onClick={handleOpen}
        sx={{
          py: 2,
          px: 4,
          borderRadius: 8,
          fontSize: '1.2rem',
          boxShadow: '0 4px 10px rgba(244, 67, 54, 0.5)',
          '&:hover': {
            boxShadow: '0 6px 15px rgba(244, 67, 54, 0.6)',
          },
          animation: 'pulse 1.5s infinite',
          '@keyframes pulse': {
            '0%': {
              transform: 'scale(1)',
            },
            '50%': {
              transform: 'scale(1.05)',
            },
            '100%': {
              transform: 'scale(1)',
            },
          },
        }}
      >
        {t('Get Emergency Legal Support Now')}
      </Button>

      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <WarningIcon color="error" />
            <Typography variant="h6">{t('Confirm Emergency Legal Support')}</Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {t(
              'You are about to request emergency legal support. This service is intended for urgent legal situations only.'
            )}
          </DialogContentText>
          <DialogContentText sx={{ mt: 2 }}>
            {t('By continuing, you confirm that:')}
          </DialogContentText>
          <Box component="ul" sx={{ pl: 2 }}>
            <DialogContentText component="li">
              {t('You are in an urgent legal situation')}
            </DialogContentText>
            <DialogContentText component="li">
              {t('You consent to having your call recorded for legal documentation')}
            </DialogContentText>
            <DialogContentText component="li">
              {t(
                'You understand this is not a replacement for 911 in life-threatening emergencies'
              )}
            </DialogContentText>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="inherit">
            {t('Cancel')}
          </Button>
          <Button onClick={handleConfirm} variant="contained" color="error" autoFocus>
            {t('Confirm & Connect')}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};


// Define PropTypes
EmergencyLegalCallButton.propTypes = {
  /** TODO: Add description */
  onClick: PropTypes.any,
};

export default EmergencyLegalCallButton;
