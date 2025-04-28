import React, { useEffect, useState } from 'react';
import { Button, Snackbar, Alert } from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import config from '../config';

const NOTIFICATION_API = {
  baseURL: process.env.NODE_ENV === 'production' 
    ? `${config.baseURL}/notifications`
    : 'http://localhost:5001',
  endpoints: {
    publicKey: '/vapid-public-key',
    subscribe: '/subscribe',
  }
};

const NotificationManager = () => {
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [subscription, setSubscription] = useState(null);
  const [registration, setRegistration] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
      navigator.serviceWorker.ready.then(reg => {
        setRegistration(reg);
        return reg.pushManager.getSubscription();
      })
      .then(sub => {
        if (sub) {
          setIsSubscribed(true);
          setSubscription(sub);
        }
      })
      .catch(err => {
        console.error('Error checking subscription:', err);
        setError('Failed to check notification status');
      });
    }
  }, []);

  const subscribeUser = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${NOTIFICATION_API.baseURL}${NOTIFICATION_API.endpoints.publicKey}`);
      if (!response.ok) throw new Error('Failed to get public key');
      
      const data = await response.json();
      
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: data.publicKey
      });

      const subscribeResponse = await fetch(`${NOTIFICATION_API.baseURL}${NOTIFICATION_API.endpoints.subscribe}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(subscription)
      });

      if (!subscribeResponse.ok) throw new Error('Failed to subscribe to notifications');

      setIsSubscribed(true);
      setSubscription(subscription);
      setError(null);
    } catch (err) {
      console.error('Failed to subscribe:', err);
      setError(err.message || 'Failed to enable notifications');
    } finally {
      setLoading(false);
    }
  };

  const unsubscribeUser = async () => {
    try {
      setLoading(true);
      await subscription.unsubscribe();
      setIsSubscribed(false);
      setSubscription(null);
      setError(null);
    } catch (err) {
      console.error('Error unsubscribing:', err);
      setError('Failed to disable notifications');
    } finally {
      setLoading(false);
    }
  };

  const requestPermission = async () => {
    try {
      setLoading(true);
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        await subscribeUser();
      } else {
        setError('Notification permission denied');
      }
    } catch (err) {
      console.error('Error requesting permission:', err);
      setError('Failed to request notification permission');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Button
        variant="contained"
        color={isSubscribed ? "error" : "primary"}
        startIcon={<NotificationsIcon />}
        onClick={isSubscribed ? unsubscribeUser : requestPermission}
        disabled={!registration || loading}
      >
        {loading ? 'Processing...' : isSubscribed ? 'Disable Notifications' : 'Enable Notifications'}
      </Button>

      <Snackbar 
        open={!!error} 
        autoHideDuration={6000} 
        onClose={() => setError(null)}
      >
        <Alert 
          onClose={() => setError(null)} 
          severity="error"
          variant="filled"
        >
          {error}
        </Alert>
      </Snackbar>
    </>
  );
};

export default NotificationManager; 