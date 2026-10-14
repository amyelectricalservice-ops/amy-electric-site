import { bindings, defineConfig, triggers } from "cf/config";

export default defineConfig({
	worker: {
		name: "amy-electric-site",
		compatibilityDate: "2026-05-21",
		compatibilityFlags: [
			"nodejs_compat",
		],
		entrypoint: "worker.js",
		workersDev: true,
		observability: {
			enabled: true,
		},
		assets: {
			htmlHandling: "auto-trailing-slash",
			notFoundHandling: "404-page",
			runWorkerFirst: true,
		},
		triggers: [
			triggers.fetch({
				pattern: "amyelectric.com/*",
				zone: "amyelectric.com",
			}),
			triggers.fetch({
				pattern: "www.amyelectric.com/*",
				zone: "amyelectric.com",
			}),
		],
		env: {
			ASSETS: bindings.assets(),
		},
	},
});
