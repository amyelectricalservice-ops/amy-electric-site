---
name: cf-cli
description: Cloud Foundry cf CLI v8 for pushing apps, managing services, routes, and orgs/spaces on a Cloud Foundry foundation. Use when the task involves cf login/target, cf push, services, routes, domains, scaling, env vars, logs, tasks, or ssh on Cloud Foundry. Not for Cloudflare — that is wrangler.
metadata:
  internal: true
---

# Cloud Foundry cf CLI

`cf` here is the **Cloud Foundry** command line tool (installed: v8.19.0), not anything Cloudflare.
This repo deploys to Cloudflare Workers via `wrangler` — never use `cf` for this repo's own deploys.
Load this skill when operating an app hosted on a Cloud Foundry foundation.

Your pre-trained knowledge of cf flags may be stale. For exact syntax, prefer `cf help <command>` / `cf <command> --help` output over memory.

## 0. Confirm the CLI and its target first

```bash
cf version        # expect cf version 8.x
cf target         # shows API endpoint, org, space — or "No API endpoint set"
```

If no endpoint is set, nothing else works until login:

```bash
cf api <API-ENDPOINT>          # e.g. https://api.run.pivotal.io (or your foundation's endpoint)
cf login -u <USER> -o <ORG> -s <SPACE>
cf target -o <ORG> -s <SPACE>  # switch org/space later
cf logout
```

Never invent an endpoint. If the user has not provided one, ask — do not guess foundation URLs.

## 1. App lifecycle (the commands that matter)

```bash
cf apps                                    # list apps in the targeted space
cf push [APP] [-f manifest.yml]            # push (restages on changes)
cf app <APP>                               # status, routes, usage
cf start|stop|restart|restage <APP>
cf scale <APP> [-i INSTANCES] [-m MEMORY] [-k DISK]
cf logs <APP> [--recent]                   # tail, or dump recent
cf env <APP>                               # staged/running env incl. VCAP_SERVICES
cf set-env <APP> <KEY> <VAL> && cf restage <APP>
cf events <APP>                            # crashes, scaling, staging history
cf ssh <APP>                               # shell into a running instance
cf run-task <APP> "<CMD>"                  # one-off task
```

## 2. Services

```bash
cf marketplace [-e SERVICE]                # plans available on this foundation
cf services                                # service instances in the space
cf create-service <OFFERING> <PLAN> <NAME>
cf bind-service <APP> <NAME> && cf restage <APP>
cf unbind-service <APP> <NAME>
cf service-keys <NAME> / cf service-key <NAME> <KEY>
```

## 3. Routes and domains

```bash
cf routes                                  # routes in the space
cf create-route <DOMAIN> --hostname <HOST>
cf map-route <APP> <DOMAIN> --hostname <HOST>
cf unmap-route <APP> <DOMAIN> --hostname <HOST>
cf domains
```

## 4. Safety rules

- `cf push`, `restage`, `scale`, `set-env`, service bind/unbind, and route mapping change a
  **live foundation**. Confirm app name, org, and space from `cf target` output before mutating.
- `cf delete <APP> -r` deletes routes too — never pass `-r` unless asked.
- Credentials: prefer `cf set-env` over baking secrets into `manifest.yml`; never commit secrets.
- If a command fails with an API error, re-run `cf target` — expired tokens are the common cause, fix with `cf login`.
