/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './faq.html',
    './galerie.html',
    './sortiment.html',
    './admin/**/*.html',
    './faq/**/*.html',
    './sortiment/**/*.html',
    './pruvodce/**/*.html',
    './assets/js/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
