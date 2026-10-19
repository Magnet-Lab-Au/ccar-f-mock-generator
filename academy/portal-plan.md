# Draft plan section for the portal, and the start note for the build session

- Date: 19 October 2026
- Status: draft. The owner reads it. The build session in `~/magnetlab-academy` copies Part A into the portal's `PLAN.md` in the plan pull request.
- Source: academy decisions 0050 to 0057 in `academy/decisions/` of the repository `Magnet-Lab-Au/ccar-f-mock-generator`. An independent agent reviewed the first draft against the portal files and the decisions, and its 15 points are fixed in this text.

Part A is the text for the portal's `PLAN.md`, in the form of its other sections. Part B is the start note for the session that does the work in the portal.

---

## Part A. The section for the portal's `PLAN.md`

## Post-MVP 1 - Mocks version 2 and the two exam guide pages

**Source of the decisions:** academy decisions 0050 to 0057 in the public repository `Magnet-Lab-Au/ccar-f-mock-generator` (folder `academy/decisions/`). This section does not redesign them. `PORTAL DESIGN.md` line 132 lists "the full exam guide hosted with better breakdowns" as post-MVP, and this section starts that item. The line "Post-MVP items (Study Pack, exam guide, …) are out" under "Decisions I am not making" changes to: "The exam guide pages are in Post-MVP 1. The other post-MVP items are out."

Where the decisions are silent, the default is written here and marked **(default)**, as in the rest of this plan.

### Flags (portal rule "Stack discipline")

1. **New package `@fontsource/ibm-plex-mono`** (decision 0053). The pages show code and file names in IBM Plex Mono. It loads in `frontend/src/main.tsx` in the same way as Sora, and it goes into `TOOLING.md`.
2. **Built pages from another repository** (decisions 0050 and 0051). The two pages are built in `ccar-f-mock-generator` and copied into the portal by a script. The portal does not build them. Each copied file says so at the top.
3. **Raw HTML in a React page** (decision 0051). The page body comes from our own committed files, not from a user, and is set with `dangerouslySetInnerHTML` **(default)**. The security policy in `frontend/public/_headers` does not change **(default)**.
4. **The copy script runs with plain `node`** (an `.mjs` file), so the frontend needs no new tool **(default)**.

### Decided in academy decision 0055, listed for the record

1. **Version 2 is the default.** The mocks of version 2 load as `mock-N.v2.json`, next to the v1 files, which do not change. The rule "newest version" (`learning-service.ts` line 282) makes version 2 the default. Nobody attempted version 1, so no announcement is needed.
2. **One fixed mix of the options.** The options of each version 2 question are mixed once, so that each letter is correct about equally often. A new order on each attempt is later work.

## Plan PR - this section

Branch: `chore/plan-post-mvp-1`. This section only. Its merge is the approval.

## PR 4 - Mocks version 2

Branch: `feature/mocks-v2`

1. **Four or five options (A to E).** Search for each place that fixes A to D or four options, and change it. Known places:
   - `backend/src/content/schema.ts`: `OPTION_KEYS` (line 4), `options` as the strict object A to D (line 18) and `answer` as an enum of `OPTION_KEYS` (line 19). The new schema accepts the keys A to D, or A to E. It checks that each letter of `answer` and of `distractor_explanations` is a key of the question's own options. The check "each wrong option has one explanation" (lines 30 to 39) uses the question's own options, not a fixed list.
   - `backend/src/services/learning-service.ts`: `OPTION_LETTERS` (line 18), and the check of a selection (lines 463 to 466), which must use the item's own option keys. Its error text "Choose from options A to D" changes.
   - `backend/src/learning/download.ts`: `LETTERS` (line 31).
   - `frontend/src/components/learning/ItemBody.tsx` (`LETTERS`, and the comment "the four options") and `Explanation.tsx` (`LETTERS`).
   - `frontend/e2e/learning-fake.ts` (line 31).
   - No question of version 1 changes.
2. **Two new optional columns on `MockItem`** (migration, expand only): `point` (for example "2.5-K3") and `question_id` (for example "M1-S01-T1"). The item schema accepts both as optional. The loader stores them. `publicItem` (`learning-service.ts` lines 30 to 42) and the frontend type `AttemptItem` carry `point`, for the link of PR 5. The admin item page (`AdminItemPage.tsx`) shows `question_id` next to the item number **(default)**, so that a report leads to the question in `ccar-f-mock-generator`.
3. **The converter:** a path for version 2 in `backend/scripts/prepare-content.ts` (decision 0055, item 9), chosen by an argument. Without the argument, the script does what it does today (version 1, fixed at line 50). With the argument, it writes only the version 2 files and the letter maps, and it does not run the version 1 path. It runs once on a computer, and its output is committed. The DigitalOcean build sees only `/backend` and does not fetch from GitHub.
   - For each mock N from 1 to 5, it reads `mocks/mock-0N.questions.json` and `mocks/mock-0N.answers.json`, and `reference/guide-records.json`, from GitHub at the tag `mocks-v2` (`https://raw.githubusercontent.com/Magnet-Lab-Au/ccar-f-mock-generator/mocks-v2/<path>`).
   - It writes `backend/content/ccar-f/mock-N.v2.json`.
   - It writes the letter map to `backend/content-maps/ccar-f/mock-N.v2.letters.json`, outside `backend/content/`, because the loader reads every `*.json` under `backend/content/` and one level of subfolders (`backend/src/content/load.ts` lines 9 to 15) and would refuse the map. The map has one entry for each question: `question_id`, and for each option its letter in the source and its letter in the portal.
   - Field by field:
     - `course` "ccar-f", `course_name` "CCAR-F", `mock` N, `version` 2, `minutes` from the file (120).
     - `difficulty`: "Full mock" for mocks 1 to 4, "Review mock" for mock 5.
     - `timing_note`: empty for mocks 1 to 4. For mock 5: "Most questions revisit a problem of mocks 1 to 4 in a new setting, so take it after them."
     - `items`: one item for each question, in the order of `number` (1 to 60).
     - `n` = `number`. `scenario`, `scenario_name` and `scenario_blurb` = the `scenario`, `name` and `story` of the question's group.
     - `task_statement` = the question's own `task_statement` (for example "2.5"), then " — " (an em dash), then the title of that task statement from `reference/guide-records.json`. The titles are 42 to 87 characters, under the limit of 300.
     - `stem` = `question`. If `select` is 2, add " Select TWO." at the end.
     - The mix: for each question, first choose the letter of the correct option so that the letters stay balanced, then mix the other options with a fixed seed **(default)**. The targets: in the 260 questions with 4 options, each of A to D is correct 65 times. In the 40 questions with 5 options, the 80 correct options fall 16 times on each of A to E.
     - `options` = the mixed options. Each option keeps its text and its reason. `answer` = the new letters of the correct options.
     - `explanation` = the reason of the correct option, word for word. For two correct options: "B: <reason> C: <reason>", in the order of the new letters.
     - `distractor_explanations` = the reason of each wrong option, word for word, under its new letter.
     - `trap` = null. `point` and `question_id` = from the question.
4. **Tests.** These tests assume only the v1 files, or one paper for each mock, and must name the version that they test: `content-files.test.ts` (also line 26, "two-answer items only in Mock 5"), `content-load.test.ts` (line 46 makes a fake v2 of mock 1, which now clashes with the real v2), `content-schema.test.ts` (line 12, and line 77 that refuses `answer: ['E']`), `learning.test.ts` (lines 10 to 16, "Mock 5 (ten two-answer items)") and `learning-admin.test.ts`. New tests **(default)**: a 5-option item loads and scores; a 4-option item refuses an `E` in `answer` and in a selection; the converter output passes the schema; each reason stays with its option text; the counts of correct letters meet the targets of item 3.

**PR 4 checklist:**
- [ ] Load script run twice: 5 new versions, 300 items, second run changes nothing
- [ ] A participant starts mock 1 and gets version 2
- [ ] A 5-option question shows A to E in exam and in practice mode, and E can be chosen
- [ ] A two-answer question ends with "Select TWO." and scores all or nothing
- [ ] The answer review shows the reason of each option, also for E, under the right letter
- [ ] The download file shows 5 options where a question has 5
- [ ] Mock 5 shows "Review mock" and its timing note. Mocks 1 to 4 show "Full mock"
- [ ] Each version 2 item has `point` and `question_id`, and the admin item page shows `question_id`
- [ ] Version 1 files and their hashes are unchanged

## PR 5 - The two exam guide pages

Branch: `feature/exam-guide-pages`. It waits for the portal form of the pages from `ccar-f-mock-generator` (see "Needs from `ccar-f-mock-generator` before PR 5").

1. **Font.** Add `@fontsource/ibm-plex-mono` (flag 1), and add it to `TOOLING.md`.
2. **The copy script** `frontend/scripts/copy-academy-pages.mjs` **(default)**. It runs once on a computer, and its output is committed, because the Cloudflare Pages build (root `frontend`, `npm run build`) does not fetch from GitHub. It takes the portal form of the two pages from GitHub at a tag of `ccar-f-mock-generator`. It writes the code, data and styles into `frontend/src/academy/`, the images into `frontend/public/academy/` (the security policy allows images only from the portal itself), and the tag name into `frontend/src/academy/SOURCE.txt`. It stops if a file there differs from the last copy, so that no change made in the portal is lost (decision 0050).
3. **One React page for each tab**, in `frontend/src/pages/`: `ExamGuideBreakdownPage.tsx` at `/exam-guide-breakdown` and `BehindTheMocksPage.tsx` at `/behind-the-mocks`, inside `SectionRoute slug="learning"` in `App.tsx`, and with `AuthenticatedLayout`, as `MocksPage` is. Each page sets the built body, then starts the page script on that element, and removes it again when the page closes. React StrictMode runs this twice in development, so start and stop must be safe to run twice. Each page is a lazy chunk **(default)**, because tab 1 has about 700 KB of HTML and 450 KB of data.
4. **Sidebar.** Two entries in `frontend/src/layouts/nav.ts`, directly under "Mocks", with `sectionSlug: 'learning'` (decision 0052).
5. **Links and the scroll to a `#hash`.** After the body is set, open the part with that id and scroll to it, also when the hash changes. A click on a link between the tabs uses the router, so that the app does not load again **(default)**.
6. **Dark mode.** The pages follow the `.dark` class of `<html>` that the portal sets. In the portal, the pages have no theme button of their own (decision 0051).
7. **The link from the answer review to tab 1.** Next to "Task 2.5" in `ItemMeta.tsx`, a link to `/exam-guide-breakdown#ts-2-5`, made from `point` (decision 0055, item 8).
8. **Tests** **(default)**. Unit: the sidebar shows the two entries only with the `learning` grant. Playwright (hermetic): each page opens behind the login, a link between the tabs opens and scrolls to its part, a preview card opens, the page works at 390 px wide, and the dark theme applies.

**PR 5 checklist:**
- [ ] Both pages open from the sidebar, and only for a user with the `learning` grant
- [ ] No console error and no breach of the security policy on either page
- [ ] A link from tab 1 to a step of tab 2, and back, opens and scrolls to its part, with no full reload
- [ ] Preview cards and popups open and close with the mouse, the keyboard and touch
- [ ] Light and dark follow the portal's theme button
- [ ] Code and file names show in IBM Plex Mono
- [ ] Both pages work at 390 px wide with no sideways scrolling
- [ ] The answer review links a question to its part of tab 1
- [ ] `frontend/src/academy/SOURCE.txt` names the tag of the copied pages

### Needs from `ccar-f-mock-generator` before PR 5

The build there must write the portal form of each page, next to the page that opens alone (decision 0050, item 5), and put both under a new tag. This is work for a session in that repository. The form below is a suggestion of the assistant, so that PR 5 has a fixed target. The owner and that session settle it:

- `<tab>.body.html`: the content of `<body>` only, with no `<script>`, `<link>` or `<meta>`.
- `<tab>.data.ts`: a TypeScript module that exports the card and popup data, in place of `window.ACADEMY`. TypeScript, because the portal's `tsconfig.json` is strict and has no `allowJs`.
- `academy.ts`: a TypeScript module that exports `start(root, data)`. It binds the popups, cards, figures and parts inside `root` only, and returns a function that removes them.
- `<tab>.css`: the styles of the page, each rule scoped under `.academy-page`, with the light and dark colours keyed to `.dark` on `<html>`, and with no `@font-face` rules (the portal loads the fonts, decision 0053).
- Links between the tabs as `/exam-guide-breakdown#id` and `/behind-the-mocks#id`. Images as `/academy/<file>`.

`check-pages.js` checks both forms there.

### The portal form as built (19 October 2026, for PR 5)

This part is not in the portal's `PLAN.md`. It records what the build in `ccar-f-mock-generator` delivers, so that PR 5 builds against it.

- **Where:** `academy/pages/portal/` in `ccar-f-mock-generator`, at the tag `pages-v2`. `src/` goes to `frontend/src/academy/`, and `public/academy/` goes to `frontend/public/academy/`. `preview/` stays there: it is the test page that imitates the portal.
- **Files:** `src/academy.ts` (shared), and for each tab `src/<tab>.body.html`, `src/<tab>.data.ts` and `src/<tab>.css`. Each file says at the top that it is made there.
- **The root element:** the React element must have both classes `academy-page` and `ap-<tab>` (for example `academy-page ap-behind-the-mocks`). Each tab's styles are scoped to its own class, so the styles of the two tabs never mix after a reader opens both. `start()` does not add these classes. React must not change the class of the element after start, because `start()` adds `js-motion` to it.
- **The body:** import it with `?raw` (for example `import body from './academy/behind-the-mocks.body.html?raw'`), and set it on the root element. Render nothing else inside the root: the page undoes the portal's base styles inside it.
- **The data:** `export default data` in `<tab>.data.ts`.
- **The script:** `start(root, data)` binds the page inside `root` and returns `stop`. `stop()` removes every listener, observer, timer and added element, so start, stop and start on the same element works (React StrictMode). `stop.open(id)` opens the part with that id and scrolls to it: call it after a router change of the hash, which fires no `hashchange` event.
- **Links:** between the tabs, `/exam-guide-breakdown#id` and `/behind-the-mocks#id`, in the body and in the popups that the script makes inside `#pop` (56 in tab 2). The click handler of the router must catch both, and skip `target="_blank"` and clicks with a modifier key. Images are at `/academy/...`.
- **Width:** the width rules of the page are container rules on its root (`container: academy / inline-size`), so the page lays out by its own width, not by the window. The sides of the page have no padding, because the portal's main area has its own. The top keeps 51 px.
- **Layers:** the popup is at z-index 45, the glossary button at 41 and the glossary panel at 42: above the portal's top bar (40) and under its drawer (50). Under 1024 px, each element with an id has a scroll margin of 72 px at the top, for the top bar.
- **Fonts:** IBM Plex Mono at weights 400, 500 and 600 (the page sets `font-synthesis: none`, so a missing weight shows). Sora at 400 to 700.
- **Size:** the chunk of tab 1 is about 1.1 MB, so Vite warns about its size. The build does not fail.
- **Tests:** the script uses `matchMedia` and `IntersectionObserver`, which jsdom does not have. Test the pages with Playwright, not with vitest. Leave `src/academy/**` out of the coverage count, or it counts at 0 %.
- **Escape:** when a popup or the glossary is open, Escape closes it. A portal dialog over the page also gets Escape.
- **Checked there:** both test pages pass `check-pages.js`, light and dark, at 1280, 1024 and 390 px, once with motion on, with the base styles of Tailwind in their layer and both tabs' styles loaded. Nothing reaches out of the page element, except the tilted notepad mark of tab 1, by up to 4 px at 390 px, into the padding of the portal (listed as a known exception). Screenshots of each portal form without the side bar, taken one screen at a time (1,218 screens), match the page that opens alone pixel for pixel. An independent agent reviewed the form and found 12 points. All are fixed, or are notes in this list.

## Order of work and hand-offs

| When | Who | What |
|---|---|---|
| First | You | Merge the plan PR |
| PR 4 | Me | Branch, implement, run the converter, commit, push the branch, run the checklist locally |
| PR 4 | You | Open the PR to `staging` and merge it. Check on staging. Then the PR from `staging` to `main` |
| Before PR 5 | `ccar-f-mock-generator` | The portal form of the pages, and a new tag |
| PR 5 | Me, then you | The same steps as PR 4 |

A loaded version can never change in place: the loader refuses a changed version. A mistake in version 2 on production needs a version 3. So version 2 must be right on staging before the PR to `main`.

### If this section is wrong

The same rule as above: stop, write down what was found in this file, and flag it.

---

## Part B. Start note for the build session in `~/magnetlab-academy`

1. **Start the session inside `~/magnetlab-academy`**, so that its `CLAUDE.md` loads. Then run `/add-dir /home/triggger/ccar-f-mock-generator`, so that you can read that repository without a prompt for each file.
2. **Read only** in `/home/triggger/ccar-f-mock-generator`. Change nothing there. A change there belongs to a session in that repository. Do not open any `.env` file in either repository.
3. **Read first:**
   - this file, `/home/triggger/ccar-f-mock-generator/academy/portal-plan.md`;
   - the decisions `/home/triggger/ccar-f-mock-generator/academy/decisions/0050-*.md` to `0057-*.md`;
   - `/home/triggger/ccar-f-mock-generator/docs/portal-notes.md`, the notes for the portal about the mocks.
4. **The owner's way of working** applies here too:
   - one question at a time, with a short context, one recommendation, then the question;
   - short answers in plain words;
   - before a change to a text that the owner approved, show the old and the new text and wait for a yes;
   - a yes before a push and before a design choice that the owner did not make.
5. **The git rules of the portal** (its `CLAUDE.md`): a feature branch for each PR; never push to `staging` or `main`; the owner opens and merges each pull request; the order is feature branch, then `staging`, then `main`. The integration tests need Postgres (`TEST_DATABASE_URL`, as in CI), and all CI jobs must pass, also the frontend coverage floor and the Playwright tests.
6. **The files to take from `ccar-f-mock-generator`, always at a tag, from GitHub:**
   - the mocks: `mocks/mock-0N.questions.json` and `mocks/mock-0N.answers.json` at the tag `mocks-v2`;
   - the titles of the task statements: `reference/guide-records.json` at the tag `mocks-v2`;
   - the pages, for PR 5: the portal form at the new tag that the build there makes.
7. **The checked facts** (19 October 2026):
   - The portal had no commit after 30 September 2026.
   - Each mock of version 2: 60 questions numbered 1 to 60, 120 minutes, scenarios from 1 to 6, in 4 groups. The field `task_statement` of a question is the number only (for example "2.5").
   - 300 questions in all. 40 of them are two-answer questions (`select: 2`), 8 in each mock, and these 40 are exactly the questions with 5 options.
   - No question text ends with "Select TWO.".
   - In the 260 one-answer questions, the correct letter is D 76 times, C 67, B 63 and A 54.
   - No question and no reason names another option by its letter.
   - The `question_id` and the letters agree between `questions.json` and `answers.json`.
8. **Open before PR 5:** the portal form of the pages from `ccar-f-mock-generator`. PR 4 does not wait for it.
9. **The first step:** the plan pull request. Copy Part A into `PLAN.md` on the branch `chore/plan-post-mvp-1`, show it to the owner, and push the branch after the owner says yes. The owner opens and merges the pull request. Then PR 4.
