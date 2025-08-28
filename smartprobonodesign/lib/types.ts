export interface User {
  id: string
  email: string
  name: string
  role: "client" | "attorney" | "admin" | "paralegal"
  organizationId?: string
  avatar?: string
  createdAt: Date
  updatedAt: Date
}

export interface Organization {
  id: string
  name: string
  type: "law_firm" | "legal_clinic" | "nonprofit"
  address?: string
  phone?: string
  email?: string
  website?: string
  createdAt: Date
}

export interface Case {
  id: string
  clientId: string
  attorneyId?: string
  title: string
  description: string
  category: "immigration" | "family" | "housing" | "employment" | "benefits" | "other"
  status: "intake" | "active" | "pending" | "completed" | "closed"
  priority: "low" | "medium" | "high" | "urgent"
  createdAt: Date
  updatedAt: Date
  dueDate?: Date
}

export interface Intake {
  id: string
  userId: string
  caseId?: string
  step: number
  totalSteps: number
  data: Record<string, any>
  completed: boolean
  createdAt: Date
  updatedAt: Date
}

export interface Document {
  id: string
  caseId?: string
  userId: string
  name: string
  type: "pdf" | "doc" | "docx" | "txt" | "image"
  size: number
  url: string
  tags: string[]
  version: number
  status: "draft" | "review" | "approved" | "signed"
  createdAt: Date
  updatedAt: Date
}

export interface Template {
  id: string
  name: string
  description: string
  category: string
  content: string
  variables: string[]
  createdBy: string
  isPublic: boolean
  createdAt: Date
  updatedAt: Date
}

export interface Message {
  id: string
  caseId: string
  senderId: string
  receiverId: string
  content: string
  attachments?: string[]
  read: boolean
  createdAt: Date
}

export interface Event {
  id: string
  caseId: string
  userId: string
  type: "created" | "updated" | "document_added" | "message_sent" | "deadline" | "meeting"
  title: string
  description?: string
  date: Date
  createdAt: Date
}

export interface ImmigrationCase extends Case {
  immigrationType: "asylum" | "family_reunification" | "work_visa" | "citizenship" | "other"
  country: string
  urgency: "routine" | "expedited" | "emergency"
  documents: {
    passport: boolean
    birthCertificate: boolean
    marriageCertificate: boolean
    workAuthorization: boolean
    other: string[]
  }
}

export type DemoRole = "client" | "attorney" | "admin" | "paralegal"
