/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        'black-dark': '#00000050',
        'dull-white': '#FFFFFFB3',
        'white-light': '#FFFFFF30',
        'white-medium': '#FFFFFF40',
        'neon-blue': '#2FB8FF',
      },
      fontFamily: {
        'nunito': ['nunito', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
