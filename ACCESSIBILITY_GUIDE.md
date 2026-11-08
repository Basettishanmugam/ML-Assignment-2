# Accessibility and visual improvement guide

This update improves the Streamlit app's visual hierarchy, responsive spacing, focus visibility,
metric-card contrast, chart resolution, and text alternatives. It is an accessibility improvement,
not a certification of Section 508 or WCAG conformance.

## What changed and where

| File | Location | Change |
|---|---|---|
| `app.py` | CSS block near the top | Higher-contrast green palette, clearer cards, responsive spacing, visible keyboard focus, reduced-motion support |
| `app.py` | Main hero/header | Removed the decorative bean emoji from the heading; retained a clear text heading |
| `app.py` | Sidebar | Clearer two-step labels and short instructions |
| `app.py` | Evaluation tab | Added an expandable numeric confusion-matrix table as an alternative to the heatmap |
| `app.py` | Comparison tab | Clarified that the metric table is the exact alternative to the comparison chart |
| `app.py` | Chart rendering | Increased on-screen Matplotlib DPI to 160 |
| `app.py` | Footer | Added keyboard navigation guidance |
| `src/visualization.py` | `save_fig()` | Increased exported report figure resolution from 130 DPI to 200 DPI |

## Where to make your own design changes

1. **Theme colours and focus outline:** edit the CSS string in `app.py`, directly below `st.set_page_config()`.
   - Main green: `--bean-green` / `--bean-green-dark`
   - Body text: `--bean-ink`
   - Secondary text: `--bean-muted`
   - Focus ring: `#E09B24`
   - Keep text/background contrast at least 4.5:1 for normal text and 3:1 for large text and meaningful UI boundaries.
2. **Header/title:** edit the `# header` section in `app.py`.
3. **Sidebar controls and their order:** edit the `# sidebar` section. Keep the visual order aligned with the source order. Do not add positive `tabindex` values.
4. **Tabs:** edit the `st.tabs([...])` declaration. Keep names descriptive. Streamlit owns the generated tab markup and keyboard behavior; avoid manually injecting tab roles or `tabindex`.
5. **Metrics:** edit the `c1.metric(...)` calls in the Dashboard and Evaluation sections.
6. **Charts:** edit `src/visualization.py`. Keep a corresponding table or written interpretation wherever a chart conveys important results.
7. **Exported image resolution:** change `dpi=200` in `src/visualization.py` `save_fig()`. Higher DPI increases file size; 200 is a practical report default.
8. **App chart resolution:** change `fig.set_dpi(160)` at each `st.pyplot(...)` call in `app.py`.

## Section 508 / WCAG 2.2 AA verification checklist

These checks must be performed in a real browser with the deployed/local app. Automated Streamlit AppTest is not a complete accessibility audit.

### Keyboard-only test
- Start at the browser address bar and press Tab. Confirm focus enters the app and proceeds in a predictable visual order.
- Use Tab and Shift+Tab through upload, buttons, download, model selector, tabs, checkboxes, expanders, and tables.
- Use arrow keys to move within tab/selection widgets where supported; Enter/Space to activate.
- Confirm every focused item has a clearly visible outline and focus is never hidden behind sticky UI.
- Confirm there is no keyboard trap and all actions are possible without a mouse.
- Do not add positive `tabindex` values. Native DOM order is safer; positive tabindex creates fragile custom ordering.
- Streamlit does not expose a supported per-widget `tabindex` setting. Do not patch its generated DOM with JavaScript as a compliance workaround.

### Screen reader and semantics
- Test with NVDA + Firefox/Chrome on Windows; also test VoiceOver + Safari if available.
- Confirm headings are announced in a meaningful hierarchy and every input has a visible, descriptive label.
- Do not rely on emoji or colour alone to communicate status.
- Check that chart information is also available in a table or explanatory text.
- Verify upload errors and success messages are announced and understandable.
- Ensure data tables have meaningful column headers and do not require colour perception.

### Visual and responsive checks
- Check text contrast with a contrast checker: 4.5:1 normal text, 3:1 large text, 3:1 essential component boundaries/focus indicators.
- Zoom browser to 200% and 400%; verify content reflows without horizontal scrolling for ordinary text and controls.
- Test a narrow mobile viewport and a desktop viewport.
- Check that labels are not clipped, charts remain readable, and tables can be navigated.
- Confirm reduced-motion preference does not cause distracting animation.

### Known limits
- CSS selectors target Streamlit's rendered UI and can change across Streamlit versions.
- A visible focus ring is helpful but does not prove correct focus order or screen-reader behavior.
- Streamlit's built-in widgets determine much of the accessible markup. The application cannot reliably set arbitrary `tabindex` attributes on individual built-in widgets.
- This ZIP has not been certified by an accessibility auditor. Record actual browser/assistive-technology test results before claiming Section 508 compliance.

## Run and validate after editing

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then follow the manual checks above. Also run the project's existing test suite:

```bash
python tests/run_checks.py
```

If the test suite reports a failure, inspect that failure rather than describing the app as fully validated.
