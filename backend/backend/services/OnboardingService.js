const { createLogger } = require('../utils/logger');
const { mongo } = require('../database');
const { NotFoundError, ValidationError } = require('../utils/errors');

class OnboardingService {
  constructor() {
    this.logger = createLogger('onboarding-service');
    this.collection = mongo.db.collection('onboarding');
  }

  /**
   * Process user onboarding data and create profile
   * @param {string} userId - User ID
   * @param {Object} onboardingData - Onboarding form data
   * @returns {Promise<Object>} Processing result with next steps
   */
  async processOnboarding(userId, onboardingData) {
    try {
      // Validate required fields
      this._validateOnboardingData(onboardingData);

      // Create onboarding record
      const onboardingRecord = {
        userId,
        legalCategory: onboardingData.legalCategory,
        situationDetails: onboardingData.situationDetails,
        financialInfo: onboardingData.financialInfo,
        contactPreferences: onboardingData.contactPreferences,
        status: 'completed',
        createdAt: new Date(),
        updatedAt: new Date()
      };

      // Insert into database
      const result = await this.collection.insertOne(onboardingRecord);

      // Generate next steps based on legal category
      const nextSteps = this._generateNextSteps(onboardingData.legalCategory);
      
      // Find recommended resources
      const recommendedResources = await this._findRecommendedResources(
        onboardingData.legalCategory,
        onboardingData.situationDetails
      );

      return {
        profileId: result.insertedId,
        nextSteps,
        recommendedResources
      };
    } catch (error) {
      this.logger.error('Error processing onboarding', {
        error: error.message,
        userId
      });
      throw error;
    }
  }

  /**
   * Get user's onboarding status
   * @param {string} userId - User ID
   * @returns {Promise<Object>} Onboarding status
   */
  async getOnboardingStatus(userId) {
    try {
      const onboarding = await this.collection.findOne({ userId });
      
      if (!onboarding) {
        return {
          isComplete: false,
          currentStep: 'start'
        };
      }

      return {
        isComplete: onboarding.status === 'completed',
        currentStep: onboarding.status === 'completed' ? 'complete' : onboarding.currentStep,
        category: onboarding.legalCategory
      };
    } catch (error) {
      this.logger.error('Error fetching onboarding status', {
        error: error.message,
        userId
      });
      throw error;
    }
  }

  /**
   * Update onboarding information
   * @param {string} userId - User ID
   * @param {Object} updateData - Updated onboarding data
   * @returns {Promise<Object>} Updated onboarding record
   */
  async updateOnboarding(userId, updateData) {
    try {
      const onboarding = await this.collection.findOne({ userId });
      
      if (!onboarding) {
        throw new NotFoundError('Onboarding record not found');
      }

      const updatedRecord = {
        ...onboarding,
        ...updateData,
        updatedAt: new Date()
      };

      await this.collection.updateOne(
        { userId },
        { $set: updatedRecord }
      );

      return updatedRecord;
    } catch (error) {
      this.logger.error('Error updating onboarding', {
        error: error.message,
        userId
      });
      throw error;
    }
  }

  /**
   * Validate onboarding data
   * @private
   * @param {Object} data - Onboarding data to validate
   * @throws {ValidationError} If validation fails
   */
  _validateOnboardingData(data) {
    const requiredFields = [
      'legalCategory',
      'situationDetails',
      'financialInfo',
      'contactPreferences'
    ];

    for (const field of requiredFields) {
      if (!data[field]) {
        throw new ValidationError(`Missing required field: ${field}`);
      }
    }
  }

  /**
   * Generate next steps based on legal category
   * @private
   * @param {string} category - Legal category
   * @returns {Array<Object>} List of next steps
   */
  _generateNextSteps(category) {
    const commonSteps = [
      {
        step: 1,
        title: 'Review Your Information',
        description: 'Review the information you provided to ensure accuracy.'
      },
      {
        step: 2,
        title: 'Schedule Consultation',
        description: 'Schedule an initial consultation with a legal aid provider.'
      }
    ];

    // Add category-specific steps
    const categorySteps = this._getCategorySpecificSteps(category);

    return [...commonSteps, ...categorySteps];
  }

  /**
   * Get category-specific next steps
   * @private
   * @param {string} category - Legal category
   * @returns {Array<Object>} Category-specific steps
   */
  _getCategorySpecificSteps(category) {
    const categoryStepsMap = {
      'housing': [
        {
          step: 3,
          title: 'Gather Documentation',
          description: 'Collect lease agreements, correspondence, and relevant documents.'
        }
      ],
      'family': [
        {
          step: 3,
          title: 'Family Documentation',
          description: 'Gather marriage certificates, custody agreements, or other relevant documents.'
        }
      ],
      // Add more categories as needed
    };

    return categoryStepsMap[category] || [];
  }

  /**
   * Find recommended resources based on category and situation
   * @private
   * @param {string} category - Legal category
   * @param {Object} situationDetails - Details about the legal situation
   * @returns {Promise<Array<Object>>} Recommended resources
   */
  async _findRecommendedResources(category, situationDetails) {
    // This would typically query a resources collection
    // For now, return static recommendations
    return [
      {
        title: 'Legal Aid Overview',
        type: 'article',
        url: '/resources/legal-aid-overview'
      },
      {
        title: `Guide to ${category} Law`,
        type: 'guide',
        url: `/resources/guides/${category}`
      },
      {
        title: 'Document Checklist',
        type: 'checklist',
        url: '/resources/document-checklist'
      }
    ];
  }
}

module.exports = {
  OnboardingService
}; 