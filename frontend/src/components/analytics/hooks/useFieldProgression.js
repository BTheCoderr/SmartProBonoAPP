import { useMemo } from 'react';

export const useFieldProgression = (fieldInteractions) => {
  return useMemo(() => {
    const fields = Object.keys(fieldInteractions || {});
    const nodes = fields.map((field) => ({
      name: field,
      value: fieldInteractions[field]
    }));

    const links = fields.slice(0, -1).map((field, index) => ({
      source: field,
      target: fields[index + 1],
      value: Math.min(
        fieldInteractions[field],
        fieldInteractions[fields[index + 1]]
      )
    }));

    return { nodes, links };
  }, [fieldInteractions]);
}; 