import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Button,
  TextField,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import ChatRoom from '../components/ChatRoom';
import { v4 as uuidv4 } from 'uuid';
import PageLayout from '../components/PageLayout';

/**
 * ChatRoomPage component for joining and participating in chat rooms
 */
const ChatRoomPage = () => {
  const { t } = useTranslation();
  const { roomId } = useParams();
  const navigate = useNavigate();
  const [activeRoom, setActiveRoom] = useState(roomId || '');
  const [userName, setUserName] = useState('');
  const [userId] = useState(() => localStorage.getItem('chatUserId') || uuidv4());
  const [joinDialogOpen, setJoinDialogOpen] = useState(!roomId);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newRoomName, setNewRoomName] = useState('');
  const [error, setError] = useState('');

  // Initialize user ID on component mount
  useEffect(() => {
    localStorage.setItem('chatUserId', userId);

    // Check if the user already has a stored name
    const storedName = localStorage.getItem('chatUserName');
    if (storedName) {
      setUserName(storedName);
    }
  }, [userId]);

  // Handle joining a chat room
  const handleJoinRoom = () => {
    if (!userName.trim()) {
      setError(t('Please enter your name'));
      return;
    }

    if (!activeRoom.trim()) {
      setError(t('Please enter a room ID'));
      return;
    }

    // Save the username for future use
    localStorage.setItem('chatUserName', userName);
    
    // Close the dialog and navigate to the room if needed
    setJoinDialogOpen(false);
    if (roomId !== activeRoom) {
      navigate(`/chat-room/${activeRoom}`);
    }
  };

  // Handle creating a new chat room
  const handleCreateRoom = () => {
    if (!userName.trim()) {
      setError(t('Please enter your name'));
      return;
    }

    if (!newRoomName.trim()) {
      setError(t('Please enter a room name'));
      return;
    }

    // Create a unique room ID based on the name
    const generatedRoomId = newRoomName.toLowerCase().replace(/\s+/g, '-') + '-' + Date.now().toString(36);
    
    // Save the username for future use
    localStorage.setItem('chatUserName', userName);
    
    // Close the dialog and navigate to the new room
    setCreateDialogOpen(false);
    setActiveRoom(generatedRoomId);
    navigate(`/chat-room/${generatedRoomId}`);
  };

  // Handle leaving a chat room
  const handleLeaveRoom = () => {
    setActiveRoom('');
    setJoinDialogOpen(true);
    navigate('/chat-room');
  };

  // Reset error on input change
  const handleInputChange = (e) => {
    setError('');
    if (e.target.name === 'userName') {
      setUserName(e.target.value);
    } else if (e.target.name === 'roomId') {
      setActiveRoom(e.target.value);
    } else if (e.target.name === 'newRoomName') {
      setNewRoomName(e.target.value);
    }
  };

  return (
    <PageLayout title={t('Chat Rooms')} description={t('Join or create a chat room')}>
      <Container maxWidth="lg">
        {/* Main content */}
        {activeRoom && userName ? (
          <ChatRoom
            roomId={activeRoom}
            userId={userId}
            userName={userName}
            onLeave={handleLeaveRoom}
          />
        ) : (
          <Paper elevation={3} sx={{ p: 3, my: 4, textAlign: 'center' }}>
            <Typography variant="h5" gutterBottom>
              {t('Welcome to Chat Rooms')}
            </Typography>
            <Typography variant="body1" sx={{ mb: 3 }}>
              {t('Join an existing room or create a new one to start chatting.')}
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => setJoinDialogOpen(true)}
              >
                {t('Join Room')}
              </Button>
              <Button
                variant="outlined"
                color="secondary"
                onClick={() => setCreateDialogOpen(true)}
              >
                {t('Create Room')}
              </Button>
            </Box>
          </Paper>
        )}

        {/* Join Room Dialog */}
        <Dialog
          open={joinDialogOpen}
          onClose={() => activeRoom ? setJoinDialogOpen(false) : null}
          maxWidth="xs"
          fullWidth
        >
          <DialogTitle>{t('Join Chat Room')}</DialogTitle>
          <DialogContent>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            <TextField
              autoFocus
              margin="dense"
              name="userName"
              label={t('Your Name')}
              type="text"
              fullWidth
              variant="outlined"
              value={userName}
              onChange={handleInputChange}
              sx={{ mb: 2 }}
            />
            <TextField
              margin="dense"
              name="roomId"
              label={t('Room ID')}
              type="text"
              fullWidth
              variant="outlined"
              value={activeRoom}
              onChange={handleInputChange}
            />
          </DialogContent>
          <DialogActions>
            {activeRoom && (
              <Button onClick={() => setJoinDialogOpen(false)} color="secondary">
                {t('Cancel')}
              </Button>
            )}
            <Button onClick={handleJoinRoom} color="primary" variant="contained">
              {t('Join')}
            </Button>
          </DialogActions>
        </Dialog>

        {/* Create Room Dialog */}
        <Dialog
          open={createDialogOpen}
          onClose={() => setCreateDialogOpen(false)}
          maxWidth="xs"
          fullWidth
        >
          <DialogTitle>{t('Create New Chat Room')}</DialogTitle>
          <DialogContent>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            <TextField
              autoFocus
              margin="dense"
              name="userName"
              label={t('Your Name')}
              type="text"
              fullWidth
              variant="outlined"
              value={userName}
              onChange={handleInputChange}
              sx={{ mb: 2 }}
            />
            <TextField
              margin="dense"
              name="newRoomName"
              label={t('Room Name')}
              type="text"
              fullWidth
              variant="outlined"
              value={newRoomName}
              onChange={handleInputChange}
              helperText={t('A unique room ID will be generated based on this name')}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setCreateDialogOpen(false)} color="secondary">
              {t('Cancel')}
            </Button>
            <Button onClick={handleCreateRoom} color="primary" variant="contained">
              {t('Create')}
            </Button>
          </DialogActions>
        </Dialog>
      </Container>
    </PageLayout>
  );
};

export default ChatRoomPage; 