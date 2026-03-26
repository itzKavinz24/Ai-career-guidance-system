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
    <header className="sticky top-0 z-30 border-b border-indigo-100/60 bg-gradient-to-r from-white/90 via-blue-50/85 to-teal-50/80 backdrop-blur-xl shadow-[0_10px_30px_rgba(43,72,156,0.12)]">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-100 via-indigo-100 to-teal-100 text-blue-700 ring-1 ring-inset ring-blue-200/70 shadow-sm">
            <span className="text-lg font-bold">AI</span>
          </div>
          <div className="flex flex-col">
            <span className="headline-display text-base font-bold tracking-tight text-gray-900">
              AI Career Guide
            </span>
            <span className="text-xs text-gray-500">AI-powered career insights</span>
          </div>
        </div>

        <div className="hidden sm:flex items-center gap-1 rounded-full border border-teal-200/70 bg-white/70 px-3 py-1 text-xs text-slate-700 shadow-sm backdrop-blur">
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
                    'inline-flex items-center rounded-lg px-3 py-2 text-xs transition-all duration-300 font-semibold',
                    'hover:-translate-y-0.5 hover:bg-white/90 hover:text-blue-700 hover:shadow-sm',
                    isActive
                      ? 'bg-white text-blue-700 shadow-sm ring-1 ring-blue-200/60'
                      : 'text-slate-600',
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
