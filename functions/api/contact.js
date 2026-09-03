import { handleContact } from '../../contact-handler.js';

export function onRequest(context) {
  return handleContact(context.request, context.env, context.waitUntil.bind(context));
}
