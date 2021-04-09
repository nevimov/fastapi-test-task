import babel from '@rollup/plugin-babel'
import commonjs from '@rollup/plugin-commonjs'
import resolve from '@rollup/plugin-node-resolve'
import { terser } from 'rollup-plugin-terser'

const PRODUCTION = !process.env.ROLLUP_WATCH

const plugins = [
	resolve(),  // Allows Rollup to use code in node_modules/
	commonjs(),  // Converts CommonJS modules (majority of npm packages) to ES6
	babel({
		babelHelpers: 'bundled',
		exclude: ['./node_modules/**'],
	}),
	PRODUCTION && terser()
]

export default {
	input: './app/frontend/static/js/src/main.js',
	output: {
		name: 'main',
		file: './app/frontend/static/js/main.js',
		format: 'iife', // Suitable for <script> tags
		sourcemap: true,
	},
	plugins: plugins,
}
