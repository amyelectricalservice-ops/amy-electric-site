import { bindings, defineConfig, triggers } from "cf/config";

/**
 * This migration needs manual work. Resolve every TODO in this file, then remove the error below.
 */
/**
 * TODO(@cloudflare): cf migrate: An ancestor package.json was found, but it was not modified because it may belong to another project. Install `cf@latest` as dev dependencies in the package that owns this Worker.
 */
/**
 * TODO(@cloudflare): cf migrate: The generated wrangler.config.ts requires Wrangler 4.136.0 or newer. Add `wrangler@latest` to the package that owns this Worker and update its lockfile.
 */
throw new Error("Migration incomplete. Resolve every cf migrate TODO in `cloudflare.config.ts`.");

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
