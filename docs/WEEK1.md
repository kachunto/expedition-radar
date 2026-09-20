# Week 1 guide: foundations

Goal by the end of the week: the app is live on a real URL, CI is green, you know exactly how many items "complete" means for the Prologue and Act 1, and five testers have a name. About 6 to 8 hours in total. Everything costs nothing so far.

## Day 1: get the repo onto GitHub and CI green (about 1 hour, you)
1. Create a free GitHub account if you do not have one, then a new **public** repository named `expedition-radar`. Leave "Add a README" and other options off. It is public so testers can file reports and so the free host can build it.
2. In a terminal, in the folder with these files, run:
   `git remote add origin https://github.com/YOUR-NAME/expedition-radar.git` then `git push -u origin main`.
   If you do not want to use a terminal, use GitHub's "uploading an existing file" page instead; you lose the commit history but nothing else.
3. Edit `config/site.json`: replace `OWNER` in `repo_url` with your GitHub name, commit, push.
4. Open the repo's **Actions** tab. The CI run should be green (tests, validation, build).
Done when: CI is green and the "Report a problem" links in the built app point at your repo.

## Day 2: the area map and the real target count (about 2 to 3 hours, together)
The map lists every place in the Prologue and Act 1 with a spoiler-free name and the act it belongs to. Bulk items (pictos, weapons, outfits, flags) inherit their spoiler labels from it, and it tells us how many items "complete" means.
1. Tell me "start the area map". I will read at least two guides, draft `content/area-map.json`, and count the items per category for the two acts.
2. You review the draft: spoiler-free names only, nothing that hints at later story. Anything you are unsure about, we mark more severe.
Done when: the map is committed and we have a target number per category.

## Day 3: deploy (about 1 hour, you)
1. Create a free Cloudflare account. Go to Workers and Pages, create a Pages project, and connect your GitHub repo.
2. Build command: `python3 scripts/build.py`. Output directory: `dist`. If the build complains about Python, tell me the message and I will adjust.
3. In the Pages project, enable Web Analytics (cookie-free page-view counts, no banner needed).
4. Open the `pages.dev` address on your phone: tick items, switch story point, open a hint.
Done when: you can use the live app on your phone. A custom domain is optional for the MVP.

## Day 4: legal, testers and the API key (about 1 to 2 hours, you)
1. Fill every FILL_IN marker in `src/legal.html` (name, address, e-mail, hosting, statistics). Ask your tax adviser or a lawyer to glance at it before you share the link beyond your testers. The build prints a reminder while markers remain.
2. Write down five names: people who are playing or about to play Clair Obscur. Send the link to the first two once step 1 is done.
3. In the Anthropic Console, create an API key for the pipeline and set a monthly spend limit (I suggest 50 EUR to start; that is my rough guess, not a quote). Keep the key in a local `.env` file, which git ignores. Never paste it into a chat or commit it.
Done when: the legal page is filled in, five names are written down, and the key exists with a limit.

## Keep a log
Add one or two lines to `docs/learning-log.md` each week: where the AI got stuck or was wrong.

## Not this week
The extraction pipeline (week 2), sign-in and votes (weeks 4 to 5), a custom domain, self-hosted fonts, Act 2 content.
