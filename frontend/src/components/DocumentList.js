import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Button,
  IconButton,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Text,
  useDisclosure,
  Badge,
} from '@chakra-ui/react';
import { FiMoreVertical, FiUpload, FiDownload, FiShare2, FiTrash2, FiClock } from 'react-icons/fi';
import {
import PropTypes from 'prop-types';
  uploadDocument,
  getCaseDocuments,
  downloadDocument,
  deleteDocument,
  shareDocument,
  getDocumentVersions,
  restoreDocumentVersion,
} from '../services/documentService';
const DocumentList = ({ caseId }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [versions, setVersions] = useState([]);
  const fileInputRef = useRef();
  const toast = useToast();
  const { isOpen: isUploadOpen, onOpen: onUploadOpen, onClose: onUploadClose } = useDisclosure();
  const { isOpen: isShareOpen, onOpen: onShareOpen, onClose: onShareClose } = useDisclosure();
  const {
    isOpen: isVersionsOpen,
    onOpen: onVersionsOpen,
    onClose: onVersionsClose,
  } = useDisclosure();
  const [uploadMetadata, setUploadMetadata] = useState({
    title: '',
    description: '',
  });
  const [shareEmail, setShareEmail] = useState('');
  useEffect(() => {
    fetchDocuments();
  }, [caseId, fetchDocuments]);
  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await getCaseDocuments(caseId);
      setDocuments(response);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch documents',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };
  const handleFileSelect = async event => {
    const file = event.target.files[0];
    if (file) {
      onUploadOpen();
      setUploadMetadata({
        title: file.name,
        description: '',
      });
    }
  };
  const handleUpload = async () => {
    try {
      const file = fileInputRef.current.files[0];
      await uploadDocument(caseId, file, uploadMetadata);
      await fetchDocuments();
      onUploadClose();
      toast({
        title: 'Success',
        description: 'Document uploaded successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to upload document',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  const handleDownload = async document => {
    try {
      const blob = await downloadDocument(caseId, document.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = document.title;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to download document',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  const handleShare = async () => {
    try {
      await shareDocument(caseId, selectedDocument.id, { email: shareEmail });
      onShareClose();
      toast({
        title: 'Success',
        description: 'Document shared successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to share document',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  const handleDelete = async document => {
    try {
      await deleteDocument(caseId, document.id);
      await fetchDocuments();
      toast({
        title: 'Success',
        description: 'Document deleted successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete document',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  const handleViewVersions = async document => {
    try {
      const response = await getDocumentVersions(caseId, document.id);
      setVersions(response);
      setSelectedDocument(document);
      onVersionsOpen();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch document versions',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  const handleRestoreVersion = async versionId => {
    try {
      await restoreDocumentVersion(caseId, selectedDocument.id, versionId);
      await fetchDocuments();
      onVersionsClose();
      toast({
        title: 'Success',
        description: 'Document version restored successfully',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to restore document version',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  return (
    <Box>
      <Box mb={4}>
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileSelect}
        />
        <Button
          leftIcon={<FiUpload />}
          onClick={() => fileInputRef.current.click()}
          colorScheme="blue"
        >
          Upload Document
        </Button>
      </Box>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Title</Th>
            <Th>Type</Th>
            <Th>Size</Th>
            <Th>Uploaded</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {documents.map(doc => (
            <Tr key={doc.id}>
              <Td>{doc.title}</Td>
              <Td>
                <Badge>{doc.type}</Badge>
              </Td>
              <Td>{Math.round(doc.size / 1024)} KB</Td>
              <Td>{new Date(doc.uploaded_at).toLocaleDateString()}</Td>
              <Td>
                <Menu>
                  <MenuButton as={IconButton} icon={<FiMoreVertical />} variant="ghost" size="sm" />
                  <MenuList>
                    <MenuItem icon={<FiDownload />} onClick={() => handleDownload(doc)}>
                      Download
                    </MenuItem>
                    <MenuItem
                      icon={<FiShare2 />}
                      onClick={() => {
                        setSelectedDocument(doc);
                        onShareOpen();
                      }}
                    >
                      Share
                    </MenuItem>
                    <MenuItem icon={<FiClock />} onClick={() => handleViewVersions(doc)}>
                      Versions
                    </MenuItem>
                    <MenuItem icon={<FiTrash2 />} onClick={() => handleDelete(doc)} color="red.500">
                      Delete
                    </MenuItem>
                  </MenuList>
                </Menu>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
      {/* Upload Modal */}
      <Modal isOpen={isUploadOpen} onClose={onUploadClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Upload Document</ModalHeader>
          <ModalBody>
            <VStack spacing={4}>
              <FormControl>
                <FormLabel>Title</FormLabel>
                <Input
                  value={uploadMetadata.title}
                  onChange={e =>
                    setUploadMetadata(prev => ({
                      ...prev,
                      title: e.target.value,
                    }))
                  }
                />
              </FormControl>
              <FormControl>
                <FormLabel>Description</FormLabel>
                <Input
                  value={uploadMetadata.description}
                  onChange={e =>
                    setUploadMetadata(prev => ({
                      ...prev,
                      description: e.target.value,
                    }))
                  }
                />
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onUploadClose}>
              Cancel
            </Button>
            <Button colorScheme="blue" onClick={handleUpload}>
              Upload
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      {/* Share Modal */}
      <Modal isOpen={isShareOpen} onClose={onShareClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Share Document</ModalHeader>
          <ModalBody>
            <FormControl>
              <FormLabel>Email Address</FormLabel>
              <Input
                type="email"
                value={shareEmail}
                onChange={e => setShareEmail(e.target.value)}
                placeholder="Enter recipient's email"
              />
            </FormControl>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onShareClose}>
              Cancel
            </Button>
            <Button colorScheme="blue" onClick={handleShare}>
              Share
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      {/* Versions Modal */}
      <Modal isOpen={isVersionsOpen} onClose={onVersionsClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Document Versions</ModalHeader>
          <ModalBody>
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Version</Th>
                  <Th>Created</Th>
                  <Th>Size</Th>
                  <Th>Actions</Th>
                </Tr>
              </Thead>
              <Tbody>
                {versions.map(version => (
                  <Tr key={version.id}>
                    <Td>v{version.version_number}</Td>
                    <Td>{new Date(version.created_at).toLocaleDateString()}</Td>
                    <Td>{Math.round(version.size / 1024)} KB</Td>
                    <Td>
                      <Button size="sm" onClick={() => handleRestoreVersion(version.id)}>
                        Restore
                      </Button>
                    </Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </ModalBody>
          <ModalFooter>
            <Button onClick={onVersionsClose}>Close</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Box>
  );
};

// Define PropTypes
DocumentList.propTypes = {
  /** TODO: Add description */
  caseId: PropTypes.any,
};

export default DocumentList;