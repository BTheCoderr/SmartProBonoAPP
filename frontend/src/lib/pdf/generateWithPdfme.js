import { generate } from "@pdfme/generator";
import { fonts, template as defaultTemplate } from "./pdfmeSchemas";

export async function generatePdfBuffer(data, template = defaultTemplate) {
  const pdfBytes = await generate({
    template,
    inputs: [data],
    options: { font: fonts },
  });
  return pdfBytes; // Uint8Array
}
