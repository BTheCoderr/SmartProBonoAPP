import type { User, Organization, Case, Document, Template, Message, Event } from "./types"

export const mockUsers: User[] = [
  {
    id: "1",
    email: "maria.garcia@email.com",
    name: "Maria Garcia",
    role: "client",
    createdAt: new Date("2024-01-15"),
    updatedAt: new Date("2024-01-15"),
  },
  {
    id: "2",
    email: "john.attorney@lawfirm.com",
    name: "John Smith",
    role: "attorney",
    organizationId: "1",
    createdAt: new Date("2024-01-10"),
    updatedAt: new Date("2024-01-10"),
  },
  {
    id: "3",
    email: "admin@smartprobono.org",
    name: "Sarah Admin",
    role: "admin",
    createdAt: new Date("2024-01-01"),
    updatedAt: new Date("2024-01-01"),
  },
  {
    id: "4",
    email: "paralegal@legalclinic.org",
    name: "David Paralegal",
    role: "paralegal",
    organizationId: "2",
    createdAt: new Date("2024-01-05"),
    updatedAt: new Date("2024-01-05"),
  },
]

export const mockOrganizations: Organization[] = [
  {
    id: "1",
    name: "Community Legal Services",
    type: "legal_clinic",
    address: "123 Justice Ave, City, State 12345",
    phone: "(555) 123-4567",
    email: "info@communitylegal.org",
    createdAt: new Date("2024-01-01"),
  },
  {
    id: "2",
    name: "Pro Bono Law Firm",
    type: "law_firm",
    address: "456 Legal St, City, State 12345",
    phone: "(555) 987-6543",
    email: "contact@probonolaw.com",
    createdAt: new Date("2024-01-01"),
  },
]

export const mockCases: Case[] = [
  {
    id: "1",
    clientId: "1",
    attorneyId: "2",
    title: "Immigration Status Adjustment",
    description: "Client needs help adjusting immigration status from temporary to permanent resident.",
    category: "immigration",
    status: "active",
    priority: "high",
    createdAt: new Date("2024-01-20"),
    updatedAt: new Date("2024-01-25"),
    dueDate: new Date("2024-03-15"),
  },
  {
    id: "2",
    clientId: "1",
    title: "Housing Discrimination Case",
    description: "Client facing discrimination from landlord based on national origin.",
    category: "housing",
    status: "intake",
    priority: "medium",
    createdAt: new Date("2024-01-22"),
    updatedAt: new Date("2024-01-22"),
  },
]

export const mockDocuments: Document[] = [
  {
    id: "1",
    caseId: "1",
    userId: "1",
    name: "Passport Copy.pdf",
    type: "pdf",
    size: 2048000,
    url: "/documents/passport-copy.pdf",
    tags: ["identity", "immigration"],
    version: 1,
    status: "approved",
    createdAt: new Date("2024-01-21"),
    updatedAt: new Date("2024-01-21"),
  },
  {
    id: "2",
    caseId: "1",
    userId: "2",
    name: "I-485 Application Draft.pdf",
    type: "pdf",
    size: 1024000,
    url: "/documents/i485-draft.pdf",
    tags: ["application", "immigration"],
    version: 2,
    status: "review",
    createdAt: new Date("2024-01-23"),
    updatedAt: new Date("2024-01-25"),
  },
]

export const mockTemplates: Template[] = [
  {
    id: "1",
    name: "Immigration Intake Form",
    description: "Standard intake form for immigration cases",
    category: "immigration",
    content: "Immigration intake template content...",
    variables: ["client_name", "country_of_origin", "case_type"],
    createdBy: "2",
    isPublic: true,
    createdAt: new Date("2024-01-10"),
    updatedAt: new Date("2024-01-10"),
  },
  {
    id: "2",
    name: "Housing Rights Letter",
    description: "Template for tenant rights notification",
    category: "housing",
    content: "Housing rights letter template...",
    variables: ["tenant_name", "landlord_name", "property_address"],
    createdBy: "2",
    isPublic: true,
    createdAt: new Date("2024-01-12"),
    updatedAt: new Date("2024-01-12"),
  },
]

export const mockMessages: Message[] = [
  {
    id: "1",
    caseId: "1",
    senderId: "2",
    receiverId: "1",
    content: "Hi Maria, I've reviewed your documents. We need to schedule a meeting to discuss next steps.",
    read: false,
    createdAt: new Date("2024-01-25"),
  },
  {
    id: "2",
    caseId: "1",
    senderId: "1",
    receiverId: "2",
    content: "Thank you for the update. I'm available this week for a meeting.",
    read: true,
    createdAt: new Date("2024-01-25"),
  },
]

export const mockEvents: Event[] = [
  {
    id: "1",
    caseId: "1",
    userId: "1",
    type: "created",
    title: "Case Created",
    description: "Immigration status adjustment case opened",
    date: new Date("2024-01-20"),
    createdAt: new Date("2024-01-20"),
  },
  {
    id: "2",
    caseId: "1",
    userId: "2",
    type: "document_added",
    title: "Document Added",
    description: "I-485 application draft uploaded",
    date: new Date("2024-01-23"),
    createdAt: new Date("2024-01-23"),
  },
  {
    id: "3",
    caseId: "1",
    userId: "1",
    type: "deadline",
    title: "Application Deadline",
    description: "I-485 application must be submitted",
    date: new Date("2024-03-15"),
    createdAt: new Date("2024-01-20"),
  },
]

export const mockData = {
  users: mockUsers,
  organizations: mockOrganizations,
  cases: mockCases,
  documents: mockDocuments,
  templates: mockTemplates,
  messages: mockMessages,
  events: mockEvents,
}
