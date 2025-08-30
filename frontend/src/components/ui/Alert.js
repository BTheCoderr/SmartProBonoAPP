import React from 'react';

const Alert = ({ children, className, ...props }) => (
  <div
    className={`relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground ${className || ''}`}
    {...props}
  >
    {children}
  </div>
);

const AlertDescription = ({ children, className, ...props }) => (
  <div className={`text-sm [&_p]:leading-relaxed ${className || ''}`} {...props}>
    {children}
  </div>
);

export { Alert, AlertDescription };
