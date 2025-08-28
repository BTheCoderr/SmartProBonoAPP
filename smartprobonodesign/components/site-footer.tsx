import Link from "next/link"
import { Scale } from "lucide-react"

export function SiteFooter() {
  return (
    <footer className="border-t bg-background">
      <div className="container py-8 md:py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Scale className="h-5 w-5 text-primary" />
              <span className="font-bold">SmartProBono</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Connecting people with legal help through technology and compassion.
            </p>
          </div>

          <div className="space-y-4">
            <h4 className="text-sm font-semibold">Get Help</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/get-help" className="text-muted-foreground hover:text-foreground">
                  Start Here
                </Link>
              </li>
              <li>
                <Link href="/how-it-works" className="text-muted-foreground hover:text-foreground">
                  How it Works
                </Link>
              </li>
              <li>
                <Link href="/resources" className="text-muted-foreground hover:text-foreground">
                  Resources
                </Link>
              </li>
              <li>
                <Link href="/faq" className="text-muted-foreground hover:text-foreground">
                  FAQ
                </Link>
              </li>
            </ul>
          </div>

          <div className="space-y-4">
            <h4 className="text-sm font-semibold">For Attorneys</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/attorney" className="text-muted-foreground hover:text-foreground">
                  Attorney Portal
                </Link>
              </li>
              <li>
                <Link href="/volunteer" className="text-muted-foreground hover:text-foreground">
                  Volunteer
                </Link>
              </li>
              <li>
                <Link href="/training" className="text-muted-foreground hover:text-foreground">
                  Training
                </Link>
              </li>
            </ul>
          </div>

          <div className="space-y-4">
            <h4 className="text-sm font-semibold">Organization</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="/about" className="text-muted-foreground hover:text-foreground">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-muted-foreground hover:text-foreground">
                  Contact
                </Link>
              </li>
              <li>
                <Link href="/donate" className="text-muted-foreground hover:text-foreground">
                  Donate
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-muted-foreground hover:text-foreground">
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t mt-8 pt-8 text-center text-sm text-muted-foreground">
          <p>&copy; 2024 SmartProBono. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}
