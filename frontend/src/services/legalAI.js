// This is a free implementation using predefined responses
const legalTopics = {
  contract: {
    response:
      'A contract requires offer, acceptance, consideration, and intention to create legal relations.',
  },
  breach: {
    response:
      'A breach of contract occurs when one party fails to fulfill their obligations under the agreement.',
  },
  damages: {
    response:
      'Common remedies for breach of contract include compensatory damages, specific performance, and injunctive relief.',
  },
};

const getLegalAdvice = async query => {
  // Simple keyword matching
  const queryLower = query.toLowerCase();
  let response =
    'I apologize, but I can only provide general information about basic contract law concepts.';

  if (queryLower.includes('contract')) {
    response = legalTopics.contract.response;
  } else if (queryLower.includes('breach')) {
    response = legalTopics.breach.response;
  } else if (queryLower.includes('damages')) {
    response = legalTopics.damages.response;
  }

  // Simulate async behavior
  return new Promise(resolve => {
    setTimeout(() => {
      resolve({
        response,
        disclaimer:
          'This is general information and not legal advice. Please consult with a qualified legal professional for specific advice.',
      });
    }, 1000);
  });
};

export default getLegalAdvice;
