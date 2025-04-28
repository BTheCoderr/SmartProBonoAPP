const express = require('express');
const router = express.Router();
const { validateOnboarding } = require('../middleware/validation');
const { requireAuth } = require('../middleware/auth');
const { createLogger } = require('../utils/logger');
const { OnboardingService } = require('../services/OnboardingService');

const logger = createLogger('onboarding-routes');

// Initialize onboarding service
const onboardingService = new OnboardingService();

/**
 * @route POST /api/onboarding
 * @desc Submit onboarding information and create user profile
 * @access Private
 */
router.post('/', requireAuth, validateOnboarding, async (req, res) => {
  try {
    const userId = req.user.id;
    const onboardingData = req.body;

    logger.info(`Processing onboarding for user ${userId}`, {
      category: onboardingData.legalCategory
    });

    // Process onboarding data
    const result = await onboardingService.processOnboarding(userId, onboardingData);

    // Log successful onboarding
    logger.info(`Onboarding completed for user ${userId}`, {
      category: onboardingData.legalCategory,
      profileId: result.profileId
    });

    res.json({
      success: true,
      message: 'Onboarding completed successfully',
      data: {
        profileId: result.profileId,
        nextSteps: result.nextSteps,
        recommendedResources: result.recommendedResources
      }
    });
  } catch (error) {
    logger.error('Error processing onboarding', {
      error: error.message,
      userId: req.user.id
    });

    res.status(500).json({
      success: false,
      message: 'Failed to process onboarding information',
      error: error.message
    });
  }
});

/**
 * @route GET /api/onboarding/status
 * @desc Get user's onboarding status
 * @access Private
 */
router.get('/status', requireAuth, async (req, res) => {
  try {
    const userId = req.user.id;
    const status = await onboardingService.getOnboardingStatus(userId);

    res.json({
      success: true,
      data: status
    });
  } catch (error) {
    logger.error('Error fetching onboarding status', {
      error: error.message,
      userId: req.user.id
    });

    res.status(500).json({
      success: false,
      message: 'Failed to fetch onboarding status',
      error: error.message
    });
  }
});

/**
 * @route PUT /api/onboarding/update
 * @desc Update onboarding information
 * @access Private
 */
router.put('/update', requireAuth, validateOnboarding, async (req, res) => {
  try {
    const userId = req.user.id;
    const updateData = req.body;

    const result = await onboardingService.updateOnboarding(userId, updateData);

    res.json({
      success: true,
      message: 'Onboarding information updated successfully',
      data: result
    });
  } catch (error) {
    logger.error('Error updating onboarding information', {
      error: error.message,
      userId: req.user.id
    });

    res.status(500).json({
      success: false,
      message: 'Failed to update onboarding information',
      error: error.message
    });
  }
});

module.exports = router; 