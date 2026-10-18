// Merged estimator handler (from amy-electric-estimator worker).
// Wraps the bundled estimator code and routes its endpoints.
import estimatorBundle from './estimator-bundle.js';

export async function handleEstimatorRequest(request, env, ctx) {
  const url = new URL(request.url);
  const path = url.pathname;

  // Prefix estimator routes to avoid conflicts with main site
  // The estimator originally served at /, /download, /extract, /calculate
  // We map: /estimator -> /, /estimator/download -> /download, etc.
  // But for backward compat, also handle the original paths.

  // Rewrite the URL to the estimator's expected paths
  let estimatorPath = path;
  if (path.startsWith('/estimator')) {
    estimatorPath = path.replace('/estimator', '') || '/';
  }

  // Create a new request with the rewritten path
  const newUrl = new URL(request.url);
  newUrl.pathname = estimatorPath;
  const newRequest = new Request(newUrl.toString(), request);

  return estimatorBundle.fetch(newRequest, env, ctx);
}