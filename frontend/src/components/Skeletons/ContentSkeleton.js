import React from 'react';
import { Box, Skeleton, useTheme } from '@mui/material';

const ContentSkeleton = ({ type = 'default', rows = 3, height, width }) => {
  const theme = useTheme();

  const renderDocumentSkeleton = () => (
    <Box sx={{ width: '100%', maxWidth: 800, mx: 'auto', p: 2 }}>
      <Skeleton variant="rectangular" width="30%" height={24} sx={{ mb: 1 }} />
      <Skeleton variant="rectangular" width="60%" height={32} sx={{ mb: 3 }} />
      {[...Array(rows)].map((_, i) => (
        <Skeleton
          key={i}
          variant="rectangular"
          width={`${Math.random() * 40 + 60}%`}
          height={16}
          sx={{ mb: 2 }}
        />
      ))}
      <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
        <Skeleton variant="rectangular" width={120} height={36} />
        <Skeleton variant="rectangular" width={120} height={36} />
      </Box>
    </Box>
  );

  const renderCardSkeleton = () => (
    <Box sx={{ width: '100%', maxWidth: 400, p: 2 }}>
      <Skeleton variant="rectangular" height={200} sx={{ mb: 2, borderRadius: 1 }} />
      <Skeleton variant="rectangular" width="80%" height={24} sx={{ mb: 1 }} />
      <Skeleton variant="rectangular" width="60%" height={20} sx={{ mb: 2 }} />
      {[...Array(3)].map((_, i) => (
        <Skeleton key={i} variant="rectangular" width="100%" height={16} sx={{ mb: 1 }} />
      ))}
    </Box>
  );

  const renderTableSkeleton = () => (
    <Box sx={{ width: '100%', overflow: 'hidden' }}>
      <Box sx={{ display: 'flex', mb: 2 }}>
        {[...Array(4)].map((_, i) => (
          <Skeleton
            key={i}
            variant="rectangular"
            width={`${100 / 4}%`}
            height={48}
            sx={{ mx: 0.5 }}
          />
        ))}
      </Box>
      {[...Array(rows)].map((_, rowIndex) => (
        <Box key={rowIndex} sx={{ display: 'flex', mb: 1 }}>
          {[...Array(4)].map((_, colIndex) => (
            <Skeleton
              key={colIndex}
              variant="rectangular"
              width={`${100 / 4}%`}
              height={32}
              sx={{ mx: 0.5 }}
            />
          ))}
        </Box>
      ))}
    </Box>
  );

  const renderListSkeleton = () => (
    <Box sx={{ width: '100%' }}>
      {[...Array(rows)].map((_, i) => (
        <Box key={i} sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Skeleton variant="circular" width={40} height={40} sx={{ mr: 2 }} />
          <Box sx={{ flex: 1 }}>
            <Skeleton variant="rectangular" width="80%" height={20} sx={{ mb: 1 }} />
            <Skeleton variant="rectangular" width="60%" height={16} />
          </Box>
        </Box>
      ))}
    </Box>
  );

  const renderDefaultSkeleton = () => (
    <Box sx={{ width: width || '100%' }}>
      {[...Array(rows)].map((_, i) => (
        <Skeleton
          key={i}
          variant="rectangular"
          width="100%"
          height={height || 20}
          sx={{ mb: 1 }}
        />
      ))}
    </Box>
  );

  const skeletonMap = {
    document: renderDocumentSkeleton,
    card: renderCardSkeleton,
    table: renderTableSkeleton,
    list: renderListSkeleton,
    default: renderDefaultSkeleton,
  };

  return (
    <Box
      role="progressbar"
      aria-label="Loading content"
      aria-busy="true"
      sx={{
        animation: `${theme.transitions.create(['opacity'], {
          duration: theme.transitions.duration.standard,
        })}`,
      }}
    >
      {skeletonMap[type]?.() || renderDefaultSkeleton()}
    </Box>
  );
};

export default ContentSkeleton; 