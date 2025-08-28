import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"
import { FileText, ExternalLink, Download, BookOpen } from "lucide-react"

const resourceCategories = [
  {
    title: "Immigration Resources",
    description: "Forms, guides, and information for immigration matters",
    resources: [
      { name: "I-485 Application Guide", type: "PDF", description: "Step-by-step guide for adjustment of status" },
      { name: "Asylum Application Checklist", type: "PDF", description: "Complete checklist for asylum seekers" },
      { name: "Family Reunification Guide", type: "PDF", description: "How to petition for family members" },
      { name: "DACA Renewal Guide", type: "PDF", description: "Instructions for DACA renewal applications" },
    ],
  },
  {
    title: "Housing Rights",
    description: "Know your rights as a tenant and homeowner",
    resources: [
      {
        name: "Tenant Rights Handbook",
        type: "PDF",
        description: "Complete guide to tenant rights and responsibilities",
      },
      { name: "Eviction Defense Guide", type: "PDF", description: "How to respond to eviction notices" },
      {
        name: "Housing Discrimination Guide",
        type: "PDF",
        description: "Recognizing and reporting housing discrimination",
      },
      { name: "Security Deposit Rights", type: "PDF", description: "Understanding security deposit laws" },
    ],
  },
  {
    title: "Family Law",
    description: "Resources for family legal matters",
    resources: [
      { name: "Divorce Process Guide", type: "PDF", description: "Understanding the divorce process" },
      { name: "Child Custody Basics", type: "PDF", description: "Child custody laws and procedures" },
      { name: "Domestic Violence Resources", type: "PDF", description: "Safety planning and legal protections" },
      { name: "Name Change Guide", type: "PDF", description: "How to legally change your name" },
    ],
  },
  {
    title: "Employment Rights",
    description: "Workplace rights and protections",
    resources: [
      { name: "Wage Theft Guide", type: "PDF", description: "What to do if your wages are stolen" },
      { name: "Workplace Discrimination", type: "PDF", description: "Understanding workplace discrimination laws" },
      { name: "Unemployment Benefits Guide", type: "PDF", description: "How to apply for unemployment benefits" },
      { name: "Workers' Rights Handbook", type: "PDF", description: "Comprehensive guide to worker protections" },
    ],
  },
]

const legalAidOrganizations = [
  {
    name: "Legal Aid Society",
    description: "Provides free legal services to low-income individuals",
    website: "https://legalaid.org",
    phone: "1-800-LEGAL-AID",
  },
  {
    name: "National Immigration Law Center",
    description: "Immigration law resources and advocacy",
    website: "https://nilc.org",
    phone: "1-213-639-3900",
  },
  {
    name: "National Housing Law Project",
    description: "Housing rights advocacy and resources",
    website: "https://nhlp.org",
    phone: "1-415-546-7000",
  },
  {
    name: "National Employment Law Project",
    description: "Workers' rights advocacy and resources",
    website: "https://nelp.org",
    phone: "1-212-285-3025",
  },
]

export default function ResourcesPage() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="py-20 lg:py-32 bg-gradient-to-b from-background to-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-6 max-w-3xl mx-auto">
            <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Legal Resources</h1>
            <p className="text-muted-foreground text-lg md:text-xl">
              Access free legal guides, forms, and educational materials to help you understand your rights and navigate
              legal processes.
            </p>
          </div>
        </div>
      </section>

      {/* Resources Section */}
      <section className="py-20 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="space-y-16">
            {resourceCategories.map((category, index) => (
              <div key={index} className="space-y-8">
                <div className="text-center space-y-4">
                  <h2 className="text-3xl font-bold tracking-tighter">{category.title}</h2>
                  <p className="text-muted-foreground text-lg max-w-2xl mx-auto">{category.description}</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {category.resources.map((resource, resourceIndex) => (
                    <Card key={resourceIndex} className="hover:shadow-md transition-shadow">
                      <CardHeader>
                        <div className="flex items-start justify-between">
                          <div className="flex items-center gap-3">
                            <FileText className="h-6 w-6 text-primary" />
                            <div>
                              <CardTitle className="text-lg">{resource.name}</CardTitle>
                              <Badge variant="secondary" className="mt-1">
                                {resource.type}
                              </Badge>
                            </div>
                          </div>
                          <Button size="sm" variant="ghost">
                            <Download className="h-4 w-4" />
                          </Button>
                        </div>
                        <CardDescription>{resource.description}</CardDescription>
                      </CardHeader>
                    </Card>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Legal Aid Organizations */}
      <section className="py-20 lg:py-32 bg-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Legal Aid Organizations</h2>
            <p className="mx-auto max-w-[700px] text-muted-foreground text-lg">
              Additional organizations that provide free legal services and resources.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {legalAidOrganizations.map((org, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg">{org.name}</CardTitle>
                      <CardDescription className="mt-2">{org.description}</CardDescription>
                    </div>
                    <Button size="sm" variant="ghost" asChild>
                      <a href={org.website} target="_blank" rel="noopener noreferrer">
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm text-muted-foreground">
                    <p>Phone: {org.phone}</p>
                    <p>Website: {org.website}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-8">
            <div className="space-y-4 max-w-2xl mx-auto">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Need Personal Legal Help?</h2>
              <p className="text-muted-foreground text-lg">
                While these resources are helpful, nothing replaces personalized legal advice from a qualified attorney.
              </p>
            </div>
            <Button size="lg" asChild className="text-lg px-8">
              <Link href="/get-help">
                Get Matched with an Attorney <BookOpen className="ml-2 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
