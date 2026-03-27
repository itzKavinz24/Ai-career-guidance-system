import React, { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/skills', label: 'Skills' },
  { to: '/quiz', label: 'Quiz' },
  { to: '/results', label: 'Results' },
];

const Navbar = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const storedTheme = window.localStorage.getItem('theme-mode');
    const preferDark = mediaQuery.matches;
    const shouldUseDark = storedTheme ? storedTheme === 'dark' : preferDark;

    setIsDarkMode(shouldUseDark);
    document.documentElement.classList.toggle('theme-dark', shouldUseDark);

    const handleSystemThemeChange = (event) => {
      const savedTheme = window.localStorage.getItem('theme-mode');
      if (savedTheme) {
        return;
      }

      setIsDarkMode(event.matches);
      document.documentElement.classList.toggle('theme-dark', event.matches);
    };

    mediaQuery.addEventListener('change', handleSystemThemeChange);
    return () => {
      mediaQuery.removeEventListener('change', handleSystemThemeChange);
    };
  }, []);

  const toggleDarkMode = () => {
    const nextValue = !isDarkMode;
    setIsDarkMode(nextValue);
    document.documentElement.classList.toggle('theme-dark', nextValue);
    window.localStorage.setItem('theme-mode', nextValue ? 'dark' : 'light');
  };

  return (
    <header
      className={[
        'sticky top-0 z-30 border-b backdrop-blur-xl',
        isDarkMode
          ? 'border-blue-900/60 bg-gradient-to-r from-[#0d1729]/90 via-[#10203a]/85 to-[#0b2230]/80 shadow-[0_10px_30px_rgba(0,0,0,0.45)]'
          : 'border-indigo-100/60 bg-gradient-to-r from-white/90 via-blue-50/85 to-teal-50/80 shadow-[0_10px_30px_rgba(43,72,156,0.12)]',
      ].join(' ')}
    >
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div
            className={[
              'flex h-10 w-10 items-center justify-center rounded-xl ring-1 ring-inset shadow-sm',
              isDarkMode
                ? 'bg-gradient-to-br from-blue-900/70 via-indigo-900/70 to-teal-900/70 text-blue-200 ring-blue-700/60'
                : 'bg-gradient-to-br from-blue-100 via-indigo-100 to-teal-100 text-blue-700 ring-blue-200/70',
            ].join(' ')}
          >
            <span className="text-lg font-bold">AI</span>
          </div>
          <div className="flex flex-col">
            <span
              className={[
                'headline-display text-base font-bold tracking-tight',
                isDarkMode ? 'text-slate-100' : 'text-gray-900',
              ].join(' ')}
            >
              AI Career Guide
            </span>
            <span className={['text-xs', isDarkMode ? 'text-slate-400' : 'text-gray-500'].join(' ')}>
              AI-powered career insights
            </span>
          </div>
        </div>

        <div
          className={[
            'hidden sm:flex items-center gap-1 rounded-full border px-3 py-1 text-xs shadow-sm backdrop-blur',
            isDarkMode
              ? 'border-blue-800/70 bg-slate-900/50 text-slate-300'
              : 'border-teal-200/70 bg-white/70 text-slate-700',
          ].join(' ')}
        >
          <span className="inline-flex h-1.5 w-1.5 rounded-full bg-green-500" />
          <span>Interactive demo</span>
        </div>

        <ul className="flex items-center gap-1 text-sm font-medium">
          <li>
            <button
              type="button"
              onClick={toggleDarkMode}
              className={[
                'inline-flex items-center gap-2 rounded-lg px-3 py-2 text-xs font-semibold transition-all duration-300 hover:-translate-y-0.5 hover:shadow-sm',
                isDarkMode
                  ? 'text-slate-300 hover:bg-slate-800/80 hover:text-blue-200'
                  : 'text-slate-600 hover:bg-white/90 hover:text-blue-700',
              ].join(' ')}
              aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
              title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDarkMode ? (
                <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" aria-hidden="true">
                  <circle cx="12" cy="12" r="4" stroke="currentColor" strokeWidth="1.8" />
                  <path d="M12 2V5M12 19V22M4.93 4.93L7.05 7.05M16.95 16.95L19.07 19.07M2 12H5M19 12H22M4.93 19.07L7.05 16.95M16.95 7.05L19.07 4.93" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                </svg>
              ) : (
                <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" aria-hidden="true">
                  <path d="M21 13.2A9 9 0 1 1 10.8 3 7 7 0 0 0 21 13.2Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
              <span>{isDarkMode ? 'Light' : 'Dark'}</span>
            </button>
          </li>
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                className={({ isActive }) =>
                  [
                    'inline-flex items-center rounded-lg px-3 py-2 text-xs transition-all duration-300 font-semibold',
                    isDarkMode
                      ? 'hover:-translate-y-0.5 hover:bg-slate-800/85 hover:text-blue-200 hover:shadow-sm'
                      : 'hover:-translate-y-0.5 hover:bg-white/90 hover:text-blue-700 hover:shadow-sm',
                    isActive
                      ? isDarkMode
                        ? 'bg-slate-900/80 text-blue-200 shadow-sm ring-1 ring-blue-700/60'
                        : 'bg-white text-blue-700 shadow-sm ring-1 ring-blue-200/60'
                      : isDarkMode
                        ? 'text-slate-300'
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
