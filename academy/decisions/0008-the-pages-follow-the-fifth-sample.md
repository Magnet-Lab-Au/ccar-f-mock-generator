# 0008: The pages follow the fifth sample

- Date: 13 October 2026
- Status: accepted. Decision 0009 changes two of its rules (the K and S letters). Decision 0051 says that in the portal, the light and dark button of the portal decides.
- Text confirmed by the owner: 13 October 2026
- Diagram: none

## Question

There are five samples of task statement 1.1. Which one is the model for the look of the pages?

## Options

1. `sample/1-1-agentic-loops.html`: the first sample, text first, with one animated loop.
2. `sample/1-1-agentic-loops-ve.html`: made with the plugin visual-explainer. Figures lead, and the text is the caption of each figure.
3. `sample/1-1-agentic-loops-portal.html`: sample 2 in the colors and fonts of the academy portal.
4. `sample/1-1-agentic-loops-site.html`: sample 3 in the look of the website www.magnetlab.com.au. Square corners, flat boxes, thin lines, IBM Plex Mono labels and the website colors.
5. `sample/1-1-agentic-loops-kit.html`: sample 4 with the colors of the MagnetLab brand kit only.

## Decision

Option 5, in light mode and in dark mode.

The look has these rules:

- Square corners everywhere, also in the figures. Flat boxes with no shadow and no glow.
- Fonts: Sora for text and headings, IBM Plex Mono for small labels.
- Brand kit colors only (`claude-code-brand-kit/brand-kit.md`). Thin lines and soft fills use a kit color made fainter.
- Light mode: white page, cream boxes, navy text. Dark mode: Primary navy page, Secondary navy boxes, cream text.
- Gold is never a text color. It marks lines only: the active path, the rule over each section, the underline of links and the focus ring.
- K and S: a small legend of two solid tags, "K = Knowledge of" and "S = Skills in". The K or S of each label has the same solid fill with a navy letter: light blue `#8BC4D9` for K, gold for S.
- Status colors (success, error, warning, info) mark borders only. The words stay navy or cream.
- A button switches between light and dark. The page follows the device setting until the reader presses it.

## Reason

The owner chose the plugin look over the first sample: it "looks better by a lot". The owner then chose the portal look, and asked to match the newer website, with a corporate look and no rounded edges. The owner asked for a version with brand kit colors only, and chose it in both modes.

## How we decided

1. The assistant made each sample from the same checked data, so only the look changed between them.
2. The owner asked for the changes one at a time: the stepper of 9 single steps, the light and dark button, the website look, and the K and S legend.
3. The owner found that S had the same color as the accent of the page. The brand kit has no free fourth color. So the assistant suggested that gold is never a text color, and that K and S letters get a solid fill.
4. The kit writes its Secondary color as navy `#1A3E5C` but draws it as light blue `#8BC4D9`. The owner said yes to the light blue for K.

## Known limits

- The kit's warning yellow `#FFC107` is faint on white (1.6 to 1). In light mode, the dashed box of the guard in Fig. 5 is hard to see.
- The academy portal today has a different look: rounded corners and the portal colors. Pages in this look will differ from the mock screens until the portal changes.
- The kit says Norwester for headings and rounded buttons. The website, which is newer, uses Sora headings and square corners. The pages follow the website.

## Exam guide points

none.
