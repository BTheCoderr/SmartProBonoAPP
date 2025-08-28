"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { useAuth } from "@/lib/auth-context"

const publicNavItems = [
  { href: "/", label: "Home" },
  { href: "/how-it-works", label: "How it Works" },
  { href: "/resources", label: "Resources" },
  { href: "/about", label: "About" },
  { href: "/contact", label: "Contact" },
]

const appNavItems = [
  { href: "/app", label: "Dashboard" },
  { href: "/app/cases", label: "Cases" },
  { href: "/app/documents", label: "Documents" },
  { href: "/app/immigration", label: "Immigration" },
]

const attorneyNavItems = [
  { href: "/attorney", label: "Attorney Portal" },
  { href: "/attorney/opportunities", label: "Opportunities" },
  { href: "/attorney/clients", label: "Clients" },
]

const adminNavItems = [
  { href: "/admin", label: "Admin" },
  { href: "/admin/users", label: "Users" },
  { href: "/admin/content", label: "Content" },
]

export function MainNav() {
  const pathname = usePathname()
  const { user, demoRole } = useAuth()

  const getNavItems = () => {
    if (!user) return publicNavItems

    switch (demoRole) {
      case "attorney":
        return [...appNavItems, ...attorneyNavItems]
      case "admin":
        return [...appNavItems, ...adminNavItems]
      case "paralegal":
        return [...appNavItems, { href: "/paralegal", label: "Paralegal" }]
      default:
        return appNavItems
    }
  }

  const navItems = getNavItems()

  return (
    <nav className="flex items-center space-x-6">
      {navItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={cn(
            "text-sm font-medium transition-colors hover:text-primary",
            pathname === item.href ? "text-foreground" : "text-muted-foreground",
          )}
        >
          {item.label}
        </Link>
      ))}
      {!user && (
        <Button asChild size="sm" className="ml-4">
          <Link href="/get-help">Get Help</Link>
        </Button>
      )}
    </nav>
  )
}
