"use client"

import Link from "next/link"
import { Scale, Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { MainNav } from "./main-nav"
import { DemoRoleSelector } from "./demo-role-selector"
import { useAuth } from "@/lib/auth-context"

export function SiteHeader() {
  const { user } = useAuth()

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-20 items-center justify-between max-w-screen-xl">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <div className="flex items-center justify-center h-10 w-10 rounded-xl bg-primary/10">
              <Scale className="h-6 w-6 text-primary" />
            </div>
            <span className="font-serif font-bold text-2xl">SmartProBono</span>
          </Link>
          <div className="hidden md:flex">
            <MainNav />
          </div>
        </div>

        <div className="flex items-center gap-4">
          <DemoRoleSelector />

          {user ? (
            <div className="flex items-center gap-3">
              <span className="text-sm text-muted-foreground font-medium">Welcome, {user.name}</span>
              <Button variant="outline" size="sm" className="hover:bg-secondary transition-colors bg-transparent">
                Account
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Button variant="ghost" size="sm" className="hover:bg-secondary transition-colors" asChild>
                <Link href="/login">Sign In</Link>
              </Button>
              <Button
                size="sm"
                className="hover:scale-105 transition-all duration-200 shadow-sm hover:shadow-md"
                asChild
              >
                <Link href="/get-help">Get Help</Link>
              </Button>
            </div>
          )}

          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="sm" className="md:hidden hover:bg-secondary transition-colors">
                <Menu className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-80">
              <div className="flex flex-col space-y-6 mt-8">
                <MainNav />
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  )
}
