import { bindings, defineConfig } from "cf/config";

export default defineConfig({
	worker: {
		name: "amy-electric-site",
		compatibilityDate: "2026-10-14",
		compatibilityFlags: [
			"nodejs_compat",
		],
		entrypoint: "worker.js",
		workersDev: true,
		observability: {
			enabled: true,
			logs: {
				headSamplingRate: 1,
			},
		},
		assets: {
			htmlHandling: "auto-trailing-slash",
			notFoundHandling: "404-page",
			runWorkerFirst: ["/*", "!/css/*", "!/js/*", "!/fonts/*"],
		},
		// The zone route (`amyelectric.com/*`) is declared in wrangler.jsonc, the
		// live config. This mirror is validation-only and does not express zone
		// routes; keep the two files in step by hand.
		env: {
			ASSETS: bindings.assets(),
			IMAGES: bindings.images(),
		},
	},
});
