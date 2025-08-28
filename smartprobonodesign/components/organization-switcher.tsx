"use client"

import { useState } from "react"
import { Check, ChevronsUpDown, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { useAuth } from "@/lib/auth-context"
import { mockOrganizations } from "@/lib/mock-data"
import { cn } from "@/lib/utils"

export function OrganizationSwitcher() {
  const { user } = useAuth()
  const [open, setOpen] = useState(false)
  const [selectedOrg, setSelectedOrg] = useState(
    mockOrganizations.find((org) => org.id === user?.organizationId) || mockOrganizations[0],
  )

  // Only show for attorneys and admins who can have organizations
  if (!user || (user.role !== "attorney" && user.role !== "admin")) {
    return null
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          aria-label="Select organization"
          className="w-[200px] justify-between bg-transparent"
        >
          <span className="truncate">{selectedOrg?.name || "Select organization"}</span>
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search organizations..." />
          <CommandList>
            <CommandEmpty>No organizations found.</CommandEmpty>
            <CommandGroup heading="Organizations">
              {mockOrganizations.map((org) => (
                <CommandItem
                  key={org.id}
                  onSelect={() => {
                    setSelectedOrg(org)
                    setOpen(false)
                  }}
                  className="text-sm"
                >
                  <div className="flex flex-col">
                    <span>{org.name}</span>
                    <span className="text-xs text-muted-foreground capitalize">{org.type.replace("_", " ")}</span>
                  </div>
                  <Check className={cn("ml-auto h-4 w-4", selectedOrg?.id === org.id ? "opacity-100" : "opacity-0")} />
                </CommandItem>
              ))}
            </CommandGroup>
            <CommandSeparator />
            <CommandGroup>
              <CommandItem
                onSelect={() => {
                  setOpen(false)
                  // Handle create new organization
                }}
              >
                <Plus className="mr-2 h-4 w-4" />
                Create Organization
              </CommandItem>
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
