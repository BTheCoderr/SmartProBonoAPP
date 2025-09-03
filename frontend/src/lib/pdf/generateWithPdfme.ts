import { generate } from "@pdfme/generator";
import type { Template } from "@pdfme/common";
import { fonts, template as defaultTemplate } from "./pdfmeSchemas";

export type PdfData = {
  clientName: string;
  caseNumber: string;
  dateIssued: string;
  bodyText: string;
};

export async function generatePdfBuffer(
  data: PdfData,
  template: Template = defaultTemplate
): Promise<Uint8Array> {
  const pdfBytes = await generate({
    template,
    inputs: [data],
    options: { font: fonts },
  });
  return pdfBytes; // Uint8Array
}
