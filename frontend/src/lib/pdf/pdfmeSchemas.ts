import type { Template, Font, Schema } from "@pdfme/common";
import { BLANK_PDF } from "@pdfme/common";

// Optional: embed a TTF later by setting fonts.Roboto.data = ArrayBuffer
export const fonts: Record<string, Font> = {
  Roboto: {
    data: undefined,
    fallback: true,
  },
};

// Use a blank single-page PDF as the base until you export one from the Designer
export const basePdf = BLANK_PDF;

// Define your data schema fields
export const schema: Schema = {
  clientName: { type: "text" },
  caseNumber: { type: "text" },
  dateIssued: { type: "text" },
  bodyText: { type: "text" },
};

// Minimal template. Positions/styles will be set with the Designer UI later.
export const template: Template = {
  basePdf,
  schemas: [schema],
};
