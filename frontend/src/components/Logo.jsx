import React from 'react';
import PropTypes from 'prop-types';

const Logo = ({ size = 'medium', variant = 'light' }) => {
  // Calculate dimensions based on size
  const dimensions = {
    small: { width: 150, height: 40 },
    medium: { width: 200, height: 50 },
    large: { width: 250, height: 60 }
  };

  // Calculate color based on variant
  const getColor = () => {
    switch (variant) {
      case 'dark':
        return '#FFFFFF';
      case 'highContrast':
        return '#FFFFFF';
      case 'light':
      default:
        return '#2196F3';
    }
  };

  const { width, height } = dimensions[size] || dimensions.medium;
  const color = getColor();

  return (
    <svg width={width} height={height} viewBox="0 0 200 50" xmlns="http://www.w3.org/2000/svg">
      <g>
        <rect x="10" y="25" width="30" height="5" fill={color}/>
        <text x="50" y="35" style={{ fontFamily: 'Arial, sans-serif', fontSize: '24px', fill: color }}>
          SmartProBono
        </text>
        <rect x="160" y="10" width="30" height="30" rx="5" fill={color}/>
      </g>
    </svg>
  );
};

Logo.propTypes = {
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  variant: PropTypes.oneOf(['light', 'dark', 'highContrast'])
};

export default Logo; 