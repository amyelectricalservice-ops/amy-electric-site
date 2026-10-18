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
			runWorkerFirst: true,
		},
		// No fetch triggers: the amyelectric.com zone routes belong to the
		// amy-electric-seo edge wrapper (see seo-worker/wrangler.jsonc). This
		// Worker is reached through that wrapper's ORIGIN service binding.
		env: {
			ASSETS: bindings.assets(),
			IMAGES: bindings.images(),
		},
	},
});
