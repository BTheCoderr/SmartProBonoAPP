import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Button } from "@/components/ui/button"
import Link from "next/link"

const faqs = [
  {
    question: "Is SmartProBono really free?",
    answer:
      "Yes, SmartProBono is completely free for clients seeking legal help. Our attorneys volunteer their time to provide pro bono services. There are no hidden fees or charges.",
  },
  {
    question: "What types of legal issues do you help with?",
    answer:
      "We help with a wide range of civil legal matters including immigration, housing, family law, employment issues, benefits, consumer rights, and more. We do not handle criminal cases except for certain misdemeanors and expungement matters.",
  },
  {
    question: "How do I qualify for free legal help?",
    answer:
      "Qualification is based on income guidelines and the type of legal issue. Generally, we serve individuals and families with limited financial resources who cannot afford private attorneys. Complete our intake form to see if you qualify.",
  },
  {
    question: "How long does it take to get matched with an attorney?",
    answer:
      "Most clients are matched with an attorney within 3-5 business days. Complex cases or specialized legal areas may take longer. We'll keep you updated throughout the matching process.",
  },
  {
    question: "Can I choose my attorney?",
    answer:
      "While we use our expertise to match you with the best attorney for your case, you can request a different attorney if the initial match isn't working well. We want to ensure you're comfortable with your legal representation.",
  },
  {
    question: "Is my information secure and confidential?",
    answer:
      "Absolutely. All communications are protected by attorney-client privilege and our platform uses bank-level encryption. Your personal information is never shared without your consent.",
  },
  {
    question: "What if my case is too complex for pro bono help?",
    answer:
      "If your case requires resources beyond what pro bono services can provide, we'll help you understand your options and may refer you to reduced-fee programs or other resources.",
  },
  {
    question: "Can I get help if I don't speak English?",
    answer:
      "Yes, we work with attorneys who speak multiple languages and can provide interpretation services when needed. Language should never be a barrier to accessing legal help.",
  },
  {
    question: "What happens after my case is resolved?",
    answer:
      "After your case is completed, you'll have access to your case documents and can contact us if you have follow-up questions. We also provide resources for ongoing legal education and prevention.",
  },
  {
    question: "How can I support SmartProBono?",
    answer:
      "You can support our mission by donating, volunteering as an attorney, spreading awareness, or providing feedback to help us improve our services. Every contribution makes a difference.",
  },
]

export default function FAQPage() {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="py-20 lg:py-32 bg-gradient-to-b from-background to-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-6 max-w-3xl mx-auto">
            <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">Frequently Asked Questions</h1>
            <p className="text-muted-foreground text-lg md:text-xl">
              Find answers to common questions about SmartProBono and how we can help with your legal needs.
            </p>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 lg:py-32">
        <div className="container px-4 md:px-6">
          <div className="max-w-3xl mx-auto">
            <Accordion type="single" collapsible className="space-y-4">
              {faqs.map((faq, index) => (
                <AccordionItem key={index} value={`item-${index}`} className="border rounded-lg px-6">
                  <AccordionTrigger className="text-left font-semibold hover:no-underline">
                    {faq.question}
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground pt-2 pb-4">{faq.answer}</AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-20 lg:py-32 bg-muted/20">
        <div className="container px-4 md:px-6">
          <div className="text-center space-y-8">
            <div className="space-y-4 max-w-2xl mx-auto">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">Still Have Questions?</h2>
              <p className="text-muted-foreground text-lg">
                Can't find the answer you're looking for? Our team is here to help.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild className="text-lg px-8">
                <Link href="/contact">Contact Us</Link>
              </Button>
              <Button variant="outline" size="lg" asChild className="text-lg px-8 bg-transparent">
                <Link href="/get-help">Get Help Now</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
