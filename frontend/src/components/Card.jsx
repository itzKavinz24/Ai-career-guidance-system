import React from 'react';

const Card = ({
  title,
  subtitle,
  description,
  match,
  trend,
  actionLabel,
  onAction,
  children,
}) => {
  return (
    <article className="bg-white rounded-xl shadow-md hover:shadow-lg hover:scale-105 transition-transform duration-300 border border-gray-200 flex h-full flex-col gap-3 p-5">
      <header className="flex items-start justify-between gap-3">
        <div className="space-y-1 flex-1">
          <h3 className="text-lg font-bold text-gray-900">
            {title}
          </h3>
          {subtitle && <p className="text-xs text-gray-500">{subtitle}</p>}
        </div>

        {typeof match === 'number' && (
          <div className="flex items-baseline gap-1 whitespace-nowrap">
            <span className="text-lg font-bold text-green-600">{match}%</span>
            <span className="text-xs font-medium text-gray-500">match</span>
          </div>
        )}
      </header>

      {description && <p className="text-sm leading-relaxed text-gray-600">{description}</p>}

      {children && <div className="mt-1 flex flex-wrap gap-1.5 text-xs text-gray-600">{children}</div>}

      {actionLabel && (
        <div className="mt-3 flex justify-end">
          <button type="button" className="btn-secondary text-sm" onClick={onAction}>
            {actionLabel}
          </button>
        </div>
      )}
    </article>
  );
};

export default Card;
