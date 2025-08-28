"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import type { User, DemoRole } from "./types"
import { mockUsers } from "./mock-data"

interface AuthContextType {
  user: User | null
  demoRole: DemoRole
  setDemoRole: (role: DemoRole) => void
  login: (email: string, password: string) => Promise<boolean>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [demoRole, setDemoRole] = useState<DemoRole>("client")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate loading and set demo user based on role
    const timer = setTimeout(() => {
      const demoUser = mockUsers.find((u) => u.role === demoRole)
      setUser(demoUser || null)
      setIsLoading(false)
    }, 500)

    return () => clearTimeout(timer)
  }, [demoRole])

  const login = async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true)
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))

    const foundUser = mockUsers.find((u) => u.email === email)
    if (foundUser) {
      setUser(foundUser)
      setDemoRole(foundUser.role)
      setIsLoading(false)
      return true
    }

    setIsLoading(false)
    return false
  }

  const logout = () => {
    setUser(null)
    setDemoRole("client")
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        demoRole,
        setDemoRole,
        login,
        logout,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}

export { AuthContext }
