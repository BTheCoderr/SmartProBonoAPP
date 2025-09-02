import React from 'react';
import { useParams } from 'react-router-dom';
import { PageLayout } from '../design-system';
import DocumentChecklist from '../components/DocumentChecklist';

const DocumentChecklistPage = () => {
  const { type } = useParams();

  return (
    <PageLayout
      title="Document Checklist"
      description="Essential documents needed for your legal process"
    >
      <DocumentChecklist type={type || 'immigration'} />
    </PageLayout>
  );
};

export default DocumentChecklistPage;
