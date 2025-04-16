import React, { createContext, useContext, useState } from 'react';
import { logger } from '../utils/logger';

const Web3Context = createContext(null);

export const useWeb3 = () => useContext(Web3Context);

export const Web3Provider = ({ children }) => {
  const [account, setAccount] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [chainId, setChainId] = useState(null);

  // Placeholder for web3 connection functionality
  const connectWallet = async () => {
    logger.info('Web3 connection not fully implemented');
    // Implementation will follow in a future sprint
    setIsConnected(false);
    return false;
  };

  const disconnectWallet = () => {
    setAccount(null);
    setIsConnected(false);
    setChainId(null);
  };

  const value = {
    account,
    isConnected,
    chainId,
    connectWallet,
    disconnectWallet,
  };

  return <Web3Context.Provider value={value}>{children}</Web3Context.Provider>;
};
