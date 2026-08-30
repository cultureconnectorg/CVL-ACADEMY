// Flat ESLint config (ESLint 9) for CVLN Academy frontend.
//
// react-scripts (CRA) still lints inline during `craco start`/`build` via its
// own bundled legacy config — this file is the standalone, CI-runnable check
// (`npx eslint src`) using the plugins already declared in package.json, so
// lint issues are catchable without spinning up the whole webpack dev build.
const js = require("@eslint/js");
const globals = require("globals");
const react = require("eslint-plugin-react");
const reactHooks = require("eslint-plugin-react-hooks");
const jsxA11y = require("eslint-plugin-jsx-a11y");
const importPlugin = require("eslint-plugin-import");

module.exports = [
  js.configs.recommended,
  {
    files: ["src/**/*.{js,jsx}"],
    plugins: {
      react,
      "react-hooks": reactHooks,
      "jsx-a11y": jsxA11y,
      import: importPlugin,
    },
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "module",
      parserOptions: {
        ecmaFeatures: { jsx: true },
      },
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2021,
      },
    },
    settings: {
      react: { version: "detect" },
    },
    rules: {
      ...react.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
      ...jsxA11y.configs.recommended.rules,
      "react/react-in-jsx-scope": "off", // React 19 automatic JSX runtime
      "react/prop-types": "off", // no PropTypes convention in this codebase
      "no-unused-vars": ["warn", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
    },
  },
  {
    // shadcn/ui generated primitives: thin, content-less wrappers around
    // Radix/cmdk that always forward `{...props}`/children from the caller.
    // The a11y "no content" rules and cmdk's own data-attribute convention
    // don't apply to a reusable primitive with no content of its own.
    files: ["src/components/ui/**/*.jsx"],
    rules: {
      "jsx-a11y/heading-has-content": "off",
      "jsx-a11y/anchor-has-content": "off",
      "react/no-unknown-property": "off",
    },
  },
  {
    ignores: ["build/**", "node_modules/**", "public/**", "plugins/**"],
  },
];
