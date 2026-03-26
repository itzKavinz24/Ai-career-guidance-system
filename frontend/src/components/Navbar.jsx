import React from 'react';
import { NavLink } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/skills', label: 'Skills' },
  { to: '/quiz', label: 'Quiz' },
  { to: '/results', label: 'Results' },
];

const Navbar = () => {
  return (
    <header className="sticky top-0 z-30 border-b border-gray-200 bg-white/95 backdrop-blur shadow-sm">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50 text-blue-600 ring-1 ring-inset ring-blue-200">
            <span className="text-lg font-bold">AI</span>
          </div>
          <div className="flex flex-col">
            <span className="headline-display text-base font-bold tracking-tight text-gray-900">
              AI Career Guide
            </span>
            <span className="text-xs text-gray-500">AI-powered career insights</span>
          </div>
        </div>

        <div className="hidden sm:flex items-center gap-1 rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-xs text-gray-600 shadow-sm">
          <span className="inline-flex h-1.5 w-1.5 rounded-full bg-green-500" />
          <span>Interactive demo</span>
        </div>

        <ul className="flex items-center gap-1 text-sm font-medium">
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) =>
                  [
                    'inline-flex items-center rounded-md px-3 py-2 text-xs transition font-medium',
                    'hover:bg-blue-50 hover:text-blue-600',
                    isActive
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-600',
                  ].join(' ')
                }
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;
